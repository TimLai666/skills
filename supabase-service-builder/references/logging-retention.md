# 稽核 Log 與保留策略

系統的重要操作都要留 log，而且 log 要有自動清理機制——log 只增不減會無限膨脹、拖慢資料庫又增加成本。所以「稽核表 + 保留策略」是一組的，不能只做前半。

## 稽核表 `audit_log`

```sql
create table public.audit_log (
  id          bigint generated always as identity primary key,
  created_at  timestamptz not null default now(),
  actor_id    uuid references auth.users(id) on delete set null,
  action      text not null,            -- INSERT / UPDATE / DELETE / LOGIN / 自訂
  entity_type text,                      -- 受影響的資料表或資源類型
  entity_id   text,                      -- 受影響資料的 ID
  metadata    jsonb not null default '{}'::jsonb
);

create index audit_log_created_at_idx on public.audit_log (created_at);
create index audit_log_actor_id_idx   on public.audit_log (actor_id);
create index audit_log_entity_idx     on public.audit_log (entity_type, entity_id);

alter table public.audit_log enable row level security;
-- 刻意不給 anon／authenticated 任何 policy => 預設全拒。
-- 讀取走 service_role（繞過 RLS），或另寫只給 admin 的 select policy。
```

`created_at` 一定要有索引——保留策略的清理查詢靠它。`actor_id` 用 `on delete set null`，使用者被刪時 log 仍保留（稽核紀錄不該因為人被刪就消失）。

## 寫 log 的兩種方式

### A. 資料庫 trigger（最可靠）

用一個通用 trigger function，掛在要稽核的表上。好處是應用層繞不過去——只要資料庫被改，log 就一定有。

```sql
create function public.record_audit()
returns trigger
language plpgsql
security definer
set search_path = ''
as $$
begin
  insert into public.audit_log (actor_id, action, entity_type, entity_id, metadata)
  values (
    auth.uid(),
    tg_op,
    tg_table_name,
    coalesce(new.id::text, old.id::text),
    case
      when tg_op = 'DELETE' then jsonb_build_object('old', to_jsonb(old))
      when tg_op = 'UPDATE' then jsonb_build_object('old', to_jsonb(old), 'new', to_jsonb(new))
      else jsonb_build_object('new', to_jsonb(new))
    end
  );
  return coalesce(new, old);
end;
$$;

-- 掛到要稽核的表
create trigger audit_orders
  after insert or update or delete on public.orders
  for each row execute function public.record_audit();
```

### B. 應用層寫入

trigger 看不到的事件（純前端行為、外部 webhook、登入流程的業務面）由應用程式在伺服器端用 service_role 寫一筆 `audit_log`。

實務上兩者並用：資料異動靠 trigger 保底，業務事件靠應用層補充。

## 保留策略：用 pg_cron 自動清理

`pg_cron` 在 Supabase 可用。先啟用擴充（若 migration 內 `create extension` 失敗，到 Dashboard → Database → Extensions 開啟 `pg_cron`）：

```sql
create extension if not exists pg_cron;
```

排一個每天清理過期 log 的工作。為了讓 migration 可重複套用，先 unschedule 同名工作再重排：

```sql
select cron.unschedule('purge-audit-log')
where exists (select 1 from cron.job where jobname = 'purge-audit-log');

select cron.schedule(
  'purge-audit-log',
  '0 3 * * *',                                  -- 每天 03:00
  $$ delete from public.audit_log
     where created_at < now() - interval '90 days' $$
);
```

保留天數（這裡 90 天）依專案的稽核／法遵需求調整。要的話可拆成「一般 log 留 90 天、安全相關 log 留更久」兩個排程。

確認排程狀態：

```sql
select jobname, schedule, active from cron.job;
select * from cron.job_run_details order by start_time desc limit 10;
```

## 軟刪資料的清理

被軟刪（`deleted_at` 不為 null）的業務資料若也想定期真正清掉，同樣可用 `pg_cron`，但這屬於會真的刪資料的動作——清理週期應拉長（例如軟刪 180 天後才硬刪），且**正式環境的這類排程要先和使用者確認**。詳見 `production-safety.md`。

## 檢查清單

- [ ] `audit_log` 表存在，已 `enable row level security` 且預設拒絕一般角色。
- [ ] 重要的資料表掛了稽核 trigger，或應用層有寫 log。
- [ ] `pg_cron` 已啟用，且有清理過期 log 的排程。
- [ ] 保留天數明確、可調，且與專案的稽核需求相符。

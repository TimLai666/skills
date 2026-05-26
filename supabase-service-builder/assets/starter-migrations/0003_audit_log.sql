-- ============================================================
-- 0003_audit_log.sql
-- 起手式：稽核 log 表、通用稽核 trigger、pg_cron 保留策略
-- ============================================================

-- ---- 稽核表 ----
create table public.audit_log (
  id          bigint generated always as identity primary key,
  created_at  timestamptz not null default now(),
  actor_id    uuid references auth.users(id) on delete set null,
  action      text not null,         -- INSERT / UPDATE / DELETE / 自訂事件
  entity_type text,                   -- 受影響的資料表或資源類型
  entity_id   text,                   -- 受影響資料的 ID
  metadata    jsonb not null default '{}'::jsonb
);

create index audit_log_created_at_idx on public.audit_log (created_at);
create index audit_log_actor_id_idx   on public.audit_log (actor_id);
create index audit_log_entity_idx     on public.audit_log (entity_type, entity_id);

-- 啟用 RLS，且刻意不給一般角色 policy => 預設全拒。
-- 讀取走 service_role（繞過 RLS）或另外新增 admin 專用 select policy。
alter table public.audit_log enable row level security;

-- ---- 通用稽核 trigger function ----
-- 掛在要稽核的表上即可自動記錄 INSERT / UPDATE / DELETE。
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
-- 用法（在各資料表的 migration 內）：
--   create trigger audit_<table>
--     after insert or update or delete on public.<table>
--     for each row execute function public.record_audit();

-- ---- 保留策略：每天清理過期 log ----
-- 先移除同名排程，讓此 migration 可重複套用。
select cron.unschedule('purge-audit-log')
where exists (select 1 from cron.job where jobname = 'purge-audit-log');

-- 每天 03:00 刪除 90 天前的 log（天數依稽核需求調整）。
select cron.schedule(
  'purge-audit-log',
  '0 3 * * *',
  $$ delete from public.audit_log
     where created_at < now() - interval '90 days' $$
);

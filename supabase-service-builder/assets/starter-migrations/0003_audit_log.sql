-- ============================================================
-- 0003_audit_log.sql
-- 起手式：Tier 1 DB-layer 稽核 log + 通用 trigger + pg_cron 保留策略
--
-- 配套 0004_request_log.sql（Tier 2 application/request audit）。
-- 兩個一起做才是業界小商家及格線；缺 Tier 2 等於失明（DB trigger 抓不到 IP/UA）。
-- 完整 4 層分工與法規保留期見 references/logging-architecture.md。
-- ============================================================

-- ---- 稽核表 ----
create table public.audit_log (
  id          bigint generated always as identity primary key,
  created_at  timestamptz not null default now(),
  actor_id    uuid references auth.users(id) on delete set null,
  actor_email text,                       -- 寫入當下的 email 快照（不靠 join auth.users）
  action      text not null,              -- INSERT / UPDATE / DELETE / 自訂事件
  entity_type text,                       -- 受影響的資料表或資源類型
  entity_id   text,                       -- 受影響資料的 ID
  metadata    jsonb not null default '{}'::jsonb
);

comment on column public.audit_log.actor_email is
  '寫入 log 當下的 actor email snapshot；之後 auth.users 改 email 或被刪都不影響顯示';

create index audit_log_created_at_idx on public.audit_log (created_at);
create index audit_log_actor_id_idx   on public.audit_log (actor_id);
create index audit_log_entity_idx     on public.audit_log (entity_type, entity_id);

-- 啟用 RLS，且刻意不給一般角色 policy => 預設全拒。
-- 讀取走 service_role（繞過 RLS）或另外新增 admin 專用 select policy。
alter table public.audit_log enable row level security;

-- ---- 共用：auth.users id → email lookup ----
-- log trigger 寫入時用，把 FK reference 凍成欄位 snapshot。
-- 一定要 revoke execute 避免 PostgREST 把它暴露成 /rpc/lookup_user_email
-- 變成「UUID 換 email」的列舉漏洞。
create function public.lookup_user_email(p_user_id uuid)
returns text
language sql
security definer
set search_path = ''
stable
as $$
  select email::text from auth.users where id = p_user_id;
$$;

revoke execute on function public.lookup_user_email(uuid) from anon, authenticated, public;

comment on function public.lookup_user_email(uuid) is
  'log trigger 專用：給定 auth.users.id 回傳 email。已 revoke 公開 EXECUTE 避免 RPC 列舉。';

-- ---- 通用稽核 trigger function ----
-- 掛在要稽核的表上即可自動記錄 INSERT / UPDATE / DELETE。
-- 寫入時順便 snapshot actor_email 進去，避免之後 auth.users 改 email 或刪帳號
-- 害 log 顯示遺失（見 references/db-integrity-checklist.md B2）。
create function public.record_audit()
returns trigger
language plpgsql
security definer
set search_path = ''
as $func$
declare
  v_actor uuid := auth.uid();
begin
  insert into public.audit_log (actor_id, actor_email, action, entity_type, entity_id, metadata)
  values (
    v_actor,
    case when v_actor is not null then public.lookup_user_email(v_actor) else null end,
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
$func$;

revoke execute on function public.record_audit() from anon, authenticated, public;

-- 用法（在各資料表的 migration 內）：
--   create trigger audit_<table>
--     after insert or update or delete on public.<table>
--     for each row execute function public.record_audit();

-- ---- 保留策略：每天清理過期 log ----
-- 先移除同名排程，讓此 migration 可重複套用。
select cron.unschedule('purge-audit-log')
where exists (select 1 from cron.job where jobname = 'purge-audit-log');

-- 預設 90 天（適合「剛起步、還沒業務表」的階段）。
-- 等業務表（orders / customers / products…）加進來後，請改成下方分流版：
-- 業務憑證類至少 5 年（台灣商業會計法第 38 條），派生資料 90 天即可。
select cron.schedule(
  'purge-audit-log',
  '0 3 * * *',
  $$ delete from public.audit_log
     where created_at < now() - interval '90 days' $$
);

-- ★ 業務表加入後改成這個分流版（取消上方 schedule 再用這個）：
-- select cron.schedule(
--   'purge-audit-log',
--   '0 3 * * *',
--   $job$
--     -- 業務憑證：5 年（商業會計法第 38 條 / 稅務查核 7 年最長）
--     delete from public.audit_log
--     where created_at < now() - interval '5 years'
--       and entity_type in ('orders', 'order_items', 'customers', 'profiles', 'products');
--
--     -- 派生資料 / 運算 cache：90 天
--     delete from public.audit_log
--     where created_at < now() - interval '90 days'
--       and entity_type in ('customer_segments');
--
--     -- 其他未分類：1 年（保守值，發現新表時要更新分類）
--     delete from public.audit_log
--     where created_at < now() - interval '1 year'
--       and entity_type not in (
--         'orders', 'order_items', 'customers', 'profiles', 'products',
--         'customer_segments'
--       );
--   $job$
-- );

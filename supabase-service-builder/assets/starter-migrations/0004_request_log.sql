-- ============================================================
-- 0004_request_log.sql
-- 起手式：Tier 2 application/request audit log
--
-- DB trigger（Tier 1，0003）只蓋「DB 狀態變更」，抓不到:
--   - IP / user agent（客訴「不是我下的單」追不到來源）
--   - request_id（跨服務 trace 串不起）
--   - failed auth 嘗試（401/403 完全靜默）
--   - service token 來源（cron / 腳本看不出差別）
--   - 路徑 / 方法 / latency（API 健康度盤點不到）
--
-- 缺 Tier 2 等於失明。完整 4 層分工見 references/logging-architecture.md。
-- 對應 backend middleware 範例見同檔的 Tier 2 段落（Gin 寫法）。
-- ============================================================

create table public.request_log (
  id            bigint generated always as identity primary key,
  created_at    timestamptz not null default now(),
  request_id    text,                          -- UUID per request，跨服務串
  method        text not null,                 -- GET/POST/PATCH/DELETE
  path          text not null,                 -- 路由模板 /api/admin/orders/:id（非實值，方便 group）
  status        int,                           -- HTTP status code
  latency_ms    int,
  source        text not null,                 -- 'liff' | 'admin' | 'service' | 'public' | 'webhook'
  actor_id      uuid,                          -- 不設 FK：log 是 append-only，actor 可能刪
  actor_email   text,                          -- JWT claims snapshot；不靠 join auth.users
  actor_kind    text,                          -- 'user' | 'service' | 'anon'
  ip            inet,
  user_agent    text,
  error_message text,                          -- status >= 400 時填
  metadata      jsonb not null default '{}'::jsonb
);

comment on table public.request_log is
  'Tier 2: 每支 API 呼叫的脈絡 log。middleware 寫入，async 不阻塞業務。';
comment on column public.request_log.path is
  '路由模板（c.FullPath() / req.route.path），不是含實值的 URL。查特定資源走 audit_log.entity_id';
comment on column public.request_log.actor_email is
  'JWT 解出的 email snapshot；不靠 join auth.users';

create index request_log_created_at_idx on public.request_log (created_at);
create index request_log_actor_idx      on public.request_log (actor_id) where actor_id is not null;
create index request_log_status_idx     on public.request_log (status);
create index request_log_path_idx       on public.request_log (path);

-- 異常查詢用：status >= 400 的失敗請求單獨索引（資安事件、debug 都靠它）
create index request_log_failed_idx
  on public.request_log (created_at, status)
  where status >= 400;

alter table public.request_log enable row level security;
-- 啟用 RLS 但暫時不給 policy => 預設全拒。
-- 寫入走 service_role（backend middleware 用 service key 寫），不受 RLS 限制。
-- 等專案建立 admin RLS（is_admin() function）後，補上讀取 policy：
--
--   create policy "request_log_admin_read"
--     on public.request_log for select
--     to authenticated
--     using (public.is_admin());

-- ---- 保留策略：30 天 ----
-- request_log 量比 audit_log 大很多（每支 API 一筆），保留期可短。
-- 資安事件通常在 30 天內被發現；高敏感 endpoint 要久存的話，
-- 未來拆 request_log_critical 表單獨設更長保留期。
select cron.unschedule('purge-request-log')
where exists (select 1 from cron.job where jobname = 'purge-request-log');

select cron.schedule(
  'purge-request-log',
  '5 3 * * *',                                  -- 03:05，與 purge-audit-log 錯開
  $$ delete from public.request_log
     where created_at < now() - interval '30 days' $$
);

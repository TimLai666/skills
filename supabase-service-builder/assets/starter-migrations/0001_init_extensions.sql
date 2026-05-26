-- ============================================================
-- 0001_init_extensions.sql
-- 起手式：擴充套件與共用 function
-- 複製進 supabase/migrations/ 時，把檔名前綴換成 CLI 產生的時間戳。
-- ============================================================

-- moddatetime：自動維護 updated_at 欄位
create extension if not exists moddatetime schema extensions;

-- pgcrypto：提供 gen_random_uuid()（多數情況 Supabase 已內建可用）
create extension if not exists pgcrypto schema extensions;

-- pg_cron：排程，給 audit_log 等保留策略使用
-- 若此行在 migration 中失敗，改到 Dashboard → Database → Extensions 啟用 pg_cron
create extension if not exists pg_cron;

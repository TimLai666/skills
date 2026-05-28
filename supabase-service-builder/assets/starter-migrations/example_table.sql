-- ============================================================
-- example_table.sql
-- 示範表：一張業務資料表「該長什麼樣」的完整樣板。
-- 同一個 migration 內一次寫齊：欄位 + RLS + policy + trigger + 索引。
-- 新建表時照這個模式做。
-- ============================================================

create table public.notes (
  id         uuid primary key default gen_random_uuid(),
  -- CASCADE：notes 屬於 user 的個人資料，user 被硬刪（如 GDPR 抹除）時連帶清掉合理。
  -- 但若 children 是「業務歷史不可丟」（如成交明細、稽核），改用 RESTRICT。
  -- 詳見 references/db-integrity-checklist.md 的 A 段。
  owner_id   uuid not null references auth.users(id) on delete cascade,
  title      text not null,
  body       text,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now(),
  deleted_at timestamptz                       -- 軟刪除標記
);

-- ---- 一律啟用 RLS ----
alter table public.notes enable row level security;

-- 三個寫法細節（少一個都會踩坑，見 references/performance-pitfalls.md）：
--   1. to authenticated：明確指定 role，避免預設 public 連 service_role 都檢查
--   2. (select auth.uid())：包成子查詢避免 per-row 重算
--   3. owner_id 是 FK：下方有對應索引

-- 擁有者才能讀自己的、且未軟刪的資料
create policy "notes_select_own"
  on public.notes for select
  to authenticated
  using ((select auth.uid()) = owner_id and deleted_at is null);

-- 只能新增屬於自己的資料
create policy "notes_insert_own"
  on public.notes for insert
  to authenticated
  with check ((select auth.uid()) = owner_id);

-- 只能更新自己的、未軟刪的資料
create policy "notes_update_own"
  on public.notes for update
  to authenticated
  using ((select auth.uid()) = owner_id and deleted_at is null)
  with check ((select auth.uid()) = owner_id);

-- 刻意「不」給 delete policy：
-- 硬刪一律被擋，刪除只能透過 UPDATE 設 deleted_at（軟刪）。

-- ---- updated_at 自動維護 ----
create trigger set_updated_at
  before update on public.notes
  for each row execute function extensions.moddatetime(updated_at);

-- ---- 稽核 ----
create trigger audit_notes
  after insert or update or delete on public.notes
  for each row execute function public.record_audit();

-- ---- 索引 ----
-- FK 欄位一律建索引；用部分索引避開軟刪列、更省空間
-- （Postgres 不會自動幫 FK 建索引，沒索引時 PostgREST embed 會走 seq scan）
create index notes_owner_active_idx
  on public.notes (owner_id)
  where deleted_at is null;

-- ---- 只露出未刪資料的 view（選用，方便應用層查詢）----
create view public.active_notes as
  select * from public.notes where deleted_at is null;

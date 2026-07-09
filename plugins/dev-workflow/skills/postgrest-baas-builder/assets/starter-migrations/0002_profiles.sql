-- ============================================================
-- 0002_profiles.sql
-- 起手式：使用者擴充表 profiles
-- 認證走 Supabase 內建 auth.users；此表只存「附加的」使用者資料。
-- ============================================================

create table public.profiles (
  id           uuid primary key references auth.users(id) on delete cascade,
  display_name text,
  avatar_url   text,
  role         text not null default 'user',   -- 'user' / 'admin' 等
  created_at   timestamptz not null default now(),
  updated_at   timestamptz not null default now(),
  deleted_at   timestamptz
);

-- 一律啟用 RLS
alter table public.profiles enable row level security;

-- policy 寫法細節（見 references/performance-pitfalls.md）：
--   to authenticated + (select auth.uid()) 兩個都要，避免 per-row 重算 & 預設 public

-- 使用者只能讀自己的 profile
create policy "profiles_select_own"
  on public.profiles for select
  to authenticated
  using ((select auth.uid()) = id and deleted_at is null);

-- 使用者只能改自己的 profile
create policy "profiles_update_own"
  on public.profiles for update
  to authenticated
  using ((select auth.uid()) = id and deleted_at is null)
  with check ((select auth.uid()) = id);
-- 刻意不給 insert / delete policy：
--   insert 由下方註冊 trigger 負責；delete 走軟刪（更新 deleted_at）。

-- updated_at 由 moddatetime 自動維護
create trigger set_updated_at
  before update on public.profiles
  for each row execute function extensions.moddatetime(updated_at);

-- 註冊時自動建立 profile
create function public.handle_new_user()
returns trigger
language plpgsql
security definer
set search_path = ''
as $$
begin
  insert into public.profiles (id, display_name)
  values (new.id, new.raw_user_meta_data ->> 'display_name');
  return new;
end;
$$;

create trigger on_auth_user_created
  after insert on auth.users
  for each row execute function public.handle_new_user();

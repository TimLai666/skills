# 認證（Supabase Auth）

認證一律用 Supabase 內建的 Auth，**不要自己開一張 users 表來存帳號密碼**。Supabase 已經處理好密碼雜湊、Email 驗證、OAuth、Magic Link、JWT 簽發、Session、密碼重設等等——自製這些等於重造輪子又多一個資安破口。

## 來源：`auth.users`

`auth.users` 是所有使用者的唯一真實來源（source of truth）。每個使用者有一個固定的 `id`（uuid）。應用程式裡所有「這筆資料屬於誰」的外鍵都指向 `auth.users(id)`。

RLS policy 裡用 `auth.uid()` 取得目前請求者的使用者 ID，用 `auth.jwt()` 取得 JWT 內容。

不要直接對 `auth` schema 的表做結構改動——那是 Supabase 管理的。

## 擴充使用者資料：`profiles` 表

`auth.users` 不該被塞應用層的欄位。要存暱稱、頭像、偏好設定、角色等等，**另開一張 `profiles` 擴充表**，主鍵就是 `auth.users.id`：

```sql
create table public.profiles (
  id uuid primary key references auth.users(id) on delete cascade,
  display_name text,
  avatar_url text,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now(),
  deleted_at timestamptz
);

alter table public.profiles enable row level security;

create policy "profiles_select_own"
  on public.profiles for select
  using (auth.uid() = id);

create policy "profiles_update_own"
  on public.profiles for update
  using (auth.uid() = id)
  with check (auth.uid() = id);

create trigger set_updated_at
  before update on public.profiles
  for each row execute function extensions.moddatetime(updated_at);
```

`on delete cascade` 讓使用者被刪時 profile 一併清掉。這是「擴充使用者資訊」的合理例外——它不是另一套帳密系統，只是 `auth.users` 的衛星表。

## 註冊時自動建立 profile

用一個掛在 `auth.users` 上的 trigger，使用者一註冊就自動補一筆 profile：

```sql
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
```

`security definer` 讓這個 function 有權寫入 `public.profiles`；`set search_path = ''` 是安全慣例，避免 search_path 被攻擊。註冊時可在 client 端把暱稱放進 user metadata，trigger 就能取用。

## 角色與權限

需要區分「一般使用者／管理員」時：

- 在 `profiles` 加一個 `role` 欄位（`text` 或 enum），**不要**另開一套使用者表。
- 或把角色放進 JWT 的 custom claims，policy 裡用 `auth.jwt()` 判斷。
- policy 中可寫 `(select role from public.profiles where id = auth.uid()) = 'admin'` 這類判斷，或包成 `security definer` function 重用。

## 什麼可以、什麼不行

| 情境 | 做法 |
|---|---|
| 帳號、密碼、登入、OAuth、Session | ✅ 全部交給 Supabase Auth |
| 暱稱、頭像、偏好、角色等使用者附加資料 | ✅ 開 `profiles` 擴充表，FK 到 `auth.users` |
| 自己開 `users` 表存 email + password | ❌ 禁止 |
| 自己實作 JWT 簽發／密碼雜湊 | ❌ 禁止 |
| 直接改 `auth.users` 的結構 | ❌ 禁止 |

## 認證事件的稽核

登入、登出、密碼重設等認證事件，Supabase 本身會記錄在 `auth.audit_log_entries`，不需要自己重做。專案自訂的 `audit_log`（見 `logging-retention.md`）負責的是**應用層的業務操作**（建立訂單、修改資料…），兩者互補。

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
  to authenticated
  using ((select auth.uid()) = id);

create policy "profiles_update_own"
  on public.profiles for update
  to authenticated
  using ((select auth.uid()) = id)
  with check ((select auth.uid()) = id);

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

## 後端驗 JWT：用 JWKS 本地驗章，不要打 `/auth/v1/user`

當後端（Go／Node／Python…）收到帶 Supabase JWT 的請求要驗身分時，**不要**每次都呼叫 Supabase 的 `/auth/v1/user` 來驗——那是一趟跨網路 HTTP 往返，單支 API 會多 100-500ms（看你的服務跟 Supabase 機房的距離），admin 介面或 dashboard 切 tab 時感受最明顯。

### 用 JWKS 本地驗章

新版 Supabase 用**非對稱 signing keys**（ES256/RS256），公鑰透過 JWKS 端點公開：

```
<SUPABASE_URL>/auth/v1/.well-known/jwks.json
```

公鑰本來就公開、**不需要設任何 secret env**。後端啟動時抓一次 JWKS、cache 在記憶體，之後每個請求都本地驗章（微秒級），完全不打 Supabase。

### Go 範例（golang-jwt + keyfunc）

```go
import (
    "github.com/MicahParks/keyfunc/v3"
    "github.com/golang-jwt/jwt/v5"
)

var kf, _ = keyfunc.NewDefault([]string{
    supabaseURL + "/auth/v1/.well-known/jwks.json",
})

func VerifyJWT(token string) (userID string, err error) {
    parsed, err := jwt.Parse(token, kf.Keyfunc,
        jwt.WithValidMethods([]string{"ES256", "RS256"}))
    if err != nil {
        return "", err
    }
    claims := parsed.Claims.(jwt.MapClaims)
    return claims["sub"].(string), nil
}
```

`keyfunc/v3` 會自動 cache JWKS、定期 refresh，且遇到不認得的 `kid` 時主動 refetch——所以 Supabase 輪換 signing keys 時**後端不必重啟**。

### 其他語言

| 語言 | 套件 |
|---|---|
| Node | `jose`（`createRemoteJWKSet` + `jwtVerify`）|
| Python | `PyJWT` + `PyJWKClient`（`jwt.decode(..., algorithms=["ES256","RS256"])`）|
| Rust | `jsonwebtoken` + JWKS fetch |

### Legacy JWT Secret（HS256）

舊版 Supabase project（或手動切回 legacy 的）用 HS256 + 共享 JWT Secret 簽。判斷方式：打 JWKS 端點，若沒回 keys 或回的是 HS 相關內容，就是 legacy。這時要：

- 在 Supabase Dashboard → Settings → API → JWT Settings 拿 JWT Secret
- 設成後端 env（**敏感**，等同 service_role 風險級別——洩了能偽造任意使用者）
- 用 HS256 + secret 本地驗

新專案優先用 signing keys，可零設定、可線上輪換、洩風險低（只洩公鑰）。

### 不要做的事

- ❌ 每個請求都打 `/auth/v1/user`：跨網路、慢、會被 Supabase rate limit。
- ❌ 把 JWT Secret 暴露給前端：等同把 service_role 給人。
- ❌ 跳過簽章驗證只解 base64 讀 claims：完全沒安全可言，誰都能偽造 JWT。
- ❌ 自己手刻 HS/ES 驗章：用成熟套件，別自製密碼學程式碼。

## 認證事件的稽核

登入、登出、密碼重設等認證事件，Supabase 本身會記錄在 `auth.audit_log_entries`，不需要自己重做。專案自訂的 `audit_log`（見 `logging-retention.md`）負責的是**應用層的業務操作**（建立訂單、修改資料…），兩者互補。

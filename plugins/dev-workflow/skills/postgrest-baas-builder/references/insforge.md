# InsForge (Cloud / 自架) 補充規範

InsForge 是 PostgREST-compatible BaaS，跟 Supabase 形狀近 1:1：底層 Postgres + PostgREST，RLS 模型相同，`auth.uid()` / `auth.email()` / `auth.role()` 都有，PostgREST filter 語法 (`eq.`, `neq.`, `in.`, `is.`) 一模一樣。SKILL.md 的十條鐵則完全套用。

差異集中在四件事：**API URL 前綴**、**admin 認證方式**、**幾個 Supabase 特有功能在 InsForge 平台不允許**、**dev/prod 兩個獨立 instance 怎麼部署**。

---

## API endpoint mapping（Supabase → InsForge）

| 操作 | Supabase | InsForge |
|---|---|---|
| 資料 CRUD | `GET/POST/PATCH/DELETE /rest/v1/<table>` | `GET/POST/PATCH/DELETE /api/database/records/<table>` |
| RPC | `POST /rest/v1/rpc/<fn>` | `POST /api/database/rpc/<fn>` |
| Admin SQL（繞 RLS） | service_role JWT 對 `/rest/v1/...` | `POST /api/database/advance/rawsql` 帶 admin API key |
| Auth sign in | `POST /auth/v1/token?grant_type=password` | `POST /api/auth/sessions` |
| Current user | `GET /auth/v1/user` | `GET /api/auth/sessions/current` |
| Refresh | `POST /auth/v1/token?grant_type=refresh_token` | `POST /api/auth/refresh` |
| Create user (admin) | `POST /auth/v1/admin/users` | `POST /api/auth/users?client_type=server` |
| Delete user (admin) | `DELETE /auth/v1/admin/users/<id>` | `DELETE /api/auth/users` body `{userIds:[...]}` |
| Storage upload | `POST /storage/v1/object/<bucket>/<key>` | `PUT /api/storage/buckets/<bucket>/objects/<key>` |
| Storage list buckets | `GET /storage/v1/bucket` | `GET /api/storage/buckets` |
| Storage signed URL（私有 bucket） | `POST /storage/v1/object/sign/<bucket>/<key>` | **沒有原生 endpoint**；走 backend proxy |

**Header 規則**：InsForge 只看 `Authorization: Bearer <token>`，**不需要 `apikey:` header**（Supabase 兩個都要）。把 Supabase client port 過去時記得拔掉 `apikey:` 設定。

---

## Admin 認證（取代 service_role）

| 元素 | Supabase | InsForge |
|---|---|---|
| 後端繞 RLS 用 | `SUPABASE_SERVICE_ROLE_KEY`（JWT，以 JWT_SECRET 簽） | **admin API key**（`ik_` 前綴，非 JWT）|
| 後端驗 user JWT | HS256 + `SUPABASE_JWT_SECRET`（自架） / JWKS（Cloud） | HS256 + InsForge `JWT_SECRET`（值取自 instance 設定，自架見下節） |
| 對應 Postgres role | `service_role`（pg_role） | **沒有** `service_role` role；admin API key 走平台層 auth |

實務後端 client 改造：
- env var 名稱可保留 `SUPABASE_SERVICE_ROLE_KEY` 跟 `SUPABASE_JWT_SECRET` 當歷史包袱，但值換成 InsForge 的 admin API key 跟 JWT secret。
- 任何 `grant ... to service_role` 在 InsForge migration 內**要拿掉**；admin 操作走 admin API key 不靠 role。

---

## InsForge 平台限制 → 適配清單

從 Supabase migration 搬到 InsForge 時要改的東西：

| Supabase 寫法 | InsForge 適配 |
|---|---|
| `create extension moddatetime schema extensions` | **不允許安裝**，用 plpgsql polyfill 取代（一份函式即可，trigger 語法不用改） |
| `new.raw_user_meta_data ->> 'name'` | `auth.users.raw_user_meta_data` **欄位不存在**，改 `new.profile ->> 'name'`（display name）或 `new.metadata ->> 'role'`（自訂 metadata） |
| `grant ... to service_role` | 移除（InsForge 沒這 role） |
| `cron.schedule(...)` | **不允許寫 `cron` schema**；改用 InsForge **scheduled functions**（`schedules.jobs` 表 + 一個 edge function endpoint），或退一步用 backend goroutine ticker |
| `insert into storage.buckets (...)` | `storage.buckets` columns 不同（沒 `id` 欄位），改走 InsForge API：`POST /api/storage/buckets` body `{"bucketName": "...", "isPublic": true/false}`，或 MCP `create-bucket` 工具 |
| `create policy on storage.objects` | InsForge storage 用內建 `public`/`private` flag + token，**不走 SQL RLS**；policy 不會生效，直接刪掉 |
| `auth.users.raw_user_meta_data` 在 trigger function 用 | 改 `new.profile` (jsonb) 或 `new.metadata` (jsonb) |

moddatetime polyfill 模板：

```sql
create schema if not exists extensions;
create or replace function extensions.moddatetime()
returns trigger language plpgsql as $$
declare col text := tg_argv[0];
begin
  if col is null or col = '' then col := 'updated_at'; end if;
  new := jsonb_populate_record(new, to_jsonb(new) || jsonb_build_object(col, now()));
  return new;
end; $$;
```

裝好這個之後 `execute function extensions.moddatetime(updated_at)` trigger 寫法跟 Supabase 完全相容，不用改。

---

## 第一次接手 InsForge 實例 checklist

任何時候第一次連到一個 InsForge 實例（不論 Cloud / 自架、自己建的 / 別人交接的），開工前跑這份。

### A. 連對實例

1. 確認 backend URL（Cloud `*.us-east.insforge.app` / 自架 `*.zeabur.app` 或自訂 domain）。
2. 取得 admin API key（`ik_` 開頭）。
3. 用 curl 試打：`curl $URL/api/database/advance/rawsql -H "Authorization: Bearer $KEY" -H "Content-Type: application/json" -d '{"query":"select version()","params":[]}'`。預期 HTTP 200 + version 字串。
4. 對照專案文件 / `.env.example`：URL 跟期望的 dev / prod 環境一致嗎？

### B. JWT secret 在哪 + 是不是預設值

InsForge 用 HS256 對稱簽 JWT，後端要拿到這把 secret 才能本地驗章。

- **Cloud 版**：dashboard 看 settings，或 `system.secrets` 表（ciphertext，需透過 InsForge 介面 reveal）。
- **自架版（Zeabur 上跑 InsForge template）**：
  - 從 Zeabur env vars 直接讀：`zeabur execute-command` 在 `insforge` service 內跑 `echo $JWT_SECRET`。
  - **警告**：自架 template 預設 `JWT_SECRET = your-super-secret-jwt-token-with-at-least-32-characters-long`，這是公開字串。**上 prod 前必須換成 48+ 字元隨機**，並重簽 ANON_KEY。

### C. dev/prod 是不是真的兩個 instance

回頭看鐵則 1：**一個 InsForge 實例 = 一個資料庫**。檢查：

- dev instance 跟 prod instance 是兩個分開的 InsForge project（Cloud）或兩個分開的 Zeabur project / 同 project 兩套 stack（自架）。
- 兩邊的 `JWT_SECRET` 不能共用（共用 → dev 漏 key = prod 漏 key）。
- 兩邊的 admin API key 不能共用。
- backend / dashboard 的 env vars 真的指向各自環境，沒有 dev backend 連到 prod URL 這種事。

不確定就跑：對兩個 instance 都打 `select email from auth.users limit 3`，看資料是不是一樣（一樣就是搞錯了）。

### D. Schema / extensions / RLS

```sql
-- 列 public schema 表
select tablename from pg_tables where schemaname='public' order by tablename;
-- 對齊 supabase/migrations/ 應該有的表

-- 列已裝 extensions
select extname, extversion from pg_extension order by extname;
-- 預期應該有：pgcrypto, pg_cron, pgjwt, uuid-ossp, pg_net 等

-- 每張表 RLS 狀態
select tablename, c.relrowsecurity as rls,
  (select count(*) from pg_policy where polrelid=c.oid) as policies
from pg_tables t join pg_class c on c.relname=t.tablename
where schemaname='public' order by t.tablename;
-- 鐵則 4：每張 public 表都該 rls=true 且 policies > 0
```

### E. Backend 對 InsForge 的連線測

跑一個 round-trip test（select customers + sign JWT + verify JWT + ExecRawSQL），確認後端 Go client 路徑跟 secret 都對。模板見專案的 `cmd/insforge-smoke/` 或類似一次性檔。

---

## MCP per-project 設定 SOP

InsForge MCP 是 **per-instance**（一把 API key 綁一個 URL），**必須用 project scope**，不能放 user scope（會跨專案撈錯庫）。

對比：
- Supabase Cloud MCP（claude.ai）：OAuth，跨 project 自動分流 → user scope OK
- Zeabur MCP：一把 token 管所有 project → user scope OK
- **InsForge MCP**：一把 key + URL → 必須 project scope

### 設定步驟

1. 移掉 user scope 的 insforge（如果有）：
   ```bash
   claude mcp remove insforge --scope user
   ```

2. 在專案根目錄加 project scope：
   ```bash
   claude mcp add insforge --scope project \
     -e API_KEY=ik_<your-admin-key> \
     -e API_BASE_URL=https://<instance>.<host> \
     -- npx -y @insforge/mcp@latest
   ```

3. `.mcp.json` 加進 `.gitignore`（含 API key）：
   ```
   # MCP 設定（含 InsForge API key 等，禁止進 git；範本見 .mcp.json.example）
   .mcp.json
   ```

4. 寫 `.mcp.json.example` 進 git 當範本：
   ```json
   {
     "_why_project_scope": "InsForge MCP 一把 API key 綁一個 instance，必須 per-project；放 user scope 會跟其他 project 混淆。",
     "mcpServers": {
       "insforge": {
         "type": "stdio",
         "command": "npx",
         "args": ["-y", "@insforge/mcp@latest"],
         "env": {
           "API_KEY": "ik_REPLACE_WITH_YOUR_INSFORGE_ADMIN_API_KEY",
           "API_BASE_URL": "https://<your-instance>.zeabur.app"
         }
       }
     }
   }
   ```

5. 其他開發者 clone 時：複製 `.mcp.json.example` → `.mcp.json`，填自己的 key。

### dev + prod 雙 instance 的 MCP 設定

兩種做法擇一：

**做法 A：`.mcp.json` 只列 dev**（推薦）
- 日常開發用 MCP 連 dev。
- 操作 prod 走 `curl` + 從 password manager 取 prod key，或暫時改 `.mcp.json` 指向 prod（操作完改回 dev）。
- 好處：不會無意間在 MCP 一聲令下對 prod 操作。

**做法 B：`.mcp.json` 列 dev + prod 兩個 entry**
```json
{
  "mcpServers": {
    "insforge-dev":  { "env": { "API_KEY": "ik_dev_...",  "API_BASE_URL": "https://...-dev.zeabur.app" } },
    "insforge-prod": { "env": { "API_KEY": "ik_prod_...", "API_BASE_URL": "https://...-prod.zeabur.app" } }
  }
}
```
- 工具會以 `mcp__insforge-dev__*` / `mcp__insforge-prod__*` 兩組命名出現，操作時對應到不同實例。
- 風險：工具名稱看一眼就點錯，仍要靠鐵則 8 把關。

**不論哪種，鐵則 8 不變**：操作 prod 前必須先取得使用者明確同意。

---

## dev/prod 雙實例部署原則（自架）

回到鐵則 1：「一個實例 = 一個資料庫」。自架 InsForge 要 dev/prod 兩環境，**必須部署兩份完整 InsForge stack**：

- **Zeabur**：兩個 Zeabur project，各跑一份 InsForge template（4 容器：`insforge` + `postgrest` + `postgres` + `deno`）。命名建議 `<專案>-Dev` / `<專案>-Prod`。
- **同 Zeabur 帳號下不同 project 比同 project 兩套 stack 更乾淨**：env vars / DNS / 內部 hostname 全部隔離，刪 dev 不會影響 prod。
- 兩邊的 admin API key、JWT_SECRET、ANON_KEY 全部分別產，**禁止共用**。

不要被「省一個容器」誘惑跑 「同 instance + 不同 schema 」這種偷懶分法 —— `auth.users`、`storage.buckets`、`system.secrets` 都會混在一起，違反鐵則 1。

---

## 故障排查

| 症狀 | 可能原因 | 排查 |
|---|---|---|
| `/api/database/records/*` 401 「No token provided」 | header 少帶 Authorization | 確認帶 `Authorization: Bearer <token>`，**不需要也不要帶 `apikey:`** |
| `/api/database/records/*` 401 但 token 是新的 | JWT_SECRET 不對（後端用的 secret 跟 InsForge 簽 token 的不一致） | 用 InsForge 發的 anon token 打 `/api/database/records/products`，回 200 才表示 secret 對；不對就重抓 InsForge 的 JWT_SECRET 寫進後端 env |
| RLS policy 沒生效（admin / authenticated 都拿不到） | `is_admin()` function 內 `auth.uid()` 回 null | 用 raw SQL 確認 `select auth.uid()`：admin API key 操作下會回 null（admin 不走 RLS）；以 user JWT 帶 Authorization 操作才會回 user id |
| `POST /api/auth/users` 409 ALREADY_EXISTS | InsForge 自架 template 初次部署會自動建一個 admin（用 Zeabur env vars 的 ADMIN_EMAIL） | 看 `auth.users` 已有什麼，補建 profile + 改密碼，不要重建 |
| Insert 回 400 "Expected array, received object" | InsForge 強制 body 為 array | 後端 client 自動 wrap single object 成 `[obj]`；前端 SDK 已內建處理 |
| ExecRawSQL 400 "params: Expected array, received null" | nil params 傳成 null | params 沒帶就傳 `[]`，不是 `null` |
| **INSERT 任何掛 audit trigger 的表 400 `invalid input syntax for type uuid: "project-admin-with-api-key"`** | **InsForge admin API key 操作下，把 `request.jwt.claims.sub` 設成這字串；`auth.uid()` 內部試 `::uuid` cast 直接 raise，trigger 內 `auth.uid()` 撞牆 → 整個 transaction rollback** | **必修**：所有 trigger function（`record_audit`、`is_admin`、任何用 `auth.uid()` 的）內把 `auth.uid()` 用 PL/pgSQL `begin … exception when others then … end` 包起來，cast 失敗就視為 null（或 false）。範例見下方「safe `auth.uid()` polyfill」 |
| `dev_url == prod_url` 才發現連錯 | env var 拼錯 / `.env.development` 跟 `.env.production` 共用 | 走鐵則 1 的「跑 select email from auth.users 對比」確認 |

### safe `auth.uid()` polyfill（任何 InsForge 專案開工就該套）

InsForge 用 admin API key 操作時把 `request.jwt.claims.sub` 設成 `"project-admin-with-api-key"`，原生 `auth.uid()` cast 會炸。**所有自己寫的 SECURITY DEFINER function / trigger 都要在用 `auth.uid()` 之前包 exception**：

```sql
-- 範例：record_audit trigger
create or replace function public.record_audit()
returns trigger language plpgsql security definer set search_path = '' as $body$
declare v_actor uuid;
begin
  begin
    v_actor := auth.uid();
  exception when others then
    v_actor := null;
  end;
  -- ... 後面用 v_actor 代替 auth.uid()
end;
$body$;
```

is_admin / lookup_user_email 等同樣處理。Supabase Cloud 上 `auth.uid()` 無 JWT 時回 null（不 raise），套這 polyfill 不破壞 Cloud 行為，是無痛的 cross-platform fix。**InsForge 專案初始化時就把這個 polyfill 包進每個 trigger 範本**，不要等踩到才補。

---

## InsForge 安全已知問題（部署時要記得）

- **edge function runtime 會 inject 所有 reserved secrets 成 env vars，且 function endpoint 可能無認證**（至少 cloud 版實測如此）。任何能 deploy 一個 function 的人就能撈 API_KEY / JWT_SECRET 原文。**自架部署時要管 edge function 部署權限**（只給可信操作者）。Cloud 版這是個已知設計問題（值得開 issue）。
- **自架 template 預設 secret 是公開字串**（`your-super-secret-jwt-token-with-at-least-32-characters-long`），上 prod 必換。
- 自架 template 部署時用 `ADMIN_EMAIL` / `ADMIN_PASSWORD` 自動建一個 admin user。這帳號**先於 trigger 創建**，沒對應 `public.profiles` row；如果業務系統靠 profiles.role 判 admin，要手動補 INSERT profiles + 設 role='admin'。

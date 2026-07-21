---
name: postgrest-baas-builder
description: "Build services on PostgREST-compatible BaaS (Supabase / InsForge) — RLS, Auth, PostgREST queries, MCP settings. This skill MUST be loaded before writing any RLS policy or PostgREST query, and MUST NOT be skipped because the query looks like ordinary SQL. Triggers on: 用 Supabase / InsForge 做後端, 設計 RLS policy, 寫 PostgREST query, 處理 BaaS Auth, 設定 MCP, 推 Supabase production, 自架 Supabase, InsForge"
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Grep
  - AskUserQuestion
metadata:
  version: "1.1.0"
---

## 前置

**載入這個 skill 前，先確認已載入 `db-engineering`。** 通用 DB 鐵則（migration 紀律、稽核 log、軟刪除、效能、完整性、環境分離）都在 db-engineering 裡，這裡只處理 BaaS 專用的部分。

---

## BaaS 專用鐵則

### 1. 一律啟用 RLS

`public` schema 下每一張新表，建立時就 `enable row level security`，並補上明確 policy。沒有例外、不是選項。

Policy 寫法規範見 `references/rls.md`。

### 2. Auth 用 BaaS 內建

認證一律走 `auth.users`（Supabase）或平台內建 auth（InsForge），不要自己另開一張 users 表來做帳密。要存額外的使用者資料時，才開一張 `profiles` 之類的擴充表，以 `auth.users.id` 為外鍵。

Auth 串接細節見 `references/auth.md`。

### 3. PostgREST 查詢規範

- `select=` 明列欄位，不用 `*`
- 同一張表「列表用」「計算用」「embed 用」拆不同 repo function，別共用一支胖查詢

### 4. RLS 效能

- policy 內 `auth.uid()` 一律包成 `(select auth.uid())`
- 每條 policy 寫 `to <role>`
- 同一 (role, action) 不要疊多條 permissive
- `security definer` function 要 `set search_path = ''` 並標 `stable`

### 5. MCP 設定（BaaS 跟 IaaS 不一樣）

| MCP | scope | 為什麼 |
|---|---|---|
| **Supabase Cloud** | OAuth 自動 | 一個帳號連 OAuth，跨 project 用工具參數切 |
| **InsForge** | **project scope** | 一把 API key 綁一個 instance，多 project 必須各自一份 `.mcp.json` |
| **Zeabur** | user scope | 一把 token 管所有 project |

InsForge MCP project scope 設定：

```bash
claude mcp add insforge --scope project \
  -e API_KEY=ik_xxx \
  -e API_BASE_URL=https://<instance>.<host> \
  -- npx -y @insforge/mcp@latest
```

`.mcp.json` 一定要加 `.gitignore`，同時建 `.mcp.json.example` 進 git 當範本。

---

## 自架 Supabase 補充

- **Auth 簽章**：自架 GoTrue 預設用對稱 HS256 + 共享 `JWT_SECRET`
- **ANON_KEY / SERVICE_ROLE_KEY** 是自己簽的固定 JWT，secret rotation 要自己做
- **整套 stack 12 個服務**，secret 變動牽動多個服務
- **沒有 Cloud MCP**，改用 psql 直連 / curl PostgREST

第一次接手自架 Supabase，先跑 `references/self-hosted-on-zeabur.md` 的全面 checklist。

## InsForge 補充

- URL 路徑不同：`/rest/v1/*` → `/api/database/records/*`
- Service role 等同物：admin API key（`ik_` 前綴）
- 平台限制：`moddatetime` 不能裝、`raw_user_meta_data` 不存在、`cron.schedule` 不能寫

第一次接手 InsForge，先跑 `references/insforge.md` 的 checklist。

---

## 欄位命名慣例

用 Supabase / InsForge 生態系標準名稱：

- `id` — `uuid default gen_random_uuid()` 或 `bigint generated always as identity`
- `created_at timestamptz not null default now()`
- `updated_at timestamptz not null default now()` — 由 `moddatetime` trigger 維護
- `deleted_at timestamptz`（可為 null）

禁止用 `update_time`、`is_deleted`、`removed`、`modified`。

---

## 參考檔案

- `references/rls.md` — RLS policy 樣板（擁有者制、公開讀、軟刪感知、service_role）
- `references/auth.md` — Supabase Auth、profiles 擴充表、JWT 驗證
- `references/insforge.md` — InsForge API endpoint mapping、admin key、適配清單
- `references/self-hosted-on-zeabur.md` — 自架 Supabase on Zeabur checklist

## 起手式素材（assets/）

- `assets/env.example` — `.env.example` 範本
- `assets/gitignore.snippet` — 該忽略的項目
- `assets/starter-migrations/0001_init_extensions.sql` — Supabase extensions
- `assets/starter-migrations/0002_profiles.sql` — auth.users 擴充表
- `assets/starter-migrations/example_table.sql` — 業務表範本（完整套用 BaaS 鐘則）

## 收尾自我檢查

- [ ] 每一張 `public` 表都已 `enable row level security` 且有明確 policy
- [ ] 認證走 `auth.users`；沒有自製帳密 users 表
- [ ] PostgREST 查詢 `select=` 明列欄位、不用 `*`
- [ ] policy 內 auth 函式都包成 `(select ...)`
- [ ] 每條 policy 都寫 `to <role>`
- [ ] 跑過 `get_advisors(type=performance)` 與 `get_advisors(type=security)`，沒有新 WARN

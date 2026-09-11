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
  version: "1.3.0"
---

## 前置

**載入這個 skill 前，先確認已載入 `db-engineering`。** 通用 DB 鐵則（migration 紀律、稽核 log、軟刪除、效能、完整性、環境分離）都在 db-engineering 裡，這裡只處理 BaaS 專用的部分。

---

## BaaS 專用鐵則

### 1. 一律啟用 RLS

`public` schema 下每一張新表，建立時就 `enable row level security`，並補上明確 policy。沒有例外、不是選項。

撰寫或修改 policy 前，先讀 [RLS 規範與樣板](references/rls.md)。

### 2. Auth 用 BaaS 內建

認證一律走 `auth.users`（Supabase）或平台內建 auth（InsForge），不要自己另開一張 users 表來做帳密。要存額外的使用者資料時，才開一張 `profiles` 之類的擴充表，以 `auth.users.id` 為外鍵。

串接 Auth、擴充 profiles 或處理 JWT 驗證前，先讀 [Auth 指南](references/auth.md)；InsForge 另依下方平台指南適配。

### 3. PostgREST 查詢規範

- `select=` 明列欄位，不用 `*`
- 同一張表「列表用」「計算用」「embed 用」拆不同 repo function，別共用一支胖查詢

### 4. RLS 效能

撰寫或修改 policy、PostgREST 查詢前，必讀 [效能指南](references/performance.md)。

- policy 內 `auth.uid()` 一律包成 `(select auth.uid())`
- 每條 policy 寫 `to <role>`
- 同一 (role, action) 不要疊多條 permissive
- `security definer` function 要 `set search_path = ''` 並標 `stable`

### 5. 金鑰保護

含金鑰的 `.mcp.json` 加入 `.gitignore`，另建不含真實金鑰的 `.mcp.json.example` 供版本控制。

## 自架 Supabase 補充

- **Auth 簽章**：自架 GoTrue 預設用對稱 HS256 + 共享 `JWT_SECRET`
- **ANON_KEY / SERVICE_ROLE_KEY** 是自己簽的固定 JWT，secret rotation 要自己做
- **整套 stack 12 個服務**，secret 變動牽動多個服務
- **沒有 Cloud MCP**，改用 psql 直連 / curl PostgREST

第一次接手自架 Supabase，先跑 [自架指南](references/self-hosted-on-zeabur.md) 的全面 checklist。後續處理 Auth 簽章、金鑰輪換或服務設定時，先讀其中對應章節。

## InsForge 補充

- URL 路徑不同：`/rest/v1/*` → `/api/database/records/*`
- Service role 等同物：admin API key（`ik_` 前綴）
- 平台限制：`moddatetime` 不能裝、`raw_user_meta_data` 不存在、`cron.schedule` 不能寫

第一次接手 InsForge，先跑 [InsForge 指南](references/insforge.md) 的 checklist。處理 API、Auth、資料庫適配或 MCP 設定前，先讀其中對應章節；MCP 設定依「MCP per-project 設定 SOP」操作。

## 平台與參考文件

先確認目前使用 Supabase Cloud、自架 Supabase 或 InsForge，以及目標專案與環境，再讀取對應文件：

| 平台或工作 | 必讀內容 |
|---|---|
| 自架 Supabase on Zeabur | [自架指南](references/self-hosted-on-zeabur.md)：Auth 簽章、金鑰輪換、服務設定與維運工具。第一次接手先執行其中的全面 checklist。 |
| InsForge | [InsForge 指南](references/insforge.md)：API 路徑、admin key、平台限制與適配方式。第一次接手先執行其中的 checklist；設定 MCP 時依「MCP per-project 設定 SOP」操作。 |
| RLS policy | [RLS 規範與完整樣板](references/rls.md) |
| Policy 或 PostgREST 查詢 | [效能指南](references/performance.md)，寫入前必讀。 |
| Auth 串接 | [Auth 指南](references/auth.md)：Supabase Auth、profiles 與 JWT 驗證；InsForge 同時依其平台指南適配。 |

Supabase Cloud 使用目前環境提供的工具，操作前核對工具參數與目標 project。自架與 InsForge 的連線及 MCP 設定依各自指南。

欄位命名與通用資料慣例依前置 `db-engineering` 的 `references/data-conventions.md`；平台不支援的功能依上述平台指南適配。

## 起手式素材（assets/）

- `assets/env.example` — `.env.example` 範本
- `assets/gitignore.snippet` — 該忽略的項目
- `assets/starter-migrations/0001_init_extensions.sql` — Supabase extensions
- `assets/starter-migrations/0002_profiles.sql` — auth.users 擴充表
- `assets/starter-migrations/example_table.sql` — 業務表範本（完整套用 BaaS 鐵則）

## 收尾驗證

針對本次變更留下實際驗證結果：

- 以受影響的角色測試資料讀寫權限，包括允許及拒絕的情境；只用管理員金鑰測試，不能證明 RLS 正確。
- 驗證本次 Auth 串接或 PostgREST 查詢的實際行為，並確認符合上方 BaaS 規則。
- 環境提供 `get_advisors` 時，依實際工具參數執行 performance 與 security 檢查，處理本次新增的警告。既有警告與尚未解決的項目分開記錄。
- 沒有 advisors 時，以平台可用工具檢查受影響的 schema、權限、索引及查詢計畫，搭配角色存取測試。說明實際檢查範圍與未驗證項目，不宣稱已通過 advisors 掃描。

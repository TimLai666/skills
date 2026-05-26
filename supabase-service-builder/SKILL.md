---
name: supabase-service-builder
description: 建立或開發以 Supabase 為後端的服務時使用。涵蓋開發／正式環境分離（兩個獨立 Supabase 專案、預設連開發環境）、強制 migration 並納入 git 追蹤、強制啟用 RLS、優先使用 Supabase 內建 Auth、全操作稽核 log 與自動清理保留策略、軟刪除、以及 created_at/updated_at/deleted_at 標準欄位慣例。觸發時機：使用者說「用 Supabase 做一個服務／後端」、要新增資料表或設計 schema、要寫 migration、設定 RLS、處理 Supabase Auth、規劃環境分離、要把改動推到正式環境，或在既有 Supabase 專案上做任何結構或資料變更時。任何碰到正式環境資料庫的動作都必須先取得使用者明確同意。
---

# Supabase Service Builder

開發以 Supabase 為後端的服務時的標準作業流程。這份 skill 把專案的安全與可維護性鐵則固化下來，套用到「初始化新專案」「日常 schema 變更」「上正式環境」三種情境。

開始任何 Supabase 相關工作前，先確認自己理解下面八條鐵則。它們不是建議，是這類專案的硬性規範。

## 八條鐵則（不可妥協）

1. **雙環境、雙資料庫** — 一定有 `development` 與 `production` 兩套，各自連到**不同的 Supabase 專案**。兩者的資料、金鑰、URL 完全隔離。
2. **預設開發環境** — 任何啟動服務的指令、任何資料庫連線，預設一律連 development。連 production 必須是明確、刻意、有額外確認的動作。
3. **改動只走 migration，並納入 git** — 凡是能寫成 migration 的結構改動（建表、改欄位、加索引、policy、function、trigger…）一律寫成 migration 檔放進 `supabase/migrations/` 並 commit。**絕對禁止**直接在 Dashboard SQL Editor 或 psql 改了資料庫結構卻沒留下 migration 檔。
4. **一律啟用 RLS** — `public` schema 下每一張新表，建立時就 `enable row level security`，並補上明確 policy。該用 RLS 的地方就要用，沒有例外、不是選項。
5. **Auth 用 Supabase 內建** — 認證一律走 `auth.users`，不要自己另開一張 users 表來做帳密。要存額外的使用者資料時，才開一張 `profiles` 之類的擴充表，以 `auth.users.id` 為外鍵。
6. **全操作留稽核 log** — 系統的重要操作都要寫進 `audit_log`。log 表必須搭配自動清理（保留策略），用 `pg_cron` 定期刪除過期紀錄。
7. **優先軟刪除** — 刪除預設用軟刪（`deleted_at` 設時間戳），不做硬刪。硬刪只保留給法遵抹除、測試垃圾資料等明確情境。
8. **正式環境神聖不可侵犯** — 開發完全基於 development 資料庫。production 資料庫不能亂改、亂刪、亂動，任何碰它的動作（推 migration、改資料、跑 SQL、把 CLI link 過去）都必須先取得使用者明確同意。

## 欄位命名慣例

用生態系標準名稱，讓 `moddatetime` 等內建工具與 Supabase Dashboard 能直接認得，不要自創名稱：

- `id` — 主鍵，用 `uuid default gen_random_uuid()` 或 `bigint generated always as identity`，由 Postgres 產生，不要由應用程式產。
- `created_at timestamptz not null default now()` — 建立時間。
- `updated_at timestamptz not null default now()` — 更新時間，由 `moddatetime` trigger 自動維護。
- `deleted_at timestamptz`（可為 null）— 軟刪除標記；`null` 表示未刪除。

禁止用 `update_time`、`is_deleted`、`removed`、`modified` 這類自創或非標準名稱。

## 標準專案結構

```
project/
├── supabase/
│   ├── config.toml              # CLI 設定，納入 git
│   ├── migrations/              # 所有結構改動，納入 git
│   │   └── <timestamp>_<name>.sql
│   └── seed.sql                 # 本機開發用種子資料（非機敏）
├── .env.example                 # 環境變數範本，納入 git
├── .env.development             # 開發環境金鑰，git 忽略
├── .env.production              # 正式環境金鑰，git 忽略
└── .gitignore
```

`config.toml` 與 `migrations/` 一定要進 git；`.env.development` / `.env.production` 一定不能進 git。

## 工作流程

### A. 初始化新專案

1. 讀 `references/environments.md`，建立雙環境設定：開兩個 Supabase 專案（dev／prod），寫好 `.env.example`、`.env.development`、`.env.production`、`.gitignore` 與啟動指令（預設 development）。
2. `supabase init` 建立 `supabase/` 目錄；本機開發用 `supabase start` 跑本地 stack，或 link 到 dev 專案。
3. 把 `assets/starter-migrations/` 的起手式 migration 複製進 `supabase/migrations/`（依需要調整檔名時間戳）：擴充套件與共用 function、`profiles` 擴充表、`audit_log` 與保留策略。讀 `references/auth.md` 與 `references/logging-retention.md` 確認內容。
4. `supabase db reset` 在本機套用所有 migration，確認乾淨。
5. `git add supabase/ .env.example .gitignore` 並 commit。

### B. 日常 schema 變更（最常見的迴圈）

每一次結構改動都走這個迴圈，不要跳步：

1. `supabase migration new <描述性名稱>` 產生帶時間戳的空 migration 檔。
2. 在該檔案寫 SQL。新建表時務必同時：啟用 RLS、補 policy、加 `created_at/updated_at/deleted_at`、掛 `updated_at` 的 `moddatetime` trigger。參考 `references/rls.md`、`references/data-conventions.md` 與 `assets/starter-migrations/example_table.sql`。
3. `supabase db reset`（本機）或 `supabase db push`（推到 link 著的 **dev** 專案）套用並驗證。
4. `git add supabase/migrations/ && git commit` —— migration 檔一定要進版控。
5. migration 一旦 commit／推送就視為不可變。要再改，寫**新的** migration，不要回頭編輯舊檔。

若曾不小心直接在資料庫上動了結構，用 `supabase db diff` 把差異補抓成 migration 檔，立刻補回版控，讓資料庫狀態與 migrations/ 一致。

### C. 推上正式環境

碰 production 前**先停下來，向使用者要明確同意**。流程見 `references/production-safety.md`，重點：

1. 向使用者說明這次要推哪些 migration、影響什麼，取得明確同意。
2. 確認 production 已有備份／PITR 可用。
3. `supabase db push --dry-run` 先看會套用什麼，把清單給使用者確認。
4. 確認後才 `supabase db push` 到 prod 專案。
5. 結束後把 CLI link 回 dev 專案，避免之後誤操作。

絕不對 production 跑 `supabase db reset`，絕不在 prod 跑臨時的 `DELETE`/`UPDATE`/`DROP`，絕不把 service_role 金鑰外洩到前端。

## 參考檔案

依當下任務載入需要的參考檔，不用一次全讀：

- `references/environments.md` — 雙環境分離：Supabase CLI、`.env` 檔規劃、APP_ENV 載入器（JS／Python）、啟動指令。
- `references/migrations.md` — migration 紀律：何時寫、怎麼寫、不可變原則、補抓漂移、常見錯誤。
- `references/rls.md` — RLS 規範與常見 policy 樣板（擁有者制、公開讀、軟刪感知、service_role）。
- `references/auth.md` — Supabase Auth 用法、`profiles` 擴充表樣式、註冊時自動建 profile。
- `references/logging-retention.md` — `audit_log` 表設計、通用稽核 trigger、`pg_cron` 自動清理保留策略。
- `references/data-conventions.md` — 標準欄位、`updated_at` trigger、軟刪除實作與查詢樣式。
- `references/production-safety.md` — 正式環境護欄與上線檢查清單。

## 起手式素材（assets/）

- `assets/env.example` — `.env.example` 範本。
- `assets/gitignore.snippet` — 該忽略的項目。
- `assets/starter-migrations/` — 可直接複製進 `supabase/migrations/` 的起手 migration：擴充套件與共用 function、`profiles`、`audit_log` 與保留策略、以及一張示範表（完整套用全部鐵則）。

## 收尾自我檢查

交付前逐項確認：

- [ ] dev／prod 是兩個不同 Supabase 專案，金鑰／URL 完全分離。
- [ ] 啟動指令與連線預設 development。
- [ ] 每一個結構改動都有對應 migration 檔，且已 `git add`。
- [ ] 沒有任何「改了資料庫但沒留 migration」的情況。
- [ ] 每一張 `public` 表都已 `enable row level security` 且有明確 policy。
- [ ] 認證走 `auth.users`；沒有自製帳密 users 表（擴充表 `profiles` 例外且合理）。
- [ ] 重要操作會寫進 `audit_log`，且有 `pg_cron` 清理排程。
- [ ] 刪除走軟刪（`deleted_at`）；硬刪只在明確且必要時使用。
- [ ] 欄位用 `created_at/updated_at/deleted_at` 標準名稱。
- [ ] 沒有未經使用者同意就對 production 做任何變更。

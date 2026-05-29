---
name: supabase-service-builder
description: 建立或開發以 Supabase 為後端的服務時使用。涵蓋 dev/prod 環境分離、migration 紀律、RLS、Supabase Auth（含後端 JWKS 本地驗 JWT）、稽核 log、軟刪除、標準欄位慣例、效能地雷、CASCADE 與資料完整性審查。觸發：用 Supabase 做後端、設計 schema、寫 migration、設 RLS、處理 Auth、推 production，**或任何改到 DB 相關程式碼／結構的時候**。動 prod 必須先取得使用者明確同意。
---

# Supabase Service Builder

開發以 Supabase 為後端的服務時的標準作業流程。這份 skill 把專案的安全與可維護性鐵則固化下來，套用到「初始化新專案」「日常 schema 變更」「上正式環境」三種情境。

開始任何 Supabase 相關工作前，先確認自己理解下面十條鐵則。它們不是建議，是這類專案的硬性規範。

## 十條鐵則（不可妥協）

1. **雙環境、雙資料庫** — 一定有 `development` 與 `production` 兩套，各自連到**不同的 Supabase 專案**。兩者的資料、金鑰、URL 完全隔離。
2. **預設開發環境** — 任何啟動服務的指令、任何資料庫連線，預設一律連 development。連 production 必須是明確、刻意、有額外確認的動作。
3. **改動只走 migration，並納入 git** — 凡是能寫成 migration 的結構改動（建表、改欄位、加索引、policy、function、trigger…）一律寫成 migration 檔放進 `supabase/migrations/` 並 commit。**絕對禁止**直接在 Dashboard SQL Editor 或 psql 改了資料庫結構卻沒留下 migration 檔。
4. **一律啟用 RLS** — `public` schema 下每一張新表，建立時就 `enable row level security`，並補上明確 policy。該用 RLS 的地方就要用，沒有例外、不是選項。
5. **Auth 用 Supabase 內建** — 認證一律走 `auth.users`，不要自己另開一張 users 表來做帳密。要存額外的使用者資料時，才開一張 `profiles` 之類的擴充表，以 `auth.users.id` 為外鍵。
6. **全操作留稽核 log,分四層做齊** — 業界 logging 分四層:**Tier 1** DB-layer audit(trigger 寫 `audit_log`,抓狀態變更)、**Tier 2** Application/Request audit(middleware 寫 `request_log`,抓 IP/UA/path/status/actor/request_id)、**Tier 3** Security/SIEM(認證事件 + 異常告警,部分靠 Supabase auth log)、**Tier 4** Compliance archive(冷儲存依法規)。小商家 / 早期 MVP 至少做 1+2,缺 Tier 2 等於失明(DB trigger 抓不到 IP/UA)。**保留期照法規分流**:業務憑證類(orders/customers/products…)台灣商業會計法要求**至少 5 年**、稅務 7 年;運算 cache 類(customer_segments)90 天即可;request_log 30-90 天。同一張 `audit_log` 用 `entity_type` 在 cron 內分流。**failed auth 也要走 request_log**,不能靜默 401/403。完整 4 層分工、5W1H、法規保留期見 `references/logging-architecture.md`;trigger 與 pg_cron 實作見 `references/logging-retention.md`。
7. **優先軟刪除** — 刪除預設用軟刪（`deleted_at` 設時間戳），不做硬刪。硬刪只保留給法遵抹除、測試垃圾資料等明確情境。
8. **正式環境神聖不可侵犯** — 開發完全基於 development 資料庫。production 資料庫不能亂改、亂刪、亂動，任何碰它的動作（推 migration、改資料、跑 SQL、把 CLI link 過去）都必須先取得使用者明確同意。
9. **效能在設計期就決定** — Supabase 慢九成不是平台問題、是 schema / RLS / 程式寫法沒踩好。建表、寫 policy、寫 repo function 時就要避開地雷。完整清單與 anti-pattern 對照見 `references/performance-pitfalls.md`，最低底線：
    - **Schema**：每個 FK 欄位都建索引（PostgREST embed 不會自動走索引）；常用 filter／order 欄位也補上，軟刪表用 partial index。
    - **RLS**：policy 內 `auth.uid()` 一律包成 `(select auth.uid())`；每條 policy 寫 `to <role>`；同一 (role, action) 不要疊多條 permissive；`security definer` function 要 `set search_path = ''` 並標 `stable`。
    - **PostgREST 查詢**：`select=` 明列欄位不用 `*`；同一張表「列表用」「計算用」「embed 用」拆不同 repo function，別共用一支胖查詢。
    - **應用層**：絕不在 `for` 迴圈內呼叫 DB（用 `id=in.(...)` 批次抓）；多筆寫入用 array body 一支 request 灌完；後端對 Supabase 共用 long-lived HTTP client、調好 connection pool、設 timeout；前端 fetch 與 `getSession()` 都要套 `AbortController` timeout。
    - **驗證**：migration 寫完跑一次 `get_advisors(type=performance)` 確認沒新 warning；慢的 query 用 `EXPLAIN (ANALYZE, BUFFERS)` 看計畫。
10. **完整性在設計期就守住** — 效能問題會慢、**完整性問題會丟資料且修不回來**。完整審查面向見 `references/db-integrity-checklist.md`，最低底線：
    - **CASCADE 風險**：每條 FK 明確標 `on delete`。軟刪表的 children 預設用 `RESTRICT`，避免從 Dashboard 隨手刪 parent 把歷史 children 一起吃掉；只有 derived data（segments、cache、stats）才用 CASCADE，並在 migration 加註解說明。
    - **稽核覆蓋**：每張 `public` 表的 migration 必須同時掛 `audit_<table>` trigger（除 audit_log 本身）；漏掉的話該表所有變更會成黑洞。應用層的「呼叫外部服務」操作（推播、寄信、金流）也要有對應紀錄表，不能在記憶體跑完就忘。
    - **Log 顯示用欄位要 snapshot**：`audit_log` / `push_log` 等 log 表的 FK（actor_id、sent_by…）顯示時需要的 email / 姓名要在寫入當下 snapshot 成欄位，**不要靠 join 父表抓**——父表改 email 或被刪，log 顯示就跟著變或遺失追溯。`to_jsonb(new/old)` 抓的「實體狀態」OK 不用動。
    - **Snapshot vs Reference**：業務子表（訂單／合約／出貨…）對父表的關聯欄位要判斷「業務當下的值要不要凍住」。壽命超過 audit_log 保留期 + 要熱路徑顯示 → snapshot 成子表欄位（如 `order_items.product_name`、`orders.contact_phone`），**不要靠 audit_log 還原**——它會清、查詢也貴。
    - **過時設計**：新欄位要有寫入路徑、新表要有查詢路徑；定期跑 schema 盤點 SQL 找 orphan，刪除前先 deprecate 一個版本。
    - **驗證**：每次改 DB 結構跑 `get_advisors(type=security)` + `get_advisors(type=performance)`；改完跑檢查清單 SQL 確認所有 public 表都有 audit trigger。

**任何時候改了與 DB 相關的程式碼或結構**（新 migration、改 repo function、加 trigger、改 RLS、調 PostgREST 查詢…）**都要走 `performance-pitfalls.md` 與 `db-integrity-checklist.md` 兩份清單**。兩份是並列的，缺一不可——效能讓人罵，完整性讓人吃官司。

## 自架 Supabase（如 Zeabur）的補充規範

如果這個專案的 Supabase 不是 Cloud 版而是自架（Zeabur、Render、Hetzner VM、自己 docker-compose…），上面十條鐵則仍適用，但**幾個關鍵地方有差異**：

- **Auth 簽章機制**：自架 GoTrue 預設用對稱 HS256 + 共享 `JWT_SECRET`，後端驗章用 `SUPABASE_JWT_SECRET` env var 對稱驗。**不能直接套 Cloud 版的 JWKS path**（後端 `client.go` 若用 `keyfunc` + `ES256/RS256`，搬到自架要改回 HS256）。未來如果自架 GoTrue 啟用 asymmetric signing keys，再切回 JWKS。
- **ANON_KEY / SERVICE_ROLE_KEY 是「自己簽出來」的固定 JWT**，用 JWT_SECRET 對稱簽。Secret rotation 要自己做（產新 secret → 重簽兩把 JWT → 改 stack 所有服務 env → cascade redeploy），Cloud 版的「Dashboard 點按鈕輪換」不存在。
- **整套 stack 12 個服務**：Kong / Auth / REST / Storage / Realtime / Studio / Meta / Functions / Imgproxy / MinIO / Supavisor / Postgres。每個各吃一份 env vars，secret 變動牽動多個服務。
- **沒有 Supabase Cloud MCP**：`list_migrations`、`get_advisors`、`generate_typescript_types`、`get_logs` 都沒了。改用 psql 直連 / curl PostgREST / Zeabur MCP 的 `execute-command` 自己做。

**任何時候第一次接手一個自架 Supabase**（dev / prod、自己的、別人的、剛建好的、別人交接過來的），開工前**先跑 `references/self-hosted-on-zeabur.md` 的全面 checklist** —— 尤其要排查「Zeabur 殘留的 stale shared variables / DNS entry」，這是自架 Supabase 最容易**錯連其他 project**、debug 時找不到根因的根源。

別跳這個 checklist —— 第一次接手就跑過一輪，比之後追怪 502 / Connection refused 省時間。

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
3. 把 `assets/starter-migrations/` **全部**複製進 `supabase/migrations/`（依需要調整檔名時間戳）。順序就是檔名前綴:
   - `0001_init_extensions.sql` — 擴充套件、moddatetime
   - `0002_profiles.sql` — `auth.users` 擴充表 + 註冊自動建 profile trigger
   - `0003_audit_log.sql` — **Tier 1**:`audit_log` + `record_audit()` + `lookup_user_email()` + actor_email snapshot + 保留策略
   - `0004_request_log.sql` — **Tier 2**:`request_log` 表 + 保留策略(對應 backend 要寫 RequestLog middleware,範例見 `references/logging-architecture.md`)
   - `example_table.sql` — 業務表起手範本(複製進 migrations/ 後改名,做為新表的模板)

   讀 `references/auth.md`、`references/logging-architecture.md`、`references/logging-retention.md` 確認內容。**不要只複製 0001-0003 跳過 0004**——缺 Tier 2 等於失明,業界小商家及格線會直接掛。
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
- `references/auth.md` — Supabase Auth 用法、`profiles` 擴充表樣式、註冊時自動建 profile、後端 JWKS 本地驗 JWT（不要打 `/auth/v1/user`）。
- `references/logging-architecture.md` — Logging 業界四層分工(Tier 1-4)、5W1H 該記什麼、法規保留期(台灣會計法 5 年 / 稅務 7 年…)、依專案規模選哪些層、`request_log` 設計範例。**規劃 log 體質前必讀**。
- `references/logging-retention.md` — `audit_log` 表設計、通用稽核 trigger、`pg_cron` 自動清理保留策略(Tier 1 技術細節)。
- `references/data-conventions.md` — 標準欄位、`updated_at` trigger、軟刪除實作與查詢樣式。
- `references/performance-pitfalls.md` — 設計期就要避開的效能地雷（RLS auth.uid() initplan、FK 未建索引、multiple permissive policies、`to <role>` 省略、cursor 分頁、N+1、HTTP client 設定…）。新建表或寫 policy 前必讀。
- `references/db-integrity-checklist.md` — 資料完整性審查：CASCADE 風險判斷、稽核覆蓋、過時設計清理，以及「每次改 DB 相關內容必跑」的 SOP。
- `references/production-safety.md` — 正式環境護欄與上線檢查清單。
- `references/self-hosted-on-zeabur.md` — **自架 Supabase on Zeabur 專用**：與 Cloud 版的差異、第一次接手的全面 checklist、JWT/ANON/SERVICE_ROLE 替換流程、stale shared variables / DNS entry 排查、kong.yml read-only mount 的 envsubst 機制、cascade redeploy 清單。**第一次接觸某個 Zeabur Supabase stack 必讀**。

## 起手式素材（assets/）

- `assets/env.example` — `.env.example` 範本。
- `assets/gitignore.snippet` — 該忽略的項目。
- `assets/starter-migrations/` — 可直接複製進 `supabase/migrations/` 的起手 migration:`0001` 擴充套件、`0002` profiles + 註冊自動建檔、`0003` audit_log + actor_email snapshot + record_audit trigger(Tier 1)、`0004` request_log(Tier 2)、`example_table.sql` 業務表範本(完整套用全部鐵則)。**四個編號全要複製,缺 `0004` 等於缺 Tier 2**。

## 收尾自我檢查

交付前逐項確認：

- [ ] dev／prod 是兩個不同 Supabase 專案，金鑰／URL 完全分離。
- [ ] 啟動指令與連線預設 development。
- [ ] 每一個結構改動都有對應 migration 檔，且已 `git add`。
- [ ] 沒有任何「改了資料庫但沒留 migration」的情況。
- [ ] 每一張 `public` 表都已 `enable row level security` 且有明確 policy。
- [ ] 認證走 `auth.users`；沒有自製帳密 users 表（擴充表 `profiles` 例外且合理）。
- [ ] **Tier 1 + Tier 2 logging 都有**:`audit_log`(trigger 寫,DB 狀態變更)與 `request_log`(middleware 寫,API 呼叫脈絡含 IP/UA/path/status/actor/request_id)。
- [ ] request_log 的 IP 走 `realClientIP()` helper(CF-Connecting-IP → X-Forwarded-For 最左 → X-Real-IP → fallback),**不是**框架預設的 `c.ClientIP()` / `req.ip`,否則 production 整批變 Cloudflare 邊緣 IP。CF-Ray / 平台 trace id 放進 metadata。
- [ ] 保留期照法規分流:業務憑證(orders/customers/products…)5 年起、運算 cache(segments)90 天、request_log 30-90 天;同表用 `entity_type` 分流 cron。
- [ ] failed auth(401/403)也走 request_log,不靜默。
- [ ] 刪除走軟刪（`deleted_at`）；硬刪只在明確且必要時使用。
- [ ] 欄位用 `created_at/updated_at/deleted_at` 標準名稱。
- [ ] 每個 FK 欄位都有覆蓋索引；policy 內 auth 函式都包成 `(select ...)`；每條 policy 都寫 `to <role>`。
- [ ] PostgREST 查詢 `select=` 明列欄位、不用 `*`；不同用途有不同 repo function（lean vs embed）。
- [ ] 沒有「`for ... { db.X() }`」迴圈內 DB 呼叫；批次寫入用 array body 灌完。
- [ ] 後端對 Supabase 共用 long-lived HTTP client（調 `MaxIdleConnsPerHost`、設 `Timeout`）；前端 fetch 都套 `AbortController` timeout。
- [ ] 每條 FK 都明確標 `on delete`；軟刪表的 children 用 `RESTRICT`，CASCADE 只給 derived data 並加註解。
- [ ] 每張新表都掛 `audit_<table>` trigger；外部服務呼叫有對應紀錄表。
- [ ] log 表的 FK 顯示用欄位（actor_email、sender_name…）有 snapshot，不靠 join 父表顯示。
- [ ] 業務子表對父表的關聯欄位（產品名／價格／聯絡資訊／地址…）過 snapshot 判斷：壽命超過 audit 保留期 + 要熱路徑顯示就 snapshot 在子表，不靠 audit_log 還原。
- [ ] 新欄位 / 新表有寫入與查詢路徑；不留 orphan。
- [ ] 跑過 `get_advisors(type=performance)` 與 `get_advisors(type=security)`，沒有新的 WARN。
- [ ] 沒有未經使用者同意就對 production 做任何變更。

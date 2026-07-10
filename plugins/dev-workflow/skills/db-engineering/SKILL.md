---
name: db-engineering
version: 1.0.1
description: "Universal database engineering rules. Migration discipline, audit logging, soft delete, performance, data integrity. Triggers on: 任何資料庫相關工作, 建表, 改 schema, 寫 migration, DB design, database development, 設計資料庫, 改 DB 結構, 加欄位, 加索引, 改 table, SQL, 寫 trigger, 設計 API 的 DB 層, 查詢很慢, N+1, 效能優化, 資料完整性, CASCADE, 外鍵, 新增 table, 刪除資料, backup, 環境分離, dev prod 分開"
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Grep
  - AskUserQuestion
---

## Auto-trigger

**任何與資料庫相關的工作都要先載入這個 skill。** 包括但不限于：建表、改 schema、寫 migration、設計 API 的 DB 層、查效能問題、處理外鍵/CASCADE、做 backup、設定 dev/prod 分離。不論你用的是 Supabase、自架 Postgres、MySQL、MongoDB 或其他，只要動到 DB 就先讀這個。

---

## 十一條鐵則（不可妥協）

1. **雙環境、雙資料庫** — development 與 production 兩套，各自連到**不同的資料庫實例**。兩者的資料、金鑰、URL 完全隔離。絕不可用「同一個實例 + 不同 schema」這種偷懶分法。

2. **預設開發環境** — 任何啟動服務的指令、任何資料庫連線，預設一律連 development。連 production 必須是明確、刻意、有額外確認的動作。

3. **改動只走 migration，並納入 git** — 凡是能寫成 migration 的結構改動（建表、改欄位、加索引、trigger…）一律寫成 migration 檔放進 version control。**絕對禁止**直接在資料庫上改了結構卻沒留下 migration 檔。

4. **優先軟刪除** — 刪除預設用軟刪（`deleted_at` 設時間戳），不做硬刪。硬刪只保留給法遵抹除、測試垃圾資料等明確情境。

5. **正式環境神聖不可侵犯** — 開發完全基於 development 資料庫。production 資料庫不能亂改、亂刪、亂動，任何碰它的動作都必須先取得使用者明確同意。

6. **全操作留稽核 log** — 至少做兩層：
   - **Tier 1** DB-layer audit（trigger 寫 `audit_log`，抓狀態變更）
   - **Tier 2** Application/Request audit（middleware 寫 `request_log`，抓 IP/UA/path/status/actor/request_id）
   - 缺 Tier 2 等於失明（DB trigger 抓不到 IP/UA）
   - failed auth 也要走 request_log，不能靜默 401/403
   - 保留期照法規分流：業務憑證類至少 5 年、運算 cache 類 90 天、request_log 30-90 天

7. **效能在設計期就決定** — 資料庫慢九成不是引擎問題，是 schema / 索引 / 查詢寫法沒踩好：
   - 每個 FK 欄位都建索引
   - 常用 filter / order 欄位也補索引
   - 軟刪表用 partial index
   - 絕不在 `for` 迴圈內呼叫 DB（用批次查詢）
   - 後端共用 long-lived HTTP client，調好 connection pool，設 timeout

8. **完整性在設計期就守住** — 效能問題會慢，**完整性問題會丟資料且修不回來**：
   - 每條 FK 明確標 `on delete`
   - 軟刪表的 children 預設用 `RESTRICT`
   - 只有 derived data（segments、cache、stats）才用 CASCADE，並加註解
   - 新欄位要有寫入路徑、新表要有查詢路徑；不留 orphan

9. **欄位命名用標準名稱** — 用生態系標準名稱，不要自創：
   - `id` — 主鍵，由資料庫產生，不要由應用程式產
   - `created_at timestamptz not null default now()` — 建立時間
   - `updated_at timestamptz not null default now()` — 更新時間，由 trigger 自動維護
   - `deleted_at timestamptz`（可為 null）— 軟刪除標記

10. **Log 顯示用欄位要 snapshot** — log 表的 FK 顯示用欄位（actor_email、sender_name…）要在寫入當下 snapshot 成欄位，**不要靠 join 父表抓**。父表改 email 或被刪，log 顯示就跟著變或遺失追溯。

11. **Schema 先畫 ER model，再決定拆表與正規化** — 設計或優化 schema 時，先釐清 entity、attribute、relationship、cardinality、optional relationship、candidate key 與 functional dependency，畫出 ER model 後再決定表的拆分方式。沒有特殊業務需求時，先以無損連接且盡可能保留相依性的 BCNF 設計為基準。只有在實際量測到效能瓶頸，且業務需求確實需要時，才可為效能從 BCNF 放寬到 3NF，並記錄取捨與驗證結果。這裡的放寬不能低於 3NF，不得只因為預期會比較快、方便 join 或主觀感覺就反正規化。

---

## 工作流程

### A. 初始化新專案

1. 確認雙環境設定：dev / prod 兩個資料庫實例，各自獨立。
2. 寫好 `.env.example`、`.env.development`、`.env.production`、`.gitignore`。
3. 設定 migration 工具（golang-migrate / Flyway / Alembic / Prisma / Drizzle / 原生 SQL）。
4. 建立起手 migration：extensions、audit_log、request_log。
5. 確認本機能乾淨跑完所有 migration。

### B. 日常 schema 變更

每次結構改動都走這個迴圈：

1. 若涉及 schema 設計、表拆分、欄位歸屬或關係調整，先釐清業務規則與函數相依，畫出 ER model，確認 entity、relationship、cardinality、candidate key 與外鍵邊界。
2. 依 ER model 做無損拆分，預設以 BCNF 為目標。若因已量測的效能瓶頸與業務需求選擇 3NF，必須記錄原因、查詢或 workload 證據、完整性取捨與回歸驗證，且不得低於 3NF。
3. 產生新 migration 檔（帶時間戳）。
4. 寫 SQL。新建表時務必同時：加 `created_at/updated_at/deleted_at`、掛 `updated_at` trigger。
5. 本機跑 migration 驗證。
6. `git add` 並 commit — migration 檔一定要進版控。
7. migration 一旦 commit 就視為不可變。要再改，寫**新的** migration。

### C. 推上正式環境

碰 production 前**先停下來，向使用者要明確同意**：

1. 說明這次要推哪些 migration、影響什麼，取得明確同意。
2. 確認 production 已有備份 / PITR 可用。
3. 先跑 dry-run 確認會套用什麼。
4. 確認後才執行。
5. 結束後確認狀態正確。

絕不對 production 跑 reset，絕不在 prod 跑臨時的 DELETE/UPDATE/DROP。

---

## 參考檔案

- `references/performance-pitfalls.md` — 效能地雷：FK 未建索引、N+1、connection pool、查詢優化。新建表前必讀。
- `references/db-integrity-checklist.md` — 資料完整性：CASCADE 風險判斷、稽核覆蓋、過時設計清理。每次改 DB 必跑。
- `references/logging-architecture.md` — 稽核 log 四層分工、5W1H、法規保留期。規劃 log 前必讀。
- `references/logging-retention.md` — audit_log 表設計、通用稽核 trigger、自動清理策略。
- `references/data-conventions.md` — 標準欄位、updated_at trigger、軟刪除實作與查詢樣式。
- `references/migrations.md` — migration 紀律：何時寫、怎麼寫、不可變原則、補抓漂移。
- `references/environments.md` — 雙環境分離：.env 檔規劃、啟動指令。
- `references/production-safety.md` — 正式環境護欄與上線檢查清單。

## 起手式素材（assets/）

- `assets/starter-migrations/0003_audit_log.sql` — Tier 1 稽核 trigger。
- `assets/starter-migrations/0004_request_log.sql` — Tier 2 request_log 表。

## 收尾自我檢查

- [ ] dev / prod 是兩個不同資料庫實例，金鑰 / URL 完全分離。
- [ ] 啟動指令與連線預設 development。
- [ ] 每一個結構改動都有對應 migration 檔，且已 git add。
- [ ] 沒有任何「改了資料庫但沒留 migration」的情況。
- [ ] 刪除走軟刪（`deleted_at`）；硬刪只在明確且必要時使用。
- [ ] 欄位用 `created_at/updated_at/deleted_at` 標準名稱。
- [ ] 每個 FK 欄位都有索引。
- [ ] 沒有「`for ... { db.X() }`」迴圈內 DB 呼叫。
- [ ] 後端共用 long-lived HTTP client，調好 connection pool，設 timeout。
- [ ] 每條 FK 都明確標 `on delete`；軟刪表的 children 用 `RESTRICT`。
- [ ] 每張新表都掛 audit trigger；外部服務呼叫有對應紀錄表。
- [ ] log 表的 FK 顯示用欄位有 snapshot，不靠 join 父表。
- [ ] 新欄位 / 新表有寫入與查詢路徑；不留 orphan。
- [ ] Schema 設計或優化前已畫 ER model，並確認 entity、relationship、cardinality、candidate key 與函數相依。
- [ ] 預設以 BCNF 做無損拆分；若放寬到 3NF，有實際效能瓶頸與業務需求證據，且沒有低於 3NF。
- [ ] 沒有未經使用者同意就對 production 做任何變更。

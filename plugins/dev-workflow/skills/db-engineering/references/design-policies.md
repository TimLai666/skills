# 資料庫設計政策

1. **雙環境、雙資料庫** — development 與 production 兩套，各自連到**不同的資料庫實例**。兩者的資料、金鑰、URL 完全隔離。絕不可用「同一個實例 + 不同 schema」這種偷懶分法。

2. **預設開發環境** — 任何啟動服務的指令、任何資料庫連線，預設一律連 development。連 production 必須是明確、刻意、有額外確認的動作。

3. **結構改動走 migration** — 建表、改欄位、索引、trigger 等結構改動須留下 migration 檔，並納入版本控制。

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
   - 後端共用 long-lived DB 連線或 client，調好 connection pool，設 timeout

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

# 正式環境護欄

正式環境的資料庫是真實使用者的真實資料。預設把它當成**唯讀、神聖、碰不得**。開發完全在 development（本機 stack 或 dev 專案）進行；任何會影響 production 的動作都需要使用者明確同意。

## 預設行為

在 Supabase 專案上工作時，除非使用者明講要動 production：

- 所有指令、連線、migration 操作都針對 **development**。
- 把 production 資料庫視為唯讀。
- CLI 平時就 link 著 dev 專案。

## 碰 production 前必須先取得明確同意的動作

下列每一項，**執行前都要先停下來、向使用者說明、取得明確同意**：

- `supabase db push` 推 migration 到 prod。
- 對 prod 跑任何 DDL（建表、改欄位、加 policy、改 function…）。
- 對 prod 的資料跑 `INSERT` / `UPDATE` / `DELETE`。
- 把 CLI `link` 到 prod 專案。
- 對 prod 跑任何臨時 SQL，即使只是「看起來無害」的查詢以外的操作。
- 調整 prod 的 `pg_cron` 排程。

取得同意不是「我等下要動 prod 喔」這種順帶一提，而是明確說清楚**要做什麼、影響什麼、是否可逆**，並等使用者確認。

## 絕對禁止

- ❌ 對 production 跑 `supabase db reset`——這會清空整個資料庫。`db reset` 只用在本機。
- ❌ 跑任何 `--linked` / `--db-url` 指向 prod 的 reset 類指令。
- ❌ 在 prod 跑沒有 `WHERE` 或 `WHERE` 寫錯的 `DELETE` / `UPDATE`。
- ❌ 把 `service_role` 金鑰放進前端、commit 進 git、或貼到不安全的地方。
- ❌ 直接在 prod 手改結構卻不留 migration。

## 推 migration 上正式環境的流程

1. **已在 dev 驗證**：要推的 migration 已在本機或 dev 專案套用並測過。
2. **說明並取得同意**：告訴使用者這次推哪些 migration、會改什麼、有無破壞性改動（drop 欄位、改型別等），等明確同意。
3. **確認備份**：確認 prod 有可用的備份或 Point-in-Time Recovery。破壞性改動前尤其重要。
4. **dry run**：

   ```bash
   supabase link --project-ref <PROD_REF>
   supabase db push --dry-run
   ```

   把 dry-run 列出的待套用清單給使用者看，再次確認。
5. **正式推送**：確認無誤後才

   ```bash
   supabase db push
   ```

6. **link 回 dev**：

   ```bash
   supabase link --project-ref <DEV_REF>
   ```

   復原成平時狀態，避免之後誤操作打到 prod。

## 破壞性改動的處理

會刪資料或不可逆的 migration（drop 欄位、drop 表、改型別、加 `not null` 到既有欄位）要格外小心：

- 在 migration 註解清楚標出破壞性，並向使用者特別點明。
- 能用「漸進式」就用：先加新欄位 → 搬資料 → 之後另一個 migration 才移除舊欄位，而不是一步到位。
- 確認 prod 備份就緒後才動。

## 在 prod 改資料

若真的必須直接改 prod 的資料（修補事故等）：

- 先取得使用者明確同意。
- 先在 dev 用相同資料情境演練過。
- 在交易（transaction）裡操作，`DELETE`/`UPDATE` 一定要有正確的 `WHERE`，先 `SELECT` 同樣條件確認影響範圍與筆數。
- 優先軟刪而非硬刪。
- 操作本身也應留進 `audit_log`。

## 自我檢查

碰 production 前問自己：

- [ ] 這個動作使用者明確同意了嗎？
- [ ] 我確定現在的目標是 prod 而不是 dev 嗎（CLI link 的是哪個專案）？
- [ ] 改動已在 dev 驗證過了嗎？
- [ ] prod 有可用備份嗎？
- [ ] 這個動作可逆嗎？不可逆的話使用者知道嗎？
- [ ] 做完之後 CLI link 回 dev 了嗎？

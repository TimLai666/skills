# Migration 紀律

核心原則：**資料庫的結構狀態 = `supabase/migrations/` 裡所有檔案套用後的結果**。這個等式一旦破裂，專案就失控了。所以凡是能寫成 migration 的改動都要寫成 migration，而且要進 git。

## 什麼算「結構改動」

下列全部都要走 migration：

- 建立／刪除／更名資料表、schema、view
- 新增／修改／刪除欄位、預設值、約束（constraint）、索引
- RLS 的 `enable`／`disable` 與 policy 的增刪改
- function、trigger、procedure
- 啟用擴充套件（`create extension`）
- `pg_cron` 排程的建立／調整
- 角色權限的 `grant`／`revoke`

只有「資料」層面的東西（種子資料、一次性資料修補）不算結構，但本機種子資料仍建議放 `supabase/seed.sql`。

## 標準迴圈

```bash
# 1. 產生帶時間戳的空檔
supabase migration new add_orders_table

# 2. 編輯 supabase/migrations/<timestamp>_add_orders_table.sql 寫 SQL

# 3. 本機套用驗證（會依 migrations 重建本地 DB）
supabase db reset

#    或推到 link 著的 dev 專案
supabase db push

# 4. 進版控
git add supabase/migrations/
git commit -m "migration: add orders table with RLS"
```

## 不可變原則

migration 一旦 commit 或 push 出去，就視為**不可變的歷史**。

- 要改結構，永遠是寫**新的** migration，往前疊加。
- 不要回頭編輯已經套用過的舊 migration 檔——別人的環境、dev、prod 可能已經套用過舊版，改舊檔會造成各環境狀態不一致。
- 例外：migration 還沒推出去、純本機、還沒 commit，這時直接改舊檔再 `db reset` 是可以的。

## 嚴禁的事

- ❌ 在 Supabase Dashboard 的 SQL Editor 永久改結構卻不留 migration。
- ❌ 用 psql / 任何 client 直連資料庫下 DDL 卻不留 migration。
- ❌ 在 Dashboard 的 Table Editor 點一點改了欄位卻不留 migration。

Dashboard SQL Editor 可以用來**探索、查詢、試**；但只要試出了最終要的結構，就得把那段 SQL 整理成 migration 檔，這才是真正的來源（source of truth）。

## 修補漂移（drift）

如果發現資料庫實際結構和 `migrations/` 對不上（有人手動改過），用 diff 補抓：

```bash
# 比對 link 著的遠端專案與本地 migrations 的差異
supabase db diff -f capture_manual_changes
```

它會把差異寫成一個新的 migration 檔。檢查內容、確認無誤後 commit，讓版控重新追上實際狀態。之後就不要再手改了。

## 一個 migration 的內容建議

- 一個 migration 聚焦一件邏輯改動，檔名描述清楚（`add_orders_table`、`add_rls_to_profiles`）。
- 寫 DDL 時盡量用 `if not exists` / `or replace`，讓重複套用較安全。
- 新建表的 migration 一定要在同一檔內把這些一次寫齊：欄位（含 `created_at/updated_at/deleted_at`）、`enable row level security`、policy、`updated_at` 的 `moddatetime` trigger、需要的索引。不要分次補，避免出現「表建好了但 RLS 還沒開」的空窗。
- 參考 `assets/starter-migrations/example_table.sql` 的完整樣板。

## 環境順序

migration 永遠**先在 dev 驗證過，才推 prod**。dev（或本機）是試錯的地方；prod 只接收已驗證的 migration。推 prod 的流程見 `production-safety.md`。

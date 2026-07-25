# 效能地雷：設計時就要避開的坑

資料庫慢的時候，九成不是引擎問題，是 schema／索引／查詢寫法沒踩好。這份是「設計時就應該考慮、不要等變慢才修」的通用清單，每張新表都過一遍。

Supabase／PostgREST 專屬的效能地雷（RLS initplan、`select=`、`count=exact`、`getSession()`、冷啟動…）見 `postgrest-baas-builder` skill 的 `references/performance.md`，用 BaaS 時兩份都要過。

---

## 1. FK 沒有覆蓋索引 — join 走 seq scan

**症狀**：join／關聯查詢慢；刪除被參照的列很慢。Supabase advisor 報 `unindexed_foreign_keys`。

**原因**：Postgres **不會**自動幫 FK 建索引。`order_items.order_id` 是 FK 但沒索引時，join／embed 會對 `order_items` 全表掃。刪除被參照的列時也會慢（為了檢查 FK 完整性）。

**錯**：

```sql
create table public.order_items (
  id        uuid primary key default gen_random_uuid(),
  order_id  uuid not null references public.orders(id),
  product_id uuid not null references public.products(id),
  qty       int not null
);
-- 沒有任何索引在 order_id / product_id 上
```

**對**：

```sql
create table public.order_items (
  id         uuid primary key default gen_random_uuid(),
  order_id   uuid not null references public.orders(id),
  product_id uuid not null references public.products(id),
  qty        int not null
);

create index order_items_order_id_idx   on public.order_items (order_id);
create index order_items_product_id_idx on public.order_items (product_id);
```

**設計時規則**：建表時，**每一個 FK 欄位都要有對應索引**。寫完 `references ...` 就立刻在 migration 同檔加 `create index`。例外只有兩種：

- 該欄位已是複合 PK／其他索引的**最左前綴**（已被覆蓋）。
- 該表是只寫不查的純 append（很少見，要寫註解說明）。

對軟刪表用部分索引更省空間：

```sql
create index order_items_order_id_idx
  on public.order_items (order_id)
  where deleted_at is null;
```

---

## 2. 後端應用層的 N+1（迴圈內呼叫 DB）

**症狀**：建單／批次處理慢，且時間隨 item 數量線性放大。

**原因**：後端程式裡常見的反模式：

```go
for _, it := range items {
    p, _ := db.GetProduct(it.ProductID)   // 每個 item 一次查詢！
    total += p.UnitPrice * it.Quantity
}
```

雖然每支 query 本身可能很快（DB 端 1-2ms），但 backend → 資料庫（尤其走 HTTP 的 BaaS）是跨網路往返，每次可達 100-500ms。10 個 item 就 1-5 秒。

**對**：先收集 id，一次批次抓（SQL `where id in (...)`，PostgREST 用 `id=in.(...)`）：

```go
ids := collectIDs(items)
products, _ := db.GetProductsByIDs(ids)   // 1 支查詢拿全部
for _, it := range items {
    p := products[it.ProductID]
    total += p.UnitPrice * it.Quantity
}
```

**設計時規則**：寫程式時看到「`for ... { db.Xxx(...) }`」這種 pattern 警鈴就要響起。要嘛改成批次查詢、要嘛把運算下推 SQL（用 view／RPC）。集合寫入同理：repo 層提供批次版本，一支請求灌完，不逐筆送。

---

## 3. `security definer` function 沒固定 `search_path`

**症狀**：function 在 RLS 裡呼叫時，行為不穩定、或被人利用搶提權。

**原因**：`security definer` 的 function 會以建立者身分執行；若沒固定 `search_path`，呼叫端可以塞自己的 schema 進來覆蓋裡面的 table／function 名稱。

**對**：所有 `security definer` function 都要：

```sql
create function public.is_team_member(p_team_id uuid)
returns boolean
language sql
security definer
set search_path = ''           -- 必須
stable                         -- 能標就標，RLS 內可被快取
as $$
  select exists (
    select 1 from public.team_members
    where team_id = p_team_id and user_id = (select auth.uid())
  );
$$;
```

`stable` / `immutable` 標籤也很關鍵：RLS 引擎會把 stable function 的結果在同個 query 內快取，否則每列重算。

---

## 4. 經常被過濾／排序的欄位沒索引

**症狀**：列表頁慢，但「明明 RLS 沒問題」。

**原因**：常用 filter（`status`、`category`、`deleted_at`）或 order（`created_at desc`）的欄位沒索引就會 seq scan + sort。

**對**：

```sql
-- 軟刪表：用部分索引，省空間又快
create index orders_status_active_idx
  on public.orders (status)
  where deleted_at is null;

-- 「最新的 N 筆」這種查詢
create index orders_created_at_desc_idx
  on public.orders (created_at desc);
```

**設計時規則**：每張表寫完後問自己「最常見的三個查詢長什麼樣」，照那三個查詢補索引。

---

## 5. 後端 HTTP client 預設值不適合服務間通訊

**症狀**：backend 對資料庫 API 發請求慢、CPU 沒事卻 throughput 上不去；流量稍微多就掛住整個 service。

**原因**：Go / Node / Python 的 HTTP client 預設值是給「偶爾打單一網址」設計的：

- **Go `http.Client{}`**：用 `DefaultTransport`，`MaxIdleConnsPerHost = 2`、`Timeout = 0`（永不超時）。對「同一個 API host 高並發」場景，第 3 條並發就要重新 TCP+TLS handshake，跨網路非常貴；單一掛掉的請求會把 goroutine 永久占住。
- **Node `fetch` / `axios`**：預設沒 timeout，沒 keep-alive agent；要自己包 `AbortController` 與 `http.Agent({ keepAlive: true })`。
- **Python `requests`**：每個 `requests.get()` 都新開 connection；要改用 `Session()` 才有 keep-alive。

**對**（Go 範例）：

```go
t := http.DefaultTransport.(*http.Transport).Clone()
t.MaxIdleConns = 100
t.MaxIdleConnsPerHost = 20             // 預設只 2
t.IdleConnTimeout = 90 * time.Second

client := &http.Client{
    Transport: t,
    Timeout:   30 * time.Second,         // 整個請求硬上限
}
```

**設計時規則**：後端啟動時建一個 long-lived HTTP client 共用、調好 connection pool 與 timeout；別用 `http.DefaultClient` / `&http.Client{}`，那會把預設值的兩個坑都帶上。

---

## 6. 前端 fetch 沒有 timeout — UI 永遠卡在 loading

**症狀**：API 偶爾「卡住」永遠不回，loading spinner 一直轉、按鈕按不動。F5 重新整理就好。

**原因**：`fetch()` 本身沒有 timeout；如果 backend 冷啟動、TLS handshake 卡住、token 自動 refresh 死循環，request 就會永遠 pending。Loading flag 不釋放，UI 卡死。

**對**：用 `AbortController` 套 timeout：

```js
const ctl = new AbortController()
const timer = setTimeout(() => ctl.abort(), 20_000)
try {
  const res = await fetch(url, { signal: ctl.signal, ... })
} finally {
  clearTimeout(timer)
}
```

**設計時規則**：所有對外的 fetch 都要有 timeout；UI 的 loading flag 一律在 `finally` 釋放，不靠 try 內的成功路徑。

---

## 7. 大量寫入後沒 ANALYZE — query plan 用錯統計

**症狀**：批次匯入幾萬列後，查詢突然變慢。

**原因**：Postgres planner 靠 `pg_statistic` 估列數。剛大量寫入時統計還沒更新，planner 可能誤判走 seq scan。

**對**：批次寫入結束後手動 `analyze`：

```sql
analyze public.orders;
```

migration 內若有 `insert ... select ...` 灌大量資料，後面接一條 `analyze`。

---

## 設計時自我檢查

### Schema / 索引
- [ ] 每個 FK 欄位都有索引（或被其他索引的最左前綴覆蓋）。
- [ ] 最常見的 filter／order 欄位有索引；軟刪表用部分索引 `where deleted_at is null`。
- [ ] `security definer` function 都有 `set search_path = ''` 與 `stable`/`immutable` 標籤。
- [ ] 大量寫入後跑 `analyze <table>`。

### 應用層
- [ ] 沒有「`for ... { db.X() }`」這類迴圈內 DB 呼叫——改成批次查詢。
- [ ] 集合寫入用批次，一支請求灌完。
- [ ] 後端共用一個 long-lived client，調好 connection pool、設 timeout。
- [ ] 前端所有 fetch 都套 `AbortController` timeout。

### 驗證
- [ ] 慢的 query 用 `EXPLAIN (ANALYZE, BUFFERS)` 看計畫——seq scan 大表就要補索引。
- [ ] 重要的 list endpoint 在 100x 資料量下試一次，看是否還在可接受範圍。
- [ ] 用 Supabase／PostgREST 時：另過 `postgrest-baas-builder` 的 `references/performance.md` 清單。

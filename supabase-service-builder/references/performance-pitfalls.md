# 效能地雷：設計時就要避開的坑

Supabase 慢的時候，九成不是平台問題，是 schema 與 RLS 設計沒踩好。這份是「設計時就應該考慮、不要等 advisor 警告才修」的清單。每張新表、每條 policy 都過一遍。

開發時隨時可以用 `mcp__supabase__get_advisors`（type=performance）一鍵掃出大部分問題；正式上線前也跑一次。

---

## 1. RLS auth.uid() 不包 `(select ...)` — 每列重算

**症狀**：列數一多就慢得離譜。advisor 報 `auth_rls_initplan` warning。

**原因**：policy 裡直接寫 `auth.uid()`，Postgres 把它當 volatile function，**每一列**都重新呼叫。1000 列就是 1000 次。

**錯**：

```sql
create policy "select_own"
  on public.notes for select
  using (auth.uid() = owner_id);
```

**對**：

```sql
create policy "select_own"
  on public.notes for select
  to authenticated
  using ((select auth.uid()) = owner_id);
```

把 `auth.uid()` 包進 `(select ...)` 子查詢，Postgres 會把它當 initplan **算一次**、結果快取整個 query。同樣套用於 `auth.jwt()`、`auth.role()`、`current_setting(...)`。

**設計時規則**：policy 裡只要出現 `auth.<fn>()` 或 `current_setting(...)`，**一律**包 `(select ...)`。

---

## 2. FK 沒有覆蓋索引 — embed / join 走 seq scan

**症狀**：`GET /rest/v1/orders?select=*,order_items(*)` 慢；advisor 報 `unindexed_foreign_keys`。

**原因**：Postgres **不會**自動幫 FK 建索引。`order_items.order_id` 是 FK 但沒索引時，PostgREST embed 會對 `order_items` 全表掃。刪除被參照的列時也會慢（為了檢查 FK 完整性）。

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

## 3. 同一 (role, action) 多條 permissive policy — 每條都跑

**症狀**：advisor 報 `multiple_permissive_policies`。

**原因**：RLS 對同一 role + action 有多條 `permissive` policy 時，Postgres 會把它們 `OR` 起來；每條都會被評估，每列都評估。policy 條件越複雜越貴。

**典型情境**：一張表既有「使用者讀自己的」又有「管理員讀全部」，兩條都是 `for select to authenticated`。

**改法選一**：

- **合併成一條**：用 `OR` 把條件寫在同一條 policy 裡。
  ```sql
  create policy "select_own_or_admin"
    on public.profiles for select
    to authenticated
    using (
      (select auth.uid()) = id
      or exists (select 1 from public.profiles p where p.id = (select auth.uid()) and p.role = 'admin')
    );
  ```
- **改用 restrictive**：管理員邏輯改成 `as restrictive`（restrictive 之間 `AND`，與 permissive 互動較好控制）。
- **角色拆開**：給管理員一個獨立 DB role（少見，較進階）。

**設計時規則**：規劃 policy 前先列「哪些 role 要做哪些 action」的表格，**同一格盡量只放一條 permissive policy**。

---

## 4. policy 沒指定 `to <role>` — service_role 也被檢查

**症狀**：後端用 service_role 的查詢比預期慢，advisor 不一定會報。

**原因**：policy 沒寫 `to ...` 時預設 `to public`，意味著**所有 role 都會檢查**——包括本來就繞過 RLS 的 `service_role`。雖然 service_role 最後會跳過，但條件還是會被解析、計畫；對複雜 policy 是不必要的開銷。

**對**：明確指定目標 role。前端用的就寫 `to authenticated` 或 `to anon, authenticated`。

```sql
create policy "select_own"
  on public.notes for select
  to authenticated                     -- 明確指定
  using ((select auth.uid()) = owner_id);
```

**設計時規則**：每條 policy 都寫 `to <role>`，不要靠預設。

---

## 5. PostgREST `select=*` 與 N+1

**症狀**：API 回應大、慢；前端只用了幾個欄位。

**原因**：

- `select=*` 把整列拉回來，含 `body text`、`metadata jsonb` 這種肥欄位；多了傳輸與序列化成本。
- 連續呼叫多支端點（先抓 orders、再針對每筆 order 抓 items）造成 N+1；用一次 embed 就好。

**對**：

```http
GET /rest/v1/orders?select=id,total,customer_id,order_items(id,qty,product_id)
```

**設計時規則**：

- 前端寫 query 時**明列需要的欄位**，不要 `*`。
- 一次拿齊：用 `select=*,related(...)` embed，不要做 N+1。
- embed 用到的關聯，FK 一定要有索引（見第 2 條）。

特別注意：**「同一個查詢有時要 embed、有時不要」就分兩支 repo function**。例如訂單列表頁要 embed customer + items，但跑 RFM 分析只要 customer_id / total_amount / created_at 幾個欄位——別用同一個 `ListOrders()` 含 embed，會把 RFM 場景拖慢一個數量級。多寫一支 `ListOrdersLean()` 比共用一支 fat function 划算太多。

---

## 5b. 後端應用層的 N+1（迴圈內呼叫 DB）

**症狀**：建單／批次處理慢，且時間隨 item 數量線性放大。

**原因**：後端程式裡常見的反模式：

```go
for _, it := range items {
    p, _ := db.GetProduct(it.ProductID)   // 每個 item 一支 HTTP！
    total += p.UnitPrice * it.Quantity
}
```

雖然每支 query 本身可能很快（DB 端 1-2ms），但 backend → Supabase 是跨網路 HTTP，**每次 100-500ms**。10 個 item 就 1-5 秒。

**對**：先收集 id，一次用 `id=in.(...)` 批次抓：

```go
ids := collectIDs(items)
products, _ := db.GetProductsByIDs(ids)   // 1 支查詢拿全部
for _, it := range items {
    p := products[it.ProductID]
    total += p.UnitPrice * it.Quantity
}
```

**設計時規則**：寫程式時看到「`for ... { db.Xxx(...) }`」這種 pattern 警鈴就要響起。要嘛改成批次 `in.(...)`、要嘛把運算下推 SQL（用 view／RPC）。

---

## 5c. 迴圈內逐筆寫入 — PostgREST 接受 array body

**症狀**：刷新分群、批次匯入、批次更新動輒幾十秒。

**原因**：

```go
for cid, payload := range computed {
    db.UpsertCustomerSegment(payload)   // N 支 HTTP request！
}
```

100 筆顧客就是 100 趟跨網路 round-trip，加上 100 次 RLS／trigger 評估。

**對**：PostgREST insert / upsert 端點直接吃 JSON array，一支 request 灌全部：

```go
db.UpsertCustomerSegments(allPayloads)   // 1 支
```

實作上就是 `POST /rest/v1/<table>` 的 body 從 object 改成 array，加 `Prefer: resolution=merge-duplicates` 與 `on_conflict=<pk>` 就是 bulk upsert。資料量很大時記得分批（PostgREST 預設 body 上限 1MB），通常每批 500-1000 筆夠用。

**設計時規則**：任何「對一個集合做相同操作」的場景，repo 層都要提供批次版本，handler 寫起來才不會踩進迴圈陷阱。

---

## 6. `count=exact` 在大表上很貴

**症狀**：分頁 API 慢，但只在第一頁慢。

**原因**：PostgREST `Prefer: count=exact` 會跑一次 `SELECT count(*)` 全表，配上 RLS 連 index-only scan 都用不上。

**對**：

- 不需要精確總數時用 `count=estimated`（讀 `pg_class.reltuples`，**O(1)**）或 `count=planned`。
- 前端 UI 改成「下一頁」按鈕而不是「第 N 頁／共 M 頁」。

**設計時規則**：分頁設計優先用 cursor-based（`created_at < $cursor`），少用 offset + count。

---

## 7. `security definer` function 沒固定 `search_path`

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

## 8. 經常被過濾／排序的欄位沒索引

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

## 8b. 後端 HTTP client 預設值不適合服務間通訊

**症狀**：backend 對 Supabase 發請求慢、CPU 沒事卻 throughput 上不去；流量稍微多就掛住整個 service。

**原因**：Go / Node / Python 的 HTTP client 預設值是給「偶爾打單一網址」設計的：

- **Go `http.Client{}`**：用 `DefaultTransport`，`MaxIdleConnsPerHost = 2`、`Timeout = 0`（永不超時）。對 Supabase 這種「同一個 host 高並發」場景，第 3 條並發就要重新 TCP+TLS handshake，跨網路非常貴；單一掛掉的請求會把 goroutine 永久占住。
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

## 8c. 前端 fetch 沒有 timeout — UI 永遠卡在 loading

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

## 8d. 每個 request 都打 `supabase.auth.getSession()` — refresh 鎖把全部呼叫卡住

**症狀**：操作偶爾跳 `getSession timeout`；F5 之後就好；多分頁同時開更容易發生。

**原因**：Supabase JS client 的 `getSession()` 內部有把 lock（避免多個並發呼叫同時 refresh token）。一旦背景的 token refresh 因網路抖動、auth endpoint 慢、其他分頁正在 refresh 而卡住，所有後續 `getSession()` 都會排隊等鎖直到 timeout。每個 API request 都打一次 `getSession()` 就是把這個風險放大 N 倍。

**錯**：

```js
async function authHeader() {
  const { data: { session } } = await supabase.auth.getSession()  // 每次 request 都呼叫
  return { Authorization: 'Bearer ' + session.access_token }
}
```

**對**：在 module scope 快取 session，只有快取過期或缺 token 時才真的呼叫；用 `onAuthStateChange` 同步背景 refresh 結果：

```js
let cachedSession = null
let initPromise = null

supabase.auth.onAuthStateChange((_event, session) => {
  cachedSession = session                       // Supabase 自動 refresh 完會推進來
})

function ensureInit() {
  if (!initPromise) {
    initPromise = withTimeout(supabase.auth.getSession(), 10_000, 'getSession')
      .then(({ data }) => { cachedSession = data?.session || null })
      .catch((err) => { initPromise = null; throw err })
  }
  return initPromise
}

function isTokenFresh(s) {
  return s?.access_token && Date.now() + 60_000 < s.expires_at * 1000  // 60s buffer
}

async function authHeader() {
  if (!isTokenFresh(cachedSession)) {
    await ensureInit()
    if (!isTokenFresh(cachedSession)) {
      const { data } = await withTimeout(
        supabase.auth.refreshSession(), 10_000, 'refreshSession',
      )
      cachedSession = data?.session || null
    }
  }
  if (!cachedSession?.access_token) throw new Error('未登入')
  return { Authorization: 'Bearer ' + cachedSession.access_token }
}
```

關鍵點：
- **快取在 module scope**：所有 request 共用，cache hit 時連 `getSession()` 都不呼叫。
- **`onAuthStateChange` 是同步管道**：Supabase 背景 refresh 完會推 `TOKEN_REFRESHED` 事件，快取自動更新，不用主動拉。
- **expires_at 60s buffer**：避免拿到「還有 5 秒就過期」的 token 去打 request，伺服器收到時已經過期。
- **fallback timeout 拉到 10s**：真的走到 `getSession()` 是 fallback 路徑，給多點時間覆蓋 token refresh。

**設計時規則**：前端對 Supabase 的 session 管理一律走「快取 + onAuthStateChange」模式，**永遠不要**在 request 熱路徑上直接呼叫 `getSession()`。

---

## 9. 後端每個請求都打 `/auth/v1/user` 驗 JWT

**症狀**：admin 介面 / dashboard 切 tab 慢。後端日誌看每支 API 多 100-500ms 但 DB query 很快。

**原因**：常見模式是 middleware 在每個請求都呼叫 Supabase `/auth/v1/user` 來驗使用者身分——這是跨網路 HTTP 往返，比本地驗章慢三個數量級，還會被 Supabase rate limit。

**對**：用 JWKS 本地驗章。新版 Supabase 的 signing keys 公鑰透過 `<SUPABASE_URL>/auth/v1/.well-known/jwks.json` 公開，後端 cache 一次後本地驗 ES256 / RS256；完整做法見 `auth.md` 的「後端驗 JWT」段。

**設計時規則**：後端拿到 JWT 一律本地驗章，**永遠不要**在請求路徑上打 `/auth/v1/user`。

---

## 11. 冷啟動（免費方案 / 閒置 project）

**症狀**：偶爾第一個請求要 5-15 秒，之後就正常。

**原因**：免費 project 閒置一段時間會 pause；第一個請求要喚醒整個 instance。Edge Function 也有冷啟動（~200-500ms）。

**對**：

- 上線用 Pro 方案避免 pause。
- 用 UptimeRobot / cron-job.org 每 5 分鐘 ping `/rest/v1/` 一次保活（dev 環境也很有用）。
- Edge Function 改成 keep-warm 或改回 Postgres function。

---

## 12. 大量寫入後沒 ANALYZE — query plan 用錯統計

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
- [ ] 大量寫入後跑 `analyze <table>`。

### RLS / Policy
- [ ] 每條 policy 都寫 `to <role>`，沒用預設 `public`。
- [ ] policy 裡 `auth.uid()` / `auth.jwt()` / `current_setting()` 都包了 `(select ...)`。
- [ ] 同一 (role, action) 沒有多條 permissive policy。
- [ ] `security definer` function 都有 `set search_path = ''` 與 `stable`/`immutable` 標籤。

### PostgREST 查詢
- [ ] `select=` 明列欄位，不用 `*`（特別是含 jsonb / text 大欄位的表）。
- [ ] 列表頁要 embed 的，FK 都已建索引。
- [ ] 不同用途有不同 repo function（fat 版含 embed，lean 版只抓計算需要欄位）。
- [ ] 分頁預設 cursor + `count=estimated`，不用 `count=exact`。

### 應用層
- [ ] 沒有「`for ... { db.X() }`」這類迴圈內 DB 呼叫——改成 `id=in.(...)` 批次抓。
- [ ] 集合操作（建多筆 / 更新多筆 / upsert 多筆）一律用 array body 一支 request 灌完。
- [ ] 後端對 Supabase 共用一個 long-lived HTTP client，調好 `MaxIdleConnsPerHost`、設 `Timeout`。
- [ ] 前端所有 fetch 都套 `AbortController` timeout。
- [ ] 前端 session 走「module-scope 快取 + `onAuthStateChange` 同步」模式，不在 request 熱路徑直接呼叫 `getSession()`。
- [ ] 後端驗 JWT 用 JWKS 本地驗章，沒在請求路徑上打 `/auth/v1/user`。

### 驗證
- [ ] migration 寫完後跑 `get_advisors(type=performance)`，沒有新的 WARN。
- [ ] 慢的 query 用 `EXPLAIN (ANALYZE, BUFFERS)` 看計畫——seq scan 大表就要補索引。
- [ ] 重要的 list endpoint 在 100x 資料量下試一次，看是否還在可接受範圍。

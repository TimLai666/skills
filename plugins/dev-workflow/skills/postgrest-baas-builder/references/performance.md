# Supabase / PostgREST 效能地雷

Supabase 慢的時候，九成不是平台問題，是 RLS 與查詢寫法沒踩好。這份是 BaaS 專屬的效能地雷；通用的 schema／索引／應用層地雷（FK 索引、迴圈內呼叫 DB、connection pool…）見 `db-engineering` skill 的 `references/performance-pitfalls.md`，兩份都要過。

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

## 2. 同一 (role, action) 多條 permissive policy — 每條都跑

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

## 3. policy 沒指定 `to <role>` — service_role 也被檢查

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

## 4. PostgREST `select=*` 與 N+1

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
- embed 用到的關聯，FK 一定要有索引（索引規則見 `db-engineering` 的 `performance-pitfalls.md`）。

特別注意：**「同一個查詢有時要 embed、有時不要」就分兩支 repo function**。例如訂單列表頁要 embed customer + items，但跑 RFM 分析只要 customer_id / total_amount / created_at 幾個欄位——別用同一個 `ListOrders()` 含 embed，會把 RFM 場景拖慢一個數量級。多寫一支 `ListOrdersLean()` 比共用一支 fat function 划算太多。

---

## 5. 迴圈內逐筆寫入 — PostgREST 接受 array body

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

## 7. 每個 request 都打 `supabase.auth.getSession()` — refresh 鎖把全部呼叫卡住

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

## 8. 後端每個請求都打 `/auth/v1/user` 驗 JWT

**症狀**：admin 介面 / dashboard 切 tab 慢。後端日誌看每支 API 多 100-500ms 但 DB query 很快。

**原因**：常見模式是 middleware 在每個請求都呼叫 Supabase `/auth/v1/user` 來驗使用者身分——這是跨網路 HTTP 往返，比本地驗章慢三個數量級，還會被 Supabase rate limit。

**對**：用 JWKS 本地驗章。新版 Supabase 的 signing keys 公鑰透過 `<SUPABASE_URL>/auth/v1/.well-known/jwks.json` 公開，後端 cache 一次後本地驗 ES256 / RS256；完整做法見 `auth.md` 的「後端驗 JWT」段。

**設計時規則**：後端拿到 JWT 一律本地驗章，**永遠不要**在請求路徑上打 `/auth/v1/user`。

---

## 9. 冷啟動（免費方案 / 閒置 project）

**症狀**：偶爾第一個請求要 5-15 秒，之後就正常。

**原因**：免費 project 閒置一段時間會 pause；第一個請求要喚醒整個 instance。Edge Function 也有冷啟動（~200-500ms）。

**對**：

- 上線用 Pro 方案避免 pause。
- 用 UptimeRobot / cron-job.org 每 5 分鐘 ping `/rest/v1/` 一次保活（dev 環境也很有用）。
- Edge Function 改成 keep-warm 或改回 Postgres function。

---

## 設計時自我檢查

### RLS / Policy
- [ ] 每條 policy 都寫 `to <role>`，沒用預設 `public`。
- [ ] policy 裡 `auth.uid()` / `auth.jwt()` / `current_setting()` 都包了 `(select ...)`。
- [ ] 同一 (role, action) 沒有多條 permissive policy。

### PostgREST 查詢
- [ ] `select=` 明列欄位，不用 `*`（特別是含 jsonb / text 大欄位的表）。
- [ ] 列表頁要 embed 的，FK 都已建索引。
- [ ] 不同用途有不同 repo function（fat 版含 embed，lean 版只抓計算需要欄位）。
- [ ] 分頁預設 cursor + `count=estimated`，不用 `count=exact`。
- [ ] 集合操作（建多筆 / 更新多筆 / upsert 多筆）一律用 array body 一支 request 灌完。

### Auth / Session
- [ ] 前端 session 走「module-scope 快取 + `onAuthStateChange` 同步」模式，不在 request 熱路徑直接呼叫 `getSession()`。
- [ ] 後端驗 JWT 用 JWKS 本地驗章，沒在請求路徑上打 `/auth/v1/user`。

### 驗證
- [ ] migration 寫完後跑 `get_advisors(type=performance)`，沒有新的 WARN。

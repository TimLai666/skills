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

## 9. 冷啟動（免費方案 / 閒置 project）

**症狀**：偶爾第一個請求要 5-15 秒，之後就正常。

**原因**：免費 project 閒置一段時間會 pause；第一個請求要喚醒整個 instance。Edge Function 也有冷啟動（~200-500ms）。

**對**：

- 上線用 Pro 方案避免 pause。
- 用 UptimeRobot / cron-job.org 每 5 分鐘 ping `/rest/v1/` 一次保活（dev 環境也很有用）。
- Edge Function 改成 keep-warm 或改回 Postgres function。

---

## 10. 大量寫入後沒 ANALYZE — query plan 用錯統計

**症狀**：批次匯入幾萬列後，查詢突然變慢。

**原因**：Postgres planner 靠 `pg_statistic` 估列數。剛大量寫入時統計還沒更新，planner 可能誤判走 seq scan。

**對**：批次寫入結束後手動 `analyze`：

```sql
analyze public.orders;
```

migration 內若有 `insert ... select ...` 灌大量資料，後面接一條 `analyze`。

---

## 設計時自我檢查（每張新表都過一次）

- [ ] 每個 FK 欄位都有索引（或被其他索引的最左前綴覆蓋）。
- [ ] 每條 RLS policy 都寫 `to <role>`，沒用預設 `public`。
- [ ] policy 裡 `auth.uid()` / `auth.jwt()` / `current_setting()` 都包了 `(select ...)`。
- [ ] 同一 (role, action) 沒有多條 permissive policy。
- [ ] `security definer` function 都有 `set search_path = ''` 與 `stable`/`immutable` 標籤。
- [ ] 最常見的 filter／order 欄位有索引；軟刪表用部分索引 `where deleted_at is null`。
- [ ] 分頁 API 預設用 cursor + `count=estimated`，不用 `count=exact`。
- [ ] migration 寫完後跑 `get_advisors(type=performance)`，沒有新的 WARN。

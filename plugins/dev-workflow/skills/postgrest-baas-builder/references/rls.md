# Row Level Security (RLS)

RLS 是這類專案的資安底線，不是選項。Supabase 的 anon / authenticated 角色會直接從前端帶 key 連到資料庫；**沒開 RLS 的表 = 任何人都能讀寫的表**。

## 鐵則

- `public` schema 下**每一張表**，在建立它的 migration 裡就 `enable row level security`。
- 啟用 RLS 後，沒有 policy = 預設全部拒絕（對 anon／authenticated）。所以啟用後要補上明確 policy 來「開放」需要的存取。
- 連那些「只有後端會碰」的表也要 `enable row level security`：service_role 本來就繞過 RLS，但啟用它能確保萬一前端拿到表名也讀不到——這是縱深防禦。
- policy 按操作分開寫（select／insert／update／delete），語意清楚也好稽核。
- **效能鐵則**（細節見 `performance-pitfalls.md`）：
  - 每條 policy 都寫 `to <role>`，不要靠預設 `public`（會連 service_role 都檢查）。
  - policy 內出現 `auth.uid()` / `auth.jwt()` / `current_setting(...)` 一律包成 `(select ...)`，否則 Postgres 會 per-row 重算，列數一多就爆。
  - 同一 (role, action) 不要疊多條 permissive policy；合併條件或改用 restrictive。

## 啟用 RLS

```sql
alter table public.<table> enable row level security;
```

## 常見 policy 樣板

### 1. 擁有者制（最常見）

每筆資料有 `owner_id`／`user_id` 指向 `auth.users`，使用者只能存取自己的資料：

```sql
create policy "select_own"
  on public.notes for select
  to authenticated
  using ((select auth.uid()) = owner_id and deleted_at is null);

create policy "insert_own"
  on public.notes for insert
  to authenticated
  with check ((select auth.uid()) = owner_id);

create policy "update_own"
  on public.notes for update
  to authenticated
  using ((select auth.uid()) = owner_id and deleted_at is null)
  with check ((select auth.uid()) = owner_id);
```

`using` 控制「能看到／能動哪些既有列」，`with check` 控制「寫入後的列是否合法」。insert 用 `with check`，update 兩者都要。

注意三個寫法細節（少一個都會踩坑，見 `performance-pitfalls.md`）：

- `to authenticated`：明確指定目標 role，避免預設 `public` 連 service_role 都檢查。
- `(select auth.uid())`：把 auth function 包成子查詢，Postgres 才會當 initplan 算一次而不是 per-row。
- `auth.uid() = owner_id`：`owner_id` 是 FK，記得在表上另外 `create index ... (owner_id)`。

### 2. 公開讀、限定寫

例如商品、文章列表所有人可讀，只有擁有者能改：

```sql
create policy "public_read"
  on public.products for select
  to anon, authenticated
  using (deleted_at is null);

create policy "owner_write"
  on public.products for update
  to authenticated
  using ((select auth.uid()) = owner_id)
  with check ((select auth.uid()) = owner_id);
```

### 3. 軟刪感知

policy 的 `using` 條件加上 `deleted_at is null`，被軟刪的列對一般使用者自動「消失」。需要看已刪資料的後台，走 service_role 或另寫 admin policy。

### 4. 結構性禁止硬刪

要強制軟刪，**就不要給 authenticated 角色 delete policy**。沒有 delete policy，前端發出的 `DELETE` 一律被擋；刪除只能透過「`UPDATE` 設 `deleted_at`」完成。這是用 RLS 把「優先軟刪」這條規則變成結構上做不到硬刪。

### 5. 角色／成員制

多人協作的資源（團隊、專案）用一張成員表判斷。把判斷包成 `security definer` function 避免 policy 互相遞迴：

```sql
create function public.is_team_member(p_team_id uuid)
returns boolean
language sql
security definer
set search_path = ''
stable
as $$
  select exists (
    select 1 from public.team_members
    where team_id = p_team_id and user_id = (select auth.uid())
  );
$$;

create policy "members_can_read"
  on public.team_documents for select
  to authenticated
  using (public.is_team_member(team_id) and deleted_at is null);
```

`security definer` + `set search_path = ''` + `stable` 三個標籤一個都不能少：`search_path` 是資安要求（不固定的話呼叫端可塞 schema 提權），`stable` 讓 RLS 引擎能把結果快取到 query 結束，否則每列重算就退化成 N+1。

## service_role 與 anon 的分工

- **anon key**：給前端／client 用，RLS 全程生效。
- **service_role key**：繞過 RLS，只在受信任的伺服器端使用（後台、排程、Edge Function）。絕不可外洩到瀏覽器。
- 後台需要跨使用者讀寫時，用 service_role；但能用一般使用者身分 + policy 完成的事，就不要動用 service_role。

## 檢查清單

- [ ] 每張新表的 migration 內都有 `enable row level security`。
- [ ] 每張表都有對應其用途的 policy（不是只 enable 卻沒 policy，也不是 enable 了卻忘記補）。
- [ ] policy 按 select／insert／update／delete 分開。
- [ ] 每條 policy 都寫 `to <role>`，沒用預設 `public`。
- [ ] policy 內 `auth.uid()` / `auth.jwt()` / `current_setting(...)` 都包成 `(select ...)`。
- [ ] 同一 (role, action) 沒有疊多條 permissive policy（advisor 跑一下 `multiple_permissive_policies`）。
- [ ] 要軟刪的表，policy 的 `using` 含 `deleted_at is null`，且**不給** authenticated 角色 delete policy。
- [ ] service_role key 沒有出現在前端程式碼。

# Row Level Security (RLS)

RLS 是這類專案的資安底線，不是選項。Supabase 的 anon / authenticated 角色會直接從前端帶 key 連到資料庫；**沒開 RLS 的表 = 任何人都能讀寫的表**。

## 鐵則

- `public` schema 下**每一張表**，在建立它的 migration 裡就 `enable row level security`。
- 啟用 RLS 後，沒有 policy = 預設全部拒絕（對 anon／authenticated）。所以啟用後要補上明確 policy 來「開放」需要的存取。
- 連那些「只有後端會碰」的表也要 `enable row level security`：service_role 本來就繞過 RLS，但啟用它能確保萬一前端拿到表名也讀不到——這是縱深防禦。
- policy 按操作分開寫（select／insert／update／delete），語意清楚也好稽核。

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
  using (auth.uid() = owner_id and deleted_at is null);

create policy "insert_own"
  on public.notes for insert
  with check (auth.uid() = owner_id);

create policy "update_own"
  on public.notes for update
  using (auth.uid() = owner_id and deleted_at is null)
  with check (auth.uid() = owner_id);
```

`using` 控制「能看到／能動哪些既有列」，`with check` 控制「寫入後的列是否合法」。insert 用 `with check`，update 兩者都要。

### 2. 公開讀、限定寫

例如商品、文章列表所有人可讀，只有擁有者能改：

```sql
create policy "public_read"
  on public.products for select
  using (deleted_at is null);

create policy "owner_write"
  on public.products for update
  using (auth.uid() = owner_id)
  with check (auth.uid() = owner_id);
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
    where team_id = p_team_id and user_id = auth.uid()
  );
$$;

create policy "members_can_read"
  on public.team_documents for select
  using (public.is_team_member(team_id) and deleted_at is null);
```

## service_role 與 anon 的分工

- **anon key**：給前端／client 用，RLS 全程生效。
- **service_role key**：繞過 RLS，只在受信任的伺服器端使用（後台、排程、Edge Function）。絕不可外洩到瀏覽器。
- 後台需要跨使用者讀寫時，用 service_role；但能用一般使用者身分 + policy 完成的事，就不要動用 service_role。

## 檢查清單

- [ ] 每張新表的 migration 內都有 `enable row level security`。
- [ ] 每張表都有對應其用途的 policy（不是只 enable 卻沒 policy，也不是 enable 了卻忘記補）。
- [ ] policy 按 select／insert／update／delete 分開。
- [ ] 要軟刪的表，policy 的 `using` 含 `deleted_at is null`，且**不給** authenticated 角色 delete policy。
- [ ] service_role key 沒有出現在前端程式碼。

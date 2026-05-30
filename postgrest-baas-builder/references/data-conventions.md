# 資料慣例：欄位、updated_at、軟刪除

用生態系標準的欄位名與機制，讓 `moddatetime`、Supabase Dashboard 等工具能直接認得，也讓任何接手的人一眼就懂。不要自創欄位名。

## 標準欄位

每張業務資料表都帶這組欄位：

| 欄位 | 型別 | 說明 |
|---|---|---|
| `id` | `uuid` 或 `bigint` | 主鍵，由 Postgres 產生 |
| `created_at` | `timestamptz not null default now()` | 建立時間 |
| `updated_at` | `timestamptz not null default now()` | 更新時間，由 trigger 維護 |
| `deleted_at` | `timestamptz`（可 null） | 軟刪除標記，null = 未刪除 |

時間欄位一律 `timestamptz`（含時區），不要用 `timestamp`。

### 主鍵

由資料庫產生，不要由應用程式產：

```sql
-- 方式一：UUID
id uuid primary key default gen_random_uuid()

-- 方式二：自增整數
id bigint generated always as identity primary key
```

`gen_random_uuid()` 是 Postgres 內建函式。對外公開的資源用 UUID 較好（不會洩漏數量、不可猜測）。

### 禁止的命名

不要用 `update_time`、`modify_date`、`is_deleted`、`del_flag`、`removed`、`createTime` 這類自創或非標準名稱。一律用 `created_at` / `updated_at` / `deleted_at`。`moddatetime` 擴充與多數 Supabase 範例都預設這組名稱——照慣例走，工具才接得上。

## updated_at 自動維護

不要靠應用程式記得更新 `updated_at`——用 `moddatetime` 擴充 + trigger，讓資料庫自己維護。

啟用擴充（建議放進 schema `extensions`）：

```sql
create extension if not exists moddatetime schema extensions;
```

每張帶 `updated_at` 的表掛一個 trigger：

```sql
create trigger set_updated_at
  before update on public.<table>
  for each row
  execute function extensions.moddatetime(updated_at);
```

之後任何 `UPDATE` 都會自動把 `updated_at` 設成當下時間。

## 軟刪除

刪除預設用軟刪：把 `deleted_at` 設成現在時間，而不是真的把列移除。

### 軟刪一筆資料

```sql
update public.notes
set deleted_at = now()
where id = $1;
```

### 查詢時排除已刪資料

所有「正常」查詢都要過濾掉軟刪的列：

```sql
select * from public.notes where deleted_at is null;
```

兩種方式讓「排除已刪」更不容易漏：

1. **RLS policy** 的 `using` 條件加 `deleted_at is null`（見 `rls.md`）——一般使用者根本看不到已刪列。
2. 建一個 view 只露出未刪資料，應用層查 view：

```sql
create view public.active_notes as
  select * from public.notes where deleted_at is null;
```

### 部分索引

針對未刪資料建部分索引，效能較好：

```sql
create index notes_owner_active_idx
  on public.notes (owner_id)
  where deleted_at is null;
```

### 結構性禁止硬刪

要真正落實「優先軟刪」，在 RLS 層**不給 authenticated 角色 delete policy**——這樣前端就算想硬刪也被擋下，只能透過 `UPDATE deleted_at` 軟刪。詳見 `rls.md`。

## 什麼時候才硬刪

軟刪是預設，但下列情況可以、甚至應該硬刪：

- 法遵要求的個資抹除（如使用者依個資法／GDPR 要求刪除）——這時要真的刪掉。
- 明確的測試垃圾資料、誤建資料。
- 軟刪後超過保留期、由清理排程批次硬刪的舊資料（見 `logging-retention.md`）。

硬刪正式環境資料前，務必先取得使用者同意（見 `production-safety.md`）。

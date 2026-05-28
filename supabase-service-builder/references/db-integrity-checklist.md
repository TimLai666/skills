# 資料完整性、稽核與過時設計

效能問題會讓人罵，**資料丟失與不可追蹤的操作會讓人吃官司**。這份是「不是效能、但更嚴重」的審查面向。

**任何時候改了與資料庫相關的程式碼或 schema，這份清單也要過一次**，連同 `performance-pitfalls.md` 一起。兩份是並列的，缺一不可。

---

## A. CASCADE 風險審查

每個 FK 的 `ON DELETE` / `ON UPDATE` 都是個沉默的炸彈。預設不寫的話是 `NO ACTION`，但「順手寫個 cascade」很常見、後果很重。

### 判斷流程

問三個問題：

1. **parent 在這個專案會不會硬刪？** 程式碼裡有 `delete from <parent>` 或 `DELETE` policy 嗎？沒有的話 cascade 永遠不會觸發（程式面）。
2. **parent 有沒有可能從 Dashboard / psql 被手動刪？** 永遠假設「會」。維運、debug、清測試資料時都可能發生。
3. **若 cascade 真的觸發了，child 的資料價值多高？** 是 derived data（可重算）→ CASCADE 合理；是業務歷史（如成交明細、稽核 log）→ 不可丟。

### 對照表

| Child 資料性質 | 建議 ON DELETE |
|---|---|
| Derived data（可重算）— 例：customer_segments、stats、cache | CASCADE |
| 業務歷史（不可丟）— 例：order_items 對 orders、audit_log | RESTRICT |
| Owner 關聯（人沒了東西也沒意義）— 例：個人筆記對 user | CASCADE（小心：軟刪設計時要改 RESTRICT） |
| Optional 關聯（人是誰 nice-to-have）— 例：log 記 actor_id | SET NULL |

### 與軟刪設計的衝突

採「優先軟刪」的專案，**parent 表幾乎永遠不會被硬刪**——所以 cascade 在程式面不會觸發。但 Dashboard 手動刪、cron 清過期軟刪、未來 GDPR 個資抹除流程都會繞過軟刪直接硬刪。這時 cascade 就會吃掉 children。

**建議**：軟刪表的 children FK 預設用 `RESTRICT`，強制硬刪 parent 前要刻意先處理 children。這跟軟刪精神一致——「想丟資料？請刻意。」

```sql
-- 改現有 FK 的範例：把 CASCADE 改 RESTRICT
alter table public.order_items
  drop constraint order_items_order_id_fkey;
alter table public.order_items
  add constraint order_items_order_id_fkey
  foreign key (order_id) references public.orders(id) on delete restrict;
```

### auth.users 的特殊狀況

很多教學樣板把 `profiles.id references auth.users(id) on delete cascade` 當預設。**但這意味著從 Supabase Dashboard 隨手刪 auth.users，整個 profile 軟刪歷史（角色、停權紀錄、display_name 等）會永久消失**。如果 admin 帳號的歷史是稽核要件，這個 cascade 就是大坑。

建議：profiles → auth.users 也用 `RESTRICT`。要刪使用者請先軟刪 profile（或硬刪 profile），再刪 auth.users，兩步分開。

### 設計時規則

- 寫 FK 一定明確標 `on delete ...`，**不要省略**讓它預設 NO ACTION（NO ACTION 跟 RESTRICT 行為很像但細節不同，新人讀會混淆）。
- 軟刪表的所有 children 預設 `RESTRICT`，除非該 child 是 derived data。
- 任何 `CASCADE` 都要在 migration 加註解說明「為什麼這條可以連帶刪」。

---

## B. 稽核覆蓋審查（不可追蹤的操作 = 沒發生過）

`audit_log` 表存在但**只有掛了 trigger 的表才會被記**。常見漏洞：建了新表卻忘記掛 `record_audit()` trigger，於是那張表的所有變更都成黑洞。

### 檢查 SQL

```sql
-- 列出所有 public 表，標記哪些有 audit trigger
select t.table_name,
  bool_or(tg.trigger_name like 'audit_%') as has_audit_trigger
from information_schema.tables t
left join information_schema.triggers tg
  on tg.event_object_table = t.table_name
  and tg.trigger_schema = t.table_schema
where t.table_schema='public'
  and t.table_type='BASE TABLE'
  and t.table_name not in ('audit_log')   -- 自己不記自己
group by t.table_name
order by has_audit_trigger, t.table_name;
```

任何 `has_audit_trigger=false` 的表都要補：

```sql
create trigger audit_<table_name>
  after insert or update or delete on public.<table_name>
  for each row execute function public.record_audit();
```

### 不止 DB 層：應用層也要追

有些「重要操作」不是 DB 寫入：

| 操作 | 對應紀錄 |
|---|---|
| 推播訊息（呼叫 LINE API）| 寫進 `push_log` 表 |
| 發 email / SMS | 同樣要有專屬 log 表，或寫進 `audit_log.metadata` |
| 呼叫外部 API（金流、查驗）| 同上 |
| 登入 / 登出 / 改密碼 | Supabase 自己記在 `auth.audit_log_entries`（不必重做，但要知道在哪查） |
| 軟刪 admin 帳號 | profiles 表 update → 經 audit trigger 自動記 |
| 改 admin 的 email / password | 動的是 `auth.users`，Supabase 內建 audit 會記 |

### 設計時規則

- **新建一張 `public` 表的 migration 必須同時掛 audit trigger**（除了 audit_log 自己、與真正高頻 / 不在意追蹤的 log 類表）。
- 應用層「呼叫外部服務」就要有對應紀錄表或寫進 `audit_log.metadata`，不能只在記憶體裡跑完就忘。
- 定期跑上面的檢查 SQL，看有沒有新表沒被涵蓋到。

---

## C. 過時／沒在用的設計

長期累積會出現「沒人記得幹嘛用的」schema 物件：dead columns、dead indexes、dead functions、過時 policy。它們本身不直接造成 bug，但帶來：

- **認知負擔**：讀 schema 的人要花時間搞清楚這個欄位有沒有人寫。
- **誤用風險**：新人看到欄位以為可以用，結果寫了 null，因為其實沒有寫入路徑。
- **重構障礙**：要動相關表時不確定能不能刪。

### 找 orphan 欄位

```sql
-- 列出所有 public 表的欄位（人工對照 app code）
select table_name, column_name, data_type
from information_schema.columns
where table_schema='public'
order by table_name, ordinal_position;
```

然後用 `grep` 對照後端 + 前端的程式碼。沒有任何寫入或顯示路徑的欄位就是 orphan candidate。

### 找 orphan 索引

advisor 的 `unused_index` 會列出來，**但 dev 流量小時 false positive 很多**。判斷流程：

- prod 跑超過一個月、且該索引在所有 query pattern 中都沒被用 → 真 orphan，可刪。
- dev 環境的 unused_index 一律先放著，等 prod 數據說話。
- 自訂索引刪除前用 `pg_stat_user_indexes.idx_scan` 確認次數。

### 找 orphan function / trigger / policy

```sql
-- 所有 public function
select p.proname, pg_get_function_identity_arguments(p.oid) as args
from pg_proc p
join pg_namespace n on n.oid=p.pronamespace
where n.nspname='public';

-- 所有 public trigger
select event_object_table, trigger_name, event_manipulation
from information_schema.triggers
where trigger_schema='public';

-- 所有 RLS policy
select schemaname, tablename, policyname, cmd, roles
from pg_policies where schemaname='public';
```

人工對照「程式碼有沒有呼叫」「trigger 對應的表還在嗎」「policy 條件還合理嗎」。

### 處理原則

- **找到不代表要立刻刪**——尤其 NULL 欄位幾乎不占空間，刪掉再加回成本反而高。
- 真的要刪的話：先在 migration 加 `comment on column ... is 'DEPRECATED: removed in next release'` 標記一個版本，下一輪再實際 drop，避免別的服務還在依賴。
- 維護一份「已知 orphan 候選名單」（在 README 或 ARCHITECTURE.md），定期 review。

---

## D. Snapshot vs Reference（業務歷史的兩種保存方式）

設計子表（訂單、合約、出貨單…）時，最常見的誤判是「父表欄位之後變了，子表要不要凍住當下的值」。例如 `orders.customer_id` 是 FK 到 `customers`，**那客人之後改名／改電話，去看歷史訂單該顯示哪個？**

新手會想：「不是有 `audit_log` 嗎？任何變更都被 `to_jsonb` 凍進去了，從那邊還原就好。」對一半。

### audit_log 能做的、不能做的

`audit_log` 用 trigger + `to_jsonb(old/new)` 自動凍住變更，**追「誰改了什麼、什麼時候改的」完全勝任**。但它有兩個硬限制：

1. **有保留期**：通常 90 天 cron 清掉。業務子表（訂單、合約、發票）的壽命遠超過——對帳、稅務、客訴常常 1-7 年都還在翻。超過保留期，audit_log 早就沒了。
2. **讀取成本高**：要從 audit_log 拼出「訂單 X 建立當下客人 Y 的電話」要跑時間範圍 + jsonb path 查詢。每張訂單顯示都跑一次 → 列表頁直接爆。audit_log 是**事後調查**用，不是**頁面顯示**用。

### 判斷規則

對子表的每個關聯欄位問兩個問題：

1. **這個值的「下單／簽約／出貨當下」狀態，業務需要存超過 audit 保留期嗎？**（對帳、客訴、稅務時還會翻嗎？）
2. **頁面顯示要每次都查嗎？**（訂單列表、發票、出貨單）

兩個都「是」 → **snapshot 到子表欄位**
兩個都「否」 → audit_log 就夠

### 對照表

| 場景 | 處理 | 為什麼 |
|---|---|---|
| `order_items.product_name` / `unit_price` | ✅ snapshot 在子表 | 對帳 1-3 年都看；產品改價／改名不能影響歷史訂單金額 |
| `orders.contact_name` / `contact_phone` | ✅ snapshot 在子表 | 訂單還在處理時客人改電話，畫面要顯示當時留的才能聯絡；訂單壽命 > 90 天 |
| `orders.pickup_address` | ✅ snapshot 在子表 | 出貨憑證、退貨追溯 |
| `customers.display_name` 改名歷史 | audit_log | 同一個人，不影響業務追溯；要查只是稽核 |
| `profiles.role` 變更歷史 | audit_log | 管理員權限稽核，90 天足夠 |
| `products.unit_price` 漲跌歷史 | audit_log + order_items.unit_price 雙保險 | 訂單金額凍在 order_items；產品本身的價格變化由 audit_log 追 |
| 顧客 `notes`、`address` 等隨時改的個資 | audit_log + 子表 snapshot（出貨時凍 address）| 個資追溯走 audit；業務憑證走 snapshot |

### 設計時規則

- 建立子表時，**所有「業務當下要凍住」的父表欄位都複製成子表欄位**：產品名、價格、地址、聯絡方式、適用稅率…
- **不要靠 join 顯示業務歷史值**，那會被父表後續變更污染。
- audit_log 是稽核用，**不要拿來當「業務歷史 snapshot 的唯一來源」**——保留期、查詢成本兩個坑。
- 用 `comment on column` 標清楚哪些欄位是 snapshot：
  ```sql
  comment on column public.orders.contact_phone
    is '下單當下的聯絡電話快照；之後 customers.phone 變了也不影響歷史訂單';
  ```

### 應用層搭配

- 顯示時**優先讀 snapshot 欄位**，fallback 才走父表 join。
- 提供 drift 提示：snapshot 與父表現值不同時，UI 提醒商家「這是當時留的，不是現在」。
- snapshot 欄位**也要可手動編輯**：例如 LIFF 客人留錯電話，admin 在訂單編輯介面要能改快照（改父表沒用，舊訂單還是顯示錯的）。

---

## E. 每次改 DB 相關內容的 SOP

不管是寫 migration、改 repo function、改 handler 內的 DB 呼叫、加 trigger……都過一次：

### 效能（見 `performance-pitfalls.md`）

- [ ] FK 有索引；常用 filter / order 欄位有索引（軟刪表用 partial）。
- [ ] RLS policy 用 `(select auth.uid())`、寫 `to <role>`、同 (role, action) 不疊。
- [ ] PostgREST `select=` 明列欄位、不同用途有不同 repo function。
- [ ] 沒有 `for ... { db.X() }` 迴圈；批次寫入用 array body。
- [ ] HTTP client 有 timeout、connection pool 調好。
- [ ] `get_advisors(type=performance)` 沒新 WARN。

### 完整性（本檔）

- [ ] 新／改的 FK 明確標 `on delete`，CASCADE 過 A 段三個問題、加註解。
- [ ] 新表掛了 `audit_<table>` trigger。
- [ ] 涉及外部服務的操作有對應 log 表或寫進 `audit_log.metadata`。
- [ ] schema 變更不留 orphan：刪欄位前確認 app code 沒在用；新欄位有寫入路徑。
- [ ] **業務子表（訂單／合約／出貨…）對父表的關聯欄位過 D 段判斷**：壽命超過 audit 保留期 + 要熱路徑顯示 → snapshot 成子表欄位；不靠 audit_log 還原。
- [ ] snapshot 欄位有 `comment on column` 標註目的；應用層讀取時優先讀 snapshot、有 drift 偵測。
- [ ] `get_advisors(type=security)` 沒新 WARN。

兩份清單缺一不可。效能問題會慢，完整性問題會丟資料——後者修不回來。

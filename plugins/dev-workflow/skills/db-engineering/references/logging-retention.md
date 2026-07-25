# 稽核 Log 與保留策略

系統的重要操作都要留 log，而且 log 要有自動清理機制——log 只增不減會無限膨脹、拖慢資料庫又增加成本。所以「稽核表 + 保留策略」是一組的，不能只做前半。

## 稽核表與通用 trigger

表結構、`lookup_user_email()`、`record_audit()` trigger、pg_cron 保留排程全部在 `assets/starter-migrations/0003_audit_log.sql`，直接使用，不在此重複。三個不可省的設計：

- `created_at` 一定要有索引——保留策略的清理查詢靠它。
- `actor_id` 用 `on delete set null`，使用者被刪時 log 仍保留；**顯示靠 `actor_email` snapshot，不靠 join 父表**（鐵則 10，詳見 `db-integrity-checklist.md` B2）。
- `lookup_user_email()` 必須 revoke 公開 execute，否則 PostgREST 會把它暴露成「UUID 換 email」的列舉端點。

## 寫 log 的兩種方式

### A. 資料庫 trigger（最可靠）

通用 trigger function 掛在要稽核的表上（掛法見 asset 內註解）。好處是應用層繞不過去——只要資料庫被改，log 就一定有。

### B. 應用層寫入

trigger 看不到的事件（純前端行為、外部 webhook、登入流程的業務面）由應用程式在伺服器端用 service_role 寫一筆 `audit_log`。

實務上兩者並用：資料異動靠 trigger 保底，業務事件靠應用層補充。

## 保留策略：用 pg_cron 自動清理

`pg_cron` 在 Supabase 可用；若 migration 內 `create extension` 失敗，到 Dashboard → Database → Extensions 開啟。

排程本體在 asset：預設 90 天起手，業務表（orders / customers…）加入後改用 asset 註解內的分流版——**業務憑證類照法規至少 5 年**（法規最低值對照表見 `logging-architecture.md`），派生資料 90 天即可。migration 可重複套用的關鍵是先 `cron.unschedule` 同名工作再 `cron.schedule`，asset 已內建。

確認排程狀態：

```sql
select jobname, schedule, active from cron.job;
select * from cron.job_run_details order by start_time desc limit 10;
```

## 軟刪資料的清理

被軟刪（`deleted_at` 不為 null）的業務資料若也想定期真正清掉，同樣可用 `pg_cron`，但這屬於會真的刪資料的動作——清理週期應拉長（例如軟刪 180 天後才硬刪），且**正式環境的這類排程要先和使用者確認**。詳見 `production-safety.md`。

## 檢查清單

- [ ] `audit_log` 表存在，已 `enable row level security` 且預設拒絕一般角色。
- [ ] 重要的資料表掛了稽核 trigger，或應用層有寫 log。
- [ ] `pg_cron` 已啟用，且有清理過期 log 的排程。
- [ ] 保留天數明確、可調，業務憑證類符合法規最低值。

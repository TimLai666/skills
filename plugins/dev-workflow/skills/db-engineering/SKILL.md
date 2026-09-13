---
name: db-engineering
description: "Universal database engineering rules covering migration discipline, audit logging, soft delete, performance, and data integrity. This skill MUST be loaded before any database work, and MUST NOT be skipped because a schema change looks small or obvious. Triggers on: 任何資料庫相關工作, 建表, 改 schema, 寫 migration, DB design, database development, 設計資料庫, 改 DB 結構, 加欄位, 加索引, 改 table, SQL, 寫 trigger, 設計 API 的 DB 層, 查詢很慢, N+1, 效能優化, 資料完整性, CASCADE, 外鍵, 新增 table, 刪除資料, backup, 環境分離, dev prod 分開"
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Grep
  - AskUserQuestion
metadata:
  version: "1.3.0"
---

# DB Engineering

## Overview

維護資料庫結構、效能與資料完整性。依本次工作讀取相關參考文件，遵守既有設計政策，不因小改動省略受影響的安全檢查。

## Input Contract

先確認資料庫引擎、目前環境、既有結構與 migration 工具，以及本次改動範圍。預設 development，正式環境操作須有使用者明確同意。

## Workflow

| 工作 | 必讀內容與執行重點 |
| --- | --- |
| 初始化、設計或調整 schema | 讀 [設計政策](references/design-policies.md)。涉及表拆分、欄位歸屬或關係調整時，先畫 ER model，再決定拆分與正規化。 |
| 初始化環境 | 讀 [環境分離](references/environments.md)，設定 dev/prod、環境變數與 migration 工具，建立 extensions 與稽核資料表，驗證本機可完整套用 migration。 |
| 結構變更 | 讀 [migration 紀律](references/migrations.md)。migration 檔必須納入版本控制，已提交或套用的 migration 保持不可變。 |
| 建立或修改資料表 | 讀 [資料慣例](references/data-conventions.md)，落實標準欄位、updated_at trigger 與軟刪除。 |
| 修改 DB 相關程式或 schema | 讀 [完整性檢查](references/db-integrity-checklist.md) 與 [效能檢查](references/performance-pitfalls.md)，核對本次影響的讀寫路徑、外鍵、稽核與查詢。 |
| 查詢效能調查 | 讀 [效能檢查](references/performance-pitfalls.md)，依實際查詢與量測結果定位問題。 |
| 規劃或調整稽核 | 讀 [log 架構](references/logging-architecture.md) 與 [保留與清理](references/logging-retention.md)，核對紀錄內容、保留期及歷史值。 |
| 正式環境操作 | 讀 [正式環境安全](references/production-safety.md)，確認影響、授權、開發環境驗證及備份，執行前檢查待套用內容，完成後驗證狀態並恢復預設開發連線。 |

政策中的雙實例隔離、預設開發環境、軟刪除、雙層稽核、索引、外鍵刪除行為、標準欄位、歷史值快照及 BCNF／3NF 限制維持。具體要求以相應參考文件為準。

## Output Contract

提供實際改動的 migration、相關程式或設定，以及驗證結果。說明資料影響、尚未完成的部分與下一步。單純查詢或調查只交付結果與依據。

## Quality Rules

- 結構變更須能由版本控制中的 migration 重現，並在開發環境驗證。
- 按本次任務核對已讀文件的要求，回報實際證據，不重複抄寫整份政策清單。
- 正式環境禁止 reset 與臨時 DELETE／UPDATE／DROP。正式環境護欄及既有授權要求依安全參考文件執行。

## Assets

- [0003_audit_log.sql](assets/starter-migrations/0003_audit_log.sql)：DB 層稽核 trigger。
- [0004_request_log.sql](assets/starter-migrations/0004_request_log.sql)：應用請求紀錄表。

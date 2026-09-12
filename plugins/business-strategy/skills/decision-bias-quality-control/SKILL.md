---
name: decision-bias-quality-control
description: >-
  This skill MUST be used when evaluating high-stakes decisions with
  bias-aware quality control, including proposal review, decision meeting
  facilitation, personal coaching, and autonomous agent review. MUST trigger
  on requests such as 重大決策、偏誤檢查、提案審查、決策會議引導、決策教練、
  go/no-go 決策、AI 自行審查決策。
metadata:
  version: "1.3.0"
---

# Decision Bias Quality Control

## Overview

用十二問檢查決策形成過程，找出影響判斷的偏誤、證據缺口與修正方式。
完整審查預設提供質性分析與量化評分；只有使用者明確要求腳本、局部追問或其他部分成果時，才縮小交付。

## Input Contract

從目前任務取得決策題目、背景、候選方案與限制，承接已提供的提案或討論紀錄。
模式可由使用者指定，否則依語意選擇。決策大小的三因子依 [評分規則](references/04-scoring-thresholds.md) 判定。

## Data Sufficiency Gate

先查核可自行取得的資料，再說明仍缺什麼、影響哪個結論及需要補充的內容。
可獨立處理的部分繼續。缺少決策大小因子時，依可能範圍比較門檻。
題目證據不足時保留待驗證狀態，依評分規則呈現暫定分數或範圍。

## Workflow

### 1. 選擇模式

使用者明確指定優先，混合需求依主要目的選擇：

| 模式 | 使用情境 |
| --- | --- |
| self-agent | AI 自行查核、討論或審查目前決策；ultrathink 自動轉接的預設 |
| proposal-review | 審查提案、核准條件或 go/no-go 建議 |
| meeting-facilitation | 主持決策會議、安排提問與討論收斂 |
| personal-coaching | 個人重大抉擇、選項比較與驗證行動 |

讀 [模式流程](references/03-mode-workflows.md) 的對應段落執行。

### 2. 執行十二問

讀 [十二問題庫](references/02-12-question-bank.md)，保留各題的核心語意與分組。
查核提案如何形成、替代方案及反證如何處理。
需要確認方法來源、角色分離或適用邊界時，讀 [核心原則](references/01-source-principles.md)。

完整審查逐題記錄判斷、證據與缺口；只準備腳本時覆蓋十二問的提問與證據需求。
依已有證據判定可評分的內容。

### 3. 評分與形成建議

完整審查依 [評分與門檻](references/04-scoring-thresholds.md) 計算，保留可重算的分組原始分數、總分與門檻。
以證據決定風險、修正及驗證行動的數量與優先次序。期限依決策窗口與取得資料所需時間安排。

### 4. 交付與驗收

依 [輸出模板](references/05-output-templates.md) 整理結果，確認十二問覆蓋、計算可重現、結論與證據一致。
重大缺口尚未解決時，限制可下的結論並提供補證據行動。

## Output Contract

完整審查包含決策建議、偏誤診斷、主要風險與修正，以及十二題評分、分組計算、總分與風險門檻。
缺資料時附暫定判斷或範圍及成立條件。
self-agent 另呈現方案修正，會議引導呈現提問與收斂安排，個人教練呈現選項比較與驗證行動。
只要求部分成果時按指定範圍交付，使用自然標題。

## Quality Rules

- 完整審查涵蓋十二問，完成度依實際查核範圍說明。
- 分數衡量查核完整性，風險判斷另附具體依據。
- 結論有可核對依據，區分事實、假設與未知。
- 不把單一觀點、模擬討論或 agent 相互同意當成人類團隊共識。
- 修正後複核受影響題目，保留仍未解決的缺口。

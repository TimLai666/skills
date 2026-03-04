---
name: commercial-proposal-writing
description: Use when drafting or reviewing business proposals, funding decks, or proposal optimization tasks that require STP/4P strategy, business model articulation, financial risk analysis, and evidence-backed decision writing. Trigger on requests such as 商業企劃, 募資 deck, 提案優化, STP/4P, 商業模式, 財務風險, 提案審稿.
---

# 商業企劃寫作

## Overview

把商業企劃視為「讓決策者說 Yes 的商業說服文件」。
本技能提供雙模式流程：`generate` 產生完整企劃稿，`review` 審稿並重寫關鍵段落。

## Input Contract

先標準化輸入欄位，缺值時明確標記假設：

- `proposal_type`: `internal|fundraising|partnership`
- `industry`: 產業與子領域
- `target_customer`: 目標客群輪廓
- `problem_statement`: 核心痛點
- `available_data`: 可用數據、來源與限制
- `budget`: 預算上限與分配原則
- `timeline`: 里程碑時間範圍
- `goal_kpi`: 成功指標與門檻
- `mode`: `generate|review`

若未提供 `mode`：

- 使用者給題目/想法但無完整草稿 -> 預設 `generate`
- 使用者貼已有企劃內容或要求修改 -> 預設 `review`

## Output Contract

### DraftOutput (`mode=generate`)

必含以下章節，順序不可變：

1. 執行摘要
2. 問題定義
3. 目標客群與市場區隔
4. 競爭分析與差異化定位
5. 方案與商業模式
6. 行銷策略（產品/價格/通路/推廣）
7. 執行計畫與團隊
8. 財務預估與風險評估
9. 決策請求（Ask）

### ReviewOutput (`mode=review`)

必含：

1. `缺陷清單`（Critical/Major/Minor）
2. `重寫建議`（逐段）
3. `重寫片段`（至少 3 段關鍵段落）
4. `優先修正順序`（本週必修、次要修正、可延後）

## Mandatory Strategy Flow

所有任務都要走同一主流程：

1. 行銷環境分析
2. 消費者行為分析
3. 市場競爭分析
4. STP（市場區隔 -> 目標市場 -> 市場定位）
5. 4P（產品 -> 價格 -> 通路 -> 推廣）
6. 行銷方案執行
7. 行銷績效評估

## Statistical Method Mapping

在對應章節至少給出「方法選擇理由 + 輸入欄位 + 解讀句」：

- 市場區隔：PCA/CFA、KMeans、卡方、ANOVA、Conjoint
- 目標市場選擇：卡方、ANOVA、Regression、Logistic、Conjoint
- 產品定位：MDS、Conjoint
- 4P 驗證：Conjoint、Logistic、Regression

需要技術細節時，載入 [04-statistical-method-playbook.md](./references/04-statistical-method-playbook.md) 並使用 `scripts/` 模板。

## Writing Rules From Draft

執行下列強制規則：

- 執行摘要三層：痛點開場 -> 方案亮點 -> 數字收尾
- 問題定義四元素：誰痛、痛多大、現有方案不足、不做代價
- 目標反推法：終局目標倒推漏斗指標
- 競爭三步：現況掃描、痛點定位、優勢鎖定
- 價值階梯：功能層 -> 好處層 -> 成果層
- 行銷漏斗與單位經濟：CAC/LTV/ROAS
- 財務透明化：每個關鍵數字需可推導

## Quality Gates

提交前強制檢查：

1. `Why -> What -> How -> Proof -> Ask` 是否完整
2. 財務、KPI、時程是否前後一致
3. 結論是否可追溯到數據或可驗證假設
4. 是否避免空話開場（例如「本企劃旨在」）

## Mode Workflow

### Generate

1. 依 [01-intake-and-mode-selection.md](./references/01-intake-and-mode-selection.md) 收斂輸入。
2. 套用 [02-proposal-structure-template.md](./references/02-proposal-structure-template.md) 產生章節骨架。
3. 套用 [03-stp-4p-framework-map.md](./references/03-stp-4p-framework-map.md) 填入 STP/4P 分析。
4. 需要量化時使用 [04-statistical-method-playbook.md](./references/04-statistical-method-playbook.md) 對應方法與 Python 模板。
5. 套用 [05-financial-risk-modeling-guide.md](./references/05-financial-risk-modeling-guide.md) 完成財務與風險。
6. 輸出 DraftOutput。

### Review

1. 先依 [06-review-rubric-and-rewrite-rules.md](./references/06-review-rubric-and-rewrite-rules.md) 評分。
2. 找出阻礙決策的高風險缺陷（論點斷裂、數字不一致、證據不足）。
3. 先給優先修正順序，再提供逐段重寫。
4. 輸出 ReviewOutput。

## Resources

- Intake 與模式判斷： [01-intake-and-mode-selection.md](./references/01-intake-and-mode-selection.md)
- 章節模板： [02-proposal-structure-template.md](./references/02-proposal-structure-template.md)
- STP/4P 對照： [03-stp-4p-framework-map.md](./references/03-stp-4p-framework-map.md)
- 統計方法： [04-statistical-method-playbook.md](./references/04-statistical-method-playbook.md)
- 財務風險： [05-financial-risk-modeling-guide.md](./references/05-financial-risk-modeling-guide.md)
- 審稿規則： [06-review-rubric-and-rewrite-rules.md](./references/06-review-rubric-and-rewrite-rules.md)
- 產出模板： [proposal_full_template.md](./assets/templates/proposal_full_template.md), [review_report_template.md](./assets/templates/review_report_template.md)
- Python 方法模板： `scripts/*.py`

## Note

遇到更大型、跨來源、多代理協作的研究與企劃流程，或是需輸出 Word、PDF 文件，可搭配使用其它 skills 或工具。

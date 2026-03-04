---
name: commercial-proposal-writing
description: Use when drafting or reviewing business proposals, funding decks, formal proposal outputs, and proposal optimization tasks that require STP/4P strategy, business model articulation, financial risk analysis, and evidence-backed decision writing. Trigger on requests such as 商業企劃, 正式提案, 董事會版本, 投資人版本, 標案版本, 募資 deck, 提案優化, STP/4P, 商業模式, 財務風險, 提案審稿, 資料不足先問.
---

# 商業企劃寫作

## Overview

把商業企劃視為「讓決策者說 Yes 的商業說服文件」。
本技能提供雙模式流程：`generate` 產生完整企劃稿，`review` 審稿並重寫關鍵段落，並內建可切換正式語氣檔位。

## Input Contract

先標準化輸入欄位，缺值時先進資料充足性檢查，不直接生成內容：

- `proposal_type`: `internal|fundraising|partnership`
- `industry`: 產業與子領域
- `target_customer`: 目標客群輪廓
- `problem_statement`: 核心痛點
- `available_data`: 可用數據、來源與限制
- `budget`: 預算上限與分配原則
- `timeline`: 里程碑時間範圍
- `goal_kpi`: 成功指標與門檻
- `mode`: `generate|review`
- `tone_profile`: `executive_formal|investor_formal|consulting_formal|gov_formal|auto`
- `formality_level`: `standard|strict`（預設 `strict`）
- `audience`: 受眾描述（可覆寫自動判斷）

## Data Sufficiency Gate（強制前置）

所有 `generate/review` 請求先檢查核心阻斷欄位：

- `proposal_type`
- `target_customer`
- `problem_statement`
- `goal_kpi`
- `available_data`

規則：

1. 缺任一核心欄位 -> 不進入正文生成，改輸出 `MissingDataQueryOutput`。
2. 使用者補齊後 -> 重新檢查，通過才進入原本流程。
3. 使用者明確表示「沒有資料」-> 提供 A/B/C/D 方案選單，等待使用者選擇。
4. 使用者未選擇方案前 -> 不輸出完整企劃正文。

## Mode Routing

若未提供 `mode`：

- 使用者給題目/想法但無完整草稿 -> 預設 `generate`
- 使用者貼已有企劃內容或要求修改 -> 預設 `review`

`review` 補充規則：若未提供原稿或關鍵段落，先要求貼上內容，不可憑空審稿。

若 `tone_profile=auto`：採混合策略映射

1. 先依 `proposal_type`：
   - `internal -> executive_formal`
   - `fundraising -> investor_formal`
   - `partnership -> consulting_formal`
2. 再依 `audience` 或 prompt 關鍵詞覆寫：
   - 若包含「政府、標案、審議、公部門、法遵」-> `gov_formal`
   - 若包含「董事會、經營會議、管理層」-> `executive_formal`
   - 若包含「投資人、VC、基金、IR」-> `investor_formal`
   - 若包含「策略顧問、顧問報告、MECE」-> `consulting_formal`

## Output Contract

### MissingDataQueryOutput（資料不足時優先輸出）

當核心欄位不足時，固定輸出：

- `missing_fields`: 缺失欄位清單
- `why_needed`: 每欄位用途（為何必要）
- `questions_to_user`: 精準提問清單（可直接回填）
- `no_data_options`: A/B/C/D 方案選單
- `next_step_rule`: 「補資料或選方案後才進入 generate/review」

### DraftOutput (`mode=generate`)

僅在通過 Data Sufficiency Gate 後輸出，必含以下章節：

1. 執行摘要
2. 問題定義
3. 目標客群與市場區隔
4. 競爭分析與差異化定位
5. 方案與商業模式
6. 行銷策略（產品/價格/通路/推廣）
7. 執行計畫與團隊
8. 財務預估與風險評估
9. 決策請求（Ask）
10. `Style Metadata`

`Style Metadata` 固定輸出：

- `tone_profile_final`
- `formality_level`
- `audience_assumed`

### ReviewOutput (`mode=review`)

僅在通過 Data Sufficiency Gate 且有可審核原稿時輸出，必含：

1. `缺陷清單`（Critical/Major/Minor）
2. `重寫建議`（逐段）
3. `重寫片段`（至少 3 段關鍵段落）
4. `優先修正順序`（本週必修、次要修正、可延後）
5. `語氣修正清單`

`語氣修正清單` 固定輸出：

- `口語化問題`
- `不夠正式句`
- `替換建議句`

`review` 模式最少輸出 8 條「口語句 -> 正式句」對照；短稿可降為 5 條並標註原因。

## No-Data Options（使用者明確無資料）

固定提供以下選單：

- **A. 最快假設版（當日可產出）**
  - 以通用假設建立草案，全部假設顯式標註，不可偽裝為真實資料。
- **B. 輕量訪談驗證版（2-5 天）**
  - 先做少量訪談/內部盤點，再輸出企劃，降低假設風險。
- **C. 小規模數據蒐集後正式版（1-2 週）**
  - 先蒐集最小可用數據，再輸出可送審版本。
- **D. 客製方案**
  - 依使用者限制（時程/可取得資料/受眾）客製流程。

預設不自動替使用者選 A/B/C/D。

## No-Hallucination Rules（硬性禁令）

1. 不得自行臆測關鍵數據（市場規模、轉換率、財務數字、KPI 基準）。
2. 不得把猜測寫成事實句。
3. 若採假設，必須標示：`Assumption` + `Validation Needed` + `Risk`。
4. 若使用者要求「先填數字」但未提供來源，先回問來源或切換到 A 假設版。

## Mandatory Strategy Flow

通過資料閘後再走主流程：

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

## Formal Tone Rules

正式語氣硬性規範適用所有檔位：

1. 禁用口語字與情緒詞（例如「超、爆、很猛、感覺、應該會」）。
2. 禁用模糊量詞（例如「很多、很快、大幅」）而無數字佐證。
3. 禁用無證據承諾句（例如「保證成功」「一定成長」）。
4. 每段至少包含一個可核對元素：數字、條件、時間、責任人或驗證方法。
5. 若使用者指定語氣與場景衝突，保留使用者指定並加一行風險提示。

語氣檔位細節與禁用詞，載入 [07-formal-tone-style-guide.md](./references/07-formal-tone-style-guide.md)。

## Quality Gates

提交前強制檢查：

1. `Why -> What -> How -> Proof -> Ask` 是否完整
2. 財務、KPI、時程是否前後一致
3. 結論是否可追溯到數據或可驗證假設
4. 是否避免空話開場（例如「本企劃旨在」）
5. 是否通過正式語氣檢核表（見 [08-output-polish-checklist.md](./references/08-output-polish-checklist.md)）

## Mode Workflow

### Generate

1. 依 [01-intake-and-mode-selection.md](./references/01-intake-and-mode-selection.md) 收斂輸入與語氣。
2. 先過 Data Sufficiency Gate。
3. 若缺資料則輸出 MissingDataQueryOutput。
4. 若通過，套用 [02-proposal-structure-template.md](./references/02-proposal-structure-template.md) 產生章節骨架。
5. 套用 [03-stp-4p-framework-map.md](./references/03-stp-4p-framework-map.md) 填入 STP/4P 分析。
6. 需要量化時使用 [04-statistical-method-playbook.md](./references/04-statistical-method-playbook.md) 對應方法與 Python 模板。
7. 套用 [05-financial-risk-modeling-guide.md](./references/05-financial-risk-modeling-guide.md) 完成財務與風險。
8. 最末執行語氣 polish（避免先美化後被重寫覆蓋）。
9. 輸出 DraftOutput + Style Metadata。

### Review

1. 先確認有可審核原稿內容。
2. 先過 Data Sufficiency Gate（重點檢查 `target_customer`, `problem_statement`, `goal_kpi`, `available_data`）。
3. 若缺資料或缺原稿，輸出 MissingDataQueryOutput 或原稿補件請求。
4. 若通過，依 [06-review-rubric-and-rewrite-rules.md](./references/06-review-rubric-and-rewrite-rules.md) 評分。
5. 找出阻礙決策的高風險缺陷（論點斷裂、數字不一致、證據不足）。
6. 執行語氣違規掃描與「口語句 -> 正式句」轉換。
7. 先給優先修正順序，再提供逐段重寫。
8. 輸出 ReviewOutput + 語氣修正清單。

## Resources

- Intake 與模式判斷： [01-intake-and-mode-selection.md](./references/01-intake-and-mode-selection.md)
- 章節模板： [02-proposal-structure-template.md](./references/02-proposal-structure-template.md)
- STP/4P 對照： [03-stp-4p-framework-map.md](./references/03-stp-4p-framework-map.md)
- 統計方法： [04-statistical-method-playbook.md](./references/04-statistical-method-playbook.md)
- 財務風險： [05-financial-risk-modeling-guide.md](./references/05-financial-risk-modeling-guide.md)
- 審稿規則： [06-review-rubric-and-rewrite-rules.md](./references/06-review-rubric-and-rewrite-rules.md)
- 正式語體指南： [07-formal-tone-style-guide.md](./references/07-formal-tone-style-guide.md)
- 輸出 polish 清單： [08-output-polish-checklist.md](./references/08-output-polish-checklist.md)
- 產出模板： [proposal_full_template.md](./assets/templates/proposal_full_template.md), [review_report_template.md](./assets/templates/review_report_template.md)
- Python 方法模板： `scripts/*.py`

## Note

遇到更大型、跨來源、多代理協作的研究與企劃流程，或是需輸出 Word、PDF 文件，可搭配使用其它 skills 或工具。
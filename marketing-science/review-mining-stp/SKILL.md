---
name: review-mining-stp
description: Use when customer reviews, survey comments, support tickets, app store feedback, or social replies need to be converted into STP analysis. Supports full review-to-strategy workflows and partial execution for segmentation, targeting, positioning, or custom submodules with upstream artifacts.
---

# Review Mining STP

## Overview

本技能用於將顧客評論資料轉換為可審計、可局部執行的 STP 分析框架。評論探勘構成證據底座；主流程固定為 `Segmentation -> Targeting -> Positioning -> Strategy`。

執行原則：

- 先進行 intake、scope 與 dependency gate。
- `full` 執行完整 STP；`segmentation`、`targeting`、`positioning` 允許局部執行。
- `custom` 僅執行指定子模組，並保留 prerequisite trace。
- 分群必須符合 `每群占比 > 5%`；不合格時降低 `k` 並重新執行。
- `貨` 類訊號必須標記 `System 1 / System 2`。
- Maslow 分析必須列出五需求關鍵字。
- 定位分析以前必須先建立定位評分表。
- 預設輸出語言為繁體中文。

## Trigger Conditions

適用條件：

- 任務目標為將評論資料整理為 `Segmentation -> Targeting -> Positioning -> Strategy` 分析。
- 任務僅需執行 `segmentation`、`targeting`、`positioning` 其中一段。
- 任務需依指定子模組執行局部分析，例如 `perceptual-map` 或 `target-selection`。
- 任務需將人／貨／場訊號轉換為市場區隔、目標市場與品牌定位結論。
- 任務需建立定位評分表、理想點、知覺圖與四象限策略矩陣。

排除條件：

- 無評論文本，亦無可重用 upstream artifacts，且仍要求 STP 分析。
- 任務僅為單句情緒分類。
- 任務核心為因果識別、實驗估計或媒體投放優化。
- 任務僅需文案成稿，不需分析骨架。

## Transfer Conditions

- 文案 brief 成稿需求：輸出分析結論後轉交 `$copywriting`。
- 追蹤設計需求：輸出目標市場與定位假設後轉交 `$analytics-tracking`。
- 實驗設計需求：輸出 target selection 與定位假設後轉交 `$ab-test-setup`。
- Maslow 深化需求：允許引導 `$maslow-five-needs-marketing` 補充，但本技能維持主流程控制權。

## Input Contract

必要欄位：

- `run_mode`: `full | segmentation | targeting | positioning | custom`
- `analysis_goal`: `string`
- `reviews` 或 `review_text`

建議欄位：

- `requested_modules`: `string[]`，僅 `custom` 必填
- `upstream_artifacts`: `object`
- `customer_id`: `string`
- `created_at`: `string`
- `rating`: `number`
- `product`: `string`
- `channel`: `string`
- `locale`: `string`
- `segment`: `string`
- `version`: `string`
- `comparison_axes`: `string[]`
- `brands`: `string[]`
- `ideal_point_definition`: `string`
- `positioning_method`: `factor_analysis | mds | auto`

可接受格式：

- `CSV`
- `JSON`
- 純文字清單

`custom` 白名單子模組：

- `review-foundation`
- `segmentation-variables`
- `segment-clustering`
- `segment-profiles`
- `current-target-market`
- `potential-target-market`
- `target-selection`
- `positioning-scorecard`
- `perceptual-map`
- `positioning-diagnostics`
- `strategy-matrix`

## Intake And Dependency Gates

資料不足時，回傳 `MissingDataOutput`：

```json
{
  "missing_fields": [],
  "why_needed": {},
  "questions_to_user": [],
  "temporary_assumptions": [],
  "next_step_rule": "補齊必要欄位後再進入 STP 分析。"
}
```

partial / custom run 缺少上游產物時，回傳 `MissingPrerequisiteOutput`：

```json
{
  "requested_stage": "",
  "missing_prerequisites": [],
  "acceptable_upstream_artifacts": [],
  "auto_backfill_allowed": false,
  "next_step_rule": "若有原始評論可補跑最小必要前置；若沒有，先補 upstream artifacts。"
}
```

Gate 規則：

- `run_mode=custom` 且缺少 `requested_modules`：停止。
- 缺少 `reviews` / `review_text` 且缺少可用 `upstream_artifacts`：停止。
- `targeting` 缺少 segment 輸出時：
  - 有原始評論：補跑 `review-foundation -> segmentation-variables -> segment-clustering -> segment-profiles`。
  - 無原始評論：回 `MissingPrerequisiteOutput`。
- `positioning` 缺少 scorecard / brands / ideal point 時：
  - 有原始評論：補跑 `review-foundation -> positioning-scorecard`。
  - 無原始評論：回 `MissingPrerequisiteOutput`。
- 樣本極少時，允許探索性分析；不得輸出高信心市場決策語句。

參見 [references/01-router-and-gates.md](./references/01-router-and-gates.md)。

## Execution Router

預設執行鏈：

- `full`
  - `review-foundation`
  - `segmentation-variables`
  - `segment-clustering`
  - `segment-profiles`
  - `current-target-market`
  - `potential-target-market`
  - `target-selection`
  - `positioning-scorecard`
  - `perceptual-map`
  - `positioning-diagnostics`
  - `strategy-matrix`
- `segmentation`
  - `review-foundation`
  - `segmentation-variables`
  - `segment-clustering`
  - `segment-profiles`
- `targeting`
  - 優先使用 `upstream_artifacts.segment_profiles`
  - 缺件時補跑最小 segmentation 前置
  - 再執行 `current-target-market`、`potential-target-market`、`target-selection`
- `positioning`
  - 優先使用 `upstream_artifacts.positioning_scorecard`
  - 缺件時補跑 `review-foundation -> positioning-scorecard`
  - 再執行 `perceptual-map`、`positioning-diagnostics`、`strategy-matrix`
- `custom`
  - 僅執行 `requested_modules`
  - 輸出中必須標示自動補上的 prerequisite trace

所有 mode 必填段落：

- `Execution Scope Summary`
- `Risks / Bias / Confidence Notes`

## Segmentation Rules

`Segmentation` 階段的分析主軸為人／貨／場：

- `人`：消費者特質、需求、動機、輪廓線索
- `貨`：產品特色、購買觸發、定位基礎
- `場`：使用情境、消費情境、場景線索

強制規則：

- `貨` 必須分類為 `System 1` 或 `System 2`。
- Maslow 分析必須列出：
  - 生理需求
  - 安全需求
  - 社交需求
  - 尊重需求
  - 自我實現需求
- 區隔變數 taxonomy 必須覆蓋：
  - 地理統計
  - 人口統計
  - 心理統計
  - 行為變數
- 分群前須整理區隔變數或動機因子。
- 分群後每群占比必須 `> 5%`。
- 任一群 `< 5%` 時，降低群數並重新執行，直到全部合格。
- 每群均需輸出明確特徵描述與消費者畫像敘事。

參見 [references/02-segmentation.md](./references/02-segmentation.md)。

## Targeting Rules

`Targeting` 階段固定包含兩條分析路徑：

- `current-target-market`
  - 現有高價值、忠誠、活躍、重度消費客群
- `potential-target-market`
  - 曾購與否、意圖、潛力、可爭取客群

方法規則：

- 連續或序位反應變數：`ANOVA / post-hoc / regression`
- 二元反應變數：`chi-square / logistic regression`

輸出規則：

- 不得只停留於差異表。
- 必須明確輸出優先目標市場、次優先市場、暫不投入市場。
- 每項選擇均需附統計依據、市場規模 / 占比與品牌適配理由。

參見 [references/03-targeting.md](./references/03-targeting.md)。

## Positioning Rules

`Positioning` 階段以前必須先建立定位評分表，再進行知覺圖與定位診斷。

定位評分表規格：

- 欄位必含 `品牌欄` 與 `理想點`
- 列必含：
  - 屬性功能
  - 利益與用途
  - 品牌個性與形象
- 每格代表品牌在定位基礎上的平均表現
- `Dynamic Scorecard Summary` 必須包含信度 / 效度分析

知覺圖方法規則：

- 預設方法：`factor_analysis`
- 僅在輸入為品牌相似性或非屬性資料時使用 `MDS`
- 輸出中必須標示 `positioning_method_used`

定位輸出必含：

- 關鍵因素評估
- 標竿分析
- 理想點分析
- 競爭態勢分析
- `POD / POP`
- 四象限策略矩陣：
  - 訴求重點
  - 改善重點
  - 改變重點
  - 放棄重點

參見 [references/04-positioning.md](./references/04-positioning.md)。

## Output Contract

依 mode 輸出對應段落；以下段落永遠保留：

- `Execution Scope Summary`
- `Risks / Bias / Confidence Notes`

可依需求輸出：

- `Segmentation Summary`
- `Targeting Summary`
- `Positioning Summary`
- `Integrated STP Actions`
- `Appendix (JSON)`

參見 [references/05-output-contract-and-quality-rules.md](./references/05-output-contract-and-quality-rules.md)。

## Hard Rules

- 不得臆測不存在的品牌、理想點、區隔變數或比較維度。
- 不得因 partial / custom run 省略 prerequisite trace。
- 不得跳過 `System 1 / System 2`、Maslow keywords 或 cluster `>5%` guardrail。
- 不得只做差異表而不做 target selection。
- 不得先畫知覺圖再補定位評分表。
- 不得省略理想點、`POD / POP` 或四象限策略矩陣。
- 不得將 `factor_analysis` 與 `MDS` 無規則混用。
- 不得省略 `Dynamic Scorecard Summary` 的信度 / 效度說明。
- 不得以高信心語氣包裝低樣本或缺件分析。
- 完成前必須再對照一次 `review-mining-improve.md`。

## References

- [references/01-router-and-gates.md](./references/01-router-and-gates.md)
- [references/02-segmentation.md](./references/02-segmentation.md)
- [references/03-targeting.md](./references/03-targeting.md)
- [references/04-positioning.md](./references/04-positioning.md)
- [references/05-output-contract-and-quality-rules.md](./references/05-output-contract-and-quality-rules.md)
- [references/06-end-to-end-examples.md](./references/06-end-to-end-examples.md)
- [references/07-review-mining-improve-traceability.md](./references/07-review-mining-improve-traceability.md)

## Validation Assets

- [agents/pressure-scenario-01-full-stp.md](./agents/pressure-scenario-01-full-stp.md)
- [agents/pressure-scenario-02-segmentation-only.md](./agents/pressure-scenario-02-segmentation-only.md)
- [agents/pressure-scenario-03-targeting-with-upstream.md](./agents/pressure-scenario-03-targeting-with-upstream.md)
- [agents/pressure-scenario-04-positioning-only.md](./agents/pressure-scenario-04-positioning-only.md)
- [agents/pressure-scenario-05-custom-missing-prereq.md](./agents/pressure-scenario-05-custom-missing-prereq.md)
- [agents/validation-checklist.md](./agents/validation-checklist.md)

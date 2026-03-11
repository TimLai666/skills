---
name: review-mining-stp
description: Use when customer reviews, survey comments, support tickets, app store feedback, or social replies need to be converted into STP analysis. Supports review-to-strategy workflows where AI extracts structured dimensions first and scripts run the downstream statistics.
---

# Review Mining STP

## Overview

本技能把評論資料轉成可稽核的 `Segmentation -> Targeting -> Positioning -> Strategy` 分析，並明確拆成兩層：

- `agent layer`: 讀原始 `reviews` / `review_text`，自動抽取可量化維度、三大主題、理論標籤
- `script layer`: 只吃已評分 / 已標註 artifacts，負責 `score-to-STP` 統計，不做 raw review 語意抽取

對齊原則：

- 上游由 agent layer 負責理論、評分、主題、標註抽取
- `review-mining-improve.md` 提供下游的統計方法、STP guardrails、輸出契約
- `full` mode 以 canonical scored artifact 起跑
- `segmentation / targeting / positioning / custom` 仍保留直接吃中間 artifacts 的能力，供 partial rerun / audit 使用

## Trigger Conditions

適用：

- 需要把評論資料轉成 STP 結論與策略
- 需要從評論建立 segmentation、targeting、positioning 或知覺圖
- 需要把 Product Positioning / Purchase Motivation / Maslow / WOM Motivation 落成可分析輸出
- 需要從評論衍生 scorecard、cluster、pairwise tests、ideal point、competition landscape

不適用：

- 只有情緒分類需求
- 核心任務是因果推論、投放優化、A/B test 設計
- 只要文案成稿，不需要分析框架

## Contract Layers

### Agent-Layer Request

必要欄位：

- `run_mode`: `full | segmentation | targeting | positioning | custom`
- `analysis_goal`
- `reviews` 或 `review_text`

常用補充欄位：

- `requested_modules`
- `upstream_artifacts`
- `comparison_axes`
- `brands`
- `ideal_point_definition`
- `positioning_method`

agent layer 的責任：

- 從所有評論自動抽取 dimensions、themes、theory tags
- 把 14 項案例評分視為 example schema，不是固定欄位
- 至少覆蓋三大主題：`service_experience`, `product_performance`, `value_perception`
- 把 Product Positioning / Purchase Motivation / Maslow / WOM Motivation 寫入結構化 artifacts

若缺少必要資訊，agent layer 回 `MissingDataOutput`。

### Script-Layer Artifacts

`python scripts/run_review_mining_stp.py` 不直接吃 raw reviews。canonical quantitative input 為：

- `review_scoring_table.csv`
- `review_foundation.json`
- `analysis_context.json`
- `brands.json`
- `ideal_point.json`

`review_scoring_table.csv` 必填欄位：

- `review_id`
- `unit_id`
- `brand`

其餘數值欄位由 AI 自動從評論抽取，不固定 14 項；可帶入：

- `profile_*`
- `channel`
- `rating`

`review_foundation.json` 必須同時扮演語意與統計橋接層，至少包含：

- `dimension_catalog`
- `theme_mapping`
- `people_insights`
- `product_triggers`
- `context_scenarios`
- `system1_system2_split`
- `maslow_keywords`

`dimension_catalog` 的每個 dimension 至少包含：

- `column`
- `label`
- `theme`
- `theory_tags`
- `stat_roles`

`theme_mapping` 必須涵蓋：

- `service_experience`
- `product_performance`
- `value_perception`

scripts 會在 `full` mode 自動產出三個中間統計 artifacts：

- `segmentation_variables.csv`
- `targeting_dataset.csv`
- `positioning_scorecard.csv`

partial / custom rerun 仍可直接把這三個檔案當輸入。

若缺件，script layer 只回 `MissingPrerequisiteOutput`，且：

- `missing_prerequisites` 只列真正缺少的 artifacts
- `auto_backfill_allowed` 固定為 `false`
- script layer 不負責 raw reviews -> artifacts

## Execution Router

- `full`: 讀 canonical scored artifacts，跑完整統計流程並輸出三個 intermediates
- `segmentation`: 使用 `review_foundation.json + segmentation_variables.csv`
- `targeting`: 使用 `segment_profiles.json + targeting_dataset.csv`
- `positioning`: 使用 `positioning_scorecard.csv + brands.json + ideal_point.json`
- `custom`: 只執行 `requested_modules`

`custom` 白名單：

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

## Stage Rules

### Segmentation

- 分析主軸固定為人／貨／場
- `貨` 類訊號必須標記 `System 1 / System 2`
- 必須列出 Maslow 五需求關鍵字
- 區隔變數 taxonomy 必須覆蓋地理 / 人口 / 心理 / 行為
- clustering 路徑為 `factor_analysis -> K-means`
- 若任一群 `< 5%`，降低 `k` 重跑並記錄 rerun
- 每群必須有 cluster share、persona、consumer portrait narrative

### Targeting

- 優先從 `dimension_catalog.stat_roles` 取 `current_target` / `potential_target`
- `analysis_context.comparison_axes` 可覆蓋預設 targeting 軸
- 連續反應變數：`ANOVA / regression`
- 二元反應變數：`chi-square / logistic regression`
- `ANOVA p < 0.05` 必須輸出 `pairwise_comparison_table`
- 若有 `profile_*` 欄位，必須輸出 `profile_significance_summary`
- 最終選擇必須輸出：
  - `priority_segments`
  - `secondary_segments`
  - `deprioritized_segments`
  - `target_selection_rationale`

### Positioning

- `positioning_scorecard` 由 `stat_roles` 含 `positioning` 的維度建立
- `positioning_scorecard` 必須納入理想點
- 預設方法為 `factor_analysis`
- 僅在品牌相似性 / similarity input 下使用 `MDS`
- `factor_analysis` 路徑必須輸出：
  - 品牌點 / 理想點
  - 由原點出發的 attribute vectors
  - `projection_interpretation`
- `MDS` 路徑若無向量，必須回 `projection_interpretation.status=not_available`
- `Dynamic Scorecard Summary` 至少要有：
  - 高低分定位基礎
  - 理想點距離摘要
  - 重要性 / 表現落差
  - `reliability_analysis`
  - `validity_analysis`
- `competition_landscape` 必須是品牌 pairwise 距離，不可用距理想點距離替代

## Output Contract

所有 mode 都要有：

- `Execution Scope Summary`
- `Risks / Bias / Confidence Notes`
- `Appendix (JSON)`

依 stage 輸出：

- `Segmentation Summary`
- `Targeting Summary`
- `Positioning Summary`
- `Integrated STP Actions`

推薦補充：

- `proactive_marketing_notes`
- `usp_translation_candidates`

## Hard Rules

- 不得把 raw review request 和 script artifact input 混為一談
- 不得宣稱 scripts 會做 raw review extraction 或 auto-backfill
- 不得把 14 項案例欄位寫死為 validator 契約
- 不得跳過 `System 1 / System 2`、Maslow、cluster `>5%` guardrail
- 不得省略 `profile_significance_summary`
- 不得在 `MDS` 路徑偽造 attribute vectors
- 完成前必須對照 `review-mining-improve.md`

## References

- [references/01-router-and-gates.md](./references/01-router-and-gates.md)
- [references/02-segmentation.md](./references/02-segmentation.md)
- [references/03-targeting.md](./references/03-targeting.md)
- [references/04-positioning.md](./references/04-positioning.md)
- [references/05-output-contract-and-quality-rules.md](./references/05-output-contract-and-quality-rules.md)
- [references/06-end-to-end-examples.md](./references/06-end-to-end-examples.md)
- [references/07-review-mining-improve-traceability.md](./references/07-review-mining-improve-traceability.md)
- [references/08-verification-scenarios.md](./references/08-verification-scenarios.md)

## Scripts

- Install dependencies: `python -m pip install -r requirements.txt`
- Run analysis: `python scripts/run_review_mining_stp.py --run-mode <mode> --input-dir <artifacts> --output-dir <output>`
- Partial modes: `segmentation | targeting | positioning | custom`
- Custom modules: `--requested-modules`
- Validate outputs: `python scripts/validate_review_mining_stp.py --run-mode <mode> --output-dir <output>`
- Script boundary is statistical only; raw review ingestion belongs to the agent layer

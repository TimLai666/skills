# Router And Gates

## Purpose

本文件定義 `review-mining-stp` 的兩層入口、canonical input、run mode、依賴條件與 gate 回應格式。

## Two-Layer Contract

### Agent Layer

可接輸入：

- `reviews`
- `review_text`
- 已存在的 `upstream_artifacts`

agent layer 的責任：

- 從原始評論自動抽取可量化 dimensions
- 為每個 dimension 補齊 `theme`、`theory_tags`、`stat_roles`
- 產出 `review_scoring_table.csv` 與 `review_foundation.json`

上游抽取規格在這一層的定位：

- 14 項評分只是 example schema，不是固定欄位
- 三大主題與理論對應是抽取規格的一部分

若必要欄位缺失，agent layer 回 `MissingDataOutput`。

### Script Layer

scripts 只讀 scored artifacts，不接 raw reviews。

canonical quantitative input：

- `review_scoring_table.csv`
- `review_foundation.json`
- `analysis_context.json`
- `brands.json`
- `ideal_point.json`

`full` mode 會從 canonical input 自動產出：

- `segmentation_variables.csv`
- `targeting_dataset.csv`
- `positioning_scorecard.csv`

partial / custom rerun 可直接使用：

- `segmentation_variables.csv`
- `targeting_dataset.csv`
- `segment_profiles.json`
- `positioning_scorecard.csv`

若缺件，script layer 回 `MissingPrerequisiteOutput`。

## Run Modes

- `full`
- `segmentation`
- `targeting`
- `positioning`
- `custom`

## Custom Modules

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

## Dependency Rules

- `full` 需要 canonical scored input 五件套
- `segmentation` 需要 `review_foundation.json` 與 `segmentation_variables.csv`
- `targeting` 需要 `targeting_dataset.csv` 與可用的 `segment_profiles.json`
- `positioning` 需要 `positioning_scorecard.csv`、`brands.json`、`ideal_point.json`
- `analysis_context.json` 若存在，必須寫入 `execution_scope`

## MissingDataOutput

只屬於 agent layer：

```json
{
  "missing_fields": [],
  "why_needed": {},
  "questions_to_user": [],
  "temporary_assumptions": [],
  "next_step_rule": "補齊必要欄位後再進入 STP 分析。"
}
```

## MissingPrerequisiteOutput

只屬於 script layer：

```json
{
  "requested_stage": "",
  "requested_modules": [],
  "missing_prerequisites": [],
  "acceptable_upstream_artifacts": [],
  "available_artifacts": [],
  "auto_backfill_allowed": false,
  "next_step_rule": "Scripts accept scored artifacts only; use the agent layer to build the missing files before rerunning."
}
```

規則：

- `missing_prerequisites` 只列真正缺少的檔案
- `acceptable_upstream_artifacts` 預設等於 `missing_prerequisites`
- `auto_backfill_allowed` 固定為 `false`
- 若缺的是 canonical scored artifacts，`next_step_rule` 必須明確把責任指回 agent layer preprocessing

## Backfill Policy

- raw reviews -> scored artifacts 只在 agent layer 處理
- script layer 不做 raw review NLP
- script layer 允許從 canonical scored input 推導中間統計 artifacts
- partial / custom run 若缺少必要中間檔，一律停止並回 `MissingPrerequisiteOutput`

## Required Output: Execution Scope Summary

每次輸出都必須交代：

- `run_mode`
- `requested_modules`
- `modules_executed`
- `auto_backfilled_modules`
- `upstream_artifacts_used`
- `emitted_intermediate_artifacts`
- `comparison_axes`
- `brands`
- `positioning_method_used`
- `cluster_threshold`
- `reruns_performed`
- `final_k`
- `scope_limits`

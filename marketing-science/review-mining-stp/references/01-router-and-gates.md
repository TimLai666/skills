# Router And Gates

## Purpose

本文件定義 STP 執行模式、依賴條件與 gate 回應格式。

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

- `segmentation` 需要原始評論。
- `targeting` 需要 `segment_profiles` 或可回補的原始評論。
- `positioning` 需要 `positioning_scorecard` 或可回補的原始評論。
- `strategy-matrix` 需要 `positioning-diagnostics`。

## MissingDataOutput

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

```json
{
  "requested_stage": "",
  "missing_prerequisites": [],
  "acceptable_upstream_artifacts": [],
  "auto_backfill_allowed": false,
  "next_step_rule": "若有原始評論可補跑最小必要前置；若沒有，先補 upstream artifacts。"
}
```

## Backfill Policy

- `targeting` 缺 segmentation 產物但有評論：允許補跑 `review-foundation -> segmentation-variables -> segment-clustering -> segment-profiles`
- `positioning` 缺 scorecard 但有評論：允許補跑 `review-foundation -> positioning-scorecard`
- 缺少評論且缺少 upstream artifacts：不得執行分析

## Required Output: Execution Scope Summary

每次輸出均需交代：

- `run_mode`
- `requested_modules`
- `modules_executed`
- `auto_backfilled_modules`
- `upstream_artifacts_used`
- `comparison_axes`
- `brands`
- `positioning_method_used`
- `scope_limits`

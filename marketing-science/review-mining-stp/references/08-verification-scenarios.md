# Verification Scenarios

## Purpose

本文件提供 skill-level 驗證情境，確認 agent-layer 抽取與 script-layer 統計不再混淆。

## Scenario 1: Raw Reviews, Full STP

- Input: 使用者只提供 `reviews`
- Expected: agent 先抽取 `review_scoring_table.csv` 與 `review_foundation.json`，再呼叫 scripts
- Must not do: 直接把 raw reviews 丟給 `run_review_mining_stp.py`

## Scenario 2: Full Run From Canonical Scored Input

- Input: `review_scoring_table.csv + review_foundation.json + analysis_context.json + brands.json + ideal_point.json`
- Expected:
  - full mode 可直接完成 STP
  - 同步輸出 `segmentation_variables.csv`, `targeting_dataset.csv`, `positioning_scorecard.csv`
  - `execution_scope` 要記錄 canonical inputs 與 emitted intermediates

## Scenario 3: 14 項案例 Schema

- Input: 使用既有 14 個 score columns
- Expected:
  - scripts 正常跑通
  - validator 不把 14 項欄名寫死
- Must not do: 因為欄位不是固定清單就拒絕

## Scenario 4: Flexible Custom Schema

- Input: 不沿用 14 項案例，而是自定義 score columns，且 `dimension_catalog` 合法
- Expected:
  - scripts 仍可跑 segmentation / targeting / positioning
  - targeting 仍可依 `stat_roles` 判定 current / potential 路徑

## Scenario 5: Targeting Partial Run With Upstream Segment Profiles

- Input: `targeting_dataset.csv` + `segment_profiles.json`
- Expected: script 直接產出 targeting 結果
- Must not do: 因為沒有 raw reviews 就拒絕執行

## Scenario 6: Custom Run Missing Scorecard

- Input: `brands.json` + `ideal_point.json`，要求 `perceptual-map`
- Expected: 回 `MissingPrerequisiteOutput`，只列真正缺少的 `positioning_scorecard.csv`
- Must not do: 回報其實已提供的檔案為缺件

## Scenario 7: Factor Analysis Path

- Input: 屬性型 `positioning_scorecard.csv`
- Expected:
  - `positioning_method_used = factor_analysis`
  - 有向量表
  - 有 `projection_interpretation`

## Scenario 8: MDS Path

- Input: `brands.json` 含 `similarity_matrix`
- Expected:
  - `positioning_method_used = mds`
  - `attribute_vectors_not_defined = true`
  - `projection_interpretation.status = not_available`

## Scenario 9: Input Contract Failure

- Input: canonical scored input 存在，但 `dimension_catalog` 缺失、`theme_mapping` 不完整，或可用數值欄位少於 3 個
- Expected: router 直接失敗，明確指出哪個 contract 錯誤
- Must not do: 靜默 fallback 到舊版 stage-first input

## Scenario 10: Validator Guardrail

- Input: 刻意刪掉 `appendix.execution_scope.modules_executed`
- Expected: validator 失敗
- Must not do: 因為 summary 存在就放行

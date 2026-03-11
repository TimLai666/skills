# Output Contract And Quality Rules

## Default Output Shape

所有 mode 都必須輸出：

1. `Execution Scope Summary`
2. `Risks / Bias / Confidence Notes`
3. `Appendix (JSON)`

依 stage 補充：

4. `Segmentation Summary`
5. `Targeting Summary`
6. `Positioning Summary`
7. `Integrated STP Actions`

## Required Section Specs

### Segmentation Summary

- `people_insights`
- `product_triggers`
- `context_scenarios`
- `system1_system2_split`
- `maslow_keywords`
- `segment_variable_table`
- `cluster_share_table`
- `segment_profiles`
- `consumer_portrait_narrative`

### Targeting Summary

- `current_target_market`
- `potential_target_market`
- `method_selection`
- `profile_significance_summary`
- `pairwise_comparison_table`
- `target_selection_decision`
- `target_selection_rationale`

`target_selection_decision` 必須再包含：

- `priority_segments`
- `secondary_segments`
- `deprioritized_segments`
- `comparison_axes_used`

### Positioning Summary

- `positioning_scorecard`
- `dynamic_scorecard_summary`
- `positioning_method_used`
- `perceptual_map_figure`
- `perceptual_map_coordinate_table`
- `perceptual_map_vector_table`
- `perceptual_map_method`
- `perceptual_map_interpretation`
- `projection_interpretation`
- `positioning_diagnostics`
- `strategy_matrix`

`dynamic_scorecard_summary` 至少要有：

- `highest_scoring_attributes`
- `lowest_scoring_attributes`
- `ideal_point_distance_summary`
- `importance_performance_gap`
- `reliability_analysis`
- `validity_analysis`

`positioning_diagnostics.competition_landscape` 每列至少要有：

- `brand_a`
- `brand_b`
- `distance`

## Appendix (JSON) Minimum Schema

```json
{
  "execution_scope": {},
  "segmentation_summary": {},
  "targeting_summary": {},
  "positioning_summary": {},
  "integrated_stp_actions": [],
  "proactive_marketing_notes": [],
  "usp_translation_candidates": [],
  "risks_bias_confidence_notes": [],
  "evidence": []
}
```

## Execution Scope Minimum Keys

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

## Quality Checklist

- 不得把 agent request 與 script artifacts 混用
- full mode 的 `upstream_artifacts_used` 必須列出 canonical scored input
- full mode 的 `emitted_intermediate_artifacts` 必須列出三個 generated statistical artifacts
- partial / custom run 必須保留 prerequisite trace
- segmentation 必須有 `System 1 / System 2`
- segmentation 必須有 Maslow 五需求關鍵字
- segmentation 必須記錄 `cluster_threshold / reruns_performed / final_k`
- targeting 必須同時有 current / potential 兩條分析路徑
- targeting 必須有 `priority / secondary / deprioritized`
- targeting 必須有 `profile_significance_summary`
- 若有 `ANOVA p < 0.05`，必須有 `pairwise_comparison_table`
- positioning 必須有理想點
- positioning 預設 `factor_analysis`
- positioning 的 `Dynamic Scorecard Summary` 必須有距離、落差、信度、效度
- positioning 的 `competition_landscape` 必須是品牌 pairwise 距離
- `MDS` 路徑不得偽造向量表
- validator 不得把 14 項案例欄位寫死
- 完成前必須對照 `review-mining-improve.md`

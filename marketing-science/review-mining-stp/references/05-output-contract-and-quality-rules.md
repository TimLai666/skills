# Output Contract And Quality Rules

## Default Output Shape

以下段落永遠必填：

1. `Execution Scope Summary`
2. `Risks / Bias / Confidence Notes`

依 mode 增列：

3. `Segmentation Summary`
4. `Targeting Summary`
5. `Positioning Summary`
6. `Integrated STP Actions`
7. `Appendix (JSON)`

## Required Section Specs

### Segmentation Summary

至少包含：

- `people_insights`
- `product_triggers`
- `context_scenarios`
- `system1_system2_split`
- `maslow_keywords`
- `segment_variable_table`
- `cluster_share_table`
- `segment_profiles`

### Targeting Summary

至少包含：

- `current_target_market`
- `potential_target_market`
- `method_selection`
- `target_selection_decision`
- `target_selection_rationale`

### Positioning Summary

至少包含：

- `positioning_scorecard`
- `dynamic_scorecard_summary`
- `positioning_method_used`
- `perceptual_map_figure`
- `perceptual_map_coordinate_table`
- `perceptual_map_vector_table`
- `perceptual_map_method`
- `perceptual_map_interpretation`
- `positioning_diagnostics`
- `strategy_matrix`

### Integrated STP Actions

至少包含：

- `priority_segments`
- `target_market_actions`
- `positioning_actions`
- `message_or_offer_implications`

## Appendix (JSON) Minimum Schema

```json
{
  "execution_scope": {},
  "segmentation_summary": {},
  "targeting_summary": {},
  "positioning_summary": {},
  "integrated_stp_actions": [],
  "risks_bias_confidence_notes": [],
  "evidence": []
}
```

## Quality Checklist

- 是否先輸出 `Execution Scope Summary`
- partial / custom run 是否揭露 prerequisite trace
- segmentation 是否包含 `System 1 / System 2`
- segmentation 是否列出 Maslow 五需求關鍵字
- 分群是否遵守 `每群占比 > 5%`
- targeting 是否分 current / potential 兩條路徑
- targeting 是否明確做 target selection
- positioning 是否有品牌欄與理想點
- positioning 是否預設使用 `factor_analysis`
- positioning 是否輸出真實散佈圖
- positioning 是否保留品牌點
- positioning 是否輸出由原點出發的屬性向量
- positioning 是否附座標表與向量表
- `Dynamic Scorecard Summary` 是否包含信度 / 效度分析
- 是否有 `POD / POP`
- 是否有訴求 / 改善 / 改變 / 放棄
- 是否完成 `review-mining-improve.md` 最終對照

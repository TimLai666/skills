# Output Contract And Quality Rules

## Default Output Shape

Every completed run should produce:

1. `Execution Scope Summary`
2. `Risks / Bias / Confidence Notes`
3. `Appendix (JSON)`

When the corresponding stage runs, also produce:

4. `Segmentation Summary`
5. `Targeting Summary`
6. `Positioning Summary`
7. `Integrated STP Actions`

## Stage-Level Report Contract

Each major summary section must contain:

- `what_this_section_is_doing`
- `methods_used`
- `theories_used`
- `plain_language_explanation`
- `evidence_quote_status`
- `evidence_quote_reason`
- `evidence_quotes`

### `methods_used`

Must be a non-empty list of objects with:

- `name`
- `description`

### `theories_used`

Must be a non-empty list of objects with:

- `name`
- `description`

### `evidence_quotes`

Each quote object must include:

- `review_id`
- `quote_text`
- `why_this_quote_matters`
- `linked_items`

When canonical review evidence is available:

- each major section should contain 2–3 quotes
- `quote_text` must exactly match `review_scoring_table.csv.review_text`
- `review_id` must exist in the canonical score table

## Stage-Specific Fields

### Segmentation Summary

Must retain:

- `people_insights`
- `product_triggers`
- `context_scenarios`
- `system1_system2_split`
- `maslow_keywords`
- `segment_variable_table`
- `cluster_share_table`
- `segment_profiles`
- `consumer_portrait_narrative`

`cluster_selection` must retain:

- `cluster_threshold`
- `reruns_performed`
- `final_k`

### Targeting Summary

Must retain:

- `current_target_market`
- `potential_target_market`
- `method_selection`
- `profile_significance_summary`
- `pairwise_comparison_table`
- `target_selection_decision`
- `target_selection_rationale`

`target_selection_decision` must retain:

- `priority_segments`
- `secondary_segments`
- `deprioritized_segments`
- `comparison_axes_used`

### Positioning Summary

Must retain:

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

`dynamic_scorecard_summary` must retain:

- `highest_scoring_attributes`
- `lowest_scoring_attributes`
- `ideal_point_distance_summary`
- `importance_performance_gap`
- `reliability_analysis`
- `validity_analysis`

`positioning_diagnostics.competition_landscape` rows must include:

- `brand_a`
- `brand_b`
- `distance`

## Appendix Minimum Schema

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

## Quality Checklist

- Full runs must list canonical input files in `execution_scope.upstream_artifacts_used`.
- Full runs must list all three emitted statistical intermediates in `execution_scope.emitted_intermediate_artifacts`.
- Partial and custom runs must retain accurate prerequisite traces.
- Segmentation must keep `System 1 / System 2`, Maslow, and the `>5%` cluster guardrail metadata.
- Targeting must keep current-market and potential-market outputs plus pairwise comparisons where required.
- Positioning must keep ideal-point logic, pairwise competition distance, and no fabricated vectors in `MDS`.
- Reports must explain the method and theory used in language that non-specialists can understand.
- Evidence quotes must be verbatim and traceable.
- Validators must not hardcode a fixed item count.

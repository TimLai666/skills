# Review Mining STP Traceability

## Purpose

本文件把 skill 的上游抽取規格與 `review-mining-improve.md` 的統計要求，同時對應到 skill 文檔、script output 與測試證據。

## Evidence Matrix

| Requirement | Source | Doc Coverage | Script / Output Coverage | Test Coverage |
| --- | --- | --- | --- | --- |
| raw reviews 先經 AI 抽取，再交給 scripts | upstream extraction spec | `SKILL.md`, `references/01-router-and-gates.md`, `references/06-end-to-end-examples.md` | `MissingPrerequisiteOutput.next_step_rule`, canonical scored-input contract | `test_raw_reviews_are_rejected_until_agent_layer_creates_scored_artifacts` |
| 14 項評分只是案例，不是固定 schema | upstream extraction spec | `SKILL.md`, `references/06-end-to-end-examples.md` | validator 不檢查固定欄名 | `test_full_run_accepts_canonical_inputs_and_emits_intermediate_artifacts`, `test_full_run_supports_flexible_non_14_dimension_schema` |
| 三大主題 `service_experience / product_performance / value_perception` | upstream extraction spec | `SKILL.md`, `references/01-router-and-gates.md` | `review_foundation.theme_mapping` input contract | `test_full_run_rejects_incomplete_theme_mapping` |
| Product Positioning / Purchase Motivation / Maslow / WOM Motivation 屬於 agent-layer 標註 | upstream extraction spec | `SKILL.md`, `references/06-end-to-end-examples.md` | `review_foundation.dimension_catalog.theory_tags` | `test_full_run_accepts_canonical_inputs_and_emits_intermediate_artifacts` |
| canonical input 是 `review_scoring_table.csv` | implementation plan | `SKILL.md`, `references/01-router-and-gates.md` | `execution_scope.upstream_artifacts_used` | `test_full_run_accepts_canonical_inputs_and_emits_intermediate_artifacts` |
| full mode 會輸出三個中間統計 artifacts | implementation plan | `SKILL.md`, `references/05-output-contract-and-quality-rules.md` | `segmentation_variables.csv`, `targeting_dataset.csv`, `positioning_scorecard.csv`, `execution_scope.emitted_intermediate_artifacts` | `test_full_run_accepts_canonical_inputs_and_emits_intermediate_artifacts` |
| Maslow 五需求關鍵字 | `review-mining-improve.md` | `SKILL.md`, `references/02-segmentation.md` | `segmentation_summary.maslow_keywords` | `test_segmentation_partial_run_still_supports_direct_intermediate_artifacts` |
| `System 1 / System 2` | `review-mining-improve.md` | `SKILL.md`, `references/02-segmentation.md` | `segmentation_summary.system1_system2_split` | `test_segmentation_partial_run_still_supports_direct_intermediate_artifacts` |
| cluster `> 5%` guardrail 與 rerun 紀錄 | `review-mining-improve.md` | `SKILL.md`, `references/02-segmentation.md` | `cluster_selection.cluster_threshold`, `reruns_performed`, `final_k` | `test_segmentation_partial_run_still_supports_direct_intermediate_artifacts` |
| targeting 同時含 current / potential 路徑 | `review-mining-improve.md` | `SKILL.md`, `references/03-targeting.md` | `current_target_market`, `potential_target_market` | `test_full_run_accepts_canonical_inputs_and_emits_intermediate_artifacts` |
| `comparison_axes` 可覆蓋 targeting 預設軸 | `review-mining-improve.md` + implementation plan | `SKILL.md`, `references/06-end-to-end-examples.md` | `target_selection_decision.comparison_axes_used` | `test_targeting_partial_run_works_with_emitted_intermediates` |
| `profile_significance_summary` | `review-mining-improve.md` | `SKILL.md`, `references/03-targeting.md` | `targeting_summary.profile_significance_summary` | `test_full_run_accepts_canonical_inputs_and_emits_intermediate_artifacts` |
| `pairwise_comparison_table` | `review-mining-improve.md` | `SKILL.md`, `references/03-targeting.md` | `targeting_summary.pairwise_comparison_table` | `test_full_run_accepts_canonical_inputs_and_emits_intermediate_artifacts` |
| `priority / secondary / deprioritized` | `review-mining-improve.md` | `SKILL.md`, `references/03-targeting.md` | `target_selection_decision` | `test_targeting_partial_run_works_with_emitted_intermediates` |
| positioning scorecard 含 ideal point | `review-mining-improve.md` | `SKILL.md`, `references/04-positioning.md` | `positioning_scorecard` 含 `point_type=ideal` | `test_full_run_accepts_canonical_inputs_and_emits_intermediate_artifacts` |
| 預設 `factor_analysis` | `review-mining-improve.md` | `SKILL.md`, `references/04-positioning.md` | `positioning_method_used` | `test_full_run_accepts_canonical_inputs_and_emits_intermediate_artifacts` |
| `MDS` 不偽造向量 | `review-mining-improve.md` | `SKILL.md`, `references/04-positioning.md` | `attribute_vectors_not_defined`, 空向量表 | `test_positioning_mds_does_not_fabricate_attribute_vectors` |
| `Dynamic Scorecard Summary` 含距離 / 落差 / 信度 / 效度 | `review-mining-improve.md` | `SKILL.md`, `references/05-output-contract-and-quality-rules.md` | `dynamic_scorecard_summary` | `test_full_run_accepts_canonical_inputs_and_emits_intermediate_artifacts` |
| `competition_landscape` 為 pairwise 距離 | `review-mining-improve.md` | `SKILL.md`, `references/05-output-contract-and-quality-rules.md` | `positioning_diagnostics.competition_landscape` | `test_full_run_accepts_canonical_inputs_and_emits_intermediate_artifacts` |
| partial / custom 缺件 gate | implementation plan | `SKILL.md`, `references/01-router-and-gates.md` | `MissingPrerequisiteOutput.json` | `test_custom_missing_prerequisite_lists_only_true_missing_intermediate` |
| `Execution Scope Summary` 完整欄位 | implementation plan | `SKILL.md`, `references/05-output-contract-and-quality-rules.md` | `appendix.execution_scope` | `test_validator_rejects_missing_execution_scope_fields` |
| canonical input contract 失敗要正確報錯 | implementation plan | `SKILL.md`, `references/06-end-to-end-examples.md` | router input validation | `test_full_run_rejects_missing_dimension_catalog`, `test_full_run_rejects_incomplete_theme_mapping`, `test_full_run_rejects_insufficient_score_columns` |

## Audit Note

- 這版 traceability 的完成標準是 `doc + output + test` 三者對齊。
- 上游抽取規格的責任是定義理論與維度，不是固定欄位名契約。
- `review-mining-improve.md` 的責任是統計方法、guardrails 與輸出品質規格。

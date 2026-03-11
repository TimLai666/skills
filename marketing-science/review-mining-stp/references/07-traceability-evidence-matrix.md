# Traceability Evidence Matrix

## Purpose

This matrix ties the public skill contract to documentation, script outputs, and automated tests.

## Evidence Matrix

| Requirement | Upstream Workflow Evidence | Script / Output Evidence | Test Coverage |
| --- | --- | --- | --- |
| Raw reviews are handled by the agent layer, not the scripts | `SKILL.md`, `references/01-router-and-gates.md`, `references/06-end-to-end-examples.md` | `MissingPrerequisiteOutput.next_step_rule` | `test_raw_reviews_are_rejected_until_agent_layer_creates_scored_artifacts` |
| Scoring is an agent workflow, not a Python-owned process | `SKILL.md`, `references/06-end-to-end-examples.md` | scripts validate only scored artifacts | `test_full_run_accepts_missing_scoring_rubric_metadata`, `test_full_run_accepts_custom_scoring_rubric_metadata` |
| Scripts only require canonical scored artifacts plus statistical metadata | `SKILL.md`, `references/01-router-and-gates.md` | `execution_scope.upstream_artifacts_used` | `test_full_run_accepts_dynamic_scored_inputs_and_emits_intermediate_artifacts` |
| Each review keeps verbatim `review_text` for later evidence quoting | `SKILL.md`, `references/05-output-contract-and-quality-rules.md` | `report.md`, `appendix.json` evidence quote sections | `test_full_run_accepts_dynamic_scored_inputs_and_emits_intermediate_artifacts`, `test_validator_rejects_non_traceable_evidence_quote` |
| The scored table must keep numeric inputs on the `0-7` scale | `SKILL.md`, `references/01-router-and-gates.md` | canonical input validation | `test_full_run_rejects_out_of_range_scores` |
| Scripts do not assume a fixed item count | `SKILL.md`, `references/06-end-to-end-examples.md` | dynamic `dimension_catalog` handling | `test_full_run_supports_alternate_dynamic_schema` |
| `dimension_catalog` requires theory tags, stat roles, and plain-language definitions | `SKILL.md`, `references/01-router-and-gates.md` | canonical input validation | `test_full_run_rejects_missing_plain_language_definition` |
| Three core themes are mandatory | `SKILL.md`, `references/01-router-and-gates.md` | `theme_mapping` validation | `test_full_run_rejects_incomplete_theme_mapping` |
| Full mode emits all three intermediate statistical artifacts | `SKILL.md`, `references/05-output-contract-and-quality-rules.md` | `segmentation_variables.csv`, `targeting_dataset.csv`, `positioning_scorecard.csv`, `execution_scope.emitted_intermediate_artifacts` | `test_full_run_accepts_dynamic_scored_inputs_and_emits_intermediate_artifacts` |
| Segmentation uses `factor_analysis -> K-means` with `>5%` guardrail metadata | `SKILL.md`, `references/02-segmentation.md` | `cluster_selection.cluster_threshold`, `reruns_performed`, `final_k` | `test_segmentation_partial_run_still_supports_direct_intermediate_artifacts` |
| Targeting respects `comparison_axes` override | `SKILL.md`, `references/03-targeting.md`, `references/06-end-to-end-examples.md` | `target_selection_decision.comparison_axes_used` | `test_targeting_partial_run_uses_comparison_axes_override` |
| Targeting emits profile significance and pairwise comparison outputs | `SKILL.md`, `references/03-targeting.md`, `references/05-output-contract-and-quality-rules.md` | `profile_significance_summary`, `pairwise_comparison_table` | `test_full_run_accepts_dynamic_scored_inputs_and_emits_intermediate_artifacts` |
| Positioning emits ideal-point and pairwise competition diagnostics | `SKILL.md`, `references/04-positioning.md`, `references/05-output-contract-and-quality-rules.md` | `positioning_scorecard`, `competition_landscape`, `dynamic_scorecard_summary` | `test_full_run_accepts_dynamic_scored_inputs_and_emits_intermediate_artifacts` |
| `MDS` never fabricates attribute vectors | `SKILL.md`, `references/04-positioning.md` | `attribute_vectors_not_defined`, no vector table | `test_positioning_mds_does_not_fabricate_attribute_vectors` |
| Every major report section names methods, theories, plain-language explanation, and evidence quotes | `SKILL.md`, `references/05-output-contract-and-quality-rules.md` | `appendix.json`, `report.md` | `test_full_run_accepts_dynamic_scored_inputs_and_emits_intermediate_artifacts` |
| Validator checks deep execution-scope and evidence contracts, not scoring prose | `references/05-output-contract-and-quality-rules.md`, `references/08-verification-scenarios.md` | validator failure paths | `test_validator_rejects_missing_execution_scope_fields`, `test_validator_rejects_non_traceable_evidence_quote` |

## Audit Note

- The matrix separates upstream scoring workflow evidence from downstream statistical-output evidence.
- The goal is not only statistical correctness, but also a clean boundary between agent work and script work.

---
name: review-mining-stp
description: Use when customer reviews, support tickets, app store feedback, or other review-like text must be converted into STP analysis with agent-led scoring upstream and statistical scripts downstream.
---

# Review Mining STP

## Overview

This skill converts review text into `Segmentation -> Targeting -> Positioning -> Strategy` outputs through a strict two-layer contract.

- `agent layer`: reads raw reviews, infers scored items, assigns theory tags, and preserves verbatim review text.
- `script layer`: accepts scored artifacts only and performs statistical analysis plus report assembly.

The `agent layer` is an upstream workflow boundary, not a requirement to use any specific API, service, or orchestration tool.

The scripts are tools, not the main workflow. They do not read raw reviews, decide how to score them, or define the scoring process.

## When To Use

Use this skill when:

- you need STP outputs from reviews, comments, or feedback text
- you need a repeatable scored-artifact contract before running statistics
- you need segmentation, targeting, or positioning outputs with explicit methods and theory labels
- you need report sections backed by verbatim review quotes instead of unsupported interpretation

Do not use this skill when:

- the task is only qualitative summarization with no scoring and no downstream statistics
- the user only wants raw review tagging with no STP analysis
- the user expects the CLI to ingest raw reviews directly

## Two-Layer Contract

### Agent Layer

The agent layer is the main process. It is responsible for:

- reading every review one by one
- inferring scored items from the full review set
- assigning each item to one of the three core themes:
  - `service_experience`
  - `product_performance`
  - `value_perception`
- attaching theory tags such as Product Positioning, Purchase Motivation, WOM Motivation, System 1 / System 2, and Maslow-related needs
- preserving the original `review_text` so later report evidence can quote the real source text

The agent layer must score every review against every inferred item using the fixed scale below:

- `0`: no relevant meaning appears in the review
- `1-3`: the review mentions the item slightly or indirectly
- `4`: the review is neutral or ambiguous on the item
- `5-6`: the review clearly mentions the item
- `7`: the review strongly and fully expresses the item

Scoring workflow:

1. Read each review one by one.
2. Score each inferred item on the `0-7` scale.
3. Convert qualitative review text into quantitative data.
4. Use the scored output for downstream statistical analysis and research models.

If upstream information is incomplete, the agent layer may produce `MissingDataOutput`.

### Script Layer

The scripts start only after scoring is already complete. Their responsibilities are:

- schema and numeric sanity checks for scored artifacts
- reliability checks
- factor or theme reduction
- clustering for segmentation
- ANOVA / regression for continuous targeting outcomes
- chi-square / logistic regression for binary targeting outcomes
- perceptual-map generation
- ideal-point distance analysis
- pairwise competition-distance analysis
- report assembly with explicit methods, theory labels, and evidence quotes

The scripts do not:

- infer items from raw review text
- define the scoring rubric
- enforce the wording of the scoring process
- rewrite review quotes
- auto-backfill missing scored artifacts

If prerequisites are missing, the scripts return `MissingPrerequisiteOutput`.

## Canonical Input Artifacts

### `review_scoring_table.csv`

Required columns:

- `review_id`
- `unit_id`
- `brand`
- `review_text`

All inferred item columns must:

- appear as separate columns
- use integer scores only
- stay inside the `0-7` range

Optional metadata columns may include:

- `profile_*`
- `channel`
- `rating`

The table is per-review. If no stable person-level identity exists, `unit_id` may default to `review_id`.

### `review_foundation.json`

Required keys for the scripts:

- `dimension_catalog`
- `theme_mapping`
- `people_insights`
- `product_triggers`
- `context_scenarios`
- `system1_system2_split`
- `maslow_keywords`

Optional audit metadata:

- `scoring_rubric`

Each `dimension_catalog` item must include:

- `column`
- `label`
- `theme`
- `theory_tags`
- `stat_roles`
- `plain_language_definition`

`theme_mapping` must cover:

- `service_experience`
- `product_performance`
- `value_perception`

### Auto-Discovered Context Files

- `analysis_context.json`
  - `analysis_goal`
  - `comparison_axes`
  - `scope_limits`
- `brands.json`
- `ideal_point.json`

## Run Modes

- `full`: starts from canonical scored artifacts and emits the three statistical intermediates
- `segmentation`: uses `review_foundation.json + segmentation_variables.csv`
- `targeting`: uses `segment_profiles.json + targeting_dataset.csv`
- `positioning`: uses `positioning_scorecard.csv + brands.json + ideal_point.json`
- `custom`: runs only requested downstream modules

Generated intermediate artifacts in `full` mode:

- `segmentation_variables.csv`
- `targeting_dataset.csv`
- `positioning_scorecard.csv`

## Statistical Rules

### Segmentation

- use `factor_analysis -> K-means`
- rerun when any cluster falls below the `>5%` guardrail
- record `cluster_threshold`, `reruns_performed`, and `final_k`
- retain `System 1 / System 2`, Maslow, cluster share, and consumer-portrait outputs

### Targeting

- resolve current and potential targeting variables from `dimension_catalog.stat_roles`
- allow `analysis_context.comparison_axes` to override the default comparison axes
- use `ANOVA / regression` for continuous outcomes
- use `chi-square / logistic regression` for binary outcomes
- emit `pairwise_comparison_table` when ANOVA significance justifies post-hoc comparison
- emit `priority_segments`, `secondary_segments`, and `deprioritized_segments`

### Positioning

- build the scorecard from `stat_roles` containing `positioning`
- default to `factor_analysis`
- allow `MDS` when similarity-based input is explicitly requested
- include ideal-point distance and pairwise competition distance
- draw the perceptual map as a Python-generated figure from the coordinate table
- treat `perceptual_map_figure + perceptual_map_coordinate_table + perceptual_map_method + perceptual_map_interpretation` as the public positioning-map contract
- allow factor-analysis-only vector and projection diagnostics as optional internal outputs
- never fabricate attribute vectors for `MDS`
- emit `dynamic_scorecard_summary` with distance, gap, reliability, and validity sections

## Report Contract

Each major report section must contain:

- `What this section is doing`
- `Statistical methods used`
- `Theories used`
- `Plain-language explanation`
- `Evidence quotes`

Each major report section must also contain a non-empty `findings` list.

Each finding must contain:

- `finding_id`
- `finding_statement`
- `business_implication`
- `methods_used`
- `theories_used`
- `reproducibility`
- `statistical_results`
- `plain_language_explanation`
- `evidence_quotes`

Each `reproducibility` package must contain:

- `input_artifacts`
- `input_columns`
- `filters`
- `preprocessing`
- `analysis_steps`
- `decision_rule`

Each `statistical_results` package must contain:

- `method_family`
- `test_or_model`
- `sample_size`
- `statistic`
- `degrees_of_freedom`
- `p_value`
- `effect_size`
- `coefficient`
- `confidence_interval`
- `result_direction`

Evidence-quote rules:

- quotes must come verbatim from `review_scoring_table.csv.review_text`
- each quote must include `review_id`
- each quote must explain why it matters
- each quote must link back to the scored items it supports
- when canonical review evidence is available, each major section should include 2-3 quotes
- when canonical review evidence is available, each finding should include at least 1 quote

The goal is to make the report readable for non-specialists while keeping every key claim traceable to real review text and reproducible from the emitted statistical artifacts.

## Hard Rules

- Never blur agent-layer requests with script-layer artifacts.
- Never let scripts consume raw reviews directly.
- Never hardcode a fixed item count into the validator or statistical pipeline.
- Always keep scored items on the fixed `0-7` scale.
- Always preserve verbatim `review_text` for evidence quoting.
- Always state the statistical method and theory used in each major report section.
- Always attach reproducibility steps and statistical results to each finding.
- Never fabricate evidence quotes or attribute vectors.

## References

- [references/01-router-and-gates.md](./references/01-router-and-gates.md)
- [references/02-segmentation.md](./references/02-segmentation.md)
- [references/03-targeting.md](./references/03-targeting.md)
- [references/04-positioning.md](./references/04-positioning.md)
- [references/05-output-contract-and-quality-rules.md](./references/05-output-contract-and-quality-rules.md)
- [references/06-end-to-end-examples.md](./references/06-end-to-end-examples.md)
- [references/07-traceability-evidence-matrix.md](./references/07-traceability-evidence-matrix.md)
- [references/08-verification-scenarios.md](./references/08-verification-scenarios.md)

## Scripts

- Install dependencies: `python -m pip install -r requirements.txt`
- Run analysis: `python scripts/run_review_mining_stp.py --run-mode <mode> --input-dir <artifacts> --output-dir <output>`
- Validate outputs: `python scripts/validate_review_mining_stp.py --run-mode <mode> --output-dir <output>`
- Script boundary: statistical analysis only; raw review intake belongs to the agent layer

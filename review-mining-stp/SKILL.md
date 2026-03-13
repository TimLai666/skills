---
name: review-mining-stp
description: Use when customer reviews, support tickets, app store feedback, or other review-like text must be converted into STP analysis through a review scoring workflow upstream and statistical scripts downstream.
---

# Review Mining STP

## Overview

This skill converts review text into `Segmentation -> Targeting -> Positioning -> Strategy` outputs through a strict workflow contract.

- `review scoring workflow`: reads raw reviews, infers scored items, assigns theory tags, and preserves verbatim review text.
- `scripts`: accept scored artifacts only and perform statistical analysis plus report assembly.

The review scoring workflow is an upstream workflow boundary, not a requirement to use any specific API, service, or orchestration tool.

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

## Workflow Contract

### Review Scoring Workflow

The review scoring workflow is the main process. It is responsible for:

- reading every review one by one
- extracting at least 30 important attributes from the full review set whenever the corpus supports it
- freezing the attribute catalog before formal scoring begins
- inferring scored items from the full review set
- assigning each item to dynamic themes inferred from the full review set
- attaching theory metadata at both family and subtheory level
- keeping a paired salience and valence scoring plan for every inferred attribute
- preserving the original `review_text` so later report evidence can quote the real source text

Theme names and theme count are not fixed. They come from the corpus, not from a hardcoded taxonomy.

The review scoring workflow must score every review against every inferred attribute on two axes:

- `Salience (0-7)`
  - `0`: no relevant meaning appears in the review
  - `1-3`: the review mentions the attribute slightly or indirectly
  - `4`: the review is neutral or ambiguous on how much the attribute matters
  - `5-6`: the review clearly mentions the attribute
  - `7`: the review strongly and fully emphasizes the attribute
- `Valence (0-10)`
  - `0`: strongly negative evaluation
  - `5`: mixed, neutral, or unclear evaluation
  - `10`: strongly positive evaluation
- dependency rule
  - when `salience = 0`, `valence` must stay empty
  - when `salience >= 1`, `valence` must be present

Scoring workflow:

1. Read each review one by one.
2. Run an attribute-discovery pass across the full corpus.
3. Freeze the attribute catalog with definitions, theory annotations, and paired score-column names.
4. Score every review against the frozen attribute catalog with paired `salience + valence`.
5. Convert qualitative review text into quantitative data.
6. Use the scored output for downstream statistical analysis and research models.

If upstream information is incomplete, the review scoring workflow may produce `MissingDataOutput`.

### Scripts

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
- change the attribute catalog during statistical execution
- rewrite review quotes
- auto-backfill missing scored artifacts

If prerequisites are missing, the scripts return `MissingPrerequisiteOutput`.

## Canonical Input Artifacts

### `review_scoring_table.csv`

Required columns:

- `review_id`
- `unit_id`
- `brand`
- `product`
- `review_text`

All inferred attributes must appear as paired columns:

- `<attribute_key>_salience`
- `<attribute_key>_valence`

Each pair must follow these rules:

- `*_salience` uses integer scores only and stays inside the `0-7` range
- `*_valence` uses integer scores only and stays inside the `0-10` range
- when `*_salience = 0`, `*_valence` must be empty
- when `*_salience >= 1`, `*_valence` must be present

Optional metadata columns may include:

- `profile_*`
- `channel`
- `rating`

The table is per-review. If no stable person-level identity exists, `unit_id` may default to `review_id`.

### `review_foundation.json`

Required keys for the scripts:

- `dimension_catalog`
- `theme_mapping`
- `attribute_extraction_summary`
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
- `attribute_group`
- `salience_column`
- `valence_column`
- `stat_roles`
- `plain_language_definition`
- `theory_annotations`

`attribute_group` must use one of:

- `attribute_function`
- `benefit_use`
- `brand_personality`
- `brand_image`

Legacy compatibility is allowed through:

- `theory_tags`

`theme_mapping` must cover:

- every `dimension_catalog` column exactly once
- only valid `dimension_catalog` columns
- the same theme name recorded in each item's `theme`

`theory_annotations` should map each scored item to theory family plus subtheory, for example:

- `product_positioning`
- `purchase_motivation`
- `wom_motivation`
- `dual_process`
- `maslow`

`attribute_extraction_summary` must record:

- `target_minimum`
- `actual_count`
- `shortfall_reason`

### `attribute_catalog.csv`

Required columns:

- `attribute_key`
- `label`
- `theme`
- `attribute_group`
- `definition`
- `source_type`
- `mention_count`
- `salience_column`
- `valence_column`
- `example_review_id`
- `example_quote`

The catalog is the script-facing bridge from upstream attribute extraction into downstream statistics and report evidence.

### Auto-Discovered Context Files

- `analysis_context.json`
  - `analysis_goal`
  - `comparison_axes`
  - `scope_limits`
- `brands.json`
- `ideal_point.json`

## Run Modes

- `full`: starts from canonical scored artifacts and emits the three statistical intermediates
- `full` canonical input requires `review_scoring_table.csv + review_foundation.json + attribute_catalog.csv + analysis_context.json + brands.json + ideal_point.json`
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

- standardize `salience` and `valence` columns separately, then model them together
- use `factor_analysis -> K-means`
- rerun when any cluster falls below the `>5%` guardrail
- record `cluster_threshold`, `reruns_performed`, and `final_k`
- retain `System 1 / System 2`, Maslow, cluster share, and consumer-portrait outputs

### Targeting

- resolve current and potential targeting variables from `dimension_catalog.stat_roles`
- allow `analysis_context.comparison_axes` to override the default comparison axes
- model both `salience` and `valence` columns as candidate drivers
- use `ANOVA / regression` for continuous outcomes
- use `chi-square / logistic regression` for binary outcomes
- emit `pairwise_comparison_table` when ANOVA significance justifies post-hoc comparison
- emit `priority_segments`, `secondary_segments`, and `deprioritized_segments`

### Positioning

- build the scorecard from `stat_roles` containing `positioning`
- combine paired `salience` and `valence` features into the perceptual-map feature matrix
- default to `factor_analysis`
- allow `MDS` when similarity-based input is explicitly requested
- include ideal-point distance and pairwise competition distance
- draw the perceptual map as a Python-generated figure from the coordinate table
- treat `perceptual_map_figure + perceptual_map_coordinate_table + perceptual_map_method + perceptual_map_interpretation` as the public positioning-map contract
- allow factor-analysis-only vector and projection diagnostics as optional internal outputs
- never fabricate attribute vectors for `MDS`
- emit `dynamic_scorecard_summary` with distance, gap, reliability, and validity sections

## Report Contract

The final report must contain an `Attribute Extraction Summary` that shows:

- `target_minimum`
- `actual_count`
- `shortfall_reason`
- discovered themes
- attribute-group counts
- representative attributes with real example quotes

Each major report section must contain:

- `What this section is doing`
- `Axis modeling summary`
- `Statistical methods used`
- `Theories used`
- `Theme coverage summary`
- `Theory coverage summary`
- `Plain-language explanation`
- `Evidence quotes`

Each major report section must also contain a non-empty `findings` list.

Each finding must contain:

- `finding_id`
- `finding_statement`
- `business_implication`
- `axes_used`
- `methods_used`
- `theories_used`
- `themes_used`
- `subtheories_used`
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
- `axis_breakdown`

Evidence-quote rules:

- quotes must come verbatim from `review_scoring_table.csv.review_text`
- each quote must include `review_id`
- each quote must explain why it matters
- each quote must link back to the scored items it supports
- when canonical review evidence is available, each major section should include 2-3 quotes
- when canonical review evidence is available, each finding should include at least 1 quote

The goal is to make the report readable for non-specialists while keeping every key claim traceable to real review text and reproducible from the emitted statistical artifacts.

The final report should visibly show:

- the dynamically inferred themes for this corpus
- which findings use which themes
- theory families plus subtheories
- which subtheories are `not_evidenced` in the current dataset

## Hard Rules

- Never blur review-scoring inputs with script-ready artifacts.
- Never let scripts consume raw reviews directly.
- Never hardcode a fixed item count into the validator or statistical pipeline.
- Always use `product` as the product field name.
- Always keep scoring on the paired `salience 0-7` and `valence 0-10` scales.
- Always preserve verbatim `review_text` for evidence quoting.
- Always state the statistical method and theory used in each major report section.
- Always show how `salience` and `valence` were modeled in each major report section.
- Always show dynamic theme coverage and theory coverage in the report body.
- Always show the attribute-extraction summary and representative attributes in the report body.
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
- Script boundary: statistical analysis only; raw reviews must first be converted into scored artifacts during the review scoring workflow

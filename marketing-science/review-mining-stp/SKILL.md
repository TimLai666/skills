---
name: review-mining-stp
description: Use when customer reviews, support tickets, app store feedback, or other review-like text must be converted into STP analysis with AI-assisted scoring upstream and statistical scripts downstream.
---

# Review Mining STP

## Overview

This skill turns review text into `Segmentation -> Targeting -> Positioning -> Strategy` outputs through a strict two-layer contract.

- `agent layer`: reads raw reviews, infers scored items, applies theory tags, and preserves verbatim review text.
- `script layer`: accepts scored artifacts only and runs the downstream statistics plus the final evidence-backed report.

The scripts do not perform raw-review NLP. Their job is quantitative analysis and reporting after the agent has already converted text into structured scores.

## When To Use

Use this skill when:

- you need STP outputs from reviews, comments, or feedback text
- you need a repeatable scored-artifact contract before running statistics
- you need segmentation, targeting, or positioning outputs with explicit methods and theory labels
- you need report sections backed by verbatim review quotes, not unsupported interpretation

Do not use this skill when:

- the task is only qualitative summarization with no scoring and no downstream statistics
- the user only wants raw review tagging with no STP analysis
- the user expects the CLI to ingest raw reviews directly

## Two-Layer Contract

### Agent Layer

The agent layer is responsible for:

- reading every review one by one
- inferring scored items from the full review set
- assigning each item to one of the three themes:
  - `service_experience`
  - `product_performance`
  - `value_perception`
- attaching theory tags such as Product Positioning, Purchase Motivation, WOM Motivation, System 1 / System 2, and Maslow-related needs
- preserving the original `review_text` so later report evidence can quote the real source text

The agent layer must score every review against every inferred item using the fixed 0–7 rubric below:

- `0`: 評論中未出現與該題項相關的語意
- `1–3`: 輕微或間接提及
- `4`: 中立或模糊表達
- `5–6`: 明確提及
- `7`: 評論中強烈且完整表達該構面

Scoring process:

1. 每則評論需逐條分析。
2. 根據語意關聯程度對每個歸納題項進行 0–7 分評分。
3. 將質性評論文本轉換為量化數據。
4. 所得評分可用於後續統計分析與研究模型建立。

If upstream information is incomplete, the agent layer may produce `MissingDataOutput`.

### Script Layer

The scripts start from scored artifacts and do the quantitative work:

- reliability checks
- factor or theme reduction
- clustering for segmentation
- ANOVA / regression for continuous targeting outcomes
- chi-square / logistic regression for binary targeting outcomes
- perceptual-map generation
- ideal-point distance analysis
- pairwise competition-distance analysis

The scripts do not:

- infer items from raw review text
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
- stay inside the `0–7` range

Optional metadata columns may include:

- `profile_*`
- `channel`
- `rating`

The table is per-review. If no stable person-level identity exists, `unit_id` may default to `review_id`.

### `review_foundation.json`

Required keys:

- `scoring_rubric`
- `dimension_catalog`
- `theme_mapping`
- `people_insights`
- `product_triggers`
- `context_scenarios`
- `system1_system2_split`
- `maslow_keywords`

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
- never fabricate attribute vectors for `MDS`
- emit `dynamic_scorecard_summary` with distance, gap, reliability, and validity sections

## Report Contract

Each major report section must contain:

- `What this section is doing`
- `Statistical methods used`
- `Theories used`
- `Plain-language explanation`
- `Evidence quotes`

Evidence-quote rules:

- quotes must come verbatim from `review_scoring_table.csv.review_text`
- each quote must include `review_id`
- each quote must explain why it matters
- each quote must link back to the scored items it supports
- when canonical review evidence is available, each major section should include 2–3 quotes

The point is to make the report readable for non-specialists while keeping every key claim traceable to real review text.

## Hard Rules

- Never blur agent-layer requests with script-layer artifacts.
- Never let scripts consume raw reviews directly.
- Never hardcode a fixed item count into the validator or statistical pipeline.
- Always keep scored items on the fixed 0–7 rubric.
- Always preserve verbatim `review_text` for evidence quoting.
- Always state the statistical method and theory used in each major report section.
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

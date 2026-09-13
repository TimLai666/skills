# Router And Gates

## Purpose

This reference defines what belongs to the review scoring workflow, what belongs to the scripts, and which artifacts each run mode requires.

## Workflow Boundary

### Review Scoring Workflow

The review scoring workflow handles:

- raw `reviews` or `review_text`
- extracting or curating the corpus-level attribute catalog
- freezing that catalog before formal scoring starts
- inferring scored items from the full corpus
- applying paired `salience` and `quality` scoring to every inferred attribute for every review
- assigning dynamic `theme` names inferred from the corpus
- assigning `theory_annotations` and `stat_roles`
- preserving verbatim review text for later evidence quoting

The review scoring workflow emits the scored artifacts that the scripts need.
It is a workflow boundary, not a requirement to use a specific API.

### Scripts

The scripts accept scored artifacts only.

Canonical input:

- `review_scoring_table.csv`
- `review_foundation.json`
- `attribute_catalog.csv`
- `analysis_context.json`
- `brands.json`
- `ideal_point.json`

The scripts may emit:

- `segmentation_variables.csv`
- `targeting_dataset.csv`
- `positioning_scorecard.csv`

They do not accept raw reviews and they do not define the scoring workflow.
They also do not modify the frozen attribute catalog while statistics are running.

## Canonical Input Rules

### `review_scoring_table.csv`

Must be per-review and must include:

- `review_id`
- `unit_id`
- `brand`
- `product`
- `review_text`

All scored attributes must:

- exist in `dimension_catalog`
- exist as paired `*_salience` and `*_quality` columns
- keep `*_salience` as numeric integers inside `0-7`
- keep non-empty `*_quality` as numeric integers inside `0-10`
- keep `*_quality` empty when `*_salience = 0`
- allow empty `*_quality` when `*_salience >= 1` if the review gives no evaluation

The scored item count is dynamic. The contract never assumes a fixed item count.

`unit_id` may default to `review_id` when no stable person-level identity exists. Optional metadata includes `profile_*`, `channel`, and `rating`. Keep the `product` field name.

A blank quality cell means no evaluation, not a score of 0 or 5. Quality aggregation uses only non-empty evaluations. `positioning_scorecard.csv` retains `mention_count` and `evaluation_count` separately for each brand and attribute. Unit-level intermediates retain `<attribute_key>_mention_count` and `<attribute_key>_evaluation_count`. A group with no evaluations has an empty quality mean.

### `review_foundation.json`

Must include:

- `dimension_catalog`
- `theme_mapping`
- `attribute_extraction_summary`

It may also include audit-only metadata such as:

- `scoring_rubric`

Each `dimension_catalog` item must include:

- `column`
- `label`
- `theme`
- `attribute_group`
- `salience_column`
- `quality_column`
- `stat_roles`
- `plain_language_definition`
- `theory_annotations`

`attribute_group` is one of `attribute_function`, `benefit_use`, `brand_personality`, or `brand_image`.

Each item needs applicable family and subtheory pairs in `theory_annotations`. Four default families and the `theory_extensions` registration format are defined in [attribute discovery and theories](09-attribute-discovery-and-theories.md).

`attribute_extraction_summary` records `target_minimum`, `actual_count`, `shortfall_reason`, and `theory_gap`. The target is 30 when the corpus supports that many distinct attributes. Record absent default families in `theory_gap`; absence is a finding, not a requirement to invent attributes.

`theory_gap` is a list of the default family keys absent from `dimension_catalog.theory_annotations`. Canonical input validation derives this list when omitted and checks a supplied list against the annotations. The report always includes the list.

Retain available `people_insights`, `product_triggers`, `context_scenarios`, `system1_system2_split`, and `maslow_keywords` for segmentation interpretation. Missing evidence must remain identified as missing.

Legacy compatibility is allowed through:

- `theory_tags`

`theme_mapping` must:

- contain at least one theme
- keep a non-empty column list for each theme
- reference only columns present in `dimension_catalog`
- cover every `dimension_catalog` column exactly once
- match the `theme` value stored on each `dimension_catalog` item

### `attribute_catalog.csv`

Must include:

- `attribute_key`
- `label`
- `theme`
- `attribute_group`
- `definition`
- `source_type`
- `mention_count`
- `salience_column`
- `quality_column`
- `example_review_id`
- `example_quote`

The scoring workflow also records `theory_families` and `theory_subtheories` as comma-separated lists, aligned with `dimension_catalog.theory_annotations`.

Rules:

- it must align one-to-one with `dimension_catalog`
- `example_quote` must stay verbatim so downstream evidence is auditable
- if fewer than `30` attributes are extracted, `attribute_extraction_summary.shortfall_reason` must explain why

### Context Files

- `analysis_context.json`: `analysis_goal`, `comparison_axes`, `scope_limits`.
- `brands.json`: `brands` is a flat list of brand-name strings. `similarity_matrix` is used for `--positioning-method mds`.
- `ideal_point.json`: `label` and `attributes`. Each attribute value is a scalar or an object such as `{"salience": 4, "quality": 8}`. Only attribute keys that overlap with the positioning scorecard are used. Positioning requires at least two complete feature columns, counting salience and quality separately.

The full runner derives brand-level quality from per-review scores and emits it as `quality` rows in `positioning_scorecard.csv`. Do not prepare a separate manually judged product-quality matrix.

## Run Modes

- `full`
  - starts from canonical scored input
  - emits all three statistical intermediates
- `segmentation`
  - requires `review_foundation.json + segmentation_variables.csv`
- `targeting`
  - requires `targeting_dataset.csv + segment_profiles.json`
- `positioning`
  - requires `positioning_scorecard.csv + brands.json + ideal_point.json`
- `custom`
  - runs only requested downstream modules

## Missing Outputs

### `MissingDataOutput`

Review-scoring-workflow artifact used when the user has not provided enough upstream context to build scored artifacts.

### `MissingPrerequisiteOutput`

Script artifact used when required scored artifacts or intermediate statistical artifacts are missing.

Expected shape:

```json
{
  "requested_stage": "",
  "requested_modules": [],
  "missing_prerequisites": [],
  "acceptable_upstream_artifacts": [],
  "available_artifacts": [],
  "auto_backfill_allowed": false,
  "next_step_rule": "Scripts accept scored artifacts only; run the review scoring workflow to build the missing files before rerunning."
}
```

Rules:

- `missing_prerequisites` must list only truly missing files
- `acceptable_upstream_artifacts` should mirror the missing files
- `auto_backfill_allowed` must stay `false`
- when canonical scored input is missing, `next_step_rule` must point back to the review scoring workflow

## Execution Scope Summary

Every completed run must record:

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

## Reporting Gate

Scripts assemble the report structure from scored artifacts. Required stage and finding fields are defined once in [Output Contract And Quality Rules](05-output-contract-and-quality-rules.md). The scoring workflow supplies the scores, metadata, and unchanged review text that support those fields.

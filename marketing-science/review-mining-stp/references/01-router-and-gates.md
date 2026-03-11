# Router And Gates

## Purpose

This reference defines what belongs to the agent layer, what belongs to the script layer, and which artifacts each run mode requires.

## Layer Boundary

### Agent Layer

The agent layer handles:

- raw `reviews` or `review_text`
- inferring scored items from the full corpus
- applying the `0-7` scoring scale to every inferred item for every review
- assigning `theme`, `theory_tags`, and `stat_roles`
- preserving verbatim review text for later evidence quoting

The agent layer emits the scored artifacts that the scripts need.
It is a workflow boundary, not a requirement to use a specific API.

### Script Layer

The scripts accept scored artifacts only.

Canonical input:

- `review_scoring_table.csv`
- `review_foundation.json`
- `analysis_context.json`
- `brands.json`
- `ideal_point.json`

The scripts may emit:

- `segmentation_variables.csv`
- `targeting_dataset.csv`
- `positioning_scorecard.csv`

They do not accept raw reviews and they do not define the scoring workflow.

## Canonical Input Rules

### `review_scoring_table.csv`

Must be per-review and must include:

- `review_id`
- `unit_id`
- `brand`
- `review_text`

All scored item columns must:

- exist in `dimension_catalog`
- be numeric integers
- stay in the `0-7` range

The scored item count is dynamic. The contract never assumes a fixed item count.

### `review_foundation.json`

Must include:

- `dimension_catalog`
- `theme_mapping`

It may also include audit-only metadata such as:

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

Agent-layer artifact used when the user has not provided enough upstream context to build scored artifacts.

### `MissingPrerequisiteOutput`

Script-layer artifact used when required scored artifacts or intermediate statistical artifacts are missing.

Expected shape:

```json
{
  "requested_stage": "",
  "requested_modules": [],
  "missing_prerequisites": [],
  "acceptable_upstream_artifacts": [],
  "available_artifacts": [],
  "auto_backfill_allowed": false,
  "next_step_rule": "Scripts accept scored artifacts only; use the agent layer to build the missing files before rerunning."
}
```

Rules:

- `missing_prerequisites` must list only truly missing files
- `acceptable_upstream_artifacts` should mirror the missing files
- `auto_backfill_allowed` must stay `false`
- when canonical scored input is missing, `next_step_rule` must point back to agent-layer preprocessing

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

Each stage summary must keep:

- section-level `methods_used`, `theories_used`, `plain_language_explanation`, and `evidence_quotes`
- a non-empty `findings` list

Each finding must keep:

- `finding_id`
- `finding_statement`
- `business_implication`
- `methods_used`
- `theories_used`
- `reproducibility`
- `statistical_results`
- `plain_language_explanation`
- `evidence_quotes`

The scripts are responsible for assembling this reporting structure from scored artifacts. The agent layer is responsible for the upstream scoring workflow only.

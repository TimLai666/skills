---
name: review-mining-stp
description: >-
  This skill MUST be used when customer reviews, support tickets, app store
  feedback, or other review-like text must be converted into STP analysis
  through a review scoring workflow upstream and statistical scripts
  downstream.
metadata:
  version: "1.2.0"
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

## Theory Framework

Attribute extraction and theory annotation should draw from these four theory families. Additional families may be added when the corpus clearly warrants it, but every attribute must map to at least one family.

### 1. Product Positioning Theory (`product_positioning`)

Subtheories:
- `attributes` — physical or verifiable product properties (e.g. ANSI certification, lens material, weight)
- `functions` — what the product does in use (e.g. anti-fog, side coverage, UV blocking)
- `benefits` — perceived value or outcome the customer gains (e.g. confidence, style, value for money)
- `usage_context_service_experience` — context of use, service touchpoints, post-purchase experience

### 2. Maslow's Hierarchy of Needs (`maslow`)

Subtheories:
- `physiological` — sensory comfort, physical ease, visual clarity during use
- `safety` — protection from harm, certification compliance, structural durability
- `social` — fitting into a community, sports group, or professional identity
- `esteem` — status signalling, brand prestige, professional image display
- `self_actualization` — enabling personal performance goals, empowerment, achievement

### 3. Purchase Motivation Theory (`purchase_motivation`)

Subtheories:
- `functional` — driven by performance, fit, ergonomics, multi-scenario utility
- `security` — driven by safety standards, brand trust, durability assurance, after-sales protection
- `relational` — driven by customer service quality, gifting intent, repeat purchase loyalty

### 4. Word-of-Mouth Motivation Theory (`wom_motivation`)

Subtheories:
- `altruistic` — sharing to genuinely help other buyers (tips, warnings, balanced reviews)
- `social_identity` — sharing to signal group membership (sports community, professional role)
- `self_enhancement` — sharing to display expertise or superior knowledge
- `emotional_expression` — sharing driven by strong positive or negative emotion

## Attribute Extraction Rules

When extracting attributes from the full corpus:

- Extract at least 30 attributes whenever the corpus supports it.
- Every attribute must be mappable to at least one of the four theory families above.
- Each attribute must carry `theory_annotations` listing all applicable family + subtheory pairs.
- Attribute themes are dynamically inferred from the corpus — do not hardcode theme names.
- Freeze the attribute catalog before formal scoring begins.
- Attributes must cover all four theory families. If any family has zero coverage, flag it in `attribute_extraction_summary.theory_gap`.

## Attribute Discovery Pass — How To Execute

The discovery pass is a dedicated read-through of the full corpus before any scoring begins. Its sole output is the frozen attribute catalog. Execute it in four stages:

### Stage 1 — Read all reviews and collect raw signals

Read every review in the corpus. For each review, note any concern, praise, complaint, or observation the reviewer expresses about the product or their experience. Do not score yet. Collect these as raw signals in a working list. Signals can be short phrases or paraphrases — they do not need to be final attribute names yet.

Examples of raw signals:
- "fogged up immediately with mask on"
- "arms hooked in my hair every time I removed them"
- "military-grade, Z87 certified"
- "bought three pairs over two years"
- "bought these as a gift for my son"

### Stage 2 — Cluster signals into candidate attributes

Group raw signals that represent the same underlying customer concern or product dimension. Each cluster becomes one candidate attribute. Apply these rules:

- One attribute per distinct construct. Do not merge two different concerns just because they co-occur (e.g. "fogging" and "scratching" are separate attributes even if one reviewer mentions both).
- Split an attribute if reviewers clearly treat it as two separate things (e.g. "nose pad comfort" and "nose pad staying in place" may warrant two attributes if complaints differ).
- Name each attribute with a short noun phrase that a non-specialist can understand. Use the language reviewers actually use, not academic terminology.
- Count how many reviews contributed signals to each cluster — this becomes `mention_count`.

### Stage 3 — Map every attribute to the four theory frameworks

For each candidate attribute, assign `theory_annotations` by working through all four theory families in order:

**product_positioning** — ask: does this attribute describe a physical property (`attributes`), a functional capability (`functions`), a perceived benefit or outcome (`benefits`), or a usage context / service touchpoint (`usage_context_service_experience`)? Assign all that apply.

**maslow** — ask: which need does concern about this attribute reflect?
- `physiological`: physical sensation, visual comfort, weight, pressure on face
- `safety`: protection level, certification, structural durability, after-sales security
- `social`: fitting into a community, professional group, sport team
- `esteem`: brand status, professional image, visible identity
- `self_actualization`: enabling personal goals, performance achievement, empowerment

**purchase_motivation** — ask: what drives someone to care about this at the point of purchase?
- `functional`: performance, fit, ergonomics, multi-use utility
- `security`: standards compliance, brand trust, warranty, durability assurance
- `relational`: customer service, gifting intent, loyalty and repeat purchase

**wom_motivation** — ask: why would a reviewer write about this attribute?
- `altruistic`: to warn or help other buyers
- `social_identity`: to signal membership in a group (sport, profession, military)
- `self_enhancement`: to display expertise or superior product knowledge
- `emotional_expression`: because strong feeling (delight or frustration) compels them to write

An attribute may carry multiple families and multiple subtheories. There is no maximum. However, every attribute must carry at least one family, and the full catalog must cover all four families.

### Stage 4 — Freeze and validate the catalog

Before scoring begins:

1. Confirm the attribute count meets the `target_minimum` (at least 30 when corpus supports it).
2. Confirm all four theory families appear at least once across the catalog. If any family is absent, revisit Stage 2 — missing coverage usually means signals were merged incorrectly or a whole class of reviewer concerns was overlooked.
3. Assign a stable `attribute_key` to each attribute (snake_case, e.g. `anti_fog_performance`, `hinge_durability`). Keys must not change after freezing.
4. Write the `plain_language_definition` for each attribute — one sentence describing what the attribute measures and what a high vs low signal looks like in a review.
5. Select one `example_review_id` and `example_quote` per attribute from the raw corpus. The quote must be verbatim.
6. Record the frozen catalog in `attribute_catalog.csv` and `review_foundation.json -> dimension_catalog` before any scoring row is written.

No attribute may be added, removed, or renamed after the catalog is frozen. If a gap is found during scoring, record it in `attribute_extraction_summary.shortfall_reason` and complete scoring with the frozen catalog as-is.

## Workflow Contract

### Review Scoring Workflow

The review scoring workflow is the main process. It is responsible for:

- reading every review one by one
- extracting at least 30 important attributes from the full review set whenever the corpus supports it
- freezing the attribute catalog before formal scoring begins
- inferring scored items from the full review set
- assigning each item to dynamic themes inferred from the full review set
- attaching theory metadata at both family and subtheory level — exclusively from the four permitted families
- keeping a paired salience and product-quality scoring plan for every inferred attribute
- preserving the original `review_text` so later report evidence can quote the real source text

Theme names and theme count are not fixed. They come from the corpus, not from a hardcoded taxonomy.

### Two Scoring Axes

This skill uses two distinct scoring axes applied to different units of analysis:

#### Axis A — Customer × Attribute: Salience (0–7)

Applied per review (or per customer). Measures how prominently the attribute features in a given review.

- `0`: the attribute is absent from the review — no relevant content at all
- `1–3`: the attribute is mentioned slightly or indirectly
- `4`: the review is neutral, ambiguous, or tangential on this attribute
- `5–6`: the review clearly and explicitly addresses this attribute
- `7`: the review strongly emphasises this attribute as a central concern

Dependency rule: when `salience = 0`, the attribute is treated as absent for this review and must not be included in any per-review analysis. Only reviews with `salience ≥ 1` are counted as mentioning the attribute.

#### Axis B — Quality Score (0–10)

**Scored per review, reported per product.** Score each review's evaluation of the attribute, then let the scripts aggregate those scores into the product-level figure. Do not skip the per-review step and judge the product directly — a product-level number with no per-review scores behind it cannot be traced to any review, and this skill's whole evidence contract depends on being able to trace it.

Per review, the score measures how well that reviewer judged the product to perform on this attribute:

- `0`: outright failure — this reviewer says the attribute did not work at all
- `1–3`: poor — clear complaint, the problem outweighs anything positive they say about it
- `4`: leaning negative — reservations dominate, but they concede something
- `5`: mixed or neutral — praise and complaint roughly balance, or the reviewer is genuinely undecided
- `6–7`: decent — satisfied overall, with a caveat they bothered to write down
- `8–9`: strong — clearly satisfied, at most a minor nitpick
- `10`: exceptional — unreserved praise on this attribute

The wording is about one reviewer's verdict, not a tally across reviewers. Counting across reviewers happens in aggregation.

Leave the cell empty when `salience = 0`. A reviewer who never raised the attribute has no opinion on it, and averaging in a default would drag every product toward the middle.

**Aggregation is the scripts' job, not yours.** `build_positioning_scorecard` averages the per-review quality scores across the reviews that actually mentioned the attribute (`salience >= 1`), per brand. The product-level figure is therefore always derived, always reproducible, and always traceable back to the exact reviews that produced it.

Column naming, both per review in `review_scoring_table.csv`:
- Salience: `<attribute_key>_salience`
- Quality: `<attribute_key>_quality`

### Scoring Workflow Steps

1. Read each review one by one.
2. Run an attribute-discovery pass across the full corpus.
3. Freeze the attribute catalog with definitions, theory annotations (from the four permitted families only), and paired score-column names.
4. Score every review against the frozen attribute catalog on **both** axes: Axis A (salience 0–7) and Axis B (quality 0–10, left empty wherever salience is 0).
5. Stop there. The product-level quality figure is aggregated by the scripts from these per-review scores — do not judge products directly.
6. Convert qualitative review text into quantitative data on both axes.
7. Use the scored output for downstream statistical analysis and research models.

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

All inferred attributes must appear as salience columns (Axis A, per review):

- `<attribute_key>_salience`

Each salience column must follow these rules:

- integer scores only, range `0–7`
- `0` means the attribute is absent from this review

Optional metadata columns may include:

- `profile_*`
- `channel`
- `rating`

The table is per-review. If no stable person-level identity exists, `unit_id` may default to `review_id`.

### Product-level quality — derived, not supplied

There is no product × attribute file to prepare. The runner computes the product-level quality matrix from `review_scoring_table.csv` and emits it as the `quality` rows of `positioning_scorecard.csv`, one row per brand × attribute.

Supply the per-review scores and the aggregate follows. Anything you hand-write at product level would be an unauditable second opinion competing with the derived figure.

> **Column label note.** `dimension_catalog` still declares the Axis B column under the field name `valence_column`, and `positioning_scorecard.csv` still labels the aggregated axis `valence`. Those are the internal field and axis names; the data column itself follows the `<attribute_key>_quality` convention. The internal labels are stale but harmless — do not rename them without updating `io.py`, `positioning.py` and `reporting.py` together.

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

`theory_annotations` must map each scored item to at least one theory family plus subtheory. The four default families for this skill are:

- `product_positioning` (subtheories: `attributes`, `functions`, `benefits`, `usage_context_service_experience`)
- `maslow` (subtheories: `physiological`, `safety`, `social`, `esteem`, `self_actualization`)
- `purchase_motivation` (subtheories: `functional`, `security`, `relational`)
- `wom_motivation` (subtheories: `altruistic`, `social_identity`, `self_enhancement`, `emotional_expression`)

Additional theory families may be used when the corpus clearly calls for them. Any added family must be documented in `review_foundation.json` with its name, rationale, and subtheory list.

`attribute_extraction_summary` must record:

- `target_minimum`
- `actual_count`
- `shortfall_reason`
- `theory_gap` — list any of the four theory families with zero attribute coverage

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
- `theory_families` — comma-separated list of applicable theory families from the four permitted
- `theory_subtheories` — comma-separated list of applicable subtheories

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
- `full` canonical input requires `review_scoring_table.csv + review_foundation.json + attribute_catalog.csv + analysis_context.json + brands.json + ideal_point.json` — this list matches what `router.py` enforces. There is no product-level file to supply; the quality matrix is derived from the per-review scores
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

- standardize `salience` columns (Axis A) across reviews to identify customer concern patterns
- use `factor_analysis -> K-means`
- rerun when any cluster falls below the `>5%` guardrail
- record `cluster_threshold`, `reruns_performed`, and `final_k`
- retain `System 1 / System 2`, Maslow, cluster share, and consumer-portrait outputs

### Targeting

- resolve current and potential targeting variables from `dimension_catalog.stat_roles`
- allow `analysis_context.comparison_axes` to override the default comparison axes
- model `salience` columns (Axis A) as customer-side drivers
- model `quality` columns (Axis B) as product-side performance indicators
- use `ANOVA / regression` for continuous outcomes
- use `chi-square / logistic regression` for binary outcomes
- emit `pairwise_comparison_table` when ANOVA significance justifies post-hoc comparison
- emit `priority_segments`, `secondary_segments`, and `deprioritized_segments`

### Positioning

- build the scorecard from `stat_roles` containing `positioning`
- use the aggregated `quality` scores (Axis B) from `positioning_scorecard.csv` as the primary product positioning features
- cross-reference with `salience` columns (Axis A) to weight attributes by customer concern level
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
- `theory_gap` — any of the four theory families with zero coverage
- discovered themes
- attribute-group counts
- theory family and subtheory coverage breakdown
- representative attributes with real example quotes

Each major report section must contain:

- `What this section is doing`
- `Axis modeling summary` — specify whether Axis A (salience), Axis B (quality), or both are used
- `Statistical methods used`
- `Theories used` — must name specific families and subtheories from the four permitted
- `Theme coverage summary`
- `Theory coverage summary`
- `Plain-language explanation`
- `Evidence quotes`

Each major report section must also contain a non-empty `findings` list.

Each finding must contain:

- `finding_id`
- `finding_statement`
- `business_implication`
- `axes_used` — `salience`, `quality`, or both
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
- theory families plus subtheories — drawn exclusively from the four permitted families
- which subtheories are `not_evidenced` in the current dataset

## Hard Rules

- Never blur review-scoring inputs with script-ready artifacts.
- Never let scripts consume raw reviews directly.
- Never hardcode a fixed item count into the validator or statistical pipeline.
- Always use `product` as the product field name.
- Axis A scoring (customer × attribute): always use `salience 0–7`.
- Axis B scoring (product × attribute): always use `quality 0–10`.
- Never use `valence` as a column name — it is replaced by `quality` in this skill.
- Always preserve verbatim `review_text` for evidence quoting.
- Always state the statistical method and theory used in each major report section.
- Always show how Axis A and Axis B were modeled in each major report section.
- Always show dynamic theme coverage and theory coverage in the report body.
- Always show the attribute-extraction summary and representative attributes in the report body.
- Always attach reproducibility steps and statistical results to each finding.
- Never fabricate evidence quotes or attribute vectors.
- Theory annotations default to the four built-in families: `product_positioning`, `maslow`, `purchase_motivation`, `wom_motivation`. Additional families may be introduced when the corpus clearly warrants it, provided they are documented with name, rationale, and subtheory list in `review_foundation.json`.
- Every attribute must be covered by at least one theory family. Attributes with no theory mapping must be flagged and reconsidered.

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
- Run analysis: `python scripts/run_review_mining_stp.py --run-mode <mode> --input-dir <artifacts> --output-dir <o>`
- Validate outputs: `python scripts/validate_review_mining_stp.py --run-mode <mode> --output-dir <o>`
- Script boundary: statistical analysis only; raw reviews must first be converted into scored artifacts during the review scoring workflow

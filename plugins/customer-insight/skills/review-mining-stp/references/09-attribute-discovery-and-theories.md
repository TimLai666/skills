# Attribute Discovery And Theory Annotation

## Read the Corpus Before Scoring

Read every review and collect concerns, praise, complaints, observations, and usage contexts. Group signals into distinct attributes. Split two concerns when the reviews distinguish them, not to reach a target count. Count contributing reviews as `mention_count`.

For each attribute, record a stable snake_case `attribute_key`, plain-language definition, applicable theory annotations, paired score-column names, and a verbatim `example_quote` with `example_review_id`. Freeze the catalog in `attribute_catalog.csv` and `review_foundation.json.dimension_catalog` before scoring. Record later discoveries as limitations without changing that run's catalog.

Use `target_minimum = 30` when the corpus supports at least 30 distinct attributes. If fewer are supported, keep the supported set and explain `shortfall_reason`. Check every default theory family for relevant evidence; record absent families in `theory_gap`. Missing coverage does not require another attribute or an inferred motive.

## Default Theory Families

Assign all applicable family/subtheory pairs that the review evidence supports. Each attribute needs at least one appropriate family. Reconsider an unmapped attribute's definition or document an appropriate extension. Do not infer a reviewer's motive merely because that motive is in the dictionary.

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

## Extension Families

When a corpus needs another theory, register it in `review_foundation.json.theory_extensions` before using it in `dimension_catalog.theory_annotations`:

```json
{
  "theory_extensions": {
    "expectation_confirmation": {
      "rationale": "Use when reviews explicitly compare experienced performance with prior expectations.",
      "subtheories": ["confirmation", "disconfirmation"]
    }
  }
}
```

This is an illustrative registration, not a required theory. Use the registered family key and subtheory names consistently in the catalog and reports. Built-in `dual_process` annotations remain available for existing System 1 / System 2 metadata. An added family must have its own rationale and non-empty subtheory list, and must not replace an existing family definition.

`attribute_catalog.csv.theory_families` and `theory_subtheories` contain comma-separated applicable names. The structured `dimension_catalog.theory_annotations` keeps the family/subtheory pairing. Reports distinguish supported annotations from default families and subtheories with no evidence.

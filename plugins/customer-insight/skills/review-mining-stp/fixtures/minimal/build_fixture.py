#!/usr/bin/env python3
"""Regenerate the minimal canonical-input fixture.

The fixture exists so a change to the runner can be verified: run `full` mode
before the change, run it again after, diff the outputs. Everything except the
intended difference should be byte-identical.

Three brands, five attributes, twenty reviews — the smallest shape that still
satisfies every contract check (>=3 dimensions, >=2 positioning attributes,
all four theory families covered, every brand scored on every attribute).

Usage:  python3 build_fixture.py
"""

from __future__ import annotations

import csv
import json
from pathlib import Path

HERE = Path(__file__).parent

ATTRIBUTES = [
    {
        "key": "anti_fog",
        "label": "Anti-fog performance",
        "theme": "protection",
        "attribute_group": "attribute_function",
        "definition": "Whether the lens stays clear during use, especially with a mask on.",
        "stat_roles": ["segmentation", "positioning", "comparison_axis"],
        "plain_language_definition": "Does it fog up while you work?",
        "theory_annotations": {
            "product_positioning": ["functions"],
            "maslow": ["physiological"],
            "purchase_motivation": ["functional"],
        },
    },
    {
        "key": "impact_protection",
        "label": "Impact protection",
        "theme": "protection",
        "attribute_group": "attribute_function",
        "definition": "Certified resistance to flying debris and impact.",
        "stat_roles": ["segmentation", "positioning", "current_target"],
        "plain_language_definition": "Will it actually stop something hitting your eye?",
        "theory_annotations": {
            "product_positioning": ["attributes"],
            "maslow": ["safety"],
            "purchase_motivation": ["security"],
        },
    },
    {
        "key": "comfort_fit",
        "label": "Comfort and fit",
        "theme": "wearability",
        "attribute_group": "benefit_use",
        "definition": "Pressure on nose and temples across a full shift.",
        "stat_roles": ["segmentation", "positioning", "potential_target"],
        "plain_language_definition": "Can you wear it all day without it hurting?",
        "theory_annotations": {
            "product_positioning": ["benefits"],
            "maslow": ["physiological"],
            "purchase_motivation": ["functional"],
        },
    },
    {
        "key": "style_appearance",
        "label": "Style and appearance",
        "theme": "brand_experience",
        "attribute_group": "brand_image",
        "definition": "How the wearer feels being seen in them on site.",
        "stat_roles": ["segmentation", "positioning"],
        "plain_language_definition": "Do you mind being seen wearing them?",
        "theory_annotations": {
            "product_positioning": ["benefits"],
            "maslow": ["esteem"],
            "wom_motivation": ["social_identity"],
        },
    },
    {
        "key": "after_sales",
        "label": "After-sales support",
        "theme": "brand_experience",
        "attribute_group": "benefit_use",
        "definition": "Replacement, warranty handling and seller responsiveness.",
        "stat_roles": ["positioning", "potential_target"],
        "plain_language_definition": "If it breaks, does anyone help you?",
        "theory_annotations": {
            "product_positioning": ["usage_context_service_experience"],
            "purchase_motivation": ["relational"],
            "wom_motivation": ["altruistic"],
        },
    },
]

BRANDS = [
    ("ArcShield", "ArcShield Pro"),
    ("VisorMax", "VisorMax Lite"),
    ("ClearGuard", "ClearGuard X1"),
]

# brand -> attribute -> (salience, quality) per review.
# A 0 salience means the reviewer never raised it; quality is then left empty,
# which is what the contract requires.
REVIEWS = [
    ("ArcShield", "Fogged only once all winter. Impact rating is the real reason I bought them.",
     {"anti_fog": (7, 9), "impact_protection": (6, 9), "comfort_fit": (3, 6), "style_appearance": (1, 4), "after_sales": (0, None)}),
    ("ArcShield", "Wore them under a respirator for a nine hour shift, stayed clear the whole time.",
     {"anti_fog": (7, 9), "impact_protection": (2, 8), "comfort_fit": (5, 7), "style_appearance": (0, None), "after_sales": (0, None)}),
    ("ArcShield", "Lens held up to a stray grinder spark. Ugly as sin though.",
     {"anti_fog": (2, 7), "impact_protection": (7, 10), "comfort_fit": (0, None), "style_appearance": (5, 2), "after_sales": (0, None)}),
    ("ArcShield", "Temples dig in after a few hours. Everything else is excellent.",
     {"anti_fog": (3, 8), "impact_protection": (3, 9), "comfort_fit": (6, 3), "style_appearance": (1, 3), "after_sales": (0, None)}),
    ("ArcShield", "Emailed about a scratched lens, got a reply in two days with a replacement.",
     {"anti_fog": (1, 8), "impact_protection": (0, None), "comfort_fit": (0, None), "style_appearance": (0, None), "after_sales": (6, 7)}),
    ("ArcShield", "Clear vision, solid build, looks like safety gear from 1998.",
     {"anti_fog": (5, 8), "impact_protection": (4, 9), "comfort_fit": (2, 6), "style_appearance": (6, 2), "after_sales": (0, None)}),
    ("ArcShield", "No fogging even coming in from the cold. Worth every cent.",
     {"anti_fog": (7, 10), "impact_protection": (1, 8), "comfort_fit": (1, 6), "style_appearance": (0, None), "after_sales": (0, None)}),

    ("VisorMax", "Fogs the moment I put a mask on. Had to keep lifting them.",
     {"anti_fog": (7, 2), "impact_protection": (2, 8), "comfort_fit": (4, 8), "style_appearance": (2, 6), "after_sales": (0, None)}),
    ("VisorMax", "Lightest pair I have owned, I forget they are on. Shame about the fogging.",
     {"anti_fog": (5, 2), "impact_protection": (1, 8), "comfort_fit": (7, 10), "style_appearance": (3, 6), "after_sales": (0, None)}),
    ("VisorMax", "Z87 stamped and it took a knock without cracking.",
     {"anti_fog": (0, None), "impact_protection": (7, 9), "comfort_fit": (2, 8), "style_appearance": (0, None), "after_sales": (0, None)}),
    ("VisorMax", "Support never answered. Two emails, three weeks, nothing.",
     {"anti_fog": (1, 3), "impact_protection": (0, None), "comfort_fit": (2, 9), "style_appearance": (0, None), "after_sales": (7, 1)}),
    ("VisorMax", "Comfortable enough to wear over glasses, which nothing else managed.",
     {"anti_fog": (2, 3), "impact_protection": (1, 8), "comfort_fit": (7, 9), "style_appearance": (2, 5), "after_sales": (0, None)}),
    ("VisorMax", "Steams up constantly indoors. Returned them, refund took a month.",
     {"anti_fog": (7, 1), "impact_protection": (0, None), "comfort_fit": (3, 8), "style_appearance": (0, None), "after_sales": (6, 2)}),
    ("VisorMax", "Fit is great, optics are fine, anti-fog coating is marketing fiction.",
     {"anti_fog": (6, 2), "impact_protection": (2, 7), "comfort_fit": (6, 9), "style_appearance": (2, 5), "after_sales": (0, None)}),

    ("ClearGuard", "Look sharp enough that I wear them off site. Fogging is average.",
     {"anti_fog": (4, 5), "impact_protection": (1, 6), "comfort_fit": (2, 4), "style_appearance": (7, 9), "after_sales": (0, None)}),
    ("ClearGuard", "Best looking safety glasses on the market. Nose pads are torture.",
     {"anti_fog": (0, None), "impact_protection": (1, 6), "comfort_fit": (7, 2), "style_appearance": (7, 10), "after_sales": (0, None)}),
    ("ClearGuard", "Cracked lens replaced free within a week, no argument.",
     {"anti_fog": (0, None), "impact_protection": (4, 5), "comfort_fit": (0, None), "style_appearance": (2, 8), "after_sales": (7, 10)}),
    ("ClearGuard", "Mid range protection, fine for light work, would not use them grinding.",
     {"anti_fog": (2, 5), "impact_protection": (6, 4), "comfort_fit": (3, 4), "style_appearance": (3, 8), "after_sales": (0, None)}),
    ("ClearGuard", "Seller walked me through the fit guide before I ordered.",
     {"anti_fog": (0, None), "impact_protection": (0, None), "comfort_fit": (4, 5), "style_appearance": (2, 9), "after_sales": (6, 9)}),
    ("ClearGuard", "Fog clears fast once you move. Frame pinches by lunchtime.",
     {"anti_fog": (5, 6), "impact_protection": (1, 6), "comfort_fit": (6, 3), "style_appearance": (4, 8), "after_sales": (0, None)}),
]

PRODUCT_BY_BRAND = dict(BRANDS)


def write_review_scoring_table() -> None:
    header = ["review_id", "unit_id", "brand", "product", "review_text"]
    for attribute in ATTRIBUTES:
        header.append(f"{attribute['key']}_salience")
        header.append(f"{attribute['key']}_quality")

    rows = []
    for index, (brand, text, scores) in enumerate(REVIEWS, start=1):
        review_id = f"r{index:03d}"
        row = [review_id, review_id, brand, PRODUCT_BY_BRAND[brand], text]
        for attribute in ATTRIBUTES:
            salience, quality = scores[attribute["key"]]
            row.append(salience)
            row.append("" if quality is None else quality)
        rows.append(row)

    with (HERE / "review_scoring_table.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(header)
        writer.writerows(rows)


def write_attribute_catalog() -> None:
    header = [
        "attribute_key", "label", "theme", "attribute_group", "definition",
        "source_type", "mention_count", "salience_column", "valence_column",
        "example_review_id", "example_quote",
    ]
    rows = []
    for attribute in ATTRIBUTES:
        key = attribute["key"]
        mention_count = sum(1 for _, _, scores in REVIEWS if scores[key][0] >= 1)
        example_id, example_quote = next(
            (f"r{index:03d}", text)
            for index, (_, text, scores) in enumerate(REVIEWS, start=1)
            if scores[key][0] >= 5
        )
        rows.append([
            key, attribute["label"], attribute["theme"], attribute["attribute_group"],
            attribute["definition"], "review_corpus", mention_count,
            f"{key}_salience", f"{key}_quality", example_id, example_quote,
        ])

    with (HERE / "attribute_catalog.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(header)
        writer.writerows(rows)


def write_review_foundation() -> None:
    dimension_catalog = []
    theme_mapping: dict[str, list[str]] = {}
    for attribute in ATTRIBUTES:
        key = attribute["key"]
        dimension_catalog.append({
            "column": key,
            "label": attribute["label"],
            "theme": attribute["theme"],
            "attribute_group": attribute["attribute_group"],
            "salience_column": f"{key}_salience",
            "valence_column": f"{key}_quality",
            "stat_roles": attribute["stat_roles"],
            "plain_language_definition": attribute["plain_language_definition"],
            "theory_annotations": attribute["theory_annotations"],
        })
        theme_mapping.setdefault(attribute["theme"], []).append(key)

    payload = {
        "dimension_catalog": dimension_catalog,
        "theme_mapping": theme_mapping,
        "attribute_extraction_summary": {
            "target_minimum": 30,
            "actual_count": len(ATTRIBUTES),
            "shortfall_reason": "Fixture corpus is deliberately small; it exists to verify the runner, not to model a real market.",
            "theory_gap": [],
        },
    }
    (HERE / "review_foundation.json").write_text(
        json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )


def write_context_and_targets() -> None:
    (HERE / "analysis_context.json").write_text(json.dumps({
        "analysis_goal": "Verify the runner end to end on a corpus small enough to check by hand.",
        "comparison_axes": ["brand"],
        "scope_limits": ["Synthetic reviews. Not evidence about any real product."],
    }, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    # `brands` must be a flat list of brand names — reporting.py joins it into
    # a sentence, so dicts here fail late, after every artifact is already written.
    (HERE / "brands.json").write_text(json.dumps({
        "brands": [brand for brand, _ in BRANDS],
        "products": {brand: product for brand, product in BRANDS},
    }, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    (HERE / "ideal_point.json").write_text(json.dumps({
        "label": "Ideal",
        "attributes": {
            attribute["key"]: {"salience": 6, "valence": 9}
            for attribute in ATTRIBUTES
        },
    }, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


if __name__ == "__main__":
    write_review_scoring_table()
    write_attribute_catalog()
    write_review_foundation()
    write_context_and_targets()
    print(f"fixture written to {HERE}")

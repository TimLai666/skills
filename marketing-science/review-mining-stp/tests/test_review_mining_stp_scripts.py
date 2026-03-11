from __future__ import annotations

import csv
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RUN_SCRIPT = ROOT / "scripts" / "run_review_mining_stp.py"
VALIDATE_SCRIPT = ROOT / "scripts" / "validate_review_mining_stp.py"


def write_json(path: Path, payload: object) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    fieldnames = list(dict.fromkeys(key for row in rows for key in row.keys()))
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def build_dimension_catalog_base() -> list[dict[str, object]]:
    return [
        {
            "column": "fast_delivery",
            "label": "Fast Delivery",
            "theme": "service_experience",
            "theory_tags": ["purchase_motivation", "system1"],
            "stat_roles": ["segmentation", "current_target", "comparison_axis"],
            "plain_language_definition": "How strongly the review says delivery was quick and hassle-free.",
        },
        {
            "column": "support_trust",
            "label": "Support Trust",
            "theme": "service_experience",
            "theory_tags": ["safety", "wom_motivation"],
            "stat_roles": ["current_target", "comparison_axis"],
            "plain_language_definition": "How strongly the review signals trust in support, seller reliability, or issue handling.",
        },
        {
            "column": "setup_ease",
            "label": "Setup Ease",
            "theme": "product_performance",
            "theory_tags": ["purchase_motivation", "system2"],
            "stat_roles": ["segmentation", "positioning"],
            "plain_language_definition": "How clearly the review says setup or usage felt easy.",
        },
        {
            "column": "product_quality",
            "label": "Product Quality",
            "theme": "product_performance",
            "theory_tags": ["product_positioning", "esteem"],
            "stat_roles": ["current_target", "positioning"],
            "plain_language_definition": "How strongly the review praises core quality, craftsmanship, or durability.",
        },
        {
            "column": "value_for_money",
            "label": "Value For Money",
            "theme": "value_perception",
            "theory_tags": ["purchase_motivation", "esteem"],
            "stat_roles": ["potential_target", "positioning", "comparison_axis"],
            "plain_language_definition": "How strongly the review says the brand was worth the price paid.",
        },
        {
            "column": "recommendation_pull",
            "label": "Recommendation Pull",
            "theme": "value_perception",
            "theory_tags": ["wom_motivation", "belonging"],
            "stat_roles": ["segmentation", "potential_target"],
            "plain_language_definition": "How strongly the review implies recommending, repurchasing, or talking about the brand.",
        },
    ]


def build_dimension_catalog_custom() -> list[dict[str, object]]:
    return [
        {
            "column": "delivery_confidence",
            "label": "Delivery Confidence",
            "theme": "service_experience",
            "theory_tags": ["safety", "system1"],
            "stat_roles": ["segmentation", "current_target", "comparison_axis"],
            "plain_language_definition": "How strongly the review says fulfillment felt dependable and predictable.",
        },
        {
            "column": "communication_clarity",
            "label": "Communication Clarity",
            "theme": "service_experience",
            "theory_tags": ["wom_motivation", "belonging"],
            "stat_roles": ["current_target", "comparison_axis"],
            "plain_language_definition": "How clearly the review says communication was easy to follow and reassuring.",
        },
        {
            "column": "install_simplicity",
            "label": "Install Simplicity",
            "theme": "product_performance",
            "theory_tags": ["purchase_motivation", "system2"],
            "stat_roles": ["segmentation", "positioning"],
            "plain_language_definition": "How strongly the review says installation or onboarding was simple.",
        },
        {
            "column": "premium_finish",
            "label": "Premium Finish",
            "theme": "product_performance",
            "theory_tags": ["product_positioning", "esteem"],
            "stat_roles": ["segmentation", "positioning"],
            "plain_language_definition": "How strongly the review frames the product as polished, premium, or elevated.",
        },
        {
            "column": "everyday_value",
            "label": "Everyday Value",
            "theme": "value_perception",
            "theory_tags": ["purchase_motivation", "esteem"],
            "stat_roles": ["potential_target", "positioning", "comparison_axis"],
            "plain_language_definition": "How strongly the review says the brand creates practical value in daily use.",
        },
        {
            "column": "social_proof_pull",
            "label": "Social Proof Pull",
            "theme": "value_perception",
            "theory_tags": ["wom_motivation", "belonging"],
            "stat_roles": ["segmentation", "potential_target"],
            "plain_language_definition": "How strongly the review suggests telling others, gifting, or showing the brand to peers.",
        },
    ]


def build_review_foundation(
    dimension_catalog: list[dict[str, object]] | None = None,
    include_dimension_catalog: bool = True,
    include_theme_mapping: bool = True,
    complete_theme_mapping: bool = True,
    scoring_rubric: dict[str, object] | None = None,
) -> dict[str, object]:
    catalog = dimension_catalog or build_dimension_catalog_base()
    payload: dict[str, object] = {
        "people_insights": ["value-oriented buyers", "convenience-oriented buyers", "quality-seeking buyers"],
        "product_triggers": ["delivery speed", "quality confidence", "ease of setup"],
        "context_scenarios": ["first purchase", "repeat purchase", "gift purchase"],
        "system1_system2_split": {
            "system1": ["instant confidence", "visual polish"],
            "system2": ["setup comparison", "price-value justification"],
        },
        "maslow_keywords": {
            "physiological": ["fit", "comfort"],
            "safety": ["trust", "reliable"],
            "belonging": ["recommend", "share"],
            "esteem": ["premium", "confidence"],
            "self_actualization": ["upgrade", "identity"],
        },
    }
    if scoring_rubric is not None:
        payload["scoring_rubric"] = scoring_rubric
    if include_dimension_catalog:
        payload["dimension_catalog"] = catalog
    if include_theme_mapping:
        theme_mapping = {
            "service_experience": [item["column"] for item in catalog if item["theme"] == "service_experience"],
            "product_performance": [item["column"] for item in catalog if item["theme"] == "product_performance"],
            "value_perception": [item["column"] for item in catalog if item["theme"] == "value_perception"],
        }
        if not complete_theme_mapping:
            theme_mapping.pop("value_perception", None)
        payload["theme_mapping"] = theme_mapping
    return payload


def build_analysis_context(comparison_axes: list[str]) -> dict[str, object]:
    return {
        "analysis_goal": "Convert scored review evidence into STP outputs.",
        "comparison_axes": comparison_axes,
        "scope_limits": [
            "Scripts operate on scored artifacts only.",
            "Raw review interpretation belongs to the agent layer.",
        ],
    }


def build_brands_payload(include_similarity: bool = False) -> dict[str, object]:
    payload: dict[str, object] = {"brands": ["BrandA", "BrandB", "BrandC"]}
    if include_similarity:
        payload["similarity_matrix"] = [
            [0.0, 0.42, 0.63],
            [0.42, 0.0, 0.51],
            [0.63, 0.51, 0.0],
        ]
    return payload


def build_ideal_point(catalog: list[dict[str, object]]) -> dict[str, object]:
    positioning_columns = [item["column"] for item in catalog if "positioning" in item["stat_roles"]]
    return {
        "label": "IdealPoint",
        "attributes": {column: 7 - index if 7 - index >= 4 else 4 for index, column in enumerate(positioning_columns)},
    }


def build_review_rows_base() -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    brands = ["BrandA", "BrandB", "BrandC"]
    brand_offsets = {
        "BrandA": {"product_quality": 1, "value_for_money": -1},
        "BrandB": {"fast_delivery": 1, "recommendation_pull": 1},
        "BrandC": {"setup_ease": 1, "product_quality": 1},
    }
    clusters = {
        "value": {
            "profile_lifestyle": "value",
            "profile_region": "north",
            "profile_gender": "female",
            "rating": 5,
            "scores": {
                "fast_delivery": 5,
                "support_trust": 5,
                "setup_ease": 4,
                "product_quality": 4,
                "value_for_money": 7,
                "recommendation_pull": 6,
            },
            "texts": [
                "{brand} arrived quickly and felt worth the money. I would buy it again because it solves the basics without wasting cash.",
                "{brand} gave me solid delivery and fair value. It is easy to recommend when someone wants dependable quality at a sensible price.",
            ],
        },
        "convenience": {
            "profile_lifestyle": "convenience",
            "profile_region": "central",
            "profile_gender": "male",
            "rating": 6,
            "scores": {
                "fast_delivery": 6,
                "support_trust": 6,
                "setup_ease": 7,
                "product_quality": 5,
                "value_for_money": 5,
                "recommendation_pull": 5,
            },
            "texts": [
                "{brand} was easy to set up and support answered fast. The whole experience felt smooth and reliable from start to finish.",
                "I picked {brand} because everything was simple. Delivery was quick, setup was painless, and support made me trust the purchase.",
            ],
        },
        "premium": {
            "profile_lifestyle": "premium",
            "profile_region": "south",
            "profile_gender": "female",
            "rating": 7,
            "scores": {
                "fast_delivery": 4,
                "support_trust": 5,
                "setup_ease": 6,
                "product_quality": 7,
                "value_for_money": 4,
                "recommendation_pull": 5,
            },
            "texts": [
                "{brand} looks premium and the build quality feels excellent. It gives a polished impression that stands above cheaper options.",
                "The finish on {brand} feels upscale and carefully made. I trust the quality enough to mention it when friends ask what I bought.",
            ],
        },
    }
    for cluster_name, cluster in clusters.items():
        for idx in range(12):
            brand = brands[idx % len(brands)]
            row: dict[str, object] = {
                "review_id": f"{cluster_name}-review-{idx}",
                "unit_id": f"{cluster_name}-unit-{idx}",
                "brand": brand,
                "review_text": cluster["texts"][idx % len(cluster["texts"])].format(brand=brand),
                "profile_lifestyle": cluster["profile_lifestyle"],
                "profile_region": cluster["profile_region"],
                "profile_gender": cluster["profile_gender"],
                "channel": "app_store" if idx % 2 == 0 else "marketplace",
                "rating": cluster["rating"],
            }
            for column, base_score in cluster["scores"].items():
                score = base_score + brand_offsets.get(brand, {}).get(column, 0)
                if idx % 5 == 0 and column in {"fast_delivery", "setup_ease", "recommendation_pull"}:
                    score += 1
                if idx % 7 == 0 and column in {"product_quality", "value_for_money"}:
                    score -= 1
                row[column] = max(0, min(7, int(score)))
            rows.append(row)
    return rows


def build_review_rows_custom() -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    brands = ["BrandA", "BrandB", "BrandC"]
    brand_offsets = {
        "BrandA": {"premium_finish": 1},
        "BrandB": {"delivery_confidence": 1, "social_proof_pull": 1},
        "BrandC": {"install_simplicity": 1, "everyday_value": 1},
    }
    clusters = {
        "assurance": {
            "profile_lifestyle": "assurance",
            "profile_region": "north",
            "scores": {
                "delivery_confidence": 7,
                "communication_clarity": 6,
                "install_simplicity": 4,
                "premium_finish": 4,
                "everyday_value": 5,
                "social_proof_pull": 5,
            },
            "texts": [
                "{brand} felt dependable from shipping to follow-up messages. The clear updates made the whole order easy to trust.",
                "I trust {brand} because delivery was predictable and communication stayed clear the whole time.",
            ],
        },
        "ease": {
            "profile_lifestyle": "ease",
            "profile_region": "central",
            "scores": {
                "delivery_confidence": 5,
                "communication_clarity": 5,
                "install_simplicity": 7,
                "premium_finish": 5,
                "everyday_value": 6,
                "social_proof_pull": 4,
            },
            "texts": [
                "{brand} was simple to install and easy to fit into daily use. It feels useful without adding friction.",
                "The best part of {brand} is how quickly everything works. Setup is simple and the product keeps paying off in normal use.",
            ],
        },
        "prestige": {
            "profile_lifestyle": "prestige",
            "profile_region": "south",
            "scores": {
                "delivery_confidence": 4,
                "communication_clarity": 4,
                "install_simplicity": 5,
                "premium_finish": 7,
                "everyday_value": 4,
                "social_proof_pull": 6,
            },
            "texts": [
                "{brand} feels premium in a way people notice immediately. I would gladly show it to friends because it looks elevated.",
                "The finish on {brand} is polished and premium. It stands out enough that I talk about it when people ask.",
            ],
        },
    }
    for cluster_name, cluster in clusters.items():
        for idx in range(12):
            brand = brands[idx % len(brands)]
            row: dict[str, object] = {
                "review_id": f"{cluster_name}-review-{idx}",
                "unit_id": f"{cluster_name}-unit-{idx}",
                "brand": brand,
                "review_text": cluster["texts"][idx % len(cluster["texts"])].format(brand=brand),
                "profile_lifestyle": cluster["profile_lifestyle"],
                "profile_region": cluster["profile_region"],
                "channel": "app_store" if idx % 2 == 0 else "marketplace",
                "rating": 5 + (idx % 2),
            }
            for column, base_score in cluster["scores"].items():
                score = base_score + brand_offsets.get(brand, {}).get(column, 0)
                if idx % 4 == 0 and column in {"delivery_confidence", "install_simplicity"}:
                    score += 1
                if idx % 6 == 0 and column in {"premium_finish", "everyday_value"}:
                    score -= 1
                row[column] = max(0, min(7, int(score)))
            rows.append(row)
    return rows


def build_partial_segmentation_rows() -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for idx in range(24):
        rows.append(
            {
                "unit_id": f"value-{idx}",
                "brand": "BrandB",
                "profile_region": "north",
                "profile_age_band": "25-34",
                "fast_delivery": 7 if idx % 3 else 6,
                "support_trust": 6 if idx % 2 else 5,
                "setup_ease": 4,
                "product_quality": 4,
                "value_for_money": 7 if idx % 4 else 6,
                "recommendation_pull": 6 if idx % 2 else 5,
            }
        )
    for idx in range(24):
        rows.append(
            {
                "unit_id": f"ease-{idx}",
                "brand": "BrandC",
                "profile_region": "central",
                "profile_age_band": "35-44",
                "fast_delivery": 6 if idx % 3 else 5,
                "support_trust": 6,
                "setup_ease": 7 if idx % 2 else 6,
                "product_quality": 5,
                "value_for_money": 5,
                "recommendation_pull": 5,
            }
        )
    for idx in range(24):
        rows.append(
            {
                "unit_id": f"premium-{idx}",
                "brand": "BrandA",
                "profile_region": "south",
                "profile_age_band": "45-54",
                "fast_delivery": 4,
                "support_trust": 5,
                "setup_ease": 6 if idx % 2 else 5,
                "value_for_money": 4,
                "recommendation_pull": 5 if idx % 2 else 4,
                "product_quality": 7 if idx % 3 else 6,
            }
        )
    return rows


def make_canonical_input_dir(
    base: Path,
    dimension_catalog: list[dict[str, object]] | None = None,
    rows: list[dict[str, object]] | None = None,
    include_dimension_catalog: bool = True,
    include_theme_mapping: bool = True,
    complete_theme_mapping: bool = True,
    scoring_rubric: dict[str, object] | None = None,
    include_similarity: bool = False,
) -> Path:
    input_dir = base / "input"
    input_dir.mkdir()
    catalog = dimension_catalog or build_dimension_catalog_base()
    write_csv(input_dir / "review_scoring_table.csv", rows or build_review_rows_base())
    write_json(
        input_dir / "review_foundation.json",
        build_review_foundation(
            dimension_catalog=catalog,
            include_dimension_catalog=include_dimension_catalog,
            include_theme_mapping=include_theme_mapping,
            complete_theme_mapping=complete_theme_mapping,
            scoring_rubric=scoring_rubric,
        ),
    )
    comparison_axes = (
        ["delivery_confidence", "communication_clarity", "everyday_value"]
        if catalog == build_dimension_catalog_custom()
        else ["fast_delivery", "support_trust", "value_for_money"]
    )
    write_json(input_dir / "analysis_context.json", build_analysis_context(comparison_axes))
    write_json(input_dir / "brands.json", build_brands_payload(include_similarity=include_similarity))
    write_json(input_dir / "ideal_point.json", build_ideal_point(catalog))
    return input_dir


def make_partial_input_dir(base: Path) -> Path:
    input_dir = base / "input"
    input_dir.mkdir()
    write_json(input_dir / "review_foundation.json", build_review_foundation())
    write_csv(input_dir / "segmentation_variables.csv", build_partial_segmentation_rows())
    write_json(
        input_dir / "analysis_context.json",
        build_analysis_context(["fast_delivery", "support_trust", "value_for_money"]),
    )
    return input_dir


class ReviewMiningStpScriptsTest(unittest.TestCase):
    maxDiff = None

    def run_command(self, args: list[str], cwd: Path) -> subprocess.CompletedProcess[str]:
        return subprocess.run([sys.executable, *args], cwd=cwd, text=True, capture_output=True, check=False)

    def test_full_run_accepts_dynamic_scored_inputs_and_emits_intermediate_artifacts(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            input_dir = make_canonical_input_dir(tmp_path)
            output_dir = tmp_path / "output"

            result = self.run_command([str(RUN_SCRIPT), "--run-mode", "full", "--input-dir", str(input_dir), "--output-dir", str(output_dir)], cwd=ROOT)
            self.assertEqual(result.returncode, 0, result.stderr)

            validator = self.run_command([str(VALIDATE_SCRIPT), "--run-mode", "full", "--output-dir", str(output_dir)], cwd=ROOT)
            self.assertEqual(validator.returncode, 0, validator.stderr)

            appendix = json.loads((output_dir / "appendix.json").read_text(encoding="utf-8"))
            self.assertEqual(
                sorted(appendix["execution_scope"]["emitted_intermediate_artifacts"]),
                ["positioning_scorecard.csv", "segmentation_variables.csv", "targeting_dataset.csv"],
            )
            for summary_key in ["segmentation_summary", "targeting_summary", "positioning_summary"]:
                section = appendix[summary_key]
                self.assertTrue(section["methods_used"])
                self.assertTrue(section["theories_used"])
                self.assertTrue(section["plain_language_explanation"])
                self.assertGreaterEqual(len(section["evidence_quotes"]), 2)
                self.assertLessEqual(len(section["evidence_quotes"]), 3)

    def test_full_run_supports_alternate_dynamic_schema(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            catalog = build_dimension_catalog_custom()
            input_dir = make_canonical_input_dir(tmp_path, dimension_catalog=catalog, rows=build_review_rows_custom())
            output_dir = tmp_path / "output"

            result = self.run_command([str(RUN_SCRIPT), "--run-mode", "full", "--input-dir", str(input_dir), "--output-dir", str(output_dir)], cwd=ROOT)
            self.assertEqual(result.returncode, 0, result.stderr)

            appendix = json.loads((output_dir / "appendix.json").read_text(encoding="utf-8"))
            attributes = {row["attribute"] for row in appendix["positioning_summary"]["positioning_scorecard"] if row["point_type"] == "brand"}
            self.assertIn("premium_finish", attributes)
            self.assertIn("everyday_value", attributes)

    def test_segmentation_partial_run_still_supports_direct_intermediate_artifacts(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            input_dir = make_partial_input_dir(tmp_path)
            output_dir = tmp_path / "output"

            result = self.run_command([str(RUN_SCRIPT), "--run-mode", "segmentation", "--input-dir", str(input_dir), "--output-dir", str(output_dir)], cwd=ROOT)
            self.assertEqual(result.returncode, 0, result.stderr)

            payload = json.loads((output_dir / "segment_profiles.json").read_text(encoding="utf-8"))
            self.assertEqual(payload["cluster_selection"]["method"], "factor_analysis -> kmeans")
            self.assertTrue(all(item["share"] > 0.05 for item in payload["segment_profiles"]))

    def test_targeting_partial_run_uses_comparison_axes_override(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            input_dir = make_canonical_input_dir(tmp_path)
            full_dir = tmp_path / "full"
            targeting_dir = tmp_path / "targeting"

            full_result = self.run_command([str(RUN_SCRIPT), "--run-mode", "full", "--input-dir", str(input_dir), "--output-dir", str(full_dir)], cwd=ROOT)
            self.assertEqual(full_result.returncode, 0, full_result.stderr)

            result = self.run_command([str(RUN_SCRIPT), "--run-mode", "targeting", "--input-dir", str(full_dir), "--upstream-artifacts-dir", str(full_dir), "--output-dir", str(targeting_dir)], cwd=ROOT)
            self.assertEqual(result.returncode, 0, result.stderr)

            targeting = json.loads((targeting_dir / "targeting_results.json").read_text(encoding="utf-8"))
            self.assertEqual(targeting["target_selection_decision"]["comparison_axes_used"], ["fast_delivery", "support_trust", "value_for_money"])

    def test_positioning_mds_does_not_fabricate_attribute_vectors(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            input_dir = make_canonical_input_dir(tmp_path, include_similarity=True)
            output_dir = tmp_path / "output"

            result = self.run_command([str(RUN_SCRIPT), "--run-mode", "positioning", "--input-dir", str(input_dir), "--output-dir", str(output_dir), "--positioning-method", "mds"], cwd=ROOT)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertFalse((output_dir / "perceptual_map_vectors.csv").exists())

    def test_custom_missing_prerequisite_lists_only_true_missing_intermediate(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            input_dir = tmp_path / "input"
            input_dir.mkdir()
            write_json(input_dir / "brands.json", build_brands_payload())
            write_json(input_dir / "ideal_point.json", build_ideal_point(build_dimension_catalog_base()))
            output_dir = tmp_path / "output"

            result = self.run_command([str(RUN_SCRIPT), "--run-mode", "custom", "--requested-modules", "perceptual-map", "--input-dir", str(input_dir), "--output-dir", str(output_dir)], cwd=ROOT)
            self.assertEqual(result.returncode, 0, result.stderr)
            payload = json.loads((output_dir / "MissingPrerequisiteOutput.json").read_text(encoding="utf-8"))
            self.assertEqual(payload["missing_prerequisites"], ["positioning_scorecard.csv"])

    def test_full_run_rejects_missing_review_text(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            rows = build_review_rows_base()
            rows[0]["review_text"] = ""
            input_dir = make_canonical_input_dir(tmp_path, rows=rows)
            output_dir = tmp_path / "output"

            result = self.run_command([str(RUN_SCRIPT), "--run-mode", "full", "--input-dir", str(input_dir), "--output-dir", str(output_dir)], cwd=ROOT)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("review_text", result.stderr)

    def test_full_run_rejects_out_of_range_scores(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            rows = build_review_rows_base()
            rows[0]["fast_delivery"] = 8
            input_dir = make_canonical_input_dir(tmp_path, rows=rows)
            output_dir = tmp_path / "output"

            result = self.run_command([str(RUN_SCRIPT), "--run-mode", "full", "--input-dir", str(input_dir), "--output-dir", str(output_dir)], cwd=ROOT)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("0-7", result.stderr)

    def test_full_run_accepts_missing_scoring_rubric_metadata(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            input_dir = make_canonical_input_dir(tmp_path, scoring_rubric=None)
            output_dir = tmp_path / "output"

            result = self.run_command([str(RUN_SCRIPT), "--run-mode", "full", "--input-dir", str(input_dir), "--output-dir", str(output_dir)], cwd=ROOT)
            self.assertEqual(result.returncode, 0, result.stderr)

    def test_full_run_accepts_custom_scoring_rubric_metadata(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            custom_rubric = {
                "scale": {"0": "none", "1-3": "light", "4": "mixed", "5-6": "clear", "7": "strong"},
                "process": ["custom", "audit", "metadata"],
            }
            input_dir = make_canonical_input_dir(tmp_path, scoring_rubric=custom_rubric)
            output_dir = tmp_path / "output"

            result = self.run_command([str(RUN_SCRIPT), "--run-mode", "full", "--input-dir", str(input_dir), "--output-dir", str(output_dir)], cwd=ROOT)
            self.assertEqual(result.returncode, 0, result.stderr)

    def test_full_run_rejects_missing_plain_language_definition(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            catalog = build_dimension_catalog_base()
            catalog[0].pop("plain_language_definition", None)
            input_dir = make_canonical_input_dir(tmp_path, dimension_catalog=catalog)
            output_dir = tmp_path / "output"

            result = self.run_command([str(RUN_SCRIPT), "--run-mode", "full", "--input-dir", str(input_dir), "--output-dir", str(output_dir)], cwd=ROOT)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("plain_language_definition", result.stderr)

    def test_full_run_rejects_incomplete_theme_mapping(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            input_dir = make_canonical_input_dir(tmp_path, complete_theme_mapping=False)
            output_dir = tmp_path / "output"

            result = self.run_command([str(RUN_SCRIPT), "--run-mode", "full", "--input-dir", str(input_dir), "--output-dir", str(output_dir)], cwd=ROOT)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("theme_mapping", result.stderr)

    def test_raw_reviews_are_rejected_until_agent_layer_creates_scored_artifacts(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            input_dir = tmp_path / "input"
            input_dir.mkdir()
            write_json(input_dir / "reviews.json", [{"review_id": "r1", "review_text": "Fast delivery and decent value."}])
            output_dir = tmp_path / "output"

            result = self.run_command([str(RUN_SCRIPT), "--run-mode", "full", "--input-dir", str(input_dir), "--output-dir", str(output_dir)], cwd=ROOT)
            self.assertEqual(result.returncode, 0, result.stderr)
            payload = json.loads((output_dir / "MissingPrerequisiteOutput.json").read_text(encoding="utf-8"))
            self.assertIn("review_scoring_table.csv", payload["missing_prerequisites"])
            self.assertIn("agent layer", payload["next_step_rule"].lower())

    def test_validator_rejects_non_traceable_evidence_quote(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            input_dir = make_canonical_input_dir(tmp_path)
            output_dir = tmp_path / "output"

            result = self.run_command([str(RUN_SCRIPT), "--run-mode", "full", "--input-dir", str(input_dir), "--output-dir", str(output_dir)], cwd=ROOT)
            self.assertEqual(result.returncode, 0, result.stderr)

            appendix = json.loads((output_dir / "appendix.json").read_text(encoding="utf-8"))
            appendix["segmentation_summary"]["evidence_quotes"][0]["quote_text"] = "Hallucinated quote"
            write_json(output_dir / "appendix.json", appendix)

            validator = self.run_command([str(VALIDATE_SCRIPT), "--run-mode", "full", "--output-dir", str(output_dir)], cwd=ROOT)
            self.assertNotEqual(validator.returncode, 0)
            self.assertIn("evidence quote", validator.stderr.lower())

    def test_validator_rejects_missing_execution_scope_fields(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            input_dir = make_canonical_input_dir(tmp_path)
            output_dir = tmp_path / "output"

            result = self.run_command([str(RUN_SCRIPT), "--run-mode", "full", "--input-dir", str(input_dir), "--output-dir", str(output_dir)], cwd=ROOT)
            self.assertEqual(result.returncode, 0, result.stderr)

            appendix = json.loads((output_dir / "appendix.json").read_text(encoding="utf-8"))
            appendix["execution_scope"].pop("modules_executed", None)
            write_json(output_dir / "appendix.json", appendix)

            validator = self.run_command([str(VALIDATE_SCRIPT), "--run-mode", "full", "--output-dir", str(output_dir)], cwd=ROOT)
            self.assertNotEqual(validator.returncode, 0)
            self.assertIn("modules_executed", validator.stderr)


if __name__ == "__main__":
    unittest.main()

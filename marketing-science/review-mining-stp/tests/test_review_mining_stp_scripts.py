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
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def build_dimension_catalog_14() -> list[dict[str, object]]:
    return [
        {"column": "fast_shipping", "label": "Fast Shipping", "theme": "service_experience", "theory_tags": ["purchase_motivation", "system1"], "stat_roles": ["segmentation"]},
        {"column": "packaging_quality", "label": "Packaging Quality", "theme": "service_experience", "theory_tags": ["product_positioning"], "stat_roles": ["segmentation", "positioning"]},
        {"column": "easy_communication", "label": "Easy Communication", "theme": "service_experience", "theory_tags": ["wom_motivation", "belonging"], "stat_roles": ["segmentation", "current_target"]},
        {"column": "customer_support", "label": "Customer Support", "theme": "service_experience", "theory_tags": ["safety", "wom_motivation"], "stat_roles": ["current_target"]},
        {"column": "problem_resolution", "label": "Problem Resolution", "theme": "service_experience", "theory_tags": ["safety"], "stat_roles": ["current_target", "comparison_axis"]},
        {"column": "seller_trust", "label": "Seller Trust", "theme": "value_perception", "theory_tags": ["safety", "esteem"], "stat_roles": ["current_target", "comparison_axis"]},
        {"column": "repurchase_intent", "label": "Repurchase Intent", "theme": "value_perception", "theory_tags": ["wom_motivation", "esteem"], "stat_roles": ["potential_target", "comparison_axis"]},
        {"column": "size_fit", "label": "Size Fit", "theme": "product_performance", "theory_tags": ["physiological"], "stat_roles": ["segmentation", "positioning"]},
        {"column": "easy_install", "label": "Easy Install", "theme": "product_performance", "theory_tags": ["purchase_motivation"], "stat_roles": ["segmentation", "positioning"]},
        {"column": "design_appeal", "label": "Design Appeal", "theme": "product_performance", "theory_tags": ["esteem", "product_positioning"], "stat_roles": ["segmentation", "positioning"]},
        {"column": "quality_good", "label": "Quality Good", "theme": "product_performance", "theory_tags": ["product_positioning", "esteem"], "stat_roles": ["current_target", "positioning"]},
        {"column": "expectation_match", "label": "Expectation Match", "theme": "value_perception", "theory_tags": ["safety", "esteem"], "stat_roles": ["positioning"]},
        {"column": "value_for_money", "label": "Value For Money", "theme": "value_perception", "theory_tags": ["purchase_motivation"], "stat_roles": ["segmentation", "potential_target", "positioning"]},
        {"column": "description_match", "label": "Description Match", "theme": "value_perception", "theory_tags": ["safety"], "stat_roles": ["current_target"]},
    ]


def build_dimension_catalog_custom() -> list[dict[str, object]]:
    return [
        {"column": "delivery_confidence", "label": "Delivery Confidence", "theme": "service_experience", "theory_tags": ["safety"], "stat_roles": ["segmentation", "current_target", "comparison_axis"]},
        {"column": "setup_clarity", "label": "Setup Clarity", "theme": "product_performance", "theory_tags": ["purchase_motivation"], "stat_roles": ["segmentation", "positioning"]},
        {"column": "core_quality", "label": "Core Quality", "theme": "product_performance", "theory_tags": ["product_positioning"], "stat_roles": ["current_target", "positioning"]},
        {"column": "social_proof_pull", "label": "Social Proof Pull", "theme": "value_perception", "theory_tags": ["wom_motivation", "belonging"], "stat_roles": ["potential_target", "comparison_axis"]},
        {"column": "premium_feel", "label": "Premium Feel", "theme": "value_perception", "theory_tags": ["esteem"], "stat_roles": ["segmentation", "positioning"]},
    ]


def build_review_foundation(
    dimension_catalog: list[dict[str, object]] | None = None,
    include_dimension_catalog: bool = True,
    include_theme_mapping: bool = True,
    complete_theme_mapping: bool = True,
) -> dict[str, object]:
    catalog = dimension_catalog or build_dimension_catalog_14()
    payload: dict[str, object] = {
        "people_insights": ["Price-aware shoppers", "Convenience-first shoppers", "Premium seekers"],
        "product_triggers": ["delivery speed", "design", "quality confidence"],
        "context_scenarios": ["first purchase", "repeat purchase", "gift purchase"],
        "system1_system2_split": {
            "system1": ["aesthetic delight", "instant confidence"],
            "system2": ["feature comparison", "value justification"],
        },
        "maslow_keywords": {
            "physiological": ["fit", "comfort"],
            "safety": ["trust", "described_as_expected"],
            "belonging": ["community", "social proof"],
            "esteem": ["premium", "confidence"],
            "self_actualization": ["upgrade", "identity"],
        },
    }
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


def build_analysis_context(comparison_axes: list[str] | None = None) -> dict[str, object]:
    return {
        "analysis_goal": "Convert review-derived scoring into STP outputs.",
        "comparison_axes": comparison_axes or ["seller_trust", "repurchase_intent", "problem_resolution"],
        "scope_limits": [
            "Scripts only operate on scored artifacts.",
            "Raw review interpretation belongs to the agent layer.",
        ],
    }


def build_brands_payload(include_similarity: bool = False) -> dict[str, object]:
    payload: dict[str, object] = {"brands": ["BrandA", "BrandB", "BrandC"]}
    if include_similarity:
        payload["similarity_matrix"] = [
            [0.0, 0.45, 0.35],
            [0.45, 0.0, 0.60],
            [0.35, 0.60, 0.0],
        ]
    return payload


def build_ideal_point(attribute_names: list[str] | None = None) -> dict[str, object]:
    names = attribute_names or [
        "packaging_quality",
        "size_fit",
        "easy_install",
        "design_appeal",
        "quality_good",
        "expectation_match",
        "value_for_money",
    ]
    return {"label": "IdealPoint", "attributes": {name: 5.0 - (idx * 0.1) for idx, name in enumerate(names)}}


def build_review_scoring_rows_14() -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    brand_offsets = {
        "BrandA": {"packaging_quality": 0.5, "quality_good": 0.4, "expectation_match": 0.3, "design_appeal": 0.1},
        "BrandB": {"value_for_money": 0.6, "fast_shipping": 0.5, "easy_communication": 0.2, "repurchase_intent": 0.3},
        "BrandC": {"design_appeal": 0.6, "easy_install": 0.5, "size_fit": 0.4, "quality_good": 0.2},
    }
    cluster_patterns = {
        "value": {
            "profile_lifestyle": "value",
            "profile_region": "north",
            "profile_gender": "female",
            "fast_shipping": 3.4,
            "packaging_quality": 3.2,
            "easy_communication": 3.3,
            "customer_support": 3.5,
            "problem_resolution": 3.4,
            "seller_trust": 4.7,
            "repurchase_intent": 4.8,
            "size_fit": 3.1,
            "easy_install": 2.8,
            "design_appeal": 2.4,
            "quality_good": 3.2,
            "expectation_match": 3.8,
            "value_for_money": 4.9,
            "description_match": 4.1,
            "rating": 4,
        },
        "convenience": {
            "profile_lifestyle": "convenience",
            "profile_region": "central",
            "profile_gender": "male",
            "fast_shipping": 4.8,
            "packaging_quality": 3.5,
            "easy_communication": 4.4,
            "customer_support": 4.1,
            "problem_resolution": 4.2,
            "seller_trust": 4.0,
            "repurchase_intent": 4.3,
            "size_fit": 3.7,
            "easy_install": 4.6,
            "design_appeal": 3.0,
            "quality_good": 3.9,
            "expectation_match": 3.8,
            "value_for_money": 3.6,
            "description_match": 4.0,
            "rating": 4,
        },
        "premium": {
            "profile_lifestyle": "premium",
            "profile_region": "south",
            "profile_gender": "female",
            "fast_shipping": 3.6,
            "packaging_quality": 4.5,
            "easy_communication": 3.6,
            "customer_support": 3.9,
            "problem_resolution": 3.8,
            "seller_trust": 4.1,
            "repurchase_intent": 3.8,
            "size_fit": 4.5,
            "easy_install": 4.2,
            "design_appeal": 4.9,
            "quality_good": 4.8,
            "expectation_match": 4.6,
            "value_for_money": 3.1,
            "description_match": 4.4,
            "rating": 5,
        },
    }
    brands = ["BrandA", "BrandB", "BrandC"]
    for cluster_name, base in cluster_patterns.items():
        for idx in range(12):
            brand = brands[idx % len(brands)]
            row: dict[str, object] = {
                "review_id": f"{cluster_name}-review-{idx}",
                "unit_id": f"{cluster_name}-unit-{idx}",
                "brand": brand,
                "channel": "app_store" if idx % 2 == 0 else "marketplace",
            }
            for column, value in base.items():
                if column.startswith("profile_") or column == "rating":
                    row[column] = value
                    continue
                adjusted = value + ((idx % 3) * 0.05) + brand_offsets.get(brand, {}).get(column, 0.0)
                row[column] = round(min(adjusted, 5.0), 2)
            row["rating"] = min(5, int(base["rating"]) + (1 if idx % 5 == 0 else 0))
            rows.append(row)
    return rows


def build_review_scoring_rows_custom() -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    cluster_patterns = {
        "trust": {"profile_segment": "trust", "delivery_confidence": 4.7, "setup_clarity": 3.2, "core_quality": 3.6, "social_proof_pull": 4.5, "premium_feel": 3.0},
        "clarity": {"profile_segment": "clarity", "delivery_confidence": 3.8, "setup_clarity": 4.8, "core_quality": 4.0, "social_proof_pull": 3.4, "premium_feel": 3.6},
        "premium": {"profile_segment": "premium", "delivery_confidence": 3.6, "setup_clarity": 4.0, "core_quality": 4.8, "social_proof_pull": 3.1, "premium_feel": 4.9},
    }
    brand_offsets = {
        "BrandA": {"core_quality": 0.3},
        "BrandB": {"delivery_confidence": 0.4, "social_proof_pull": 0.2},
        "BrandC": {"premium_feel": 0.5, "setup_clarity": 0.3},
    }
    brands = ["BrandA", "BrandB", "BrandC"]
    for cluster_name, base in cluster_patterns.items():
        for idx in range(12):
            brand = brands[idx % len(brands)]
            row: dict[str, object] = {
                "review_id": f"{cluster_name}-review-{idx}",
                "unit_id": f"{cluster_name}-unit-{idx}",
                "brand": brand,
                "profile_region": ["north", "central", "south"][idx % 3],
            }
            for column, value in base.items():
                if column.startswith("profile_"):
                    row[column] = value
                    continue
                row[column] = round(min(value + ((idx % 3) * 0.05) + brand_offsets.get(brand, {}).get(column, 0.0), 5.0), 2)
            rows.append(row)
    return rows


def build_partial_segmentation_rows() -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for idx in range(24):
        rows.append({"unit_id": f"value-{idx}", "profile_region": "north", "profile_age_band": "25-34", "value_seek": 4.8 + ((idx % 3) * 0.05), "trust_seek": 4.4 + ((idx % 2) * 0.05), "design_seek": 2.3 + ((idx % 2) * 0.05)})
    for idx in range(24):
        rows.append({"unit_id": f"convenience-{idx}", "profile_region": "central", "profile_age_band": "35-44", "value_seek": 3.2 + ((idx % 3) * 0.05), "trust_seek": 3.9 + ((idx % 2) * 0.05), "design_seek": 4.5 + ((idx % 2) * 0.05)})
    for idx in range(24):
        rows.append({"unit_id": f"premium-{idx}", "profile_region": "south", "profile_age_band": "45-54", "value_seek": 2.8 + ((idx % 3) * 0.05), "trust_seek": 4.1 + ((idx % 2) * 0.05), "design_seek": 4.9 + ((idx % 2) * 0.05)})
    return rows


def make_canonical_input_dir(
    base: Path,
    dimension_catalog: list[dict[str, object]] | None = None,
    rows: list[dict[str, object]] | None = None,
    include_analysis_context: bool = True,
    include_dimension_catalog: bool = True,
    include_theme_mapping: bool = True,
    complete_theme_mapping: bool = True,
    include_similarity: bool = False,
) -> Path:
    input_dir = base / "input"
    input_dir.mkdir()
    catalog = dimension_catalog or build_dimension_catalog_14()
    write_csv(input_dir / "review_scoring_table.csv", rows or build_review_scoring_rows_14())
    write_json(input_dir / "review_foundation.json", build_review_foundation(catalog, include_dimension_catalog, include_theme_mapping, complete_theme_mapping))
    if include_analysis_context:
        default_axes = ["delivery_confidence", "social_proof_pull"]
        comparison_axes = default_axes if catalog == build_dimension_catalog_custom() else None
        write_json(input_dir / "analysis_context.json", build_analysis_context(comparison_axes))
    write_json(input_dir / "brands.json", build_brands_payload(include_similarity))
    positioning_columns = [item["column"] for item in catalog if "positioning" in item["stat_roles"]]
    write_json(input_dir / "ideal_point.json", build_ideal_point(positioning_columns))
    return input_dir


def make_partial_input_dir(base: Path) -> Path:
    input_dir = base / "input"
    input_dir.mkdir()
    write_json(input_dir / "review_foundation.json", build_review_foundation())
    write_csv(input_dir / "segmentation_variables.csv", build_partial_segmentation_rows())
    write_json(input_dir / "analysis_context.json", build_analysis_context())
    return input_dir


class ReviewMiningStpScriptsTest(unittest.TestCase):
    maxDiff = None

    def run_command(self, args: list[str], cwd: Path) -> subprocess.CompletedProcess[str]:
        return subprocess.run([sys.executable, *args], cwd=cwd, text=True, capture_output=True, check=False)

    def test_full_run_accepts_canonical_inputs_and_emits_intermediate_artifacts(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            input_dir = make_canonical_input_dir(tmp_path)
            output_dir = tmp_path / "output"

            result = self.run_command([str(RUN_SCRIPT), "--run-mode", "full", "--input-dir", str(input_dir), "--output-dir", str(output_dir)], cwd=ROOT)
            self.assertEqual(result.returncode, 0, result.stderr)

            expected = [
                "report.md",
                "appendix.json",
                "segment_profiles.json",
                "segment_summary.md",
                "targeting_results.json",
                "target_selection_decision.json",
                "perceptual_map.png",
                "perceptual_map_coordinates.csv",
                "perceptual_map_vectors.csv",
                "positioning_diagnostics.json",
                "strategy_matrix.json",
                "segmentation_variables.csv",
                "targeting_dataset.csv",
                "positioning_scorecard.csv",
            ]
            for filename in expected:
                self.assertTrue((output_dir / filename).exists(), filename)

            validator = self.run_command([str(VALIDATE_SCRIPT), "--run-mode", "full", "--output-dir", str(output_dir)], cwd=ROOT)
            self.assertEqual(validator.returncode, 0, validator.stderr)

            appendix = json.loads((output_dir / "appendix.json").read_text(encoding="utf-8"))
            execution_scope = appendix["execution_scope"]
            self.assertIn("review_scoring_table.csv", execution_scope["upstream_artifacts_used"])
            self.assertIn("review_foundation.json", execution_scope["upstream_artifacts_used"])
            self.assertIn("analysis_context.json", execution_scope["upstream_artifacts_used"])
            self.assertIn("brands.json", execution_scope["upstream_artifacts_used"])
            self.assertIn("ideal_point.json", execution_scope["upstream_artifacts_used"])
            self.assertEqual(sorted(execution_scope["emitted_intermediate_artifacts"]), ["positioning_scorecard.csv", "segmentation_variables.csv", "targeting_dataset.csv"])
            self.assertTrue(appendix["targeting_summary"]["target_selection_decision"]["priority_segments"])
            self.assertTrue(appendix["targeting_summary"]["target_selection_decision"]["comparison_axes_used"])

    def test_full_run_supports_flexible_non_14_dimension_schema(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            catalog = build_dimension_catalog_custom()
            input_dir = make_canonical_input_dir(tmp_path, dimension_catalog=catalog, rows=build_review_scoring_rows_custom())
            output_dir = tmp_path / "output"

            result = self.run_command([str(RUN_SCRIPT), "--run-mode", "full", "--input-dir", str(input_dir), "--output-dir", str(output_dir)], cwd=ROOT)
            self.assertEqual(result.returncode, 0, result.stderr)

            validator = self.run_command([str(VALIDATE_SCRIPT), "--run-mode", "full", "--output-dir", str(output_dir)], cwd=ROOT)
            self.assertEqual(validator.returncode, 0, validator.stderr)

            appendix = json.loads((output_dir / "appendix.json").read_text(encoding="utf-8"))
            attributes = {row["attribute"] for row in appendix["positioning_summary"]["positioning_scorecard"] if row["point_type"] == "brand"}
            self.assertIn("setup_clarity", attributes)
            self.assertIn("premium_feel", attributes)

    def test_segmentation_partial_run_still_supports_direct_intermediate_artifacts(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            input_dir = make_partial_input_dir(tmp_path)
            output_dir = tmp_path / "output"

            result = self.run_command([str(RUN_SCRIPT), "--run-mode", "segmentation", "--input-dir", str(input_dir), "--output-dir", str(output_dir)], cwd=ROOT)
            self.assertEqual(result.returncode, 0, result.stderr)

            payload = json.loads((output_dir / "segment_profiles.json").read_text(encoding="utf-8"))
            shares = [item["share"] for item in payload["segment_profiles"]]
            self.assertTrue(all(share > 0.05 for share in shares))
            self.assertEqual(payload["cluster_selection"]["method"], "factor_analysis -> kmeans")
            self.assertTrue(payload["consumer_portrait_narrative"])

    def test_targeting_partial_run_works_with_emitted_intermediates(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            input_dir = make_canonical_input_dir(tmp_path)
            full_dir = tmp_path / "full"
            targeting_dir = tmp_path / "targeting"

            full_result = self.run_command([str(RUN_SCRIPT), "--run-mode", "full", "--input-dir", str(input_dir), "--output-dir", str(full_dir)], cwd=ROOT)
            self.assertEqual(full_result.returncode, 0, full_result.stderr)

            result = self.run_command(
                [str(RUN_SCRIPT), "--run-mode", "targeting", "--input-dir", str(full_dir), "--upstream-artifacts-dir", str(full_dir), "--output-dir", str(targeting_dir)],
                cwd=ROOT,
            )
            self.assertEqual(result.returncode, 0, result.stderr)

            targeting = json.loads((targeting_dir / "targeting_results.json").read_text(encoding="utf-8"))
            decision = targeting["target_selection_decision"]
            self.assertTrue(decision["priority_segments"])
            self.assertTrue(decision["secondary_segments"] or decision["deprioritized_segments"])
            self.assertEqual(decision["comparison_axes_used"], build_analysis_context()["comparison_axes"])

    def test_positioning_mds_does_not_fabricate_attribute_vectors(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            input_dir = make_canonical_input_dir(tmp_path, include_similarity=True)
            output_dir = tmp_path / "output"

            result = self.run_command([str(RUN_SCRIPT), "--run-mode", "positioning", "--input-dir", str(input_dir), "--output-dir", str(output_dir), "--positioning-method", "mds"], cwd=ROOT)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertFalse((output_dir / "perceptual_map_vectors.csv").exists())

            diagnostics = json.loads((output_dir / "positioning_diagnostics.json").read_text(encoding="utf-8"))
            self.assertTrue(diagnostics["attribute_vectors_not_defined"])
            self.assertEqual(diagnostics["projection_interpretation"]["status"], "not_available")

    def test_custom_missing_prerequisite_lists_only_true_missing_intermediate(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            input_dir = tmp_path / "input"
            input_dir.mkdir()
            write_json(input_dir / "brands.json", build_brands_payload())
            write_json(input_dir / "ideal_point.json", build_ideal_point())
            output_dir = tmp_path / "output"

            result = self.run_command([str(RUN_SCRIPT), "--run-mode", "custom", "--requested-modules", "perceptual-map", "--input-dir", str(input_dir), "--output-dir", str(output_dir)], cwd=ROOT)
            self.assertEqual(result.returncode, 0, result.stderr)
            payload = json.loads((output_dir / "MissingPrerequisiteOutput.json").read_text(encoding="utf-8"))
            self.assertEqual(payload["missing_prerequisites"], ["positioning_scorecard.csv"])
            self.assertIn("positioning_scorecard.csv", payload["acceptable_upstream_artifacts"])

    def test_full_run_rejects_missing_dimension_catalog(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            input_dir = make_canonical_input_dir(tmp_path, include_dimension_catalog=False)
            output_dir = tmp_path / "output"

            result = self.run_command([str(RUN_SCRIPT), "--run-mode", "full", "--input-dir", str(input_dir), "--output-dir", str(output_dir)], cwd=ROOT)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("dimension_catalog", result.stderr)

    def test_full_run_rejects_incomplete_theme_mapping(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            input_dir = make_canonical_input_dir(tmp_path, complete_theme_mapping=False)
            output_dir = tmp_path / "output"

            result = self.run_command([str(RUN_SCRIPT), "--run-mode", "full", "--input-dir", str(input_dir), "--output-dir", str(output_dir)], cwd=ROOT)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("theme_mapping", result.stderr)

    def test_full_run_rejects_insufficient_score_columns(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            input_dir = make_canonical_input_dir(
                tmp_path,
                dimension_catalog=build_dimension_catalog_custom()[:2],
                rows=[
                    {"review_id": "r1", "unit_id": "u1", "brand": "BrandA", "delivery_confidence": 4.5, "setup_clarity": 4.1},
                    {"review_id": "r2", "unit_id": "u2", "brand": "BrandB", "delivery_confidence": 3.8, "setup_clarity": 4.4},
                ],
            )
            output_dir = tmp_path / "output"

            result = self.run_command([str(RUN_SCRIPT), "--run-mode", "full", "--input-dir", str(input_dir), "--output-dir", str(output_dir)], cwd=ROOT)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("at least 3", result.stderr.lower())

    def test_raw_reviews_are_rejected_until_agent_layer_creates_scored_artifacts(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            input_dir = tmp_path / "input"
            input_dir.mkdir()
            write_json(input_dir / "reviews.json", [{"review_id": "r1", "review_text": "Fast shipping, good value."}])
            output_dir = tmp_path / "output"

            result = self.run_command([str(RUN_SCRIPT), "--run-mode", "full", "--input-dir", str(input_dir), "--output-dir", str(output_dir)], cwd=ROOT)
            self.assertEqual(result.returncode, 0, result.stderr)
            payload = json.loads((output_dir / "MissingPrerequisiteOutput.json").read_text(encoding="utf-8"))
            self.assertIn("review_scoring_table.csv", payload["missing_prerequisites"])
            self.assertIn("agent layer", payload["next_step_rule"].lower())

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

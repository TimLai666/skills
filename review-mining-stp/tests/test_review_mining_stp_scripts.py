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


def make_dimension(
    column: str,
    label: str,
    theme: str,
    attribute_group: str,
    theory_tags: list[str],
    theory_annotations: dict[str, list[str]],
    stat_roles: list[str],
    plain_language_definition: str,
) -> dict[str, object]:
    return {
        "column": column,
        "label": label,
        "theme": theme,
        "attribute_group": attribute_group,
        "salience_column": f"{column}_salience",
        "valence_column": f"{column}_valence",
        "theory_tags": theory_tags,
        "theory_annotations": theory_annotations,
        "stat_roles": stat_roles,
        "plain_language_definition": plain_language_definition,
    }


def build_dimension_catalog_base() -> list[dict[str, object]]:
    return [
        make_dimension("fast_delivery", "Fast Delivery", "service_journey", "attribute_function", ["purchase_motivation", "system1"], {"purchase_motivation": ["functional"], "dual_process": ["system1"]}, ["segmentation", "current_target", "comparison_axis"], "How strongly the review says delivery was quick and hassle-free."),
        make_dimension("support_trust", "Support Trust", "service_journey", "benefit_use", ["safety", "wom_motivation"], {"purchase_motivation": ["security"], "wom_motivation": ["altruistic"], "maslow": ["safety"]}, ["current_target", "comparison_axis"], "How strongly the review signals trust in support and issue handling."),
        make_dimension("setup_ease", "Setup Ease", "ease_of_use", "benefit_use", ["purchase_motivation", "system2"], {"purchase_motivation": ["functional"], "dual_process": ["system2"]}, ["segmentation", "positioning"], "How clearly the review says setup or usage felt easy."),
        make_dimension("product_quality", "Product Quality", "product_excellence", "attribute_function", ["product_positioning", "esteem"], {"product_positioning": ["benefits"], "maslow": ["esteem"]}, ["current_target", "positioning"], "How strongly the review praises core quality."),
        make_dimension("value_for_money", "Value For Money", "value_and_advocacy", "benefit_use", ["purchase_motivation", "esteem"], {"purchase_motivation": ["functional"], "product_positioning": ["functions"], "maslow": ["esteem"]}, ["potential_target", "positioning", "comparison_axis"], "How strongly the review says the brand was worth the price paid."),
        make_dimension("recommendation_pull", "Recommendation Pull", "value_and_advocacy", "brand_image", ["wom_motivation", "belonging"], {"wom_motivation": ["social_identity", "self_enhancement"], "maslow": ["social"]}, ["segmentation", "potential_target"], "How strongly the review implies recommending or talking about the brand."),
    ]


def build_dimension_catalog_custom() -> list[dict[str, object]]:
    return [
        make_dimension("delivery_confidence", "Delivery Confidence", "assurance", "attribute_function", ["safety", "system1"], {"purchase_motivation": ["security"], "dual_process": ["system1"], "maslow": ["safety"]}, ["segmentation", "current_target", "comparison_axis"], "How strongly the review says fulfillment felt dependable."),
        make_dimension("communication_clarity", "Communication Clarity", "assurance", "benefit_use", ["wom_motivation", "belonging"], {"wom_motivation": ["altruistic", "social_identity"], "maslow": ["social"]}, ["current_target", "comparison_axis"], "How clearly the review says communication was easy to follow."),
        make_dimension("install_simplicity", "Install Simplicity", "assurance", "benefit_use", ["purchase_motivation", "system2"], {"purchase_motivation": ["functional"], "dual_process": ["system2"]}, ["segmentation", "positioning"], "How strongly the review says installation was simple."),
        make_dimension("premium_finish", "Premium Finish", "market_signal", "brand_personality", ["product_positioning", "esteem"], {"product_positioning": ["benefits"], "maslow": ["esteem"]}, ["segmentation", "positioning"], "How strongly the review frames the product as polished and premium."),
        make_dimension("everyday_value", "Everyday Value", "market_signal", "benefit_use", ["purchase_motivation", "esteem"], {"purchase_motivation": ["functional"], "product_positioning": ["functions"], "maslow": ["esteem"]}, ["potential_target", "positioning", "comparison_axis"], "How strongly the review says the brand creates practical value."),
        make_dimension("social_proof_pull", "Social Proof Pull", "market_signal", "brand_image", ["wom_motivation", "belonging"], {"wom_motivation": ["social_identity", "self_enhancement"], "maslow": ["social"]}, ["segmentation", "potential_target"], "How strongly the review suggests telling others or showing the brand to peers."),
    ]


def build_theme_mapping(catalog: list[dict[str, object]]) -> dict[str, list[str]]:
    mapping: dict[str, list[str]] = {}
    for item in catalog:
        mapping.setdefault(str(item["theme"]), []).append(str(item["column"]))
    return mapping


def build_review_foundation(
    *,
    catalog: list[dict[str, object]],
    theme_mapping_override: dict[str, list[str]] | None = None,
    include_theme_mapping: bool = True,
    complete_theme_mapping: bool = True,
    scoring_rubric: dict[str, object] | None = None,
    attribute_extraction_summary: dict[str, object] | None = None,
) -> dict[str, object]:
    payload: dict[str, object] = {
        "dimension_catalog": catalog,
        "people_insights": ["value buyers", "convenience buyers", "quality seekers"],
        "product_triggers": ["delivery speed", "quality confidence", "ease of setup"],
        "context_scenarios": ["first purchase", "repeat purchase", "gift purchase"],
        "system1_system2_split": {"system1": ["instant confidence"], "system2": ["price-value justification"]},
        "maslow_keywords": {"safety": ["trust"], "belonging": ["recommend"], "esteem": ["premium"]},
        "attribute_extraction_summary": attribute_extraction_summary or {"target_minimum": 30, "actual_count": len(catalog), "shortfall_reason": "Synthetic fixture uses fewer than 30 attributes to keep tests small."},
    }
    if scoring_rubric is not None:
        payload["scoring_rubric"] = scoring_rubric
    if include_theme_mapping:
        theme_mapping = theme_mapping_override if theme_mapping_override is not None else build_theme_mapping(catalog)
        if not complete_theme_mapping and theme_mapping:
            theme_mapping.pop(next(reversed(theme_mapping)), None)
        payload["theme_mapping"] = theme_mapping
    return payload


def build_analysis_context(comparison_axes: list[str]) -> dict[str, object]:
    return {
        "analysis_goal": "Convert dual-axis review scoring into STP outputs.",
        "comparison_axes": comparison_axes,
        "scope_limits": ["Scripts operate on scored artifacts only.", "Raw review interpretation belongs to the agent layer."],
    }


def build_brands_payload(include_similarity: bool = False) -> dict[str, object]:
    payload: dict[str, object] = {"brands": ["BrandA", "BrandB", "BrandC"]}
    if include_similarity:
        payload["similarity_matrix"] = [[0.0, 0.42, 0.63], [0.42, 0.0, 0.51], [0.63, 0.51, 0.0]]
    return payload


def build_ideal_point(catalog: list[dict[str, object]]) -> dict[str, object]:
    attributes: dict[str, object] = {}
    for index, item in enumerate([row for row in catalog if "positioning" in row["stat_roles"]]):
        attributes[str(item["column"])] = {"salience": max(4, 7 - index), "valence": max(7, 10 - index)}
    return {"label": "IdealPoint", "attributes": attributes}


def _clamp(value: int, low: int, high: int) -> int:
    return max(low, min(high, int(value)))


def build_rows_from_profiles(
    profiles: dict[str, dict[str, object]],
    *,
    brands: list[str],
    products: dict[str, str],
    zero_out_column: str,
) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for profile_name, profile in profiles.items():
        for idx in range(12):
            brand = brands[idx % len(brands)]
            row: dict[str, object] = {
                "review_id": f"{profile_name}-review-{idx}",
                "unit_id": f"{profile_name}-unit-{idx}",
                "brand": brand,
                "product": products[brand],
                "review_text": str(profile["texts"][idx % len(profile["texts"])]) .format(brand=brand, product=products[brand]),
                "profile_lifestyle": profile["profile_lifestyle"],
                "profile_region": profile["profile_region"],
                "channel": "app_store" if idx % 2 == 0 else "marketplace",
                "rating": int(profile["rating"]),
            }
            for column, (salience, valence) in profile["scores"].items():
                s = _clamp(int(salience), 0, 7)
                v = _clamp(int(valence), 0, 10)
                if idx % 5 == 0 and column in {zero_out_column, "fast_delivery", "setup_ease", "delivery_confidence", "install_simplicity"}:
                    s = _clamp(s + 1, 0, 7)
                if idx % 7 == 0 and column in {"product_quality", "value_for_money", "premium_finish", "everyday_value"}:
                    v = _clamp(v - 1, 0, 10)
                if idx % 6 == 0 and column == zero_out_column:
                    s = 0
                row[f"{column}_salience"] = s
                row[f"{column}_valence"] = "" if s == 0 else v
            rows.append(row)
    return rows


def build_review_rows_base() -> list[dict[str, object]]:
    return build_rows_from_profiles(
        {
            "value": {"profile_lifestyle": "value", "profile_region": "north", "rating": 5, "scores": {"fast_delivery": (5, 8), "support_trust": (5, 7), "setup_ease": (4, 7), "product_quality": (4, 6), "value_for_money": (7, 9), "recommendation_pull": (6, 8)}, "texts": ["{brand} arrived quickly and felt worth the money. I would buy this {product} again because it solves the basics without wasting cash.", "{brand} gave me solid delivery and fair value. It is easy to recommend when someone wants dependable quality at a sensible price."]},
            "convenience": {"profile_lifestyle": "convenience", "profile_region": "central", "rating": 6, "scores": {"fast_delivery": (6, 8), "support_trust": (6, 8), "setup_ease": (7, 9), "product_quality": (5, 7), "value_for_money": (5, 7), "recommendation_pull": (5, 7)}, "texts": ["{brand} was easy to set up and support answered fast. The whole experience felt smooth and reliable from start to finish.", "I picked {brand} because everything was simple. Delivery was quick, setup was painless, and support made me trust the purchase."]},
            "premium": {"profile_lifestyle": "premium", "profile_region": "south", "rating": 7, "scores": {"fast_delivery": (4, 6), "support_trust": (5, 7), "setup_ease": (6, 8), "product_quality": (7, 10), "value_for_money": (4, 6), "recommendation_pull": (5, 8)}, "texts": ["{brand} looks premium and the build quality feels excellent. It gives a polished impression that stands above cheaper options.", "The finish on {brand} feels upscale and carefully made. I trust the quality enough to mention it when friends ask what I bought."]},
        },
        brands=["BrandA", "BrandB", "BrandC"],
        products={"BrandA": "Core", "BrandB": "Plus", "BrandC": "Ultra"},
        zero_out_column="recommendation_pull",
    )


def build_review_rows_custom() -> list[dict[str, object]]:
    return build_rows_from_profiles(
        {
            "assurance": {"profile_lifestyle": "assurance", "profile_region": "north", "rating": 5, "scores": {"delivery_confidence": (7, 8), "communication_clarity": (6, 8), "install_simplicity": (4, 6), "premium_finish": (4, 6), "everyday_value": (5, 7), "social_proof_pull": (5, 7)}, "texts": ["{brand} felt dependable from shipping to follow-up messages. The clear updates made the whole order easy to trust.", "I trust {brand} because delivery was predictable and communication stayed clear the whole time."]},
            "ease": {"profile_lifestyle": "ease", "profile_region": "central", "rating": 6, "scores": {"delivery_confidence": (5, 7), "communication_clarity": (5, 7), "install_simplicity": (7, 9), "premium_finish": (5, 7), "everyday_value": (6, 8), "social_proof_pull": (4, 6)}, "texts": ["{brand} was simple to install and easy to fit into daily use. It feels useful without adding friction.", "The best part of {brand} is how quickly everything works. Setup is simple and the product keeps paying off in normal use."]},
            "prestige": {"profile_lifestyle": "prestige", "profile_region": "south", "rating": 7, "scores": {"delivery_confidence": (4, 6), "communication_clarity": (4, 6), "install_simplicity": (5, 7), "premium_finish": (7, 10), "everyday_value": (4, 6), "social_proof_pull": (6, 8)}, "texts": ["{brand} feels premium in a way people notice immediately. I would gladly show it to friends because it looks elevated.", "The finish on {brand} is polished and premium. It stands out enough that I talk about it when people ask."]},
        },
        brands=["BrandA", "BrandB", "BrandC"],
        products={"BrandA": "Studio", "BrandB": "Flow", "BrandC": "Prime"},
        zero_out_column="social_proof_pull",
    )


def build_attribute_catalog(catalog: list[dict[str, object]], rows: list[dict[str, object]]) -> list[dict[str, object]]:
    review_lookup = {str(row["review_id"]): str(row["review_text"]) for row in rows}
    output_rows: list[dict[str, object]] = []
    for item in catalog:
        salience_column = str(item["salience_column"])
        candidates = [row for row in rows if int(row.get(salience_column, 0) or 0) >= 1]
        example = candidates[0] if candidates else rows[0]
        output_rows.append({"attribute_key": item["column"], "label": item["label"], "theme": item["theme"], "attribute_group": item["attribute_group"], "definition": item["plain_language_definition"], "source_type": "agent_extracted", "mention_count": len(candidates), "salience_column": item["salience_column"], "valence_column": item["valence_column"], "example_review_id": example["review_id"], "example_quote": review_lookup[str(example["review_id"])]})
    return output_rows


def build_partial_segmentation_rows() -> list[dict[str, object]]:
    row = {"brand": "BrandB", "product": "Plus", "profile_region": "north", "fast_delivery_salience": 7, "fast_delivery_valence": 8, "support_trust_salience": 6, "support_trust_valence": 7, "setup_ease_salience": 4, "setup_ease_valence": 6, "product_quality_salience": 4, "product_quality_valence": 6, "value_for_money_salience": 7, "value_for_money_valence": 9, "recommendation_pull_salience": 6, "recommendation_pull_valence": 8}
    return [{"unit_id": f"value-{idx}", **row} for idx in range(72)]


def make_canonical_input_dir(
    base: Path,
    *,
    catalog: list[dict[str, object]] | None = None,
    rows: list[dict[str, object]] | None = None,
    include_attribute_catalog: bool = True,
    include_theme_mapping: bool = True,
    complete_theme_mapping: bool = True,
    theme_mapping_override: dict[str, list[str]] | None = None,
    scoring_rubric: dict[str, object] | None = None,
    attribute_extraction_summary: dict[str, object] | None = None,
    include_similarity: bool = False,
) -> Path:
    catalog = catalog or build_dimension_catalog_base()
    rows = rows or build_review_rows_base()
    input_dir = base / "input"
    input_dir.mkdir()
    write_csv(input_dir / "review_scoring_table.csv", rows)
    write_json(input_dir / "review_foundation.json", build_review_foundation(catalog=catalog, include_theme_mapping=include_theme_mapping, complete_theme_mapping=complete_theme_mapping, theme_mapping_override=theme_mapping_override, scoring_rubric=scoring_rubric, attribute_extraction_summary=attribute_extraction_summary))
    if include_attribute_catalog:
        write_csv(input_dir / "attribute_catalog.csv", build_attribute_catalog(catalog, rows))
    comparison_axes = ["delivery_confidence", "communication_clarity", "everyday_value"] if catalog == build_dimension_catalog_custom() else ["fast_delivery", "support_trust", "value_for_money"]
    write_json(input_dir / "analysis_context.json", build_analysis_context(comparison_axes))
    write_json(input_dir / "brands.json", build_brands_payload(include_similarity=include_similarity))
    write_json(input_dir / "ideal_point.json", build_ideal_point(catalog))
    return input_dir


def make_partial_input_dir(base: Path) -> Path:
    input_dir = base / "input"
    input_dir.mkdir()
    write_json(input_dir / "review_foundation.json", build_review_foundation(catalog=build_dimension_catalog_base()))
    write_csv(input_dir / "segmentation_variables.csv", build_partial_segmentation_rows())
    write_json(input_dir / "analysis_context.json", build_analysis_context(["fast_delivery", "support_trust", "value_for_money"]))
    return input_dir


class ReviewMiningStpScriptsTest(unittest.TestCase):
    maxDiff = None

    def run_command(self, args: list[str], cwd: Path) -> subprocess.CompletedProcess[str]:
        return subprocess.run([sys.executable, *args], cwd=cwd, text=True, capture_output=True, check=False)

    def assert_finding_contract(self, finding: dict[str, object], review_lookup: dict[str, str]) -> None:
        self.assertIn(finding["axes_used"], {"salience", "valence", "mixed"})
        self.assertEqual(set(finding["reproducibility"].keys()), {"input_artifacts", "input_columns", "filters", "preprocessing", "analysis_steps", "decision_rule"})
        self.assertEqual(set(finding["statistical_results"].keys()), {"method_family", "test_or_model", "sample_size", "statistic", "degrees_of_freedom", "p_value", "effect_size", "coefficient", "confidence_interval", "result_direction", "axis_breakdown"})
        self.assertEqual(set(finding["statistical_results"]["axis_breakdown"].keys()), {"salience", "valence"})
        for quote in finding["evidence_quotes"]:
            self.assertEqual(quote["quote_text"], review_lookup[quote["review_id"]])

    def test_full_run_accepts_dual_axis_inputs_and_emits_intermediate_artifacts(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            input_dir = make_canonical_input_dir(tmp_path)
            output_dir = tmp_path / "output"
            result = self.run_command([str(RUN_SCRIPT), "--run-mode", "full", "--input-dir", str(input_dir), "--output-dir", str(output_dir)], cwd=ROOT)
            self.assertEqual(result.returncode, 0, result.stderr)
            validator = self.run_command([str(VALIDATE_SCRIPT), "--run-mode", "full", "--output-dir", str(output_dir)], cwd=ROOT)
            self.assertEqual(validator.returncode, 0, validator.stderr)
            appendix = json.loads((output_dir / "appendix.json").read_text(encoding="utf-8"))
            with (output_dir / "review_scoring_table.csv").open(encoding="utf-8", newline="") as handle:
                review_lookup = {row["review_id"]: row["review_text"] for row in csv.DictReader(handle)}
            self.assertIn("attribute_catalog.csv", appendix["execution_scope"]["upstream_artifacts_used"])
            self.assertEqual(appendix["attribute_extraction_summary"]["target_minimum"], 30)
            self.assertTrue(appendix["attribute_extraction_summary"]["representative_attributes"])
            self.assertEqual(sorted(appendix["execution_scope"]["emitted_intermediate_artifacts"]), ["positioning_scorecard.csv", "segmentation_variables.csv", "targeting_dataset.csv"])
            for key in ["segmentation_summary", "targeting_summary", "positioning_summary"]:
                self.assertTrue(appendix[key]["axis_modeling_summary"])
                for finding in appendix[key]["findings"]:
                    self.assert_finding_contract(finding, review_lookup)
            report_text = (output_dir / "report.md").read_text(encoding="utf-8")
            self.assertIn("Attribute Extraction Summary", report_text)
            self.assertIn("Representative attributes", report_text)
            self.assertIn("Axis modeling summary", report_text)
            self.assertIn("System 1 / System 2", report_text)
            self.assertIn("Maslow > Safety", report_text)

    def test_full_run_supports_alternate_dynamic_schema_with_two_themes(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            input_dir = make_canonical_input_dir(tmp_path, catalog=build_dimension_catalog_custom(), rows=build_review_rows_custom())
            output_dir = tmp_path / "output"
            result = self.run_command([str(RUN_SCRIPT), "--run-mode", "full", "--input-dir", str(input_dir), "--output-dir", str(output_dir)], cwd=ROOT)
            self.assertEqual(result.returncode, 0, result.stderr)
            appendix = json.loads((output_dir / "appendix.json").read_text(encoding="utf-8"))
            self.assertEqual({row["theme"] for row in appendix["positioning_summary"]["theme_coverage_summary"]}, {"assurance", "market_signal"})

    def test_segmentation_partial_run_still_supports_direct_intermediate_artifacts(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            input_dir = make_partial_input_dir(tmp_path)
            output_dir = tmp_path / "output"
            result = self.run_command([str(RUN_SCRIPT), "--run-mode", "segmentation", "--input-dir", str(input_dir), "--output-dir", str(output_dir)], cwd=ROOT)
            self.assertEqual(result.returncode, 0, result.stderr)
            payload = json.loads((output_dir / "segment_profiles.json").read_text(encoding="utf-8"))
            self.assertEqual(payload["cluster_selection"]["method"], "factor_analysis -> kmeans")

    def test_targeting_partial_run_uses_comparison_axes_override(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            input_dir = make_canonical_input_dir(tmp_path)
            full_dir = tmp_path / "full"
            targeting_dir = tmp_path / "targeting"
            self.assertEqual(self.run_command([str(RUN_SCRIPT), "--run-mode", "full", "--input-dir", str(input_dir), "--output-dir", str(full_dir)], cwd=ROOT).returncode, 0)
            result = self.run_command([str(RUN_SCRIPT), "--run-mode", "targeting", "--input-dir", str(full_dir), "--upstream-artifacts-dir", str(full_dir), "--output-dir", str(targeting_dir)], cwd=ROOT)
            self.assertEqual(result.returncode, 0, result.stderr)
            targeting = json.loads((targeting_dir / "targeting_results.json").read_text(encoding="utf-8"))
            self.assertEqual(targeting["target_selection_decision"]["comparison_axes_used"], ["fast_delivery_salience", "fast_delivery_valence", "support_trust_salience", "support_trust_valence", "value_for_money_salience", "value_for_money_valence"])

    def test_positioning_mds_does_not_fabricate_attribute_vectors(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            input_dir = make_canonical_input_dir(tmp_path, include_similarity=True)
            output_dir = tmp_path / "output"
            result = self.run_command([str(RUN_SCRIPT), "--run-mode", "positioning", "--input-dir", str(input_dir), "--output-dir", str(output_dir), "--positioning-method", "mds"], cwd=ROOT)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertFalse((output_dir / "perceptual_map_vectors.csv").exists())
            self.assertTrue((output_dir / "perceptual_map.png").exists())

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
            result = self.run_command([str(RUN_SCRIPT), "--run-mode", "full", "--input-dir", str(make_canonical_input_dir(tmp_path, rows=rows)), "--output-dir", str(tmp_path / "output")], cwd=ROOT)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("review_text", result.stderr)

    def test_full_run_rejects_missing_product_and_missing_pair(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            rows = build_review_rows_base()
            for row in rows:
                row.pop("product", None)
            result = self.run_command([str(RUN_SCRIPT), "--run-mode", "full", "--input-dir", str(make_canonical_input_dir(tmp_path, rows=rows)), "--output-dir", str(tmp_path / "output")], cwd=ROOT)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("product", result.stderr)
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            rows = build_review_rows_base()
            for row in rows:
                row.pop("fast_delivery_valence", None)
            result = self.run_command([str(RUN_SCRIPT), "--run-mode", "full", "--input-dir", str(make_canonical_input_dir(tmp_path, rows=rows)), "--output-dir", str(tmp_path / "output")], cwd=ROOT)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("fast_delivery_valence", result.stderr)

    def test_full_run_rejects_invalid_axis_values(self) -> None:
        cases = [
            ("fast_delivery_salience", 8, "0-7"),
            ("fast_delivery_valence", 11, "0-10"),
            ("recommendation_pull_salience", 0, "must be empty", "recommendation_pull_valence", 7),
            ("fast_delivery_valence", "", "must be present", "fast_delivery_salience", 4),
        ]
        for case in cases:
            with tempfile.TemporaryDirectory() as tmp:
                tmp_path = Path(tmp)
                rows = build_review_rows_base()
                rows[0][case[0]] = case[1]
                if len(case) == 5:
                    rows[0][case[3]] = case[4]
                result = self.run_command([str(RUN_SCRIPT), "--run-mode", "full", "--input-dir", str(make_canonical_input_dir(tmp_path, rows=rows)), "--output-dir", str(tmp_path / "output")], cwd=ROOT)
                self.assertNotEqual(result.returncode, 0)
                self.assertIn(case[2], result.stderr)

    def test_full_run_accepts_optional_scoring_rubric_metadata(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            input_dir = make_canonical_input_dir(tmp_path, scoring_rubric={"salience": {"0": "none"}, "valence": {"0-10": "sentiment"}})
            result = self.run_command([str(RUN_SCRIPT), "--run-mode", "full", "--input-dir", str(input_dir), "--output-dir", str(tmp_path / "output")], cwd=ROOT)
            self.assertEqual(result.returncode, 0, result.stderr)

    def test_full_run_requires_attribute_catalog_and_valid_attribute_contract(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            input_dir = make_canonical_input_dir(tmp_path, include_attribute_catalog=False)
            output_dir = tmp_path / "output"
            result = self.run_command([str(RUN_SCRIPT), "--run-mode", "full", "--input-dir", str(input_dir), "--output-dir", str(output_dir)], cwd=ROOT)
            self.assertEqual(result.returncode, 0, result.stderr)
            payload = json.loads((output_dir / "MissingPrerequisiteOutput.json").read_text(encoding="utf-8"))
            self.assertIn("attribute_catalog.csv", payload["missing_prerequisites"])
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            input_dir = make_canonical_input_dir(tmp_path)
            with (input_dir / "attribute_catalog.csv").open(encoding="utf-8", newline="") as handle:
                rows = list(csv.DictReader(handle))
            rows[0]["salience_column"] = "wrong_salience_column"
            write_csv(input_dir / "attribute_catalog.csv", rows)
            result = self.run_command([str(RUN_SCRIPT), "--run-mode", "full", "--input-dir", str(input_dir), "--output-dir", str(tmp_path / "output")], cwd=ROOT)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("attribute_catalog.csv", result.stderr)

    def test_full_run_rejects_shortfall_without_reason_and_bad_theme_mapping(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            input_dir = make_canonical_input_dir(tmp_path, attribute_extraction_summary={"target_minimum": 30, "actual_count": 6, "shortfall_reason": ""})
            result = self.run_command([str(RUN_SCRIPT), "--run-mode", "full", "--input-dir", str(input_dir), "--output-dir", str(tmp_path / "output")], cwd=ROOT)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("shortfall_reason", result.stderr)
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            catalog = build_dimension_catalog_base()
            theme_mapping = build_theme_mapping(catalog)
            theme_mapping["ease_of_use"].append("fast_delivery")
            input_dir = make_canonical_input_dir(tmp_path, catalog=catalog, theme_mapping_override=theme_mapping)
            result = self.run_command([str(RUN_SCRIPT), "--run-mode", "full", "--input-dir", str(input_dir), "--output-dir", str(tmp_path / "output")], cwd=ROOT)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("multiple themes", result.stderr)

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
            self.assertIn("attribute_catalog.csv", payload["missing_prerequisites"])
            self.assertIn("agent layer", payload["next_step_rule"].lower())

    def test_validator_rejects_quote_and_axis_contract_breaks(self) -> None:
        scenarios = [("segmentation_summary", "evidence_quotes", "Hallucinated quote", "evidence quote"), ("segmentation_summary", "axis_modeling_summary", None, "axis_modeling_summary"), ("positioning_summary", "axes_used", None, "axes_used"), ("positioning_summary", "axis_breakdown", None, "axis_breakdown"), ("attribute_extraction_summary", "example_quote", "Hallucinated quote", "attribute_extraction_summary")]
        for section_name, broken_key, broken_value, message in scenarios:
            with tempfile.TemporaryDirectory() as tmp:
                tmp_path = Path(tmp)
                input_dir = make_canonical_input_dir(tmp_path)
                output_dir = tmp_path / "output"
                self.assertEqual(self.run_command([str(RUN_SCRIPT), "--run-mode", "full", "--input-dir", str(input_dir), "--output-dir", str(output_dir)], cwd=ROOT).returncode, 0)
                appendix = json.loads((output_dir / "appendix.json").read_text(encoding="utf-8"))
                if broken_key == "evidence_quotes":
                    appendix[section_name][broken_key][0]["quote_text"] = str(broken_value)
                elif broken_key == "example_quote":
                    appendix[section_name]["representative_attributes"][0]["example_quote"] = str(broken_value)
                elif broken_key == "axis_modeling_summary":
                    appendix[section_name].pop(broken_key, None)
                elif broken_key == "axes_used":
                    appendix[section_name]["findings"][0].pop("axes_used", None)
                else:
                    appendix[section_name]["findings"][0]["statistical_results"].pop("axis_breakdown", None)
                write_json(output_dir / "appendix.json", appendix)
                validator = self.run_command([str(VALIDATE_SCRIPT), "--run-mode", "full", "--output-dir", str(output_dir)], cwd=ROOT)
                self.assertNotEqual(validator.returncode, 0)
                self.assertIn(message, validator.stderr.lower())

    def test_validator_accepts_positioning_summary_without_public_vector_fields(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            input_dir = make_canonical_input_dir(tmp_path)
            output_dir = tmp_path / "output"
            self.assertEqual(self.run_command([str(RUN_SCRIPT), "--run-mode", "full", "--input-dir", str(input_dir), "--output-dir", str(output_dir)], cwd=ROOT).returncode, 0)
            appendix = json.loads((output_dir / "appendix.json").read_text(encoding="utf-8"))
            appendix["positioning_summary"].pop("perceptual_map_vector_table", None)
            appendix["positioning_summary"].pop("projection_interpretation", None)
            write_json(output_dir / "appendix.json", appendix)
            validator = self.run_command([str(VALIDATE_SCRIPT), "--run-mode", "full", "--output-dir", str(output_dir)], cwd=ROOT)
            self.assertEqual(validator.returncode, 0, validator.stderr)


if __name__ == "__main__":
    unittest.main()

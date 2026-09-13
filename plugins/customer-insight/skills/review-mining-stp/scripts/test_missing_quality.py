import tempfile
import json
import unittest
from pathlib import Path

import pandas as pd
from stp_runner.io import validate_canonical_inputs, aggregate_review_scoring_table, build_positioning_scorecard

FIXTURE = Path(__file__).resolve().parents[1] / "fixtures/minimal"

class MissingQualityTests(unittest.TestCase):
    def setUp(self):
        self.scores = pd.read_csv(FIXTURE / "review_scoring_table.csv")
        self.foundation = json.loads((FIXTURE / "review_foundation.json").read_text())
        self.catalog = pd.read_csv(FIXTURE / "attribute_catalog.csv")
        item = self.foundation["dimension_catalog"][0]
        self.base, self.sal, self.qual = item["column"], item["salience_column"], item["quality_column"]

    def contract(self):
        return validate_canonical_inputs(self.scores, self.foundation, self.catalog)

    def test_mentioned_without_evaluation_is_valid(self):
        self.scores.loc[0, self.sal] = 7
        self.scores.loc[0, self.qual] = float("nan")
        self.contract()

    def test_unmentioned_with_quality_is_rejected(self):
        self.scores.loc[0, self.sal] = 0
        self.scores.loc[0, self.qual] = 5
        with self.assertRaises(SystemExit):
            self.contract()

    def test_means_preserve_missing_and_real_zero_with_counts(self):
        contract = self.contract()
        self.scores[self.sal] = 7
        self.scores[self.qual] = float("nan")
        self.scores.loc[0, self.qual] = 0
        units = aggregate_review_scoring_table(self.scores, contract)
        self.assertTrue(units[self.qual].isna().any())
        self.assertEqual(units[self.base + "_evaluation_count"].sum(), 1)
        card = build_positioning_scorecard(self.scores, contract)
        quality = card[(card.attribute == self.base) & (card.axis == "quality")]
        self.assertEqual(quality.evaluation_count.sum(), 1)
        self.assertEqual(quality.mention_count.sum(), len(self.scores))
        self.assertEqual(quality.score.dropna().tolist(), [0.0])

    def test_documented_extra_family_is_valid(self):
        self.foundation["theory_extensions"] = {"service_quality": {"rationale": "Service evidence", "subtheories": ["reliability"]}}
        self.foundation["dimension_catalog"][0]["theory_annotations"] = {"service_quality": ["reliability"]}
        self.contract()

    def test_undocumented_extra_family_rejected(self):
        self.foundation["dimension_catalog"][0]["theory_annotations"] = {"unknown": ["unknown"]}
        with self.assertRaises(SystemExit):
            self.contract()

    def test_segmentation_omits_incomplete_quality(self):
        from stp_runner.io import build_segmentation_variables
        from stp_runner.segmentation import run_segmentation
        contract = self.contract()
        self.scores.loc[0, self.qual] = float("nan")
        units = aggregate_review_scoring_table(self.scores, contract)
        result = run_segmentation(self.foundation, build_segmentation_variables(units, contract))
        self.assertIn(self.qual, result["excluded_missing_features"])
        self.assertEqual(len(result["segment_assignments"]), len(units))

    def test_positioning_omits_sparse_quality_and_keeps_missing(self):
        from stp_runner.positioning import run_positioning
        contract = self.contract()
        self.scores.loc[self.scores.brand == self.scores.brand.iloc[0], self.qual] = float("nan")
        card = build_positioning_scorecard(self.scores, contract)
        with tempfile.TemporaryDirectory() as directory:
            result = run_positioning(card, json.loads((FIXTURE / "brands.json").read_text()), json.loads((FIXTURE / "ideal_point.json").read_text()), "factor_analysis", Path(directory))
        self.assertIn(self.qual, result["excluded_missing_features"])
        self.assertTrue(any(row["score"] is None for row in result["positioning_scorecard"]))

    def test_observed_and_missing_mean_uses_only_evaluations(self):
        contract = self.contract()
        self.scores[self.sal] = 7
        self.scores[self.qual] = float("nan")
        self.scores["brand"] = "One"
        self.scores["unit_id"] = "One"
        self.scores.loc[0, self.qual] = 0
        self.scores.loc[1, self.qual] = 8
        units = aggregate_review_scoring_table(self.scores, contract)
        self.assertEqual(units[self.qual].tolist(), [4.0])
        self.assertEqual(units[self.base + "_evaluation_count"].tolist(), [2])

    def test_all_empty_quality_stays_empty(self):
        contract = self.contract()
        for pair in contract["pair_columns_by_base"].values():
            self.scores[pair["quality"]] = float("nan")
        card = build_positioning_scorecard(self.scores, contract)
        self.assertTrue(card.loc[card.axis == "quality", "score"].isna().all())
        self.assertTrue((card.evaluation_count == 0).all())

    def test_incomplete_target_response_uses_observed_rows(self):
        import math
        from stp_runner.targeting import run_targeting
        dataset = pd.DataFrame({"cluster": ["a"] * 4 + ["b"] * 4, "q": [1, 2, 3, float("nan"), 5, 6, 7, 8]})
        result = run_targeting(dataset, {"segment_profiles": []}, ["q"], {"current_target": ["q"], "potential_target": ["q"]})
        self.assertTrue(math.isfinite(result["current_target_market"][0]["regression_r2"]))

    def test_ranking_uses_axes_observed_for_every_cluster(self):
        from stp_runner.targeting import run_targeting
        dataset = pd.DataFrame({"cluster": ["a"] * 4 + ["b"] * 4, "q": [1, 2, 3, 4] + [float("nan")] * 4, "s": [1, 2, 3, 4, 4, 5, 6, 7]})
        result = run_targeting(dataset, {"segment_profiles": []}, ["q", "s"], {"current_target": ["q", "s"], "potential_target": ["q", "s"]})
        self.assertEqual(result["target_selection_decision"]["comparison_axes_used"], ["s"])
        self.assertEqual(result["excluded_comparison_axes"], ["q"])
        with self.assertRaisesRegex(SystemExit, "complete"):
            run_targeting(dataset, {"segment_profiles": []}, ["q"], {"current_target": ["q"], "potential_target": ["q"]})

    def test_theory_gap_is_derived_without_forcing_coverage(self):
        for item in self.foundation["dimension_catalog"]:
            item["theory_annotations"] = {"product_positioning": ["attributes"]}
        self.foundation["attribute_extraction_summary"].pop("theory_gap", None)
        result = self.contract()
        self.assertEqual(set(result["attribute_extraction_summary"]["theory_gap"]), {"maslow", "purchase_motivation", "wom_motivation"})
        self.foundation["attribute_extraction_summary"]["theory_gap"] = "maslow"
        with self.assertRaises(SystemExit):
            self.contract()

    def test_full_cli_preserves_completed_modules_when_positioning_blocked(self):
        import shutil
        import subprocess
        import sys
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / "input"
            output = Path(directory) / "output"
            shutil.copytree(FIXTURE, source)
            self.scores[self.qual] = float("nan")
            self.scores.to_csv(source / "review_scoring_table.csv", index=False)
            (source / "ideal_point.json").write_text(json.dumps({"label": "Ideal", "attributes": {self.base: {"salience": 6, "quality": 9}}}))
            result = subprocess.run([sys.executable, str(Path(__file__).parent / "run_review_mining_stp.py"), "--run-mode", "full", "--input-dir", str(source), "--output-dir", str(output)], capture_output=True, text=True)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("Excluded incomplete features", result.stderr)
            self.assertTrue((output / "segment_profiles.json").exists())
            self.assertTrue((output / "targeting_results.json").exists())
            self.assertFalse((output / "report.md").exists())

    def test_output_validator_rejects_missing_or_malformed_gap(self):
        from stp_runner.reporting import build_attribute_extraction_summary_contract
        from stp_runner.validation import _validate_attribute_extraction_summary
        summary = build_attribute_extraction_summary_contract(self.foundation, self.catalog)
        summary["theory_gap"] = "maslow"
        with self.assertRaises(SystemExit):
            _validate_attribute_extraction_summary(summary, {})
        summary.pop("theory_gap")
        with self.assertRaises(SystemExit):
            _validate_attribute_extraction_summary(summary, {})

if __name__ == "__main__":
    unittest.main()

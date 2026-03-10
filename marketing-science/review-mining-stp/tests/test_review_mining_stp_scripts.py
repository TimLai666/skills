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


def build_review_foundation() -> dict[str, object]:
    return {
        "people_insights": ["家庭採購者偏好高可靠度與便利性"],
        "product_triggers": ["續航", "易清潔", "價格合理"],
        "context_scenarios": ["通勤", "辦公室", "居家"],
        "system1_system2_split": {
            "system1": ["外觀", "第一印象", "品牌感"],
            "system2": ["規格", "耐用度", "售後"],
        },
        "maslow_keywords": {
            "physiological": ["便利", "省時"],
            "safety": ["耐用", "可靠"],
            "belonging": ["家庭", "分享"],
            "esteem": ["質感", "專業"],
            "self_actualization": ["升級", "探索"],
        },
        "evidence": ["評論基礎樣本 60 筆"],
    }


def build_segmentation_rows() -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for idx in range(20):
        rows.append(
            {
                "customer_id": f"budget-{idx}",
                "geo_region": "north",
                "age_group": "25-34",
                "psychographic": "value",
                "behavior_frequency": 2 + (idx % 2),
                "motivation_score": 2.0 + (idx % 3) * 0.1,
                "value_seek": 4.6 + (idx % 4) * 0.1,
                "convenience_seek": 2.0 + (idx % 3) * 0.1,
                "status_seek": 1.0 + (idx % 2) * 0.1,
            }
        )
    for idx in range(20):
        rows.append(
            {
                "customer_id": f"busy-{idx}",
                "geo_region": "central",
                "age_group": "35-44",
                "psychographic": "convenience",
                "behavior_frequency": 5 + (idx % 2),
                "motivation_score": 4.1 + (idx % 3) * 0.1,
                "value_seek": 2.2 + (idx % 4) * 0.1,
                "convenience_seek": 4.7 + (idx % 3) * 0.1,
                "status_seek": 2.2 + (idx % 2) * 0.1,
            }
        )
    for idx in range(20):
        rows.append(
            {
                "customer_id": f"premium-{idx}",
                "geo_region": "south",
                "age_group": "45-54",
                "psychographic": "status",
                "behavior_frequency": 4 + (idx % 2),
                "motivation_score": 4.7 + (idx % 3) * 0.1,
                "value_seek": 2.1 + (idx % 4) * 0.1,
                "convenience_seek": 3.1 + (idx % 3) * 0.1,
                "status_seek": 4.8 + (idx % 2) * 0.1,
            }
        )
    return rows


def build_targeting_rows(include_profiles: bool = True) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    specs = {
        "segment_0": (140, 4.6, 0.88, 1, 1, 4.2, "female", "shopping", "variety"),
        "segment_1": (95, 3.9, 0.52, 1, 0, 3.6, "male", "gaming", "news"),
        "segment_2": (70, 3.2, 0.31, 0, 0, 2.4, "male", "sports", "drama"),
    }
    for cluster, (
        value,
        loyalty,
        active,
        potential,
        tried,
        intent,
        gender,
        leisure,
        channel,
    ) in specs.items():
        for idx in range(18):
            row: dict[str, object] = {
                "cluster": cluster,
                "current_value": value + idx,
                "loyalty_score": loyalty + (idx % 4) * 0.05,
                "active_rate": active - (idx % 3) * 0.01,
                "potential_conversion": potential,
                "tried_before": tried,
                "intent_score": intent + (idx % 3) * 0.1,
            }
            if include_profiles:
                row["profile_gender"] = gender
                row["profile_leisure"] = leisure if idx % 5 else "mixed"
                row["profile_channel"] = channel
            rows.append(row)
    return rows


def build_positioning_rows() -> list[dict[str, object]]:
    return [
        {"brand": "BrandA", "attribute": "quality", "score": 4.6},
        {"brand": "BrandA", "attribute": "value", "score": 3.4},
        {"brand": "BrandA", "attribute": "convenience", "score": 4.2},
        {"brand": "BrandA", "attribute": "personality", "score": 4.1},
        {"brand": "BrandB", "attribute": "quality", "score": 3.7},
        {"brand": "BrandB", "attribute": "value", "score": 4.5},
        {"brand": "BrandB", "attribute": "convenience", "score": 3.2},
        {"brand": "BrandB", "attribute": "personality", "score": 3.1},
        {"brand": "BrandC", "attribute": "quality", "score": 4.1},
        {"brand": "BrandC", "attribute": "value", "score": 2.9},
        {"brand": "BrandC", "attribute": "convenience", "score": 4.7},
        {"brand": "BrandC", "attribute": "personality", "score": 4.6},
    ]


def build_brands_payload(include_similarity: bool = False) -> dict[str, object]:
    payload: dict[str, object] = {"brands": ["BrandA", "BrandB", "BrandC"]}
    if include_similarity:
        payload["similarity_matrix"] = [
            [0.0, 0.4, 0.3],
            [0.4, 0.0, 0.6],
            [0.3, 0.6, 0.0],
        ]
    return payload


def build_ideal_point() -> dict[str, object]:
    return {
        "label": "IdealPoint",
        "attributes": {
            "quality": 4.9,
            "value": 4.2,
            "convenience": 4.8,
            "personality": 4.5,
        },
    }


def make_input_dir(base: Path, include_similarity: bool = False, include_profiles: bool = True) -> Path:
    input_dir = base / "input"
    input_dir.mkdir()
    write_json(input_dir / "review_foundation.json", build_review_foundation())
    write_csv(input_dir / "segmentation_variables.csv", build_segmentation_rows())
    write_csv(input_dir / "targeting_dataset.csv", build_targeting_rows(include_profiles=include_profiles))
    write_csv(input_dir / "positioning_scorecard.csv", build_positioning_rows())
    write_json(input_dir / "brands.json", build_brands_payload(include_similarity=include_similarity))
    write_json(input_dir / "ideal_point.json", build_ideal_point())
    return input_dir


class ReviewMiningStpScriptsTest(unittest.TestCase):
    maxDiff = None

    def run_command(self, args: list[str], cwd: Path) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, *args],
            cwd=cwd,
            text=True,
            capture_output=True,
            check=False,
        )

    def test_full_run_generates_required_outputs_and_passes_validation(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            input_dir = make_input_dir(tmp_path)
            output_dir = tmp_path / "output"

            result = self.run_command(
                [
                    str(RUN_SCRIPT),
                    "--run-mode",
                    "full",
                    "--input-dir",
                    str(input_dir),
                    "--output-dir",
                    str(output_dir),
                ],
                cwd=ROOT,
            )
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
            ]
            for filename in expected:
                self.assertTrue((output_dir / filename).exists(), filename)

            validator = self.run_command(
                [
                    str(VALIDATE_SCRIPT),
                    "--run-mode",
                    "full",
                    "--output-dir",
                    str(output_dir),
                ],
                cwd=ROOT,
            )
            self.assertEqual(validator.returncode, 0, validator.stderr)

            targeting = json.loads((output_dir / "targeting_results.json").read_text(encoding="utf-8"))
            self.assertIn("profile_significance_summary", targeting)
            self.assertEqual(targeting["profile_significance_summary"]["status"], "available")
            self.assertIn("pairwise_comparison_table", targeting)
            self.assertTrue(targeting["pairwise_comparison_table"])

            diagnostics = json.loads(
                (output_dir / "positioning_diagnostics.json").read_text(encoding="utf-8")
            )
            self.assertIn("projection_interpretation", diagnostics)
            self.assertEqual(diagnostics["projection_interpretation"]["status"], "defined")

            appendix = json.loads((output_dir / "appendix.json").read_text(encoding="utf-8"))
            self.assertIn("proactive_marketing_notes", appendix)
            self.assertIn("usp_translation_candidates", appendix)

    def test_segmentation_only_outputs_clusters_above_threshold(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            input_dir = make_input_dir(tmp_path)
            output_dir = tmp_path / "output"

            result = self.run_command(
                [
                    str(RUN_SCRIPT),
                    "--run-mode",
                    "segmentation",
                    "--input-dir",
                    str(input_dir),
                    "--output-dir",
                    str(output_dir),
                ],
                cwd=ROOT,
            )
            self.assertEqual(result.returncode, 0, result.stderr)

            payload = json.loads((output_dir / "segment_profiles.json").read_text(encoding="utf-8"))
            shares = [item["share"] for item in payload["segment_profiles"]]
            self.assertTrue(all(share > 0.05 for share in shares))
            self.assertTrue(payload["cluster_selection"]["all_clusters_above_threshold"])

    def test_positioning_mds_does_not_fabricate_attribute_vectors(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            input_dir = make_input_dir(tmp_path, include_similarity=True)
            output_dir = tmp_path / "output"

            result = self.run_command(
                [
                    str(RUN_SCRIPT),
                    "--run-mode",
                    "positioning",
                    "--input-dir",
                    str(input_dir),
                    "--output-dir",
                    str(output_dir),
                    "--positioning-method",
                    "mds",
                ],
                cwd=ROOT,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertTrue((output_dir / "perceptual_map.png").exists())
            self.assertTrue((output_dir / "perceptual_map_coordinates.csv").exists())
            self.assertFalse((output_dir / "perceptual_map_vectors.csv").exists())

            diagnostics = json.loads(
                (output_dir / "positioning_diagnostics.json").read_text(encoding="utf-8")
            )
            self.assertTrue(diagnostics["attribute_vectors_not_defined"])
            self.assertEqual(diagnostics["projection_interpretation"]["status"], "not_available")

    def test_custom_missing_prerequisite_writes_missing_prerequisite_output(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            input_dir = tmp_path / "input"
            input_dir.mkdir()
            write_json(input_dir / "review_foundation.json", build_review_foundation())
            output_dir = tmp_path / "output"

            result = self.run_command(
                [
                    str(RUN_SCRIPT),
                    "--run-mode",
                    "custom",
                    "--requested-modules",
                    "perceptual-map",
                    "--input-dir",
                    str(input_dir),
                    "--output-dir",
                    str(output_dir),
                ],
                cwd=ROOT,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertTrue((output_dir / "MissingPrerequisiteOutput.json").exists())

    def test_validator_rejects_non_origin_vectors(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            input_dir = make_input_dir(tmp_path)
            output_dir = tmp_path / "output"

            result = self.run_command(
                [
                    str(RUN_SCRIPT),
                    "--run-mode",
                    "positioning",
                    "--input-dir",
                    str(input_dir),
                    "--output-dir",
                    str(output_dir),
                ],
                cwd=ROOT,
            )
            self.assertEqual(result.returncode, 0, result.stderr)

            with (output_dir / "perceptual_map_vectors.csv").open(encoding="utf-8") as handle:
                rows = list(csv.DictReader(handle))
            rows[0]["x_start"] = "1"
            with (output_dir / "perceptual_map_vectors.csv").open(
                "w", newline="", encoding="utf-8"
            ) as handle:
                writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
                writer.writeheader()
                writer.writerows(rows)

            validator = self.run_command(
                [
                    str(VALIDATE_SCRIPT),
                    "--run-mode",
                    "positioning",
                    "--output-dir",
                    str(output_dir),
                ],
                cwd=ROOT,
            )
            self.assertNotEqual(validator.returncode, 0)
            self.assertIn("origin", validator.stderr.lower())

    def test_targeting_without_profile_columns_reports_not_available(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            input_dir = make_input_dir(tmp_path, include_profiles=False)
            output_dir = tmp_path / "output"

            result = self.run_command(
                [
                    str(RUN_SCRIPT),
                    "--run-mode",
                    "full",
                    "--input-dir",
                    str(input_dir),
                    "--output-dir",
                    str(output_dir),
                ],
                cwd=ROOT,
            )
            self.assertEqual(result.returncode, 0, result.stderr)

            targeting = json.loads((output_dir / "targeting_results.json").read_text(encoding="utf-8"))
            summary = targeting["profile_significance_summary"]
            self.assertEqual(summary["status"], "not_available")
            self.assertTrue(summary["reason"])

            validator = self.run_command(
                [
                    str(VALIDATE_SCRIPT),
                    "--run-mode",
                    "full",
                    "--output-dir",
                    str(output_dir),
                ],
                cwd=ROOT,
            )
            self.assertEqual(validator.returncode, 0, validator.stderr)

    def test_validator_rejects_missing_projection_interpretation(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            input_dir = make_input_dir(tmp_path)
            output_dir = tmp_path / "output"

            result = self.run_command(
                [
                    str(RUN_SCRIPT),
                    "--run-mode",
                    "positioning",
                    "--input-dir",
                    str(input_dir),
                    "--output-dir",
                    str(output_dir),
                ],
                cwd=ROOT,
            )
            self.assertEqual(result.returncode, 0, result.stderr)

            diagnostics = json.loads(
                (output_dir / "positioning_diagnostics.json").read_text(encoding="utf-8")
            )
            diagnostics.pop("projection_interpretation", None)
            write_json(output_dir / "positioning_diagnostics.json", diagnostics)

            validator = self.run_command(
                [
                    str(VALIDATE_SCRIPT),
                    "--run-mode",
                    "positioning",
                    "--output-dir",
                    str(output_dir),
                ],
                cwd=ROOT,
            )
            self.assertNotEqual(validator.returncode, 0)
            self.assertIn("projection_interpretation", validator.stderr)


if __name__ == "__main__":
    unittest.main()

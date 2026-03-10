from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path
from typing import Any


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate review-mining-stp outputs.")
    parser.add_argument(
        "--run-mode",
        required=True,
        choices=["full", "segmentation", "targeting", "positioning", "custom"],
    )
    parser.add_argument("--output-dir", required=True)
    return parser.parse_args()


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def fail(message: str) -> None:
    print(message, file=sys.stderr)
    raise SystemExit(1)


def require_output_files(output_dir: Path, names: list[str]) -> None:
    missing = [name for name in names if not (output_dir / name).exists()]
    if missing:
        fail(f"Missing required output files: {', '.join(missing)}")


def validate_positioning(output_dir: Path) -> None:
    require_output_files(
        output_dir,
        [
            "perceptual_map.png",
            "perceptual_map_coordinates.csv",
            "positioning_diagnostics.json",
            "strategy_matrix.json",
        ],
    )
    if (output_dir / "perceptual_map.png").stat().st_size == 0:
        fail("perceptual_map.png is empty")

    diagnostics = read_json(output_dir / "positioning_diagnostics.json")
    method = read_json(output_dir / "run_metadata.json").get("positioning_method", "factor_analysis")

    with (output_dir / "perceptual_map_coordinates.csv").open(encoding="utf-8") as handle:
        coordinate_rows = list(csv.DictReader(handle))
    point_types = {row["point_type"] for row in coordinate_rows}
    if "brand" not in point_types:
        fail("Perceptual map must retain brand points.")
    if "ideal" not in point_types:
        fail("Perceptual map must retain ideal point.")

    vector_path = output_dir / "perceptual_map_vectors.csv"
    if method == "mds" and diagnostics.get("attribute_vectors_not_defined"):
        if vector_path.exists():
            fail("MDS output must not fabricate attribute vectors.")
        return

    if not vector_path.exists():
        fail("Factor-analysis perceptual map requires a vector table.")

    with vector_path.open(encoding="utf-8") as handle:
        vector_rows = list(csv.DictReader(handle))
    if not vector_rows:
        fail("Vector table is empty.")
    for row in vector_rows:
        if float(row["x_start"]) != 0.0 or float(row["y_start"]) != 0.0:
            fail("Attribute vectors must start at the origin.")

    pod_pop = diagnostics.get("pod_pop", {})
    if "pod" not in pod_pop or "pop" not in pod_pop:
        fail("Positioning diagnostics must contain POD/POP.")


def validate_appendix(output_dir: Path, run_mode: str) -> None:
    require_output_files(output_dir, ["appendix.json", "report.md", "run_metadata.json"])
    appendix = read_json(output_dir / "appendix.json")
    if "execution_scope" not in appendix:
        fail("Appendix is missing execution_scope.")
    if run_mode in {"full", "segmentation"} and not appendix.get("segmentation_summary"):
        fail("Appendix is missing segmentation_summary.")
    if run_mode in {"full", "targeting"} and not appendix.get("targeting_summary"):
        fail("Appendix is missing targeting_summary.")
    if run_mode in {"full", "positioning"} and not appendix.get("positioning_summary"):
        fail("Appendix is missing positioning_summary.")


def main() -> None:
    args = parse_args()
    output_dir = Path(args.output_dir)

    if (output_dir / "MissingPrerequisiteOutput.json").exists():
        print("Validation skipped because output is a MissingPrerequisiteOutput artifact.")
        return

    require_output_files(output_dir, ["report.md", "appendix.json", "run_metadata.json"])

    if args.run_mode == "full":
        require_output_files(
            output_dir,
            [
                "segment_profiles.json",
                "segment_summary.md",
                "targeting_results.json",
                "target_selection_decision.json",
            ],
        )
        validate_positioning(output_dir)
    elif args.run_mode == "segmentation":
        require_output_files(output_dir, ["segment_profiles.json", "segment_summary.md"])
    elif args.run_mode == "targeting":
        require_output_files(output_dir, ["targeting_results.json", "target_selection_decision.json"])
    elif args.run_mode == "positioning":
        validate_positioning(output_dir)

    validate_appendix(output_dir, args.run_mode)
    print("Validation passed.")

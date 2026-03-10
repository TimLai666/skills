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
    mds_without_vectors = bool(method == "mds" and diagnostics.get("attribute_vectors_not_defined"))
    if mds_without_vectors:
        if vector_path.exists():
            fail("MDS output must not fabricate attribute vectors.")
    else:
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

    projection = diagnostics.get("projection_interpretation")
    if not isinstance(projection, dict):
        fail("Positioning diagnostics must contain projection_interpretation.")
    status = projection.get("status")
    if status not in {"defined", "not_available"}:
        fail("projection_interpretation status must be defined or not_available.")
    if method == "factor_analysis":
        if status != "defined":
            fail("Factor-analysis run must provide a defined projection interpretation.")
        summary_rows = projection.get("attribute_projection_summary")
        if not isinstance(summary_rows, list) or not summary_rows:
            fail("Factor-analysis projection interpretation must include attribute projection summary.")
        if not projection.get("importance_interpretation"):
            fail("Factor-analysis projection interpretation must include importance interpretation text.")
    if mds_without_vectors:
        if status != "not_available":
            fail("MDS run without vectors must mark projection interpretation as not_available.")
        if not projection.get("reason"):
            fail("MDS projection interpretation must include an explicit not_available reason.")


def validate_targeting(output_dir: Path) -> None:
    require_output_files(output_dir, ["targeting_results.json", "target_selection_decision.json"])
    targeting = read_json(output_dir / "targeting_results.json")

    profile_significance = targeting.get("profile_significance_summary")
    if not isinstance(profile_significance, dict):
        fail("Targeting results must contain profile_significance_summary.")
    profile_status = profile_significance.get("status")
    if profile_status == "available":
        variables = profile_significance.get("variables")
        if not isinstance(variables, list) or not variables:
            fail("profile_significance_summary.status=available requires non-empty variables.")
        for item in variables:
            if not isinstance(item, dict):
                fail("profile_significance_summary.variables items must be objects.")
            required_keys = {"variable", "method", "p_value", "significant"}
            if not required_keys.issubset(item.keys()):
                fail("Each profile significance result must include variable/method/p_value/significant.")
    elif profile_status == "not_available":
        if not profile_significance.get("reason"):
            fail("profile_significance_summary.status=not_available requires reason.")
    else:
        fail("profile_significance_summary.status must be available or not_available.")

    pairwise_table = targeting.get("pairwise_comparison_table")
    if not isinstance(pairwise_table, list):
        fail("Targeting results must contain pairwise_comparison_table.")
    for row in pairwise_table:
        if not isinstance(row, dict):
            fail("pairwise_comparison_table entries must be objects.")
        required_keys = {"variable", "comparison", "p_value", "significant"}
        if not required_keys.issubset(row.keys()):
            fail("Each pairwise comparison row must include variable/comparison/p_value/significant.")

    significant_anova_variables = set()
    for bucket in ["current_target_market", "potential_target_market"]:
        for record in targeting.get(bucket, []):
            anova = record.get("anova")
            if not isinstance(anova, dict):
                continue
            p_value = float(anova.get("p_value", 1.0))
            if p_value < 0.05:
                significant_anova_variables.add(str(record.get("variable")))
    pairwise_variables = {str(row.get("variable")) for row in pairwise_table}
    missing_pairwise = sorted(
        variable
        for variable in significant_anova_variables
        if variable and variable not in pairwise_variables
    )
    if missing_pairwise:
        fail(
            "Missing pairwise comparisons for ANOVA-significant variables: "
            + ", ".join(missing_pairwise)
        )


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

    targeting_summary = appendix.get("targeting_summary")
    if isinstance(targeting_summary, dict):
        if "profile_significance_summary" not in targeting_summary:
            fail("targeting_summary is missing profile_significance_summary.")
        if "pairwise_comparison_table" not in targeting_summary:
            fail("targeting_summary is missing pairwise_comparison_table.")

    positioning_summary = appendix.get("positioning_summary")
    if isinstance(positioning_summary, dict):
        if "projection_interpretation" not in positioning_summary:
            fail("positioning_summary is missing projection_interpretation.")

    for optional_key in ["proactive_marketing_notes", "usp_translation_candidates"]:
        if optional_key in appendix and not isinstance(appendix[optional_key], list):
            fail(f"{optional_key} must be a list when present.")


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
        validate_targeting(output_dir)
        validate_positioning(output_dir)
    elif args.run_mode == "segmentation":
        require_output_files(output_dir, ["segment_profiles.json", "segment_summary.md"])
    elif args.run_mode == "targeting":
        validate_targeting(output_dir)
    elif args.run_mode == "positioning":
        validate_positioning(output_dir)

    validate_appendix(output_dir, args.run_mode)
    print("Validation passed.")

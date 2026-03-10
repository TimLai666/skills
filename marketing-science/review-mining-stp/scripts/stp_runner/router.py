from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any

from .constants import ALLOWED_CUSTOM_MODULES, RUN_MODE_MODULES
from .io import build_missing_prereq_output, write_json
from .positioning import load_positioning_inputs, run_positioning
from .reporting import write_execution_files
from .segmentation import build_segment_summary, load_segmentation_inputs, run_segmentation
from .targeting import load_targeting_inputs, run_targeting


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run review-mining-stp analysis from artifacts.")
    parser.add_argument(
        "--run-mode",
        required=True,
        choices=["full", "segmentation", "targeting", "positioning", "custom"],
    )
    parser.add_argument("--requested-modules", default="", help="Comma-separated custom modules")
    parser.add_argument("--input-dir", required=True, help="Path to artifact directory")
    parser.add_argument("--output-dir", required=True, help="Path to output directory")
    parser.add_argument(
        "--upstream-artifacts-dir",
        help="Optional second artifact directory used for stage-specific runs",
    )
    parser.add_argument(
        "--positioning-method",
        choices=["factor_analysis", "mds"],
        default="factor_analysis",
    )
    parser.add_argument("--ideal-point-file", help="Optional explicit ideal point JSON path")
    parser.add_argument("--brands-file", help="Optional explicit brands JSON path")
    return parser.parse_args()


def ensure_dependencies() -> None:
    try:
        import matplotlib  # noqa: F401
        import numpy  # noqa: F401
        import pandas  # noqa: F401
        import scipy  # noqa: F401
        import sklearn  # noqa: F401
        import statsmodels  # noqa: F401
    except ImportError as exc:
        print(
            "Missing dependency. Install required packages from requirements.txt before running.",
            file=sys.stderr,
        )
        raise SystemExit(1) from exc


def parse_requested_modules(args: argparse.Namespace) -> list[str]:
    if args.run_mode != "custom":
        return list(RUN_MODE_MODULES[args.run_mode])
    modules = [item.strip() for item in args.requested_modules.split(",") if item.strip()]
    if not modules:
        raise SystemExit("--requested-modules is required when --run-mode custom.")
    unknown = [item for item in modules if item not in ALLOWED_CUSTOM_MODULES]
    if unknown:
        raise SystemExit(f"Unsupported custom modules: {', '.join(sorted(unknown))}")
    return modules


def build_recommended_extensions(
    targeting_summary: dict[str, Any] | None,
    positioning_summary: dict[str, Any] | None,
) -> tuple[list[str], list[dict[str, Any]]]:
    proactive_marketing_notes: list[str] = []
    usp_translation_candidates: list[dict[str, Any]] = []

    if targeting_summary:
        decision = targeting_summary.get("target_selection_decision", {})
        selected_cluster = decision.get("selected_cluster", "selected segment")
        proactive_marketing_notes.append(
            f"Prioritize demand-shaping messages for {selected_cluster} instead of only reactive conversion tactics."
        )

    if positioning_summary:
        pod = positioning_summary.get("positioning_diagnostics", {}).get("pod_pop", {}).get("pod", [])
        if pod:
            proactive_marketing_notes.append(
                "Use strongest POD attributes to define category meaning, not just compare with current competitors."
            )
        projection = positioning_summary.get("projection_interpretation", {})
        if projection.get("status") == "defined":
            proactive_marketing_notes.append(
                "Focus creative direction on attributes with the highest ideal-point projection scores."
            )

    if targeting_summary and positioning_summary:
        decision = targeting_summary.get("target_selection_decision", {})
        persona = decision.get("persona", "")
        selected_cluster = decision.get("selected_cluster", "selected segment")
        pod = positioning_summary.get("positioning_diagnostics", {}).get("pod_pop", {}).get("pod", [])
        for attribute in pod[:3]:
            usp_translation_candidates.append(
                {
                    "target_cluster": selected_cluster,
                    "usp_attribute": attribute,
                    "usp_statement": f"For {selected_cluster}, lead with {attribute} as the primary differentiation claim.",
                    "persona_anchor": persona,
                }
            )

    return proactive_marketing_notes, usp_translation_candidates


def main() -> None:
    ensure_dependencies()
    args = parse_args()

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    artifact_paths = [Path(args.input_dir)]
    if args.upstream_artifacts_dir:
        artifact_paths.append(Path(args.upstream_artifacts_dir))

    requested_modules = parse_requested_modules(args)

    appendix: dict[str, Any] = {
        "execution_scope": {
            "run_mode": args.run_mode,
            "requested_modules": requested_modules,
        },
        "segmentation_summary": None,
        "targeting_summary": None,
        "positioning_summary": None,
        "integrated_stp_actions": [],
        "proactive_marketing_notes": [],
        "usp_translation_candidates": [],
        "risks_bias_confidence_notes": [
            "Upstream artifacts are assumed to be generated by the agent layer.",
            "Statistical outputs are decision support, not causal proof.",
        ],
        "evidence": [],
    }

    generated_segmentation: dict[str, Any] | None = None

    segmentation_needed = any(
        module in requested_modules
        for module in ["review-foundation", "segmentation-variables", "segment-clustering", "segment-profiles"]
    ) or args.run_mode == "full"
    targeting_needed = any(
        module in requested_modules
        for module in ["current-target-market", "potential-target-market", "target-selection"]
    ) or args.run_mode == "full"
    positioning_needed = any(
        module in requested_modules
        for module in ["positioning-scorecard", "perceptual-map", "positioning-diagnostics", "strategy-matrix"]
    ) or args.run_mode == "full"

    if segmentation_needed:
        segmentation_inputs = load_segmentation_inputs(artifact_paths)
        if segmentation_inputs is None:
            build_missing_prereq_output(
                output_dir,
                args.run_mode,
                requested_modules,
                ["review_foundation.json", "segmentation_variables.csv"],
            )
            return
        generated_segmentation = run_segmentation(*segmentation_inputs)
        write_json(output_dir / "segment_profiles.json", generated_segmentation)
        (output_dir / "segment_summary.md").write_text(
            build_segment_summary(generated_segmentation),
            encoding="utf-8",
        )
        appendix["segmentation_summary"] = generated_segmentation

    if targeting_needed:
        targeting_inputs = load_targeting_inputs(artifact_paths, generated_segmentation)
        if targeting_inputs is None:
            build_missing_prereq_output(
                output_dir,
                args.run_mode,
                requested_modules,
                ["segment_profiles.json", "targeting_dataset.csv"],
            )
            return
        targeting = run_targeting(*targeting_inputs)
        write_json(output_dir / "targeting_results.json", targeting)
        write_json(output_dir / "target_selection_decision.json", targeting["target_selection_decision"])
        appendix["targeting_summary"] = targeting
        appendix["integrated_stp_actions"].append(
            {
                "stage": "targeting",
                "selected_cluster": targeting["target_selection_decision"]["selected_cluster"],
                "rationale": targeting["target_selection_decision"]["rationale"],
            }
        )

    if positioning_needed:
        positioning_inputs = load_positioning_inputs(
            artifact_paths, args.ideal_point_file, args.brands_file
        )
        if positioning_inputs is None:
            build_missing_prereq_output(
                output_dir,
                args.run_mode,
                requested_modules,
                ["positioning_scorecard.csv", "brands.json", "ideal_point.json"],
            )
            return
        positioning = run_positioning(*positioning_inputs, args.positioning_method, output_dir)
        write_json(output_dir / "positioning_diagnostics.json", positioning["positioning_diagnostics"])
        write_json(output_dir / "strategy_matrix.json", positioning["strategy_matrix"])
        appendix["positioning_summary"] = positioning
        appendix["integrated_stp_actions"].append(
            {
                "stage": "positioning",
                "method": positioning["positioning_method_used"],
                "pod": positioning["positioning_diagnostics"]["pod_pop"]["pod"],
                "pop": positioning["positioning_diagnostics"]["pod_pop"]["pop"],
            }
        )

    proactive_marketing_notes, usp_translation_candidates = build_recommended_extensions(
        appendix.get("targeting_summary"),
        appendix.get("positioning_summary"),
    )
    appendix["proactive_marketing_notes"] = proactive_marketing_notes
    appendix["usp_translation_candidates"] = usp_translation_candidates

    write_execution_files(output_dir, args.run_mode, requested_modules, appendix, args.positioning_method)

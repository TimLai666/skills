from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .io import write_json


def write_report(output_dir: Path, run_mode: str, appendix: dict[str, Any]) -> None:
    execution_scope = appendix.get("execution_scope", {})
    lines = [
        "# Review Mining STP Report",
        "",
        "## Execution Scope Summary",
        f"- run_mode: {run_mode}",
        f"- requested modules: {', '.join(execution_scope.get('requested_modules', [])) or 'none'}",
        f"- executed modules: {', '.join(execution_scope.get('modules_executed', [])) or 'none'}",
        f"- upstream artifacts used: {', '.join(execution_scope.get('upstream_artifacts_used', [])) or 'none'}",
        f"- emitted intermediates: {', '.join(execution_scope.get('emitted_intermediate_artifacts', [])) or 'none'}",
        f"- comparison axes: {', '.join(execution_scope.get('comparison_axes', [])) or 'none'}",
        f"- brands: {', '.join(execution_scope.get('brands', [])) or 'none'}",
        f"- positioning method: {execution_scope.get('positioning_method_used', 'unknown')}",
        f"- cluster threshold: {execution_scope.get('cluster_threshold', 'n/a')}",
        f"- reruns performed: {execution_scope.get('reruns_performed', 0)}",
        f"- final_k: {execution_scope.get('final_k', 'n/a')}",
        f"- scope limits: {'; '.join(execution_scope.get('scope_limits', [])) or 'none'}",
        "",
        "## Risks / Bias / Confidence Notes",
        "- Output quality depends on the quality of upstream scored artifacts.",
        "- Statistical outputs are directional; validate with domain review before decisions.",
    ]

    segmentation = appendix.get("segmentation_summary")
    if segmentation:
        lines.extend(
            [
                "",
                "## Segmentation Summary",
                f"- clusters: {len(segmentation['segment_profiles'])}",
                f"- selected_k: {segmentation['cluster_selection']['selected_k']}",
                f"- consumer portrait narrative: {segmentation['consumer_portrait_narrative']}",
            ]
        )

    targeting = appendix.get("targeting_summary")
    if targeting:
        profile_significance = targeting.get("profile_significance_summary", {})
        pairwise_rows = targeting.get("pairwise_comparison_table", [])
        lines.extend(
            [
                "",
                "## Targeting Summary",
                f"- selected cluster: {targeting['target_selection_decision']['selected_cluster']}",
                f"- rationale: {targeting['target_selection_rationale']}",
                (
                    "- priority/secondary/deprioritized: "
                    f"{targeting['target_selection_decision']['priority_segments']} / "
                    f"{targeting['target_selection_decision']['secondary_segments']} / "
                    f"{targeting['target_selection_decision']['deprioritized_segments']}"
                ),
                f"- profile significance status: {profile_significance.get('status', 'unknown')}",
                f"- pairwise comparisons: {len(pairwise_rows)}",
            ]
        )

    positioning = appendix.get("positioning_summary")
    if positioning:
        projection = positioning.get("projection_interpretation", {})
        lines.extend(
            [
                "",
                "## Positioning Summary",
                f"- method: {positioning['positioning_method_used']}",
                f"- perceptual map figure: {positioning['perceptual_map_figure']}",
                f"- projection interpretation status: {projection.get('status', 'unknown')}",
                f"- POD: {', '.join(positioning['positioning_diagnostics']['pod_pop']['pod']) or 'none'}",
                f"- POP: {', '.join(positioning['positioning_diagnostics']['pod_pop']['pop']) or 'none'}",
                f"- strategy matrix: {json.dumps(positioning['strategy_matrix'], ensure_ascii=False)}",
            ]
        )

    proactive_notes = appendix.get("proactive_marketing_notes", [])
    usp_candidates = appendix.get("usp_translation_candidates", [])
    if proactive_notes or usp_candidates:
        lines.extend(["", "## Strategy Extensions (Recommended)"])
        if proactive_notes:
            lines.extend([f"- proactive note: {item}" for item in proactive_notes])
        if usp_candidates:
            for candidate in usp_candidates:
                lines.append(
                    "- usp candidate: "
                    f"{candidate.get('usp_attribute')} -> {candidate.get('usp_statement')}"
                )

    (output_dir / "report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_execution_files(
    output_dir: Path,
    run_mode: str,
    requested_modules: list[str],
    appendix: dict[str, Any],
    positioning_method: str,
) -> None:
    write_json(
        output_dir / "run_metadata.json",
        {
            "run_mode": run_mode,
            "requested_modules": requested_modules,
            "positioning_method": positioning_method,
        },
    )
    write_json(output_dir / "appendix.json", appendix)
    write_report(output_dir, run_mode, appendix)

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .io import write_json


THEORY_DETAILS = {
    "product_positioning": {
        "name": "Product Positioning Theory",
        "description": "Used to explain how attributes shape brand meaning and perceived differentiation.",
    },
    "purchase_motivation": {
        "name": "Purchase Motivation Theory",
        "description": "Used to explain which needs and decision drivers are pushing the purchase.",
    },
    "wom_motivation": {
        "name": "Word-of-Mouth Motivation Theory",
        "description": "Used to interpret why reviewers share experiences and recommendations.",
    },
    "dual_process": {
        "name": "System 1 / System 2",
        "description": "Used to separate intuitive reactions from deliberate evaluation.",
    },
    "maslow": {
        "name": "Maslow's Hierarchy of Needs",
        "description": "Used to interpret whether reviews reflect safety, belonging, esteem, or other need layers.",
    },
}

MASLOW_TAGS = {"physiological", "safety", "belonging", "esteem", "self_actualization"}
DUAL_PROCESS_TAGS = {"system1", "system2"}


def _catalog_lookup(foundation: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {
        str(item.get("column")): item
        for item in foundation.get("dimension_catalog", [])
        if isinstance(item, dict) and item.get("column")
    }


def _columns_for_stage(
    foundation: dict[str, Any],
    stage: str,
    stage_summary: dict[str, Any],
) -> list[str]:
    role_map: dict[str, list[str]] = {}
    for item in foundation.get("dimension_catalog", []):
        if not isinstance(item, dict):
            continue
        column = str(item.get("column", ""))
        for role in item.get("stat_roles", []):
            if column:
                role_map.setdefault(str(role), []).append(column)

    if stage == "segmentation":
        return list(dict.fromkeys(role_map.get("segmentation", [])))
    if stage == "targeting":
        return list(
            dict.fromkeys(
                role_map.get("current_target", [])
                + role_map.get("potential_target", [])
                + role_map.get("comparison_axis", [])
            )
        )
    if stage == "positioning":
        columns = [row["attribute"] for row in stage_summary.get("positioning_scorecard", []) if row.get("point_type") == "brand"]
        if columns:
            return list(dict.fromkeys(columns))
        return list(dict.fromkeys(role_map.get("positioning", [])))
    return []


def _theories_for_columns(foundation: dict[str, Any], columns: list[str], include_segmentation_overlays: bool = False) -> list[dict[str, str]]:
    catalog = _catalog_lookup(foundation)
    theory_keys: list[str] = []
    for column in columns:
        item = catalog.get(column, {})
        tags = {str(tag) for tag in item.get("theory_tags", [])}
        if "product_positioning" in tags:
            theory_keys.append("product_positioning")
        if "purchase_motivation" in tags:
            theory_keys.append("purchase_motivation")
        if "wom_motivation" in tags:
            theory_keys.append("wom_motivation")
        if tags & MASLOW_TAGS:
            theory_keys.append("maslow")
        if tags & DUAL_PROCESS_TAGS:
            theory_keys.append("dual_process")
    if include_segmentation_overlays:
        if foundation.get("system1_system2_split"):
            theory_keys.append("dual_process")
        if foundation.get("maslow_keywords"):
            theory_keys.append("maslow")
    unique_keys = list(dict.fromkeys(theory_keys))
    return [THEORY_DETAILS[key] for key in unique_keys if key in THEORY_DETAILS]


def _fallback_theories(stage: str) -> list[dict[str, str]]:
    labels = {
        "segmentation": "Segmentation Theory Metadata",
        "targeting": "Targeting Theory Metadata",
        "positioning": "Positioning Theory Metadata",
    }
    return [
        {
            "name": labels[stage],
            "description": "Theory tags were not available for this rerun, so only the statistical method could be resolved from the artifacts.",
        }
    ]


def _quote_candidates(
    score_table: Any,
    relevant_columns: list[str],
    catalog: dict[str, dict[str, Any]],
    unit_cluster_map: dict[str, str] | None = None,
    selected_cluster: str | None = None,
    selected_brand: str | None = None,
) -> list[dict[str, Any]]:
    import pandas as pd

    if score_table is None or score_table.empty:
        return []
    relevant_columns = [column for column in relevant_columns if column in score_table.columns]
    if not relevant_columns:
        return []

    frame = score_table.copy()
    if unit_cluster_map:
        frame["cluster"] = frame["unit_id"].astype(str).map(unit_cluster_map)
    if selected_cluster:
        cluster_series = frame.get("cluster")
        if cluster_series is not None:
            filtered = frame[cluster_series == selected_cluster]
            if not filtered.empty:
                frame = filtered
    if selected_brand and "brand" in frame.columns:
        filtered = frame[frame["brand"].astype(str) == selected_brand]
        if not filtered.empty:
            frame = filtered

    score_matrix = frame[relevant_columns].apply(pd.to_numeric, errors="coerce")
    frame = frame.assign(_relevance=score_matrix.mean(axis=1))
    frame = frame.sort_values("_relevance", ascending=False)

    quotes: list[dict[str, Any]] = []
    for _, row in frame.iterrows():
        review_text = str(row.get("review_text", "")).strip()
        if not review_text:
            continue
        linked_columns = []
        for column in relevant_columns:
            value = row.get(column)
            if value is None:
                continue
            try:
                numeric_value = float(value)
            except (TypeError, ValueError):
                continue
            if numeric_value >= 5:
                linked_columns.append(column)
        if not linked_columns:
            top_columns = sorted(
                relevant_columns,
                key=lambda column: float(row.get(column, 0) or 0),
                reverse=True,
            )
            linked_columns = [column for column in top_columns[:2] if column in catalog]
        linked_items = [str(catalog.get(column, {}).get("label", column)) for column in linked_columns]
        quotes.append(
            {
                "review_id": str(row["review_id"]),
                "quote_text": review_text,
                "why_this_quote_matters": (
                    "This review strongly reflects "
                    + ", ".join(linked_items)
                    + "."
                ),
                "linked_items": linked_items,
            }
        )
        if len(quotes) >= 3:
            break
    return quotes[:3]


def _stage_methods(stage: str, positioning_method: str | None = None) -> list[dict[str, str]]:
    if stage == "segmentation":
        return [
            {"name": "Factor Analysis", "description": "Reduces many scored items into a smaller set of shared patterns."},
            {"name": "K-Means Clustering", "description": "Groups similar reviewers or units into segments based on those patterns."},
            {"name": "Cluster Size Guardrail", "description": "Re-runs clustering if any segment is too small to trust."},
        ]
    if stage == "targeting":
        return [
            {"name": "ANOVA / Regression", "description": "Tests whether clusters differ on continuous outcomes and how strongly cluster membership explains them."},
            {"name": "Chi-Square / Logistic Regression", "description": "Tests whether clusters differ on binary outcomes or conversion-like behaviors."},
            {"name": "Tukey HSD", "description": "Shows which specific clusters differ when the overall ANOVA is significant."},
        ]
    method_name = "Factor Analysis" if positioning_method != "mds" else "Multidimensional Scaling"
    method_description = (
        "Maps brand and ideal-point relationships using attribute structure."
        if positioning_method != "mds"
        else "Maps brand similarity distances when only similarity structure is available."
    )
    return [
        {"name": method_name, "description": method_description},
        {"name": "Ideal-Point Distance", "description": "Shows which brand is closest to the desired market ideal."},
        {"name": "Reliability / Validity Checks", "description": "Checks whether the scorecard behaves coherently as an analytical tool."},
    ]


def _what_this_section_is_doing(stage: str) -> str:
    messages = {
        "segmentation": "Finding distinct reviewer or customer groups based on shared score patterns.",
        "targeting": "Comparing segments to decide which audience should be prioritized, watched, or deprioritized.",
        "positioning": "Comparing brands against ideal expectations to clarify competitive position and strategic gaps.",
    }
    return messages[stage]


def _plain_language_explanation(stage: str, stage_summary: dict[str, Any]) -> str:
    if stage == "segmentation":
        return (
            "This section groups similar review patterns together so you can see different customer mindsets instead of one average customer."
        )
    if stage == "targeting":
        selected_cluster = stage_summary.get("target_selection_decision", {}).get("selected_cluster", "the top segment")
        return (
            f"This section checks which segment is most attractive to prioritize. Right now {selected_cluster} stands out on the most important scoring dimensions."
        )
    closest_brand = stage_summary.get("positioning_diagnostics", {}).get("benchmark_analysis", {}).get("closest_to_ideal", "the leading brand")
    return (
        f"This section shows how close each brand is to the ideal customer expectation. Right now {closest_brand} is nearest to that ideal."
    )


def build_stage_report_contract(
    stage: str,
    stage_summary: dict[str, Any] | None,
    foundation: dict[str, Any] | None,
    score_table: Any | None,
    positioning_method: str | None = None,
    unit_cluster_map: dict[str, str] | None = None,
) -> dict[str, Any] | None:
    if not isinstance(stage_summary, dict):
        return stage_summary
    foundation = foundation or {}

    catalog = _catalog_lookup(foundation)
    relevant_columns = _columns_for_stage(foundation, stage, stage_summary)
    include_segmentation_overlays = stage == "segmentation"
    selected_cluster = None
    selected_brand = None
    if stage == "targeting":
        selected_cluster = stage_summary.get("target_selection_decision", {}).get("selected_cluster")
    if stage == "positioning":
        selected_brand = stage_summary.get("positioning_diagnostics", {}).get("benchmark_analysis", {}).get("closest_to_ideal")

    evidence_quotes = _quote_candidates(
        score_table,
        relevant_columns,
        catalog,
        unit_cluster_map=unit_cluster_map,
        selected_cluster=selected_cluster,
        selected_brand=selected_brand,
    )
    evidence_status = "available" if evidence_quotes else "not_available"
    evidence_reason = "" if evidence_quotes else "Canonical per-review scoring evidence was not provided for this run."

    enriched = dict(stage_summary)
    enriched["what_this_section_is_doing"] = _what_this_section_is_doing(stage)
    enriched["methods_used"] = _stage_methods(stage, positioning_method)
    theories_used = _theories_for_columns(
        foundation,
        relevant_columns,
        include_segmentation_overlays=include_segmentation_overlays,
    )
    enriched["theories_used"] = theories_used or _fallback_theories(stage)
    enriched["plain_language_explanation"] = _plain_language_explanation(stage, stage_summary)
    enriched["evidence_quote_status"] = evidence_status
    enriched["evidence_quote_reason"] = evidence_reason
    enriched["evidence_quotes"] = evidence_quotes
    return enriched


def _render_report_section(title: str, section: dict[str, Any]) -> list[str]:
    lines = [
        "",
        f"## {title}",
        f"- What this section is doing: {section.get('what_this_section_is_doing', 'n/a')}",
        "- Statistical methods used:",
    ]
    for method in section.get("methods_used", []):
        lines.append(f"  - {method.get('name')}: {method.get('description')}")
    lines.append("- Theories used:")
    for theory in section.get("theories_used", []):
        lines.append(f"  - {theory.get('name')}: {theory.get('description')}")
    lines.append(
        f"- Plain-language explanation: {section.get('plain_language_explanation', 'n/a')}"
    )
    lines.append("- Evidence quotes:")
    if section.get("evidence_quotes"):
        for quote in section["evidence_quotes"]:
            lines.append(
                f"  - [{quote.get('review_id')}] \"{quote.get('quote_text')}\""
            )
            lines.append(
                f"    Why it matters: {quote.get('why_this_quote_matters')}"
            )
            lines.append(
                f"    Linked items: {', '.join(quote.get('linked_items', [])) or 'none'}"
            )
    else:
        lines.append(
            f"  - not available: {section.get('evidence_quote_reason', 'No evidence quotes were attached.')}"
        )
    return lines


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

    section_map = [
        ("Segmentation Summary", appendix.get("segmentation_summary")),
        ("Targeting Summary", appendix.get("targeting_summary")),
        ("Positioning Summary", appendix.get("positioning_summary")),
    ]
    for title, section in section_map:
        if section:
            lines.extend(_render_report_section(title, section))

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

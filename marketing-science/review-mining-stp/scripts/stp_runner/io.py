from __future__ import annotations

import json
from pathlib import Path
from typing import Any


CORE_THEMES = {
    "service_experience",
    "product_performance",
    "value_perception",
}

REQUIRED_DIMENSION_KEYS = {
    "column",
    "label",
    "theme",
    "theory_tags",
    "stat_roles",
    "plain_language_definition",
}


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: Any) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def find_artifact(paths: list[Path], name: str) -> Path | None:
    for root in paths:
        candidate = root / name
        if candidate.exists():
            return candidate
    return None


def resolve_required_files(
    artifact_paths: list[Path],
    files: list[str],
) -> tuple[dict[str, Path], list[str]]:
    located: dict[str, Path] = {}
    missing: list[str] = []
    for filename in files:
        path = find_artifact(artifact_paths, filename)
        if path is None:
            missing.append(filename)
        else:
            located[filename] = path
    return located, missing


def require_files(artifact_paths: list[Path], files: list[str]) -> dict[str, Path] | None:
    located, missing = resolve_required_files(artifact_paths, files)
    if missing:
        return None
    return located


def list_available_artifacts(paths: list[Path]) -> list[str]:
    artifact_names: set[str] = set()
    for root in paths:
        if not root.exists():
            continue
        for candidate in root.iterdir():
            if candidate.is_file():
                artifact_names.add(candidate.name)
    return sorted(artifact_names)


def load_analysis_context(artifact_paths: list[Path]) -> dict[str, Any]:
    path = find_artifact(artifact_paths, "analysis_context.json")
    if path is None:
        return {"analysis_goal": "", "comparison_axes": [], "scope_limits": []}
    payload = read_json(path)
    payload.setdefault("analysis_goal", "")
    payload.setdefault("comparison_axes", [])
    payload.setdefault("scope_limits", [])
    return payload


def _fail_contract(message: str) -> None:
    raise SystemExit(message)


def validate_canonical_inputs(score_table: Any, foundation: dict[str, Any]) -> dict[str, Any]:
    import pandas as pd

    unit_id_defaulted = False
    if "unit_id" not in score_table.columns and "review_id" in score_table.columns:
        score_table["unit_id"] = score_table["review_id"]
        unit_id_defaulted = True

    required_columns = {"review_id", "unit_id", "brand", "review_text"}
    missing_columns = sorted(required_columns - set(score_table.columns))
    if missing_columns:
        _fail_contract(
            "review_scoring_table.csv is missing required columns: " + ", ".join(missing_columns)
        )

    review_text = score_table["review_text"].fillna("").astype(str).str.strip()
    if (review_text == "").any():
        _fail_contract("review_scoring_table.csv must contain non-empty review_text for every row.")

    dimension_catalog = foundation.get("dimension_catalog")
    if not isinstance(dimension_catalog, list) or not dimension_catalog:
        _fail_contract("review_foundation.json must contain a non-empty dimension_catalog.")

    theme_mapping = foundation.get("theme_mapping")
    if not isinstance(theme_mapping, dict):
        _fail_contract("review_foundation.json must contain theme_mapping.")

    missing_themes = sorted(theme for theme in CORE_THEMES if theme not in theme_mapping)
    if missing_themes:
        _fail_contract("theme_mapping is missing required themes: " + ", ".join(missing_themes))

    dimension_columns: list[str] = []
    role_map: dict[str, list[str]] = {}
    catalog_by_column: dict[str, dict[str, Any]] = {}
    for item in dimension_catalog:
        if not isinstance(item, dict):
            _fail_contract("dimension_catalog entries must be objects.")
        missing_keys = sorted(REQUIRED_DIMENSION_KEYS - set(item.keys()))
        if missing_keys:
            _fail_contract("dimension_catalog entries are missing keys: " + ", ".join(missing_keys))

        column = str(item["column"])
        if column in catalog_by_column:
            _fail_contract(f"dimension_catalog contains duplicate column '{column}'.")

        theme = str(item["theme"])
        if theme not in CORE_THEMES:
            _fail_contract(f"dimension_catalog column '{column}' uses unsupported theme '{theme}'.")

        theory_tags = item.get("theory_tags")
        stat_roles = item.get("stat_roles")
        plain_language_definition = str(item.get("plain_language_definition", "")).strip()
        if not isinstance(theory_tags, list) or not theory_tags:
            _fail_contract(f"dimension_catalog column '{column}' must define theory_tags.")
        if not isinstance(stat_roles, list) or not stat_roles:
            _fail_contract(f"dimension_catalog column '{column}' must define stat_roles.")
        if not plain_language_definition:
            _fail_contract(f"dimension_catalog column '{column}' must define plain_language_definition.")

        catalog_by_column[column] = item
        dimension_columns.append(column)
        for role in stat_roles:
            role_map.setdefault(str(role), []).append(column)

    missing_dimension_columns = sorted(
        column for column in dimension_columns if column not in score_table.columns
    )
    if missing_dimension_columns:
        _fail_contract(
            "review_scoring_table.csv is missing dimension columns declared in dimension_catalog: "
            + ", ".join(missing_dimension_columns)
        )

    numeric_dimension_columns: list[str] = []
    for column in dimension_columns:
        numeric_values = pd.to_numeric(score_table[column], errors="coerce")
        if numeric_values.isna().any():
            _fail_contract(
                f"review_scoring_table.csv column '{column}' must contain numeric scores for every review."
            )
        if ((numeric_values < 0) | (numeric_values > 7)).any():
            _fail_contract(
                f"review_scoring_table.csv column '{column}' must keep every score inside the 0-7 range."
            )
        if not ((numeric_values % 1) == 0).all():
            _fail_contract(
                f"review_scoring_table.csv column '{column}' must use integer scores that follow the 0-7 scale."
            )
        score_table[column] = numeric_values.astype(int)
        numeric_dimension_columns.append(column)

    if len(numeric_dimension_columns) < 3:
        _fail_contract(
            "review_scoring_table.csv must provide at least 3 numeric score columns from dimension_catalog."
        )

    for theme, columns in theme_mapping.items():
        if theme not in CORE_THEMES:
            continue
        if not isinstance(columns, list) or not columns:
            _fail_contract(f"theme_mapping.{theme} must be a non-empty list.")
        invalid_columns = sorted(column for column in columns if column not in catalog_by_column)
        if invalid_columns:
            _fail_contract(
                f"theme_mapping.{theme} references columns not present in dimension_catalog: "
                + ", ".join(invalid_columns)
            )

    return {
        "dimension_catalog": dimension_catalog,
        "catalog_by_column": catalog_by_column,
        "dimension_columns": dimension_columns,
        "numeric_dimension_columns": numeric_dimension_columns,
        "role_map": {role: list(dict.fromkeys(columns)) for role, columns in role_map.items()},
        "theme_mapping": theme_mapping,
        "unit_id_defaulted": unit_id_defaulted,
    }


def aggregate_review_scoring_table(score_table: Any, contract: dict[str, Any]) -> Any:
    import pandas as pd

    dimension_columns = contract["dimension_columns"]
    metadata_columns = [
        column
        for column in score_table.columns
        if column not in {"review_id", "review_text"} | set(dimension_columns)
    ]
    rows: list[dict[str, Any]] = []
    for unit_id, group in score_table.groupby("unit_id", sort=False):
        row: dict[str, Any] = {"unit_id": unit_id}
        row["brand"] = str(group["brand"].mode().iloc[0])
        row["review_count"] = int(len(group))
        for column in dimension_columns:
            row[column] = round(float(pd.to_numeric(group[column]).mean()), 4)
        for column in metadata_columns:
            if column in {"unit_id", "brand"}:
                continue
            series = group[column].dropna()
            if series.empty:
                continue
            if pd.api.types.is_numeric_dtype(group[column]):
                row[column] = round(float(pd.to_numeric(series).mean()), 4)
            else:
                mode = series.mode()
                row[column] = str(mode.iloc[0]) if not mode.empty else str(series.iloc[0])
        rows.append(row)
    return pd.DataFrame(rows)


def build_segmentation_variables(unit_table: Any, contract: dict[str, Any]) -> Any:
    segmentation_columns = [
        column
        for column in contract["role_map"].get("segmentation", [])
        if column in unit_table.columns
    ]
    if len(segmentation_columns) < 3:
        for column in contract["numeric_dimension_columns"]:
            if column not in segmentation_columns and column in unit_table.columns:
                segmentation_columns.append(column)
            if len(segmentation_columns) >= 3:
                break
    profile_columns = [column for column in unit_table.columns if column.startswith("profile_")]
    passthrough_columns = [
        column
        for column in ["unit_id", *profile_columns, "rating", "brand"]
        if column in unit_table.columns
    ]
    selected_columns = list(dict.fromkeys(passthrough_columns + segmentation_columns))
    return unit_table[selected_columns].copy()


def build_targeting_dataset(
    unit_table: Any,
    segment_assignments: Any,
    contract: dict[str, Any],
    comparison_axes: list[str],
) -> Any:
    role_map = contract["role_map"]
    targeting_columns = [
        column
        for column in role_map.get("current_target", []) + role_map.get("potential_target", [])
        if column in unit_table.columns
    ]
    if comparison_axes:
        targeting_columns.extend(column for column in comparison_axes if column in unit_table.columns)
    if not targeting_columns:
        targeting_columns.extend(contract["numeric_dimension_columns"])
    profile_columns = [column for column in unit_table.columns if column.startswith("profile_")]
    extra_columns = [column for column in ["unit_id", "brand", *profile_columns] if column in unit_table.columns]
    selected_columns = list(dict.fromkeys(extra_columns + targeting_columns))
    frame = unit_table[selected_columns].copy()
    assignments = segment_assignments.copy()
    if "unit_id" not in assignments.columns or "cluster" not in assignments.columns:
        raise SystemExit("Segmentation assignments must contain unit_id and cluster.")
    merged = frame.merge(assignments[["unit_id", "cluster"]], on="unit_id", how="left")
    if merged["cluster"].isna().any():
        raise SystemExit("Targeting dataset could not align all unit_id rows to segmentation clusters.")
    cluster = merged.pop("cluster")
    merged.insert(0, "cluster", cluster)
    return merged


def build_positioning_scorecard(score_table: Any, contract: dict[str, Any]) -> Any:
    import pandas as pd

    positioning_columns = [
        column
        for column in contract["role_map"].get("positioning", [])
        if column in score_table.columns
    ]
    if len(positioning_columns) < 2:
        positioning_columns = [
            column
            for column in contract["numeric_dimension_columns"]
            if column in score_table.columns
        ]
    rows: list[dict[str, Any]] = []
    brand_means = score_table.groupby("brand")[positioning_columns].mean(numeric_only=True)
    for brand, values in brand_means.iterrows():
        for attribute, score in values.items():
            rows.append(
                {
                    "brand": str(brand),
                    "attribute": str(attribute),
                    "score": round(float(score), 4),
                }
            )
    return pd.DataFrame(rows)


def derive_role_columns(foundation: dict[str, Any]) -> dict[str, list[str]]:
    role_map: dict[str, list[str]] = {}
    for item in foundation.get("dimension_catalog", []):
        if not isinstance(item, dict):
            continue
        column = str(item.get("column", ""))
        for role in item.get("stat_roles", []):
            if column:
                role_map.setdefault(str(role), []).append(column)
    return {role: list(dict.fromkeys(columns)) for role, columns in role_map.items()}


def build_missing_prereq_output(
    output_dir: Path,
    run_mode: str,
    requested_modules: list[str],
    artifact_paths: list[Path],
    required: list[str],
) -> None:
    _, missing = resolve_required_files(artifact_paths, required)
    next_step_rule = "Provide the missing upstream artifacts before rerunning this stage."
    if "review_scoring_table.csv" in missing or "review_foundation.json" in missing:
        next_step_rule = (
            "Scripts accept scored artifacts only; use the agent layer to convert raw reviews "
            "into review_scoring_table.csv and review_foundation.json before rerunning."
        )
    payload = {
        "requested_stage": run_mode,
        "requested_modules": requested_modules,
        "missing_prerequisites": missing,
        "acceptable_upstream_artifacts": missing,
        "available_artifacts": list_available_artifacts(artifact_paths),
        "auto_backfill_allowed": False,
        "next_step_rule": next_step_rule,
    }
    write_json(output_dir / "MissingPrerequisiteOutput.json", payload)

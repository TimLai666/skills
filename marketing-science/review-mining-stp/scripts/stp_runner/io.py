from __future__ import annotations

import json
from pathlib import Path
from typing import Any


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


def require_files(artifact_paths: list[Path], files: list[str]) -> dict[str, Path] | None:
    located: dict[str, Path] = {}
    for filename in files:
        path = find_artifact(artifact_paths, filename)
        if path is None:
            return None
        located[filename] = path
    return located


def build_missing_prereq_output(
    output_dir: Path, run_mode: str, requested_modules: list[str], missing: list[str]
) -> None:
    payload = {
        "requested_stage": run_mode,
        "requested_modules": requested_modules,
        "missing_prerequisites": missing,
        "acceptable_upstream_artifacts": [
            "review_foundation.json",
            "segmentation_variables.csv",
            "segment_profiles.json",
            "targeting_dataset.csv",
            "positioning_scorecard.csv",
            "brands.json",
            "ideal_point.json",
        ],
        "auto_backfill_allowed": False,
        "next_step_rule": "Provide the missing upstream artifacts before rerunning this stage.",
    }
    write_json(output_dir / "MissingPrerequisiteOutput.json", payload)

#!/usr/bin/env python3
"""Regression test for comparison-axis resolution in targeting.

The bug: `_resolve_comparison_axes` expanded a bare attribute name into
`f"{name}_salience"` / `f"{name}_quality"` by string guessing. When a
dimension_catalog declares axis columns that do not follow that suffix
convention — which the contract permits, since the column names are
arbitrary — targeting silently dropped those axes.

Run:  python3 scripts/test_targeting_axes.py
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

import pandas as pd

from stp_runner.targeting import _resolve_comparison_axes


def test_non_conventional_axis_columns_are_resolved_via_catalog() -> None:
    # anti_fog declares axis columns that do NOT end in _salience / _quality.
    dataset = pd.DataFrame(
        {
            "brand": ["A", "B"],
            "af_sal": [3, 5],
            "af_qual": [8, 4],
        }
    )
    axis_expansion = {"anti_fog": ["af_sal", "af_qual"]}

    resolved = _resolve_comparison_axes(
        dataset,
        comparison_axes=["anti_fog"],
        current_columns=[],
        potential_columns=[],
        role_comparison_columns=[],
        axis_expansion=axis_expansion,
    )

    assert resolved == ["af_sal", "af_qual"], (
        f"both declared axis columns must be resolved via the catalog, got {resolved}"
    )


def test_conventional_names_still_work_without_catalog() -> None:
    # Empty catalog (e.g. a targeting-only rerun with no foundation): the
    # suffix fallback must still resolve conventionally named columns.
    dataset = pd.DataFrame(
        {
            "brand": ["A", "B"],
            "anti_fog_salience": [3, 5],
            "anti_fog_quality": [8, 4],
        }
    )

    resolved = _resolve_comparison_axes(
        dataset,
        comparison_axes=["anti_fog"],
        current_columns=[],
        potential_columns=[],
        role_comparison_columns=[],
        axis_expansion={},
    )

    assert resolved == ["anti_fog_salience", "anti_fog_quality"], (
        f"suffix fallback must still work when no catalog is available, got {resolved}"
    )


def test_direct_column_name_is_used_as_is() -> None:
    dataset = pd.DataFrame({"brand": ["A", "B"], "anti_fog_salience": [3, 5]})

    resolved = _resolve_comparison_axes(
        dataset,
        comparison_axes=["brand"],
        current_columns=[],
        potential_columns=[],
        role_comparison_columns=[],
        axis_expansion={"anti_fog": ["anti_fog_salience"]},
    )

    assert resolved == ["brand"], f"a real dataset column must be used directly, got {resolved}"


if __name__ == "__main__":
    test_non_conventional_axis_columns_are_resolved_via_catalog()
    test_conventional_names_still_work_without_catalog()
    test_direct_column_name_is_used_as_is()
    print("all targeting-axis tests passed")

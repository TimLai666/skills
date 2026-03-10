from __future__ import annotations

import math
from pathlib import Path
from typing import Any

from .io import find_artifact, read_json


def load_positioning_inputs(
    artifact_paths: list[Path], ideal_point_file: str | None, brands_file: str | None
) -> tuple[Any, dict[str, Any], dict[str, Any]] | None:
    import pandas as pd

    scorecard_path = find_artifact(artifact_paths, "positioning_scorecard.csv")
    if scorecard_path is None:
        return None

    brands_path = Path(brands_file) if brands_file else find_artifact(artifact_paths, "brands.json")
    ideal_path = Path(ideal_point_file) if ideal_point_file else find_artifact(artifact_paths, "ideal_point.json")
    if brands_path is None or ideal_path is None or not brands_path.exists() or not ideal_path.exists():
        return None

    scorecard = pd.read_csv(scorecard_path)
    brands = read_json(brands_path)
    ideal_point = read_json(ideal_path)
    return scorecard, brands, ideal_point


def run_positioning(
    scorecard: Any, brands: dict[str, Any], ideal_point: dict[str, Any], method: str, output_dir: Path
) -> dict[str, Any]:
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import numpy as np
    import pandas as pd
    from sklearn.decomposition import FactorAnalysis
    from sklearn.manifold import MDS
    from sklearn.preprocessing import StandardScaler

    pivot = scorecard.pivot_table(index="brand", columns="attribute", values="score", aggfunc="mean")
    ideal_series = pd.Series(ideal_point["attributes"], name=ideal_point["label"])
    shared_columns = [column for column in pivot.columns if column in ideal_series.index]
    pivot = pivot[shared_columns].sort_index()
    ideal_series = ideal_series[shared_columns]
    brand_matrix = pivot.copy()

    coordinate_rows: list[dict[str, Any]] = []
    vector_rows: list[dict[str, Any]] = []

    if method == "factor_analysis":
        combined = pd.concat([brand_matrix, ideal_series.to_frame().T], axis=0)
        scaler = StandardScaler()
        scaled = scaler.fit_transform(combined)
        model = FactorAnalysis(n_components=2, random_state=42)
        factor_scores = model.fit_transform(scaled)
        loadings = model.components_.T

        for idx, label in enumerate(combined.index):
            point_type = "ideal" if label == ideal_point["label"] else "brand"
            coordinate_rows.append(
                {
                    "label": str(label),
                    "point_type": point_type,
                    "x": float(factor_scores[idx, 0]),
                    "y": float(factor_scores[idx, 1]),
                }
            )
        for idx, attribute in enumerate(combined.columns):
            vector_rows.append(
                {
                    "label": str(attribute),
                    "vector_type": "attribute",
                    "x_start": 0.0,
                    "y_start": 0.0,
                    "x_end": float(loadings[idx, 0]),
                    "y_end": float(loadings[idx, 1]),
                    "x_loading": float(loadings[idx, 0]),
                    "y_loading": float(loadings[idx, 1]),
                }
            )
        positioning_method_used = "factor_analysis"
        attribute_vectors_not_defined = False
        perceptual_map_method = {
            "method": positioning_method_used,
            "brand_point_source": "factor scores",
            "ideal_point_source": "factor scores",
            "attribute_vector_source": "factor loadings",
        }
    else:
        similarity_matrix = brands.get("similarity_matrix")
        if not similarity_matrix:
            raise SystemExit(
                "MDS requires brands.json to contain similarity_matrix for the first version."
            )
        dissimilarity = np.array(similarity_matrix, dtype=float)
        model = MDS(
            n_components=2,
            dissimilarity="precomputed",
            random_state=42,
            n_init=4,
        )
        brand_coords = model.fit_transform(dissimilarity)

        ideal_vector = ideal_series.to_numpy(dtype=float)
        brand_vectors = brand_matrix.to_numpy(dtype=float)
        weights = brand_vectors @ ideal_vector
        weights = weights / weights.sum()
        ideal_coord = np.average(brand_coords, axis=0, weights=weights)

        for idx, label in enumerate(brand_matrix.index):
            coordinate_rows.append(
                {
                    "label": str(label),
                    "point_type": "brand",
                    "x": float(brand_coords[idx, 0]),
                    "y": float(brand_coords[idx, 1]),
                }
            )
        coordinate_rows.append(
            {
                "label": str(ideal_point["label"]),
                "point_type": "ideal",
                "x": float(ideal_coord[0]),
                "y": float(ideal_coord[1]),
            }
        )
        positioning_method_used = "mds"
        attribute_vectors_not_defined = True
        perceptual_map_method = {
            "method": positioning_method_used,
            "brand_point_source": "mds coordinates",
            "ideal_point_source": "weighted centroid from ideal profile",
            "attribute_vector_source": "attribute_vectors_not_defined",
        }

    coordinate_frame = pd.DataFrame(coordinate_rows)
    coordinate_frame.to_csv(output_dir / "perceptual_map_coordinates.csv", index=False, encoding="utf-8")
    if vector_rows:
        pd.DataFrame(vector_rows).to_csv(
            output_dir / "perceptual_map_vectors.csv", index=False, encoding="utf-8"
        )

    figure_path = output_dir / "perceptual_map.png"
    fig, ax = plt.subplots(figsize=(8, 6))
    for row in coordinate_rows:
        if row["point_type"] == "brand":
            ax.scatter(row["x"], row["y"], color="#1f77b4", s=90)
            ax.text(row["x"] + 0.03, row["y"] + 0.03, row["label"], fontsize=9)
        else:
            ax.scatter(row["x"], row["y"], color="#d62728", marker="*", s=180)
            ax.text(row["x"] + 0.03, row["y"] + 0.03, row["label"], fontsize=10)
    for row in vector_rows:
        ax.arrow(
            0.0,
            0.0,
            row["x_end"],
            row["y_end"],
            color="#2ca02c",
            length_includes_head=True,
            head_width=0.04,
            alpha=0.85,
        )
        ax.text(row["x_end"] + 0.02, row["y_end"] + 0.02, row["label"], fontsize=8, color="#2ca02c")
    ax.axhline(0.0, color="#888888", linewidth=0.8)
    ax.axvline(0.0, color="#888888", linewidth=0.8)
    ax.set_xlabel("Factor 1" if method == "factor_analysis" else "MDS Dimension 1")
    ax.set_ylabel("Factor 2" if method == "factor_analysis" else "MDS Dimension 2")
    ax.set_title("Perceptual Map")
    ax.grid(alpha=0.2)
    fig.tight_layout()
    fig.savefig(figure_path, dpi=200)
    plt.close(fig)

    coordinates_by_label = {row["label"]: row for row in coordinate_rows}
    ideal_coords = coordinates_by_label[ideal_point["label"]]
    brand_distance_table = []
    for label in brand_matrix.index:
        row = coordinates_by_label[label]
        distance = math.dist((row["x"], row["y"]), (ideal_coords["x"], ideal_coords["y"]))
        brand_distance_table.append({"brand": label, "distance_to_ideal": round(distance, 4)})
    nearest = min(brand_distance_table, key=lambda item: item["distance_to_ideal"])

    top_attributes = []
    for attribute in shared_columns:
        scores = pivot[attribute].sort_values(ascending=False)
        leader = scores.index[0]
        gap = float(scores.iloc[0] - scores.iloc[1]) if len(scores) > 1 else float(scores.iloc[0])
        top_attributes.append({"attribute": attribute, "leader": str(leader), "gap": round(gap, 4)})

    pod = [item["attribute"] for item in top_attributes if item["gap"] >= 0.4]
    pop = [
        attribute
        for attribute in shared_columns
        if float(pivot[attribute].min()) >= float(ideal_series[attribute] - 1.5)
    ]

    brand_name = nearest["brand"]
    strategy_matrix = {"appeal": [], "improve": [], "change": [], "abandon": []}
    for attribute in shared_columns:
        brand_score = float(pivot.loc[brand_name, attribute])
        ideal_score = float(ideal_series[attribute])
        gap = ideal_score - brand_score
        if gap <= 0.3:
            strategy_matrix["appeal"].append(attribute)
        elif gap <= 0.8:
            strategy_matrix["improve"].append(attribute)
        elif gap <= 1.4:
            strategy_matrix["change"].append(attribute)
        else:
            strategy_matrix["abandon"].append(attribute)

    if not attribute_vectors_not_defined and vector_rows:
        projection_summary = []
        for vector in vector_rows:
            vector_norm = math.sqrt((vector["x_end"] ** 2) + (vector["y_end"] ** 2))
            if vector_norm == 0:
                continue
            ideal_projection = (
                ideal_coords["x"] * vector["x_end"] + ideal_coords["y"] * vector["y_end"]
            ) / vector_norm
            brand_projection_rows = []
            for label in brand_matrix.index:
                row = coordinates_by_label[label]
                projection_value = (row["x"] * vector["x_end"] + row["y"] * vector["y_end"]) / vector_norm
                brand_projection_rows.append(
                    {
                        "brand": str(label),
                        "projection": round(float(projection_value), 4),
                    }
                )
            brand_projection_rows.sort(key=lambda item: item["projection"], reverse=True)
            projection_summary.append(
                {
                    "attribute": vector["label"],
                    "ideal_projection": round(float(ideal_projection), 4),
                    "leading_brand": brand_projection_rows[0]["brand"],
                    "leading_projection": brand_projection_rows[0]["projection"],
                    "brand_rankings": brand_projection_rows,
                }
            )
        projection_summary.sort(key=lambda item: item["ideal_projection"], reverse=True)
        projection_interpretation = {
            "status": "defined",
            "method": "factor_analysis",
            "rule": (
                "Brand performance is interpreted by projecting brand points onto attribute vectors "
                "from the origin; ideal-point projection indicates relative attribute importance."
            ),
            "attribute_projection_summary": projection_summary,
            "importance_interpretation": (
                "Higher ideal-point projection values imply higher relative importance for the segment."
            ),
        }
    else:
        projection_interpretation = {
            "status": "not_available",
            "method": positioning_method_used,
            "reason": (
                "Attribute vectors are not defined in this MDS run because the input is similarity-based "
                "rather than attribute-based."
            ),
            "attribute_projection_summary": [],
            "importance_interpretation": "",
        }

    diagnostics = {
        "attribute_vectors_not_defined": attribute_vectors_not_defined,
        "key_factor_assessment": top_attributes,
        "benchmark_analysis": {"closest_to_ideal": nearest["brand"], "distance_to_ideal": nearest["distance_to_ideal"]},
        "ideal_point_analysis": brand_distance_table,
        "competition_landscape": sorted(brand_distance_table, key=lambda item: item["distance_to_ideal"]),
        "pod_pop": {"pod": pod, "pop": pop},
        "strategy_matrix": strategy_matrix,
        "projection_interpretation": projection_interpretation,
    }
    interpretation = (
        f"{nearest['brand']} is closest to the ideal point. "
        "Distance between brand points indicates competitive crowding; "
        "projection along vectors indicates attribute performance."
    )

    return {
        "positioning_scorecard": scorecard.to_dict("records"),
        "dynamic_scorecard_summary": {
            "brand_count": int(len(brand_matrix)),
            "attribute_count": int(len(shared_columns)),
            "reliability_note": "Directional only. Uses artifact-derived score inputs.",
            "validity_note": "Interpret scores together with review evidence and target selection.",
        },
        "positioning_method_used": positioning_method_used,
        "perceptual_map_method": perceptual_map_method,
        "perceptual_map_interpretation": interpretation,
        "projection_interpretation": projection_interpretation,
        "positioning_diagnostics": diagnostics,
        "strategy_matrix": strategy_matrix,
    }

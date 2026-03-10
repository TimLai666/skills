from __future__ import annotations

from typing import Any

from .io import read_json, require_files


def load_segmentation_inputs(artifact_paths: list) -> tuple[dict[str, Any], Any] | None:
    import pandas as pd

    located = require_files(artifact_paths, ["review_foundation.json", "segmentation_variables.csv"])
    if located is None:
        return None
    foundation = read_json(located["review_foundation.json"])
    frame = pd.read_csv(located["segmentation_variables.csv"])
    return foundation, frame


def run_segmentation(foundation: dict[str, Any], frame: Any) -> dict[str, Any]:
    import pandas as pd
    from sklearn.cluster import KMeans
    from sklearn.compose import ColumnTransformer
    from sklearn.preprocessing import OneHotEncoder, StandardScaler

    feature_columns = [column for column in frame.columns if column != "customer_id"]
    numeric_columns = frame[feature_columns].select_dtypes(include=["number"]).columns.tolist()
    categorical_columns = [column for column in feature_columns if column not in numeric_columns]

    transformer = ColumnTransformer(
        transformers=[
            ("numeric", StandardScaler(), numeric_columns),
            ("categorical", OneHotEncoder(handle_unknown="ignore"), categorical_columns),
        ]
    )
    encoded = transformer.fit_transform(frame[feature_columns])
    if hasattr(encoded, "toarray"):
        encoded = encoded.toarray()

    initial_k = min(6, max(3, len(frame) // 12))
    best_labels = None
    selected_k = initial_k

    for clusters in range(initial_k, 1, -1):
        model = KMeans(n_clusters=clusters, random_state=42, n_init=10)
        labels = model.fit_predict(encoded)
        counts = pd.Series(labels).value_counts(normalize=True)
        if bool((counts > 0.05).all()):
            best_labels = labels
            selected_k = clusters
            break
        if best_labels is None:
            best_labels = labels
            selected_k = clusters

    segmented = frame.copy()
    segmented["cluster"] = [f"segment_{int(label)}" for label in best_labels]
    counts = segmented["cluster"].value_counts().sort_index()
    shares = (counts / counts.sum()).to_dict()

    segment_profiles: list[dict[str, Any]] = []
    for cluster in counts.index:
        subset = segmented[segmented["cluster"] == cluster]
        numeric_summary = {
            column: round(float(subset[column].mean()), 4) for column in numeric_columns
        }
        categorical_summary = {
            column: str(subset[column].mode().iloc[0]) for column in categorical_columns
        }
        top_numeric = sorted(numeric_summary.items(), key=lambda item: item[1], reverse=True)[:2]
        persona = (
            f"{categorical_summary.get('psychographic', 'mixed')} shoppers prioritize "
            f"{', '.join(name for name, _ in top_numeric)}."
        )
        segment_profiles.append(
            {
                "cluster": cluster,
                "sample_size": int(len(subset)),
                "share": round(float(shares[cluster]), 4),
                "numeric_summary": numeric_summary,
                "categorical_summary": categorical_summary,
                "persona": persona,
            }
        )

    return {
        "cluster_selection": {
            "initial_k": int(initial_k),
            "selected_k": int(selected_k),
            "all_clusters_above_threshold": bool(all(item["share"] > 0.05 for item in segment_profiles)),
        },
        "segment_profiles": segment_profiles,
        "segment_variable_table": {
            "geographic": ["geo_region"],
            "demographic": ["age_group"],
            "psychographic": ["psychographic"],
            "behavioral": ["behavior_frequency"],
        },
        "review_foundation": foundation,
    }


def build_segment_summary(segmentation: dict[str, Any]) -> str:
    foundation = segmentation["review_foundation"]
    lines = [
        "# Segmentation Summary",
        "",
        "## Review Foundation",
        f"- People insights: {', '.join(foundation.get('people_insights', []))}",
        f"- Product triggers: {', '.join(foundation.get('product_triggers', []))}",
        f"- Context scenarios: {', '.join(foundation.get('context_scenarios', []))}",
        "",
        "## Cluster Share Table",
    ]
    for profile in segmentation["segment_profiles"]:
        lines.append(
            f"- {profile['cluster']}: {profile['sample_size']} customers, share={profile['share']:.2%}"
        )
    lines.extend(["", "## Segment Personas"])
    for profile in segmentation["segment_profiles"]:
        lines.append(f"- {profile['cluster']}: {profile['persona']}")
    return "\n".join(lines) + "\n"

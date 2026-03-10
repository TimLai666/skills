from __future__ import annotations

from typing import Any

from .io import find_artifact, read_json


def load_targeting_inputs(
    artifact_paths: list, generated_segmentation: dict[str, Any] | None
) -> tuple[Any, dict[str, Any]] | None:
    import pandas as pd

    dataset_path = find_artifact(artifact_paths, "targeting_dataset.csv")
    if dataset_path is None:
        return None

    if generated_segmentation is None:
        segment_profiles_path = find_artifact(artifact_paths, "segment_profiles.json")
        if segment_profiles_path is None:
            return None
        segmentation = read_json(segment_profiles_path)
    else:
        segmentation = generated_segmentation

    dataset = pd.read_csv(dataset_path)
    return dataset, segmentation


def run_targeting(dataset: Any, segmentation: dict[str, Any]) -> dict[str, Any]:
    import pandas as pd
    from scipy.stats import chi2_contingency, f_oneway
    from sklearn.linear_model import LogisticRegression
    from sklearn.preprocessing import StandardScaler
    import statsmodels.api as sm

    cluster_profiles = {item["cluster"]: item for item in segmentation["segment_profiles"]}
    continuous_columns = []
    binary_columns = []
    for column in dataset.columns:
        if column == "cluster":
            continue
        series = dataset[column].dropna()
        if series.nunique() <= 2 and set(series.unique()).issubset({0, 1}):
            binary_columns.append(column)
        else:
            continuous_columns.append(column)

    current_columns = [
        column for column in ["current_value", "loyalty_score", "active_rate"] if column in continuous_columns
    ] or continuous_columns
    potential_binary = [
        column for column in ["potential_conversion", "tried_before"] if column in binary_columns
    ] or binary_columns
    potential_continuous = [
        column for column in ["intent_score"] if column in continuous_columns and column not in current_columns
    ]

    current_results = []
    for column in current_columns:
        groups = [group[column].dropna().to_numpy() for _, group in dataset.groupby("cluster")]
        f_stat, p_value = f_oneway(*groups)
        design = pd.get_dummies(dataset["cluster"], drop_first=True, dtype=float)
        model = sm.OLS(dataset[column], sm.add_constant(design)).fit()
        current_results.append(
            {
                "variable": column,
                "method": "anova_regression",
                "anova": {"f_stat": float(f_stat), "p_value": float(p_value)},
                "regression_r2": float(model.rsquared),
            }
        )

    potential_results = []
    for column in potential_binary:
        table = pd.crosstab(dataset["cluster"], dataset[column])
        chi2, p_value, _, _ = chi2_contingency(table)
        design = pd.get_dummies(dataset["cluster"], drop_first=True, dtype=float)
        scaler = StandardScaler(with_mean=False)
        design_scaled = scaler.fit_transform(design)
        model = LogisticRegression(max_iter=1000)
        model.fit(design_scaled, dataset[column])
        potential_results.append(
            {
                "variable": column,
                "method": "chi_square_logistic_regression",
                "chi_square": {"chi2": float(chi2), "p_value": float(p_value)},
                "coefficients": [
                    {"cluster_dummy": design.columns[idx], "coefficient": float(value)}
                    for idx, value in enumerate(model.coef_[0])
                ],
            }
        )
    for column in potential_continuous:
        groups = [group[column].dropna().to_numpy() for _, group in dataset.groupby("cluster")]
        f_stat, p_value = f_oneway(*groups)
        potential_results.append(
            {
                "variable": column,
                "method": "anova",
                "anova": {"f_stat": float(f_stat), "p_value": float(p_value)},
            }
        )

    cluster_scores = dataset.groupby("cluster")[current_columns + potential_binary + potential_continuous].mean()
    normalized = (cluster_scores - cluster_scores.min()) / (
        (cluster_scores.max() - cluster_scores.min()).replace(0, 1)
    )
    normalized["score"] = normalized.mean(axis=1)
    selected_cluster = str(normalized["score"].idxmax())

    return {
        "current_target_market": current_results,
        "potential_target_market": potential_results,
        "method_selection": {
            "continuous_response": "ANOVA / regression",
            "binary_response": "chi-square / logistic regression",
        },
        "target_selection_decision": {
            "selected_cluster": selected_cluster,
            "score": round(float(normalized.loc[selected_cluster, "score"]), 4),
            "rationale": (
                f"{selected_cluster} leads on a balanced mix of current value, loyalty, activity, "
                "and future conversion indicators."
            ),
            "persona": cluster_profiles[selected_cluster]["persona"],
        },
        "cluster_score_table": normalized.reset_index().rename(columns={"index": "cluster"}).to_dict("records"),
    }

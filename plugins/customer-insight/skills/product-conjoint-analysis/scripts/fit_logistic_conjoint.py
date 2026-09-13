"""Conditional choice models. Split models describe exploratory associations only."""
from __future__ import annotations

import warnings

import numpy as np
import pandas as pd

from build_stacked_data import validate_stacked


def fit_single_model(
    stacked: pd.DataFrame,
    predictors: list[str],
    response: str = "y",
    *,
    choice_set_id_col: str = "choice_set_id",
    card_id_col: str = "card_id",
    customer_id_col: str = "customer_id",
    maxiter: int = 1000,
) -> dict:
    """Fit ConditionalLogit without intercept, conditional on each choice event.

    Covariance assumes independent choice events. Repeated customer events are
    accepted but do not receive cluster-robust inference. Association estimates
    require a credible observed consideration set and identifiable design.

    Estimation centers predictors within each event and divides each column by
    its within-event root mean square. Reported coefficients, standard errors,
    and covariance are converted back to the original input units. model_object
    retains the centered, normalized predictors and normalized parameters; use
    the returned coefficients with original-unit cards for choice predictions.
    """
    from statsmodels.discrete.conditional_models import ConditionalLogit
    from statsmodels.tools.sm_exceptions import ConvergenceWarning, HessianInversionWarning
    from scipy.optimize import linprog

    info = validate_stacked(stacked, customer_id_col, choice_set_id_col=choice_set_id_col,
                            card_id_col=card_id_col, response=response, predictors=predictors)
    X = stacked[predictors].astype(float)
    groups = stacked[choice_set_id_col]
    centered = X - X.groupby(groups, sort=False).transform("mean")
    scale = np.linalg.norm(centered.to_numpy(), axis=0) / np.sqrt(len(stacked))
    if np.any(scale == 0) or np.linalg.matrix_rank(centered.to_numpy() / scale) < len(predictors):
        raise ValueError("Within-choice-set design is rank deficient; effects cannot be separated")
    # Complete or quasi separation: a direction improves some chosen-versus-other
    # contrasts without worsening any. Such a likelihood has no finite maximum.
    contrasts = []
    for _, group in stacked.groupby(choice_set_id_col, sort=False):
        chosen = group.loc[group[response] == 1, predictors].to_numpy(dtype=float)[0]
        contrasts.extend(chosen - group.loc[group[response] == 0, predictors].to_numpy(dtype=float))
    contrasts = np.asarray(contrasts) / scale
    separation = linprog(np.zeros(len(predictors)),
                        A_ub=np.vstack([-contrasts, -contrasts.sum(axis=0)]),
                        b_ub=np.r_[np.zeros(len(contrasts)), -1.],
                        bounds=[(None, None)] * len(predictors), method="highs")
    if separation.success:
        raise ValueError("Complete or quasi separation: finite coefficient estimates do not exist")
    if separation.status != 2:
        raise RuntimeError("Could not verify absence of separation")
    normalized = centered / scale
    model = ConditionalLogit(stacked[response].astype(int), normalized,
                             groups=groups, missing="raise")
    try:
        with warnings.catch_warnings():
            warnings.simplefilter("error", ConvergenceWarning)
            warnings.simplefilter("error", HessianInversionWarning)
            warnings.simplefilter("error", RuntimeWarning)
            fitted = model.fit(method="bfgs", maxiter=maxiter, disp=False)
        normalized_covariance = np.asarray(fitted.cov_params())
        normalized_params = np.asarray(fitted.params)
        # ConditionalResults drops optimizer status in statsmodels 0.15.0. Check
        # the score as well as treating its convergence warnings as failures.
        # This score uses dimensionless predictors, so the acceptance threshold
        # does not depend on the user's price/attribute measurement units.
        score = np.asarray(model.score(normalized_params)) / len(stacked)
        if (not np.isfinite(normalized_params).all() or not np.isfinite(normalized_covariance).all()
                or not np.isfinite(fitted.pvalues).all() or not np.isfinite(score).all()
                or np.max(np.abs(score)) > 1e-4
                or np.any(np.linalg.eigvalsh(normalized_covariance) <= 0)):
            raise RuntimeError("Nonfinite, unconverged, or singular model result")
    except (Warning, np.linalg.LinAlgError, ValueError) as exc:
        raise RuntimeError(f"Conditional model fitting failed: {exc}") from exc
    params = normalized_params / scale
    std_errors = np.asarray(fitted.bse) / scale
    covariance = pd.DataFrame(normalized_covariance / np.outer(scale, scale),
                              index=predictors, columns=predictors)
    if (not np.isfinite(params).all() or not np.isfinite(std_errors).all()
            or not np.isfinite(covariance).all().all()):
        raise RuntimeError("Could not represent model estimates in original input units")
    ll = float(model.loglike(normalized_params))
    null_ll = float(model.loglike(np.zeros(len(predictors))))
    if not np.isfinite(ll) or not np.isfinite(null_ll):
        raise RuntimeError("Nonfinite model likelihood")
    return {"name": "full", "approach": "conditional_logit", "converged": True,
            "coefficients": dict(zip(predictors, params)),
            "p_values": dict(zip(predictors, np.asarray(fitted.pvalues))),
            "std_errors": dict(zip(predictors, std_errors)),
            "covariance": covariance, "log_likelihood": ll,
            "null_log_likelihood": null_ll, "pseudo_r2": 1 - ll / null_ll,
            "n_obs": len(stacked), "n_choice_sets": info["n_choice_sets"],
            "choice_set_id_col": choice_set_id_col, "predictors": list(predictors),
            "inference": "model_based_independent_choice_events",
            "repeated_customers": info["unique_customers"] < info["n_choice_sets"],
            "model_object": fitted,
            "model_object_exog": "within_event_centered_divided_by_predictor_scale",
            "predictor_scale": dict(zip(predictors, scale)),
            "coefficient_units": "original_input_units"}


def fit_split_models(
    stacked: pd.DataFrame,
    attribute_groups: dict[str, list[str]],
    response: str = "y",
    **kwargs,
) -> dict:
    """Fit separate exploratory associations; never combine their coefficients."""
    if not attribute_groups:
        raise ValueError("At least one attribute group is required")
    results = {}
    for name, predictors in attribute_groups.items():
        result = fit_single_model(stacked, predictors, response, **kwargs)
        result.update(name=name, exploratory_only=True)
        results[name] = result
    return {"submodels": results, "approach": "split_exploratory",
            "exploratory_only": True,
            "limitation": "Omitted attributes may confound associations; coefficients cannot be combined into utilities, importance, WTP, or shares."}


def diagnostic_report(result: dict) -> str:
    """Describe model scope without interpreting signs as proof of validity."""
    models = result.get("submodels", {"full": result})
    lines = ["CONDITIONAL CHOICE MODEL DIAGNOSTICS", f"Approach: {result['approach']}"]
    if result.get("exploratory_only"):
        lines.append("Exploratory associations only; do not combine submodel coefficients.")
    for name, model in models.items():
        lines.append(f"[{name}] Choice events: {model['n_choice_sets']}; pseudo-R²: {model['pseudo_r2']:.3f}")
        for variable, coefficient in model['coefficients'].items():
            lines.append(f"  {variable}: coefficient={coefficient:+.3f}, p={model['p_values'][variable]:.3f}")
        if model.get('repeated_customers'):
            lines.append("Repeated customers: reported uncertainty assumes independent events and is not cluster-adjusted.")
        if model['coefficients'].get('price', -1) >= 0:
            lines.append("Nonnegative price coefficient: investigate design, omitted attributes and coding; WTP is unavailable.")
    return "\n".join(lines)

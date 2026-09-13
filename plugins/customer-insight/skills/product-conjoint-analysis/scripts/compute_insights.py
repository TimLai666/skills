"""Conjoint summaries with explicit grouping and a shared utility scale.

Prediction accepts a fitted model result or raw coefficients with same_model=True.
Never combine independently fitted coefficients. WTP additionally requires model
covariance and a 95% price interval strictly below zero. Units follow the price
predictor (undo any price scaling before interpreting currency).
"""
from __future__ import annotations

from typing import Any

import numpy as np
import pandas as pd


def _softmax(values: np.ndarray) -> np.ndarray:
    exponentials = np.exp(values - np.max(values))
    return exponentials / exponentials.sum()


def _expit(values: np.ndarray) -> np.ndarray:
    result = np.empty_like(values, dtype=float)
    positive = values >= 0
    result[positive] = 1 / (1 + np.exp(-values[positive]))
    exponentials = np.exp(values[~positive])
    result[~positive] = exponentials / (1 + exponentials)
    return result


def _coefficients(source, same_model=False, require_model=False):
    if 'coefficients' in source:
        if source.get('converged') is False:
            raise ValueError('Model did not converge.')
        if source.get('exploratory_only') or source.get('approach') not in ('conditional_logit', 'full'):
            raise ValueError('A single fitted full or conditional_logit model is required.')
        coefficients = source['coefficients']
    else:
        if require_model and not same_model:
            raise ValueError('Supply a fitted model result or explicitly set same_model=True.')
        coefficients = source
    if not coefficients or not all(np.isfinite(float(v)) for v in coefficients.values()):
        raise ValueError('Coefficients must be nonempty and finite.')
    return {k: float(v) for k, v in coefficients.items()}


def _groups(coefficients, groups):
    if not groups:
        raise ValueError('Explicit attribute groups are required.')
    seen = set()
    for predictors in groups.values():
        if not predictors or any(p not in coefficients or p in seen for p in predictors):
            raise ValueError('Groups must contain available, nonoverlapping predictors.')
        if len(set(predictors)) != len(predictors):
            raise ValueError('Duplicate predictor in group.')
        seen.update(predictors)


def compute_attribute_importance(
    part_worths: dict[str, Any],
    attribute_groups: dict[str, list[str]],
    price_range: tuple[float, float] | None = None,
    price_var: str = 'price',
    binary_separately: bool = False,
    *,
    continuous_ranges: dict[str, tuple[float, float]] | None = None,
) -> pd.DataFrame:
    """Dummy-coded groups include a zero reference; define each binary separately.

    The old name-based binary heuristic is removed. binary_separately=True is
    rejected: give each independent binary its own explicit attribute group.
    continuous_ranges maps each continuous predictor to its observed/design range.
    Each continuous predictor needs its own group; all predictors must be grouped.
    """
    if binary_separately:
        raise ValueError('Define independent binary attributes as separate groups.')
    coefs = _coefficients(part_worths)
    _groups(coefs, attribute_groups)
    expected = set(coefs) - {'intercept', 'Intercept', 'const'}
    grouped = {p for predictors in attribute_groups.values() for p in predictors}
    if grouped != expected:
        raise ValueError('Importance requires every non-intercept predictor exactly once.')
    ranges = dict(continuous_ranges or {})
    if price_range is not None:
        if price_var in ranges and tuple(ranges[price_var]) != tuple(price_range):
            raise ValueError('Conflicting price ranges.')
        ranges[price_var] = price_range
    if not set(ranges).issubset(expected):
        raise ValueError('Continuous range supplied for an unknown predictor.')
    if price_var in coefs and price_var not in ranges:
        raise ValueError('Price range is required.')
    rows = []
    for attr, predictors in attribute_groups.items():
        continuous = [p for p in predictors if p in ranges]
        if continuous:
            predictor = continuous[0]
            bounds = ranges[predictor]
            if len(predictors) != 1 or len(bounds) != 2:
                raise ValueError('Continuous predictors need their own group and (min, max) range.')
            low, high = map(float, bounds)
            if not np.isfinite([low, high]).all() or high <= low:
                raise ValueError('Continuous ranges must be finite and increasing.')
            spread = abs(coefs[predictor]) * (high - low)
        else:
            values = [0.0] + [coefs[p] for p in predictors]
            spread = max(values) - min(values)
        rows.append({'attribute': attr, 'range': spread})
    df = pd.DataFrame(rows)
    total = df['range'].sum()
    df['importance_pct'] = df['range'] / total * 100 if total else np.nan
    return df.sort_values('importance_pct', ascending=False).reset_index(drop=True)


def compute_wtp(part_worths: dict[str, Any], attribute_groups: dict[str, list[str]],
                price_var: str = 'price') -> pd.DataFrame:
    """Same-model WTP in price predictor units, with approximate delta-method CI.

    Requires named covariance from a single model; a price CI crossing zero or
    absent uncertainty suppresses the calculation via ValueError. Current
    inference supports independent choice events only; repeated customers need
    cluster-aware inference and are rejected. Intervals are
    approximate, not evidence of commercial viability or causal willingness.
    """
    if 'coefficients' not in part_worths:
        raise ValueError('WTP requires a fitted model result with covariance.')
    coefs = _coefficients(part_worths, require_model=True)
    if (part_worths.get('inference') != 'model_based_independent_choice_events'
            or part_worths.get('repeated_customers', False)):
        raise ValueError('WTP requires usable independent-event inference; repeated customers need cluster-aware inference.')
    _groups(coefs, attribute_groups)
    price = coefs.get(price_var)
    if price is None or price >= 0:
        raise ValueError('WTP requires a negative price coefficient from the same model.')
    covariance = part_worths.get('covariance')
    if covariance is None:
        raise ValueError('WTP requires covariance to assess price uncertainty.')
    try:
        cov = pd.DataFrame(covariance).loc[list(coefs), list(coefs)].astype(float)
    except (KeyError, ValueError, TypeError) as exc:
        raise ValueError('Covariance must be indexed by all coefficient names.') from exc
    matrix = cov.to_numpy()
    if (not np.isfinite(matrix).all() or not np.allclose(matrix, matrix.T)
            or np.linalg.eigvalsh(matrix).min() < -1e-10):
        raise ValueError('Covariance must be finite, symmetric and positive semidefinite.')
    price_se = np.sqrt(cov.loc[price_var, price_var])
    if price_se <= 0 or price + 1.96 * price_se >= 0:
        raise ValueError('Price uncertainty does not support finite WTP inference.')
    rows = []
    for attribute, predictors in attribute_groups.items():
        for level in predictors:
            if level == price_var:
                continue
            pw = coefs[level]
            estimate = -pw / price
            gradient = np.array([-1 / price, pw / price ** 2])
            variance = gradient @ cov.loc[[level, price_var], [level, price_var]].to_numpy() @ gradient
            margin = 1.96 * np.sqrt(max(0, variance))
            rows.append({'attribute': attribute, 'level': level, 'part_worth': pw,
                         'wtp_price_units': estimate, 'ci_lower': estimate - margin,
                         'ci_upper': estimate + margin, 'reliability': 'approximate 95% delta-method interval'})
    return pd.DataFrame(rows, columns=['attribute', 'level', 'part_worth', 'wtp_price_units',
                                      'ci_lower', 'ci_upper', 'reliability'])


def _utilities(cards, part_worths, card_id_col, same_model, intercept=0):
    coefs = _coefficients(part_worths, same_model, require_model=True)
    if cards.empty or card_id_col not in cards or cards[card_id_col].isna().any() or cards[card_id_col].duplicated().any():
        raise ValueError('Cards require nonempty, unique, nonmissing IDs.')
    if any(key not in cards for key in coefs):
        raise ValueError('Every model predictor must be present in cards.')
    values = cards[list(coefs)].to_numpy(dtype=float)
    if not np.isfinite(values).all() or not np.isfinite(intercept):
        raise ValueError('Predictors and intercept must be finite.')
    utilities = values @ np.array(list(coefs.values())) + intercept
    if not np.isfinite(utilities).all():
        raise ValueError('Utility calculation overflowed; check predictor scaling.')
    return pd.DataFrame({'card_id': cards[card_id_col].to_numpy(), 'utility': utilities})


def compute_share_of_preference(
    cards: pd.DataFrame, part_worths: dict[str, Any], card_id_col: str = 'card_id',
    *, same_model: bool = False,
) -> pd.DataFrame:
    """Stable softmax over exactly one supplied choice set, conditional on its cards."""
    if len(cards) < 2:
        raise ValueError('A choice set requires at least two alternatives.')
    df = _utilities(cards, part_worths, card_id_col, same_model)
    df['share_pct'] = _softmax(df.utility.to_numpy()) * 100
    return df.sort_values('share_pct', ascending=False).reset_index(drop=True)


def compute_choice_probability(
    cards: pd.DataFrame, part_worths: dict[str, Any], intercept: float = 0.0,
    card_id_col: str = 'card_id', *, same_model: bool = False,
) -> pd.DataFrame:
    """Choice-set softmax (changed from the former independent binary sigmoid).

    Common intercepts cancel in softmax. Input is one choice set, not a dataset
    containing several tasks. Use compute_binary_response_probability for binary
    acceptance models instead.
    """
    if len(cards) < 2:
        raise ValueError('A choice set requires at least two alternatives.')
    df = _utilities(cards, part_worths, card_id_col, same_model, intercept)
    df['prob_pct'] = _softmax(df.utility.to_numpy()) * 100
    df = df.sort_values('prob_pct', ascending=False).reset_index(drop=True)
    df['rank'] = df.index + 1
    return df


def compute_binary_response_probability(
    cards: pd.DataFrame, part_worths: dict[str, Any], intercept: float = 0.0,
    card_id_col: str = 'card_id', *, same_model: bool = False,
) -> pd.DataFrame:
    """Independent yes/no response probabilities; requires a binary response model."""
    if 'coefficients' in part_worths and part_worths.get('approach') == 'conditional_logit':
        raise ValueError('Conditional choice models do not identify binary acceptance probabilities.')
    df = _utilities(cards, part_worths, card_id_col, same_model, intercept)
    df['prob_pct'] = _expit(df.utility.to_numpy()) * 100
    return df.sort_values('prob_pct', ascending=False).reset_index(drop=True)


def compute_cost_benefit_roi(part_worths: dict[str, float],
                             attribute_costs: dict[str, float | None]) -> pd.DataFrame:
    """Legacy entry point: utility per supplied cost unit, NOT financial ROI.

    Costs must use the same currency and basis. Missing costs stay unknown;
    positive ratios do not imply profitability and no pursue/drop rule is made.
    Pass only the upgrade coefficients to summarize (exclude price/intercept).
    """
    coefs = _coefficients(part_worths)
    if any(level not in coefs for level in attribute_costs):
        raise ValueError('Cost supplied for a missing coefficient.')
    rows = []
    for level, pw in coefs.items():
        cost = attribute_costs.get(level)
        if cost is not None and (not np.isfinite(float(cost)) or float(cost) <= 0):
            raise ValueError('Supplied costs must be finite and positive; omit unknown costs and compare zero/negative costs separately.')
        rows.append({'level': level, 'part_worth': pw,
                     'unit_cost': float(cost) if cost is not None else np.nan,
                     'utility_per_cost_unit': pw / float(cost) if cost is not None else np.nan})
    return pd.DataFrame(rows).sort_values('utility_per_cost_unit', ascending=False, na_position='last').reset_index(drop=True)

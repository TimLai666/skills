"""Build and validate one chosen alternative per explicitly identified choice event.

With no consideration-set column, callers must explicitly confirm that all
defined cards were available using assume_all_available=True.
"""
from __future__ import annotations

from collections.abc import Iterable
from numbers import Number

import numpy as np
import pandas as pd


def build_stacked_data(
    card_definitions: pd.DataFrame,
    purchase_records: pd.DataFrame,
    card_id_col: str = "card_id",
    customer_id_col: str = "customer_id",
    consideration_set_col: str | None = None,
    *,
    choice_set_id_col: str = "choice_set_id",
    assume_all_available: bool = False,
) -> pd.DataFrame:
    """Expand each purchase row, preserving explicit event IDs or generating them.

    Explicit event IDs must be globally unique in purchase_records. Repeated
    customers are permitted; they do not identify choice events.
    Without observed consideration sets, assume_all_available=True explicitly
    asserts that every defined card was available for every purchase event.
    """
    if consideration_set_col is None and assume_all_available is not True:
        raise ValueError("Supply consideration sets or explicitly set assume_all_available=True")
    for frame, required in [(card_definitions, [card_id_col]),
                            (purchase_records, [customer_id_col, card_id_col])]:
        if frame.empty or not frame.columns.is_unique or not set(required) <= set(frame.columns):
            raise ValueError("Nonempty data with unique, required columns is required")
        if frame[required].isna().any().any():
            raise ValueError("Identifiers cannot be missing")
        _validate_finite_identifiers(frame[required].to_numpy().ravel())
    if len({card_id_col, customer_id_col, choice_set_id_col, "y"}) != 4:
        raise ValueError("Identifier and response column names must be distinct")
    if set(card_definitions.columns) & {customer_id_col, choice_set_id_col, "y"}:
        raise ValueError("Card attributes collide with reserved output columns")
    if card_definitions[card_id_col].duplicated().any():
        raise ValueError("Duplicate card definitions")
    if consideration_set_col is not None and consideration_set_col not in purchase_records:
        raise ValueError("Missing consideration-set column")
    events = (purchase_records[choice_set_id_col].tolist() if choice_set_id_col in purchase_records
              else list(range(len(purchase_records))))
    if pd.Series(events).isna().any() or pd.Series(events).duplicated().any():
        raise ValueError("Choice event IDs must be nonmissing and unique")
    _validate_finite_identifiers(events)
    cards = card_definitions.set_index(card_id_col, drop=False)
    rows = []
    for event, (_, purchase) in zip(events, purchase_records.iterrows()):
        chosen = purchase[card_id_col]
        if chosen not in cards.index:
            raise ValueError("Unknown chosen card")
        considered = purchase[consideration_set_col] if consideration_set_col else cards.index.tolist()
        if isinstance(considered, (str, bytes)) or not isinstance(considered, Iterable):
            raise ValueError("Consideration set must be a collection of card IDs")
        considered = list(considered)
        ids = pd.Series(considered, dtype=object)
        if len(ids) < 2 or ids.isna().any() or ids.duplicated().any():
            raise ValueError("Each event requires at least two distinct nonmissing cards")
        if not ids.isin(cards.index).all() or chosen not in considered:
            raise ValueError("Unknown considered card or chosen card missing from set")
        for cid in considered:
            row = cards.loc[cid].to_dict()
            row.update({customer_id_col: purchase[customer_id_col], choice_set_id_col: event,
                        "y": int(cid == chosen)})
            rows.append(row)
    columns = [choice_set_id_col, customer_id_col, card_id_col]
    columns += [c for c in card_definitions if c != card_id_col] + ["y"]
    stacked = pd.DataFrame(rows)[columns]
    validate_stacked(stacked, customer_id_col, choice_set_id_col=choice_set_id_col,
                     card_id_col=card_id_col)
    return stacked


def _validate_finite_identifiers(values: Iterable) -> None:
    """Keep string IDs valid while rejecting nonfinite numeric identifiers."""
    if any(isinstance(value, Number) and not np.isfinite(value) for value in values):
        raise ValueError("Numeric identifiers must be finite")


def validate_stacked(
    stacked: pd.DataFrame,
    customer_id_col: str = "customer_id",
    *,
    choice_set_id_col: str = "choice_set_id",
    card_id_col: str = "card_id",
    response: str = "y",
    predictors: list[str] | None = None,
) -> dict:
    """Raise ValueError for invalid events; return event-based diagnostics."""
    required = [customer_id_col, choice_set_id_col, card_id_col, response]
    if len(set(required)) != len(required):
        raise ValueError("Identifier and response column names must be distinct")
    if stacked.empty or not stacked.columns.is_unique or not set(required) <= set(stacked.columns):
        raise ValueError("Nonempty stacked data with required unique columns is required")
    if stacked[required].isna().any().any():
        raise ValueError("Missing identifiers or response")
    _validate_finite_identifiers(stacked[required[:-1]].to_numpy().ravel())
    if not stacked[response].isin([0, 1]).all():
        raise ValueError("Response must be binary 0 or 1")
    if stacked.duplicated([choice_set_id_col, card_id_col]).any():
        raise ValueError("Duplicate alternative within choice event")
    groups = stacked.groupby(choice_set_id_col, sort=False)
    if (groups.size() < 2).any() or (groups[response].sum() != 1).any():
        raise ValueError("Every choice event requires at least two alternatives and exactly one chosen")
    if (groups[customer_id_col].nunique() != 1).any():
        raise ValueError("Each choice event must belong to one customer")
    if predictors is not None:
        if not predictors or len(set(predictors)) != len(predictors) or not set(predictors) <= set(stacked.columns):
            raise ValueError("Predictors must be nonempty, unique, existing columns")
        if set(predictors) & set(required):
            raise ValueError("Identifiers and response cannot be predictors")
        try:
            values = stacked[predictors].to_numpy(dtype=float)
        except (ValueError, TypeError) as exc:
            raise ValueError("Predictors must be finite numeric values") from exc
        if not np.isfinite(values).all():
            raise ValueError("Predictors must be finite numeric values")
    return {"total_rows": len(stacked), "unique_customers": stacked[customer_id_col].nunique(),
            "n_choice_sets": groups.ngroups, "positive_rate": float(stacked[response].mean()),
            "min_alternatives": int(groups.size().min()), "max_alternatives": int(groups.size().max())}


# ----------------------------------------------------------------------------
# Demo with the case-study data
# ----------------------------------------------------------------------------
if __name__ == "__main__":
    # 8 product cards from the safety-glasses case study
    cards = pd.DataFrame([
        # card_id, UKNOW, MORKSUKY, price, pink, purple, size_145, size_162, anti_scratch, uv_protection
        {"card_id": 1, "UKNOW": 0, "MORKSUKY": 0, "price": 15.99, "pink": 0, "purple": 0, "size_145": 0, "size_162": 0, "anti_scratch": 1, "uv_protection": 1},
        {"card_id": 2, "UKNOW": 0, "MORKSUKY": 0, "price": 15.99, "pink": 1, "purple": 0, "size_145": 0, "size_162": 0, "anti_scratch": 1, "uv_protection": 1},
        {"card_id": 3, "UKNOW": 1, "MORKSUKY": 0, "price": 13.98, "pink": 0, "purple": 0, "size_145": 0, "size_162": 1, "anti_scratch": 0, "uv_protection": 1},
        {"card_id": 4, "UKNOW": 1, "MORKSUKY": 0, "price": 13.98, "pink": 1, "purple": 0, "size_145": 0, "size_162": 1, "anti_scratch": 0, "uv_protection": 1},
        {"card_id": 5, "UKNOW": 1, "MORKSUKY": 0, "price": 13.98, "pink": 0, "purple": 1, "size_145": 0, "size_162": 1, "anti_scratch": 0, "uv_protection": 1},
        {"card_id": 6, "UKNOW": 0, "MORKSUKY": 1, "price": 14.95, "pink": 0, "purple": 0, "size_145": 1, "size_162": 0, "anti_scratch": 1, "uv_protection": 0},
        {"card_id": 7, "UKNOW": 0, "MORKSUKY": 1, "price": 14.95, "pink": 1, "purple": 0, "size_145": 1, "size_162": 0, "anti_scratch": 1, "uv_protection": 0},
        {"card_id": 8, "UKNOW": 0, "MORKSUKY": 1, "price": 14.95, "pink": 0, "purple": 1, "size_145": 1, "size_162": 0, "anti_scratch": 1, "uv_protection": 0},
    ])

    # Mock 20 customers' purchase records
    purchases = pd.DataFrame([
        {"customer_id": i+1, "card_id": (i % 8) + 1} for i in range(20)
    ])

    print("Synthetic demo assumption: all eight cards were available for every event.")
    stacked = build_stacked_data(cards, purchases, assume_all_available=True)
    print(stacked.head(10))
    print()
    print("Diagnostics:", validate_stacked(stacked))
    print(f"\nFinal shape: {stacked.shape}  (expected: 20 × 8 = 160 rows)")

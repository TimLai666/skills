"""Summarize product quality scores, excluding missing evidence from means."""


def _mean(values):
    observed = [value for value in values if value is not None]
    return {'mean': sum(observed) / len(observed) if observed else None,
            'n_scored': len(observed), 'n_total': len(values)}


def summarize_scores(scores, attribute_ids):
    """Return JSON-safe means and a ranking over all products' common attributes.

    scores maps product IDs to aligned lists of integer 0–10 scores or None.
    Ties share competition rank (1, 1, 3). No rounding is applied here.
    """
    if (not isinstance(attribute_ids, list) or not attribute_ids
            or any(not isinstance(a, str) or not a.strip() for a in attribute_ids)
            or len(set(attribute_ids)) != len(attribute_ids)):
        raise ValueError('attribute_ids must be a nonempty list of unique IDs')
    if not isinstance(scores, dict) or not scores:
        raise ValueError('scores must be a nonempty product mapping')
    for product, values in scores.items():
        if not isinstance(product, str) or not product.strip():
            raise ValueError('product IDs must be nonempty strings')
        if not isinstance(values, list) or len(values) != len(attribute_ids):
            raise ValueError(f'{product}: scores must align with attribute_ids')
        if any(v is not None and (type(v) is not int or not 0 <= v <= 10) for v in values):
            raise ValueError(f'{product}: scores must be integers 0–10 or None')

    common = [i for i in range(len(attribute_ids))
              if all(values[i] is not None for values in scores.values())]
    ranking = []
    reason = None
    if len(scores) < 2:
        reason = 'fewer_than_two_products'
    elif not common:
        reason = 'no_common_scored_attributes'
    else:
        totals = {product: sum(values[i] for i in common) for product, values in scores.items()}
        previous = None
        rank = 0
        for position, product in enumerate(sorted(totals, key=totals.get, reverse=True), 1):
            if totals[product] != previous:
                rank = position
            ranking.append({'product': product, 'rank': rank,
                            'mean': totals[product] / len(common)})
            previous = totals[product]
    return {
        'products': {product: _mean(values) for product, values in scores.items()},
        'attributes': {attribute: _mean([v[i] for v in scores.values()])
                       for i, attribute in enumerate(attribute_ids)},
        'common_attributes': [attribute_ids[i] for i in common],
        'n_common': len(common), 'n_attributes': len(attribute_ids),
        'ranking': ranking, 'ranking_unavailable_reason': reason,
    }

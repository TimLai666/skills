"""Synthetic choice data verifies the model-to-insights contract, not market claims."""
import sys
import unittest
from itertools import product
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from build_stacked_data import build_stacked_data
from fit_logistic_conjoint import fit_single_model
from compute_insights import (
    compute_attribute_importance, compute_wtp, compute_choice_probability,
    compute_cost_benefit_roi,
)


class WorkflowTests(unittest.TestCase):
    def test_full_choice_workflow(self):
        cards = pd.DataFrame(
            [(i, quality, price) for i, (quality, price) in enumerate(
                product((0, 1), (2., 4., 6.)))],
            columns=['card_id', 'quality', 'price'],
        )
        utility = .8 * cards.quality - .4 * cards.price
        probabilities = np.exp(utility - utility.max())
        probabilities /= probabilities.sum()
        rng = np.random.default_rng(82)
        purchases = pd.DataFrame({
            'customer_id': range(900),
            'card_id': rng.choice(cards.card_id, size=900, p=probabilities),
        })
        data = build_stacked_data(cards, purchases, assume_all_available=True)
        model = fit_single_model(data, ['quality', 'price'])
        np.testing.assert_allclose(list(model['coefficients'].values()), [.8, -.4], atol=.2)
        importance = compute_attribute_importance(
            model, {'quality': ['quality'], 'price': ['price']}, price_range=(2., 6.),
        )
        self.assertAlmostEqual(importance.importance_pct.sum(), 100.)
        choice = compute_choice_probability(cards, model)
        self.assertAlmostEqual(choice.prob_pct.sum(), 100.)
        self.assertEqual(choice.card_id.iloc[0], 3)  # quality=1, price=2
        wtp = compute_wtp(model, {'quality': ['quality']})
        self.assertGreater(wtp.wtp_price_units.iloc[0], 0)
        self.assertLess(wtp.ci_lower.iloc[0], wtp.wtp_price_units.iloc[0])
        self.assertGreater(wtp.ci_upper.iloc[0], wtp.wtp_price_units.iloc[0])
        costs = compute_cost_benefit_roi({'quality': model['coefficients']['quality']}, {})
        self.assertTrue(costs.utility_per_cost_unit.isna().all())


if __name__ == '__main__':
    unittest.main()

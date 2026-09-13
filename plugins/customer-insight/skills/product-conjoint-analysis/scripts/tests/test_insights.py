import sys
import unittest
from pathlib import Path
import numpy as np
import pandas as pd
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import compute_insights as ci


class InsightsTests(unittest.TestCase):
    def test_continuous_range_and_full_coverage(self):
        coefs = {'size': .5, 'x': 1}
        result = ci.compute_attribute_importance(coefs, {'size': ['size'], 'feature': ['x']},
                                                 continuous_ranges={'size': (100, 110)})
        self.assertEqual(result.loc[result.attribute == 'size', 'range'].iloc[0], 5)
        for groups in ({'size': ['size']}, {'feature': ['missing']}):
            with self.assertRaises(ValueError):
                ci.compute_attribute_importance(coefs, groups)

    def test_failed_model_and_single_choice_rejected(self):
        cards = pd.DataFrame({'card_id': [1, 2], 'x': [1, 2]})
        with self.assertRaises(ValueError):
            ci.compute_choice_probability(cards, {'coefficients': {'x': 1},
                                          'approach': 'conditional_logit', 'converged': False})
        with self.assertRaises(ValueError):
            ci.compute_choice_probability(cards.iloc[:1], {'x': 1}, same_model=True)
        ordinary = ci.compute_choice_probability(cards, {'x': 1}, same_model=True)
        shifted = ci.compute_choice_probability(cards, {'x': 1}, intercept=1000, same_model=True)
        np.testing.assert_allclose(ordinary.prob_pct, shifted.prob_pct)

    def test_wtp_model_uncertainty_gates(self):
        base = {'coefficients': {'x': 2, 'price': -1}, 'approach': 'conditional_logit',
                'inference': 'model_based_independent_choice_events', 'converged': True,
                'covariance': pd.DataFrame([[.04, 0], [0, .01]], index=['x', 'price'], columns=['x', 'price'])}
        for update in ({'coefficients': {'x': 2, 'price': 1}},
                       {'coefficients': {'x': 2, 'price': -1e-12}},
                       {'covariance': None}, {'inference': 'unavailable'},
                       {'converged': False}, {'repeated_customers': True}):
            with self.assertRaises(ValueError):
                ci.compute_wtp(dict(base, **update), {'feature': ['x']})

    def test_brand_remains_one_attribute(self):
        result = ci.compute_attribute_importance({'UKNOW': .1, 'MORKSUKY': .4}, {'brand': ['UKNOW', 'MORKSUKY']})
        self.assertEqual(result.attribute.tolist(), ['brand'])

    def test_missing_and_nonfinite_coefficients(self):
        for coefs in ({}, {'x': np.nan}):
            with self.assertRaises(ValueError):
                ci.compute_attribute_importance(coefs, {'feature': ['x']})
        with self.assertRaises(ValueError):
            ci.compute_attribute_importance({'price': 0}, {'price': ['price']}, (2, 1))

    def test_stable_choice_set(self):
        cards = pd.DataFrame({'card_id': [1, 2], 'x': [1000, 999]})
        result = ci.compute_share_of_preference(cards, {'x': 1}, same_model=True)
        self.assertAlmostEqual(result.share_pct.sum(), 100)
        self.assertAlmostEqual(result.share_pct.iloc[0], 73.105857863)
        for bad in (cards.drop(columns='x'), cards.assign(x=np.nan)):
            with self.assertRaises(ValueError):
                ci.compute_share_of_preference(bad, {'x': 1}, same_model=True)
        with self.assertRaises(ValueError):
            ci.compute_share_of_preference(cards, {'x': 1})

    def test_stable_binary(self):
        cards = pd.DataFrame({'card_id': [1, 2], 'x': [1000, -1000]})
        result = ci.compute_binary_response_probability(cards, {'x': 1}, same_model=True)
        self.assertEqual(result.prob_pct.tolist(), [100, 0])

    def test_wtp_requires_supported_negative_price(self):
        for price in (1, 0, np.nan, -1):
            with self.assertRaises(ValueError):
                ci.compute_wtp({'x': 2, 'price': price}, {'feature': ['x']})
        model = {'coefficients': {'x': 2, 'price': -1}, 'approach': 'conditional_logit',
                 'inference': 'model_based_independent_choice_events',
                 'covariance': pd.DataFrame([[.04, 0], [0, .01]], index=['x', 'price'], columns=['x', 'price'])}
        result = ci.compute_wtp(model, {'feature': ['x']})
        self.assertEqual(result.wtp_price_units.iloc[0], 2)
        self.assertLess(result.ci_lower.iloc[0], 2)
        self.assertGreater(result.ci_upper.iloc[0], 2)
        model['covariance'].loc['price', 'price'] = 1
        with self.assertRaises(ValueError):
            ci.compute_wtp(model, {'feature': ['x']})

    def test_choice_and_split_model_boundaries(self):
        cards = pd.DataFrame({'card_id': [1, 2], 'x': [1000, 999]})
        result = ci.compute_choice_probability(cards, {'x': 1}, same_model=True)
        self.assertAlmostEqual(result.prob_pct.sum(), 100)
        for model in ({'coefficients': {'x': 1}, 'approach': 'split_exploratory'},
                      {'coefficients': {'x': 1}, 'approach': 'conditional_logit', 'exploratory_only': True}):
            with self.assertRaises(ValueError):
                ci.compute_choice_probability(cards, model)

    def test_zero_importance_is_undefined(self):
        result = ci.compute_attribute_importance({'x': 0}, {'feature': ['x']})
        self.assertTrue(result.importance_pct.isna().all())
        result = ci.compute_attribute_importance({'x': 1, 'y': 2}, {'x': ['x'], 'y': ['y']})
        self.assertEqual(set(result.attribute), {'x', 'y'})

    def test_cost_unit_changes_ratio_without_recommendation(self):
        dollars = ci.compute_cost_benefit_roi({'x': 2}, {'x': 2})
        cents = ci.compute_cost_benefit_roi({'x': 2}, {'x': 200})
        self.assertAlmostEqual(dollars.utility_per_cost_unit.iloc[0], 100 * cents.utility_per_cost_unit.iloc[0])
        self.assertNotIn('recommendation', cents)

    def test_cost_ratio_is_not_financial_roi(self):
        result = ci.compute_cost_benefit_roi({'x': 2, 'y': 1}, {'x': 2})
        self.assertNotIn('roi', result.columns)
        self.assertNotIn('recommendation', result.columns)
        self.assertEqual(result.loc[result.level == 'x', 'utility_per_cost_unit'].iloc[0], 1)
        self.assertTrue(np.isnan(result.loc[result.level == 'y', 'unit_cost'].iloc[0]))
        for cost in (0, -1, np.nan):
            with self.assertRaises(ValueError):
                ci.compute_cost_benefit_roi({'x': 2}, {'x': cost})

if __name__ == '__main__':
    unittest.main()

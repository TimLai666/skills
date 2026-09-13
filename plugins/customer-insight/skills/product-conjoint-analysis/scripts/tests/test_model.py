import sys
import unittest
from pathlib import Path
import numpy as np
import pandas as pd
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from build_stacked_data import build_stacked_data, validate_stacked
from fit_logistic_conjoint import fit_single_model, fit_split_models

class DataTests(unittest.TestCase):
    def test_requires_explicit_availability_assumption(self):
        with self.assertRaisesRegex(ValueError, 'assume_all_available'):
            build_stacked_data(self.cards, self.purchases)

    def test_direct_validation_rejects_name_collisions_and_infinite_ids(self):
        data = build_stacked_data(self.cards, self.purchases, assume_all_available=True)
        with self.assertRaisesRegex(ValueError, 'distinct'):
            validate_stacked(data, choice_set_id_col='customer_id')
        for column in ['customer_id', 'choice_set_id', 'card_id']:
            with self.subTest(column=column):
                with self.assertRaises(ValueError):
                    validate_stacked(data.assign(**{column: np.inf}))

    def setUp(self):
        self.cards = pd.DataFrame({'card_id':[1,2], 'x':[0.,1.]})
        self.purchases = pd.DataFrame({'customer_id':[7,7], 'card_id':[1,2]})
    def test_repeated_customer_is_two_events(self):
        data = build_stacked_data(self.cards, self.purchases, assume_all_available=True)
        self.assertEqual(data.choice_set_id.nunique(), 2)
        self.assertEqual(validate_stacked(data)['n_choice_sets'], 2)
    def test_invalid_average_does_not_hide_events(self):
        data = pd.DataFrame({'choice_set_id':[0,0,1,1], 'customer_id':[0,0,1,1], 'card_id':[1,2,1,2], 'y':[0,0,1,1]})
        with self.assertRaises(ValueError): validate_stacked(data)
    def test_bad_cards_and_sets(self):
        for cards in [pd.concat([self.cards,self.cards.iloc[:1]]), self.cards.assign(card_id=[1,None])]:
            with self.subTest(cards=cards):
                with self.assertRaises(ValueError): build_stacked_data(cards,self.purchases, assume_all_available=True)
        for considered in [[1], [1,1], [2,3], [2,2], None]:
            with self.subTest(considered=considered):
                with self.assertRaises(ValueError): build_stacked_data(self.cards,self.purchases.assign(sets=[considered,considered]),consideration_set_col='sets')
    def test_invalid_y_duplicate_card_nonfinite(self):
        data=build_stacked_data(self.cards,self.purchases, assume_all_available=True)
        for bad in [data.assign(y=[2,0,0,1]),data.assign(card_id=[1,1,1,2]),data.assign(x=np.inf)]:
            with self.subTest(bad=bad):
                with self.assertRaises(ValueError): fit_single_model(bad,['x'])
    def test_explicit_events_and_missing_identifiers(self):
        explicit=self.purchases.assign(choice_set_id=['first','second'])
        self.assertEqual(build_stacked_data(self.cards,explicit, assume_all_available=True).choice_set_id.unique().tolist(),['first','second'])
        for purchases in [explicit.assign(choice_set_id=['a','a']),explicit.assign(choice_set_id=['a',None]),
                          explicit.assign(card_id=[1,99]),explicit.assign(customer_id=[None,7])]:
            with self.subTest(purchases=purchases):
                with self.assertRaises(ValueError): build_stacked_data(self.cards,purchases, assume_all_available=True)
    def test_missing_chosen_and_variable_sets(self):
        cards=pd.DataFrame({'card_id':[1,2,3],'x':[0,1,2]})
        with self.assertRaises(ValueError):
            build_stacked_data(cards,self.purchases.assign(sets=[[2,3],[1,2]]),consideration_set_col='sets')
        data=build_stacked_data(cards,self.purchases.assign(sets=[[1,2,3],[1,2]]),consideration_set_col='sets')
        self.assertEqual(validate_stacked(data)['min_alternatives'],2)
        self.assertEqual(validate_stacked(data)['max_alternatives'],3)

class ModelTests(unittest.TestCase):
    @staticmethod
    def synthetic(n=600):
        rng=np.random.default_rng(192)
        rows=[]
        for g in range(n):
            x=rng.normal(size=(2,2)); u=x @ np.array([.8,-.6]); p=np.exp(u-u.max()); p/=p.sum()
            chosen=rng.choice(2,p=p)
            for j in range(2): rows.append([g,g//2,j,int(j==chosen),*x[j]])
        return pd.DataFrame(rows,columns=['choice_set_id','customer_id','card_id','y','quality','price'])
    def test_recovery_and_pairwise_logistic(self):
        import statsmodels.api as sm
        data=self.synthetic(); fit=fit_single_model(data,['quality','price'])
        np.testing.assert_allclose(list(fit['coefficients'].values()), [.8,-.6],atol=.2)
        a=data.iloc[::2]; b=data.iloc[1::2]
        diff=a[['quality','price']].to_numpy()-b[['quality','price']].to_numpy()
        reference=sm.Logit(a.y.to_numpy(),diff).fit(disp=False)
        np.testing.assert_allclose(list(fit['coefficients'].values()), reference.params,atol=1e-3)
        self.assertNotIn('const',fit['coefficients'])
        self.assertEqual(fit['n_choice_sets'],600)
        self.assertIn('covariance',fit)
    def test_rank_deficient_within_sets(self):
        data=self.synthetic(20); data['confounded']=data.quality+data.choice_set_id
        with self.assertRaisesRegex(ValueError,'rank'): fit_single_model(data,['quality','confounded'])
    def test_unit_recoding_preserves_estimates_and_probabilities(self):
        from scipy.special import softmax
        predictors = ['quality', 'price']
        data = self.synthetic()
        baseline = fit_single_model(data, predictors)
        coefficients = np.array(list(baseline['coefficients'].values()))
        baseline_probabilities = softmax(
            (data[predictors].to_numpy() @ coefficients).reshape(-1, 2), axis=1)
        for scale in [1e-6, 1e6]:
            with self.subTest(scale=scale):
                recoded = data.copy()
                recoded[predictors] *= scale
                fitted = fit_single_model(recoded, predictors)
                recoded_coefficients = np.array(list(fitted['coefficients'].values()))
                np.testing.assert_allclose(recoded_coefficients * scale, coefficients, rtol=1e-5)
                np.testing.assert_allclose(fitted['covariance'] * scale**2,
                                           baseline['covariance'], rtol=1e-4)
                np.testing.assert_allclose(np.array(list(fitted['std_errors'].values())) * scale,
                                           list(baseline['std_errors'].values()), rtol=1e-4)
                np.testing.assert_allclose(list(fitted['p_values'].values()),
                                           list(baseline['p_values'].values()), rtol=1e-4)
                probabilities = softmax(
                    (recoded[predictors].to_numpy() @ recoded_coefficients).reshape(-1, 2), axis=1)
                np.testing.assert_allclose(probabilities, baseline_probabilities, atol=1e-6)
    def test_split_is_not_combined(self):
        result=fit_split_models(self.synthetic(),{'q':['quality'],'p':['price']})
        self.assertNotIn('part_worths',result)
        self.assertEqual(result['approach'],'split_exploratory')
    def test_separation_and_nonconvergence_rejected(self):
        data=self.synthetic(30); data['perfect']=data.y
        with self.assertRaises(ValueError): fit_single_model(data,['perfect'])
        with self.assertRaises(RuntimeError): fit_single_model(self.synthetic(),['quality','price'],maxiter=0)
    def test_quasi_separation_rejected(self):
        data=self.synthetic(30); data['quasi']=np.where(data.choice_set_id < 10,data.y,0)
        with self.assertRaisesRegex(ValueError,'separation'): fit_single_model(data,['quasi'])
    def test_three_alternative_equal_choice_null_model(self):
        cards=pd.DataFrame({'card_id':[0,1,2],'x':[-1.,0.,1.]})
        purchases=pd.DataFrame({'customer_id':range(90),'card_id':[0,1,2]*30})
        fit=fit_single_model(build_stacked_data(cards,purchases, assume_all_available=True),['x'])
        self.assertAlmostEqual(fit['coefficients']['x'],0.,places=5)
        self.assertAlmostEqual(fit['log_likelihood'],-90*np.log(3),places=5)

if __name__=='__main__': unittest.main()

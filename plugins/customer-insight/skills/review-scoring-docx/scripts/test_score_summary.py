import json
import unittest

from score_summary import summarize_scores


class ScoreSummaryTests(unittest.TestCase):
    def test_missing_excluded(self):
        result = summarize_scores({'A': [8, 6, None]}, ['01', '02', '03'])
        self.assertEqual(result['products']['A'], {'mean': 7, 'n_scored': 2, 'n_total': 3})

    def test_zero_included(self):
        self.assertEqual(summarize_scores({'A': [8, 6, 0]}, ['a', 'b', 'c'])['products']['A']['mean'], 14 / 3)

    def test_all_missing(self):
        result = summarize_scores({'A': [None], 'B': [None]}, ['a'])
        self.assertIsNone(result['products']['A']['mean'])
        self.assertIsNone(result['attributes']['a']['mean'])
        self.assertEqual(result['ranking'], [])
        json.dumps(result, allow_nan=False)

    def test_common_attributes_change_ranking(self):
        result = summarize_scores({'A': [8, 0], 'B': [7, None]}, ['a', 'b'])
        self.assertLess(result['products']['A']['mean'], result['products']['B']['mean'])
        self.assertEqual(result['common_attributes'], ['a'])
        self.assertEqual([r['product'] for r in result['ranking']], ['A', 'B'])
        self.assertEqual(result['attributes']['b']['n_scored'], 1)

    def test_no_common_and_missing_product_not_removed(self):
        for scores in ({'A': [8, None], 'B': [None, 6]}, {'A': [8, 6], 'B': [None, None]}):
            self.assertEqual(summarize_scores(scores, ['a', 'b'])['ranking'], [])

    def test_single_product(self):
        self.assertEqual(summarize_scores({'A': [8]}, ['a'])['ranking'], [])

    def test_ties(self):
        result = summarize_scores({'A': [8], 'B': [8], 'C': [6]}, ['a'])
        self.assertEqual([r['rank'] for r in result['ranking']], [1, 1, 3])

    def test_invalid_scores(self):
        for value in (-1, 11, True, 5.0, float('nan'), '5', ''):
            with self.subTest(value=value), self.assertRaises(ValueError):
                summarize_scores({'A': [value]}, ['a'])

    def test_invalid_shape_and_ids(self):
        for scores, ids in [({}, ['a']), ({'A': []}, []), ({'A': [8]}, ['a', 'b']),
                            ({'A': [8, 6]}, ['a', 'a']), ({'': [8]}, ['a'])]:
            with self.subTest(scores=scores, ids=ids), self.assertRaises(ValueError):
                summarize_scores(scores, ids)


if __name__ == '__main__':
    unittest.main()

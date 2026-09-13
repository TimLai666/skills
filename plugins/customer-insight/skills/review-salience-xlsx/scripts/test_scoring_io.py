import tempfile
import unittest
from pathlib import Path

from scoring_io import load_reviews, load_scored_csv, normalize_batch_scores, validate_scores


class ScoringIOTests(unittest.TestCase):
    def file(self, content):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        path = Path(temp.name) / 'reviews.csv'
        path.write_text(content, encoding='utf-8')
        return path

    def test_short_multilingual_and_full_text_preserved(self):
        path = self.file('body,other\n很容易壞,x\n悪い,x\n"  fine\nreally  ",x\n"   ",x\n,x\n')
        self.assertEqual(load_reviews(path), ['很容易壞', '悪い', '  fine\nreally  '])

    def test_malformed_csv_rejected(self):
        for content in ['', 'other\nx\n', 'body,body\nx,y\n', 'body,other\nx\n', 'body\nx,y\n', 'body\n"unfinished\n']:
            with self.subTest(content=content), self.assertRaises(ValueError):
                load_reviews(self.file(content))

    def test_scores_reject_nonintegers_and_out_of_range(self):
        for value in [True, False, 1.5, 1.0, '1', -1, 8, None]:
            with self.subTest(value=value), self.assertRaises(ValueError):
                validate_scores({'p': [[value]]}, {'p': ['text']}, [('01', 'fit')])
        validate_scores({'p': [[0], [7]]}, {'p': ['a', 'b']}, [('01', 'fit')])

    def test_scores_require_exact_products_rows_and_attributes(self):
        for scores in [{}, {'p': [[1]], 'q': []}, {'p': []}, {'p': [[1, 2]]}]:
            with self.subTest(scores=scores), self.assertRaises(ValueError):
                validate_scores(scores, {'p': ['a']}, [('01', 'fit')])

    def test_rest_list_and_object_both_validate(self):
        for response in [[[2]], {'scores': [[2]]}]:
            self.assertEqual(normalize_batch_scores(response, ['x'], [('01', 'fit')]), [[2]])
        for response in [{'scores': [[2.5]]}, {'unexpected': []}, [2], []]:
            with self.subTest(response=response), self.assertRaises(ValueError):
                normalize_batch_scores(response, ['x'], [('01', 'fit')])

    def test_csv_reordered_rows_restored(self):
        path = self.file('review_id,s01\np_0002,7\np_0001,0\n')
        self.assertEqual(load_scored_csv(path, {'p': ['a', 'b']}, [('01', 'fit')]), {'p': [[0], [7]]})

    def test_csv_rejects_invalid_scores_missing_unknown_and_duplicate_ids(self):
        for rows in ['p_0001,1.5\n', 'p_0001,1.0\n', 'p_0001,True\n', 'p_0001,8\n', 'p_0001,\n', 'wrong,1\n', '', 'p_0001,1\np_0001,2\n']:
            with self.subTest(rows=rows), self.assertRaises(ValueError):
                load_scored_csv(self.file('review_id,s01\n' + rows), {'p': ['a']}, [('01', 'fit')])


if __name__ == '__main__':
    unittest.main()

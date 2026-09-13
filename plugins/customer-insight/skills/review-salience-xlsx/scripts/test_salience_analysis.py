import unittest

import numpy as np

from salience_analysis import analyze_salience, cluster_pc_scores, fit_salience_pca, iterative_prune


class AnalysisTests(unittest.TestCase):
    def test_constant_columns_are_identified_and_keep_catalog_alignment(self):
        scores, result = fit_salience_pca([[0, 4, 7], [3, 4, 4], [7, 4, 0]])
        self.assertEqual(result['excluded_constant_columns'], [1])
        self.assertEqual(len(result['loadings']), 3)
        self.assertTrue(all(v == 0 for v in result['loadings'][1]))

    def test_pca_with_fewer_reviews_than_attributes(self):
        scores, result = fit_salience_pca(np.array([[0, 1, 2, 3], [1, 2, 3, 4], [2, 3, 4, 5]]))
        self.assertEqual(scores.shape[0], 3)
        self.assertLessEqual(result['n_components'], 3)
        self.assertTrue(np.isfinite(scores).all())

    def test_constant_data_has_no_invented_components(self):
        for matrix in (np.zeros((10, 4)), np.ones((10, 4)), np.ones((1, 4))):
            scores, result = fit_salience_pca(matrix)
            self.assertEqual(scores.shape, (len(matrix), 0))
            self.assertEqual(result['status'], 'unavailable')

    def test_outlier_does_not_survive_as_rejected_cluster(self):
        pc = np.array([[0.]] * 99 + [[7.]])
        model, active, history = iterative_prune(pc, 5, 5)
        self.assertEqual(len(set(model.predict(pc))), 1)
        self.assertEqual(active.sum(), 99)
        self.assertEqual(history[-1]['k'], 1)

    def test_normal_groups_all_rows_aligned_and_threshold_met(self):
        rows = [{'review_id': f'id-{i}', 'product': 'P', 's01': i % 2 * 7,
                 's02': (1 - i % 2) * 7} for i in range(80)]
        pca, pcs, groups = analyze_salience(rows, ['01', '02'], ['A', 'B'])
        self.assertEqual(groups['status'], 'segmented')
        self.assertEqual(groups['final_k'], 2)
        self.assertEqual(groups['review_ids'], [r['review_id'] for r in rows])
        self.assertEqual([r['review_id'] for r in pcs], groups['review_ids'])
        self.assertTrue(all(n >= 4 for n in groups['cluster_sizes'].values()))
        self.assertEqual(len(groups['final_labels']), 80)

    def test_all_zero_preserves_every_review_without_silhouette(self):
        rows = [{'review_id': i, 'product': 'P', 's01': 0} for i in range(5)]
        _, _, result = analyze_salience(rows, ['01'], ['A'])
        self.assertEqual(result['status'], 'unsegmented')
        self.assertEqual(result['final_labels'], [0] * 5)
        self.assertIsNone(result['final_silhouette'])

    def test_pruning_refits_and_reassigns_outlier_to_two_retained_groups(self):
        pc = np.array([[0.]] * 49 + [[5.]] * 50 + [[100.]])
        result = cluster_pc_scores(pc, k_start=3)
        self.assertEqual(result['final_k'], 2)
        self.assertEqual(sum(result['active_mask']), 99)
        self.assertEqual(sum(result['cluster_sizes'].values()), 100)
        self.assertTrue(all(n >= 5 for n in result['cluster_sizes'].values()))

    def test_exact_five_percent_is_retained(self):
        result = cluster_pc_scores(np.array([[0.]] * 95 + [[5.]] * 5), k_start=2)
        self.assertEqual(result['final_k'], 2)
        self.assertEqual(sorted(result['cluster_sizes'].values()), [5, 95])

    def test_tiny_corpus_all_unique_has_no_invalid_silhouette(self):
        result = cluster_pc_scores([[0.], [1.]], k_start=5)
        self.assertEqual(result['final_k'], 2)
        self.assertIsNone(result['final_silhouette'])

    def test_identical_pc_rows_returns_single_group(self):
        result = cluster_pc_scores(np.ones((10, 2)), k_start=9)
        self.assertEqual(result['status'], 'unsegmented')
        self.assertIsNone(result['final_silhouette'])

    def test_all_small_clusters_restore_full_data_single_group(self):
        result = cluster_pc_scores([[0.], [5.], [10.]], k_start=3, min_pct=0.5)
        self.assertEqual(result['final_labels'], [0, 0, 0])
        self.assertTrue(all(result['active_mask']))

    def test_invalid_scores_rejected(self):
        for value in (1.0, 1.5, float('nan'), 8, -1, True):
            with self.assertRaises(ValueError):
                analyze_salience([{'review_id': 1, 'product': 'P', 's01': value}], ['01'], ['A'])


if __name__ == '__main__':
    unittest.main()

import unittest

import pandas as pd

from stp_runner import reporting


class ReportingEvidenceTests(unittest.TestCase):
    def setUp(self):
        self.foundation = {
            'dimension_catalog': [{
                'column': 'bag', 'label': 'Storage bag', 'theme': 'accessories',
                'salience_column': 'bag_salience', 'quality_column': 'bag_quality',
                'stat_roles': ['segmentation', 'positioning'],
                'theory_annotations': {'service_value': ['convenience']},
            }],
            'theory_extensions': {'service_value': {
                'rationale': 'Explains evidence about convenience.',
                'subtheories': ['convenience', 'accessibility'],
            }},
            'attribute_extraction_summary': {'actual_count': 1, 'theory_gap': ['maslow']},
        }

    def test_targeting_reports_only_axes_actually_tested_or_selected(self):
        from stp_runner.targeting import run_targeting

        frame = pd.DataFrame({'cluster': ['a'] * 4 + ['b'] * 4,
                              'bag_salience': [1, 2, 3, 2, 4, 5, 6, 5],
                              'bag_quality': [float('nan')] * 8})
        summary = run_targeting(frame, {'segment_profiles': []}, ['bag_salience', 'bag_quality'],
                                role_columns={'current_target': ['bag_salience', 'bag_quality'],
                                              'potential_target': [],
                                              'comparison_axis': ['bag_salience', 'bag_quality']})
        self.assertEqual(summary['target_selection_decision']['comparison_axes_used'], ['bag_salience'])
        self.foundation['dimension_catalog'][0]['stat_roles'] += ['current_target', 'comparison_axis']
        report = reporting.build_stage_report_contract('targeting', summary, self.foundation, None)
        self.assertEqual(report['axis_modeling_summary']['quality_columns_used'], [])
        self.assertEqual(report['axis_modeling_summary']['salience_columns_used'], ['bag_salience'])
        self.assertEqual(report['axis_modeling_summary']['axes_mode'], 'salience')
        self.assertNotIn('and quality', report['axis_modeling_summary']['modeling_rule'])

    def test_stage_omits_unsupported_finding_and_records_reason(self):
        frame = pd.DataFrame([{'review_id': 'r1', 'unit_id': 'u1', 'review_text': 'A bag is included.',
                               'bag_salience': 4, 'bag_quality': None}])
        summary = {
            'modeled_feature_columns': ['bag_salience'],
            'excluded_missing_features': ['bag_quality'],
            'segment_variable_table': {'scored': ['bag_quality', 'bag_salience']},
            'cluster_share_table': [{'cluster': 'a', 'share': 1.0, 'sample_size': 1}],
            'segment_profiles': [{'cluster': 'a', 'numeric_summary': {'bag_salience': 4}}],
        }
        result = reporting.build_stage_report_contract('segmentation', summary, self.foundation,
                                                       frame, unit_cluster_map={'u1': 'a'})
        self.assertTrue(result['findings'])
        self.assertTrue(all(finding['evidence_quotes'] for finding in result['findings']))
        self.assertFalse(any(finding['finding_id'] == 'segmentation-psychology-overlay'
                             for finding in result['findings']))
        self.assertTrue(result['omitted_findings'][0]['reason'])
        for finding in result['findings']:
            self.assertNotIn('bag_quality', finding['reproducibility']['input_columns'])
        self.assertIn('Omitted findings', '\n'.join(reporting._render_report_section('Segmentation', result)))

    def test_extension_coverage_and_description_are_retained(self):
        coverage = reporting._theory_coverage_summary(self.foundation, ['bag_salience'])
        extension = next(row for row in coverage if row['theory_family'] == 'Service Value')
        self.assertEqual(extension['covered_subtheories'], ['Service Value > Convenience'])
        self.assertEqual(extension['not_evidenced_subtheories'], ['Service Value > Accessibility'])
        self.assertEqual(reporting._theories_for_columns(self.foundation, ['bag_salience']), [{
            'name': 'Service Value', 'description': 'Explains evidence about convenience.'}])
        self.assertTrue(any(row['theory_family'] == 'System 1 / System 2' for row in coverage))

    def test_extraction_gap_survives_report_contract_and_markdown(self):
        result = reporting.build_attribute_extraction_summary_contract(self.foundation, [])
        self.assertEqual(result['theory_gap'], ['maslow'])
        self.assertIn('theory_gap: maslow', '\n'.join(reporting._render_attribute_extraction_summary(result)))

    def test_missing_quality_does_not_create_zero_score(self):
        scores, _, _ = reporting._positioning_score_lookup({'positioning_scorecard': [
            {'brand': 'A', 'feature': 'bag_quality', 'score': None, 'point_type': 'brand'},
            {'brand': 'B', 'feature': 'bag_quality', 'score': 0, 'point_type': 'brand'},
        ]})
        self.assertNotIn('A', scores)
        self.assertEqual(scores['B']['bag_quality'], 0)

    def test_report_axes_only_include_modeled_features(self):
        for stage in ['segmentation', 'positioning']:
            summary = {'excluded_missing_features': ['bag_quality'],
                       'modeled_feature_columns': ['bag_salience'],
                       'positioning_scorecard': [
                           {'point_type': 'brand', 'feature': 'bag_salience'},
                           {'point_type': 'brand', 'feature': 'bag_quality'}]}
            columns = reporting._columns_for_stage(self.foundation, stage, summary)
            self.assertEqual(columns, ['bag_salience'])
            modeling = reporting._axis_modeling_summary(self.foundation, stage, columns, None)
            self.assertNotIn('and quality', modeling['modeling_rule'])

    def test_absent_salience_is_not_quoted_but_zero_quality_is(self):
        frame = pd.DataFrame([{'review_id': 'r1', 'review_text': 'The bag broke.',
                               'bag_salience': 0, 'bag_quality': None}])
        catalog = reporting._catalog_lookup(self.foundation)
        self.assertEqual(reporting._quote_candidates(frame, ['bag_salience'], catalog, self.foundation), [])
        frame.loc[0, ['bag_salience', 'bag_quality']] = [1, 0]
        quotes = reporting._quote_candidates(frame, ['bag_quality'], catalog, self.foundation)
        self.assertEqual(quotes[0]['review_id'], 'r1')

    def test_quote_cannot_claim_missing_quality_as_evidence(self):
        frame = pd.DataFrame([{'review_id': 'r1', 'review_text': 'A bag is included.',
                               'bag_quality': None}])
        self.assertEqual(reporting._quote_candidates(frame, ['bag_quality'],
                         reporting._catalog_lookup(self.foundation), self.foundation), [])


if __name__ == '__main__':
    unittest.main()

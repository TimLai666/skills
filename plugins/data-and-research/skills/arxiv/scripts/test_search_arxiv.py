import contextlib
import io
import unittest
import urllib.error
from unittest.mock import patch, MagicMock

import search_arxiv as arxiv


def feed(entry):
    return ('<feed xmlns="http://www.w3.org/2005/Atom">' + entry + '</feed>').encode()


class SearchTests(unittest.TestCase):
    def request(self, body, **kwargs):
        response = MagicMock()
        response.__enter__.return_value.read.return_value = body
        output = io.StringIO()
        with patch.object(arxiv.urllib.request, 'urlopen', return_value=response), contextlib.redirect_stdout(output):
            arxiv.search(**kwargs)
        return output.getvalue()

    def test_full_abstract_and_versioned_legacy_links(self):
        abstract = 'Complete abstract. ' * 50
        output = self.request(feed('<entry><id>http://arxiv.org/abs/solv-int/9701001v2</id><title>Title</title><summary>' + abstract + '</summary></entry>'), ids='solv-int/9701001v2')
        self.assertIn(abstract.strip(), output)
        self.assertIn('https://arxiv.org/abs/solv-int/9701001v2', output)
        self.assertIn('https://arxiv.org/pdf/solv-int/9701001v2', output)

    def test_modern_versioned_links(self):
        output = self.request(feed('<entry><id>http://arxiv.org/abs/2402.03300v3</id></entry>'), ids='2402.03300v3')
        self.assertIn('https://arxiv.org/pdf/2402.03300v3', output)

    def test_missing_metadata(self):
        output = self.request(feed('<entry><title/><author/><category/></entry>'), query='test')
        self.assertIn('Published: Unavailable | Updated: Unavailable', output)
        self.assertNotIn('https://arxiv.org/abs/Unavailable', output)

    def test_empty_feed(self):
        self.assertIn('No results found.', self.request(feed(''), query='test'))

    def test_bibtex_metadata_and_clean_output(self):
        output = self.request(feed('<entry><id>http://arxiv.org/abs/2402.03300v3</id><title>A &amp; B_2</title><published>2024-02-05</published><author><name>Alice Smith</name></author><author><name>Bob Jones</name></author></entry>'), ids='2402.03300v3', output_format='bibtex')
        self.assertTrue(output.startswith('@misc{arxiv_2402_03300v3,'))
        self.assertIn('Alice Smith and Bob Jones', output)
        self.assertIn('A \\& B\\_2', output)
        self.assertIn('year = {2024}', output)
        self.assertIn('eprint = {2402.03300v3}', output)
        self.assertNotIn('Found ', output)

    def test_bibtex_legacy_and_missing_fields(self):
        output = self.request(feed('<entry><id>http://arxiv.org/abs/solv-int/9701001v2</id></entry>'), ids='solv-int/9701001v2', output_format='bibtex')
        self.assertIn('@misc{arxiv_solv_int_9701001v2,', output)
        self.assertNotIn('Unavailable', output)
        self.assertNotIn('year =', output)

    def test_bibtex_missing_id_fails(self):
        with self.assertRaises(arxiv.ArxivError):
            self.request(feed('<entry><title>Missing ID</title></entry>'), query='test', output_format='bibtex')

    def test_bibtex_empty_output(self):
        self.assertEqual(self.request(feed(''), query='test', output_format='bibtex'), '')

    def test_api_error_entry(self):
        with self.assertRaisesRegex(arxiv.ArxivError, 'bad query'):
            self.request(feed('<entry><id>http://arxiv.org/api/errors#incorrect_id_format_for_2400</id><title>Error</title><summary>bad query</summary></entry>'), query='test')

    def test_transport_and_xml_errors(self):
        for error in [urllib.error.URLError('offline'), TimeoutError('timeout')]:
            with self.subTest(error=error), patch.object(arxiv.urllib.request, 'urlopen', side_effect=error), self.assertRaises(arxiv.ArxivError):
                arxiv.search(query='test')
        with self.assertRaises(arxiv.ArxivError):
            self.request(b'broken xml', query='test')


class CliTests(unittest.TestCase):
    def test_help_and_no_arguments(self):
        for argv in [[], ['--help']]:
            output = io.StringIO()
            with contextlib.redirect_stdout(output):
                try:
                    result = arxiv.main(argv)
                except SystemExit as exc:
                    result = exc.code
            self.assertEqual(result, 0)
            for term in ['--max', '--sort', '--author', '--category', '--id', 'relevance', 'updated', 'default: 5', '2402.03300,2401.12345', '2000', '3 seconds', 'Exit codes']:
                self.assertIn(term, output.getvalue())

    def test_invalid_arguments_do_not_request(self):
        for argv in [['--max'], ['test', '--max', '0'], ['test', '--max', '2001'], ['test', '--max', 'abc'], ['test', '--sort', 'bad'], ['--unknown'], ['--sort', 'date'], ['--author', ' ']]:
            with self.subTest(argv=argv), patch.object(arxiv, 'search') as search, contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit) as exc:
                arxiv.main(argv)
            self.assertEqual(exc.exception.code, 2)
            search.assert_not_called()

    def test_existing_calls(self):
        with patch.object(arxiv, 'search') as search:
            self.assertEqual(arxiv.main(['GRPO', 'reinforcement learning', '--max', '10', '--sort', 'date']), 0)
            search.assert_called_once_with(query='GRPO reinforcement learning', author=None, category=None, ids=None, max_results=10, sort='date')

    def test_bibtex_cli(self):
        with patch.object(arxiv, 'search') as search:
            self.assertEqual(arxiv.main(['--id', '2402.03300v1', '--format', 'bibtex']), 0)
            self.assertEqual(search.call_args.kwargs['output_format'], 'bibtex')

    def test_error_has_no_traceback(self):
        output = io.StringIO()
        with patch.object(arxiv, 'search', side_effect=arxiv.ArxivError('offline')), contextlib.redirect_stderr(output):
            self.assertEqual(arxiv.main(['test']), 1)
        self.assertEqual(output.getvalue(), 'Error: offline\n')


if __name__ == '__main__':
    unittest.main()

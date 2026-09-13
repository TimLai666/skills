#!/usr/bin/env python3
"""Search arXiv and display results in a clean format.

Usage:
    python search_arxiv.py "GRPO reinforcement learning"
    python search_arxiv.py "GRPO reinforcement learning" --max 10
    python search_arxiv.py "GRPO reinforcement learning" --sort date
    python search_arxiv.py --author "Yann LeCun" --max 5
    python search_arxiv.py --category cs.AI --sort date
    python search_arxiv.py --id 2402.03300
    python search_arxiv.py --id 2402.03300,2401.12345
    python search_arxiv.py --id 2402.03300v1 --format bibtex > papers.bib
"""
import argparse
import http.client
import re
import sys
import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET

NS = {'a': 'http://www.w3.org/2005/Atom'}
SORT_MAP = {"relevance": "relevance", "date": "submittedDate", "updated": "lastUpdatedDate"}


class ArxivError(Exception):
    """An actionable request or response error."""


def _text(element, path, default="Unavailable"):
    value = element.findtext(path, default='', namespaces=NS)
    return ' '.join(value.split()) or default


def _bibtex(entry):
    full_id = _text(entry, 'a:id', '').split('/abs/', 1)[-1]
    if not re.fullmatch(r'(?:\d{4}\.\d{4,5}|[a-zA-Z-]+(?:\.[A-Z]{2})?/\d{7})(?:v\d+)?', full_id):
        raise ArxivError('cannot generate BibTeX without a valid arXiv ID')
    escapes = {'\\': r'\textbackslash{}', '{': r'\{', '}': r'\}', '&': r'\&',
               '%': r'\%', '$': r'\$', '#': r'\#', '_': r'\_', '~': r'\textasciitilde{}', '^': r'\textasciicircum{}'}
    def escape(value):
        return ''.join(escapes.get(char, char) for char in value)
    fields = {'title': _text(entry, 'a:title', ''),
              'author': ' and '.join(_text(a, 'a:name', '') for a in entry.findall('a:author', NS) if _text(a, 'a:name', '')),
              'year': _text(entry, 'a:published', '')[:4],
              'eprint': full_id, 'archivePrefix': 'arXiv'}
    if not re.fullmatch(r'\d{4}', fields['year']):
        fields['year'] = ''
    category = entry.find('{http://arxiv.org/schemas/atom}primary_category')
    fields['primaryClass'] = category.get('term', '') if category is not None else ''
    fields['url'] = 'https://arxiv.org/abs/' + full_id
    key = 'arxiv_' + re.sub(r'[^A-Za-z0-9]', '_', full_id)
    lines = [f'@misc{{{key},']
    lines.extend(f'  {name} = {{{escape(value)}}},' for name, value in fields.items() if value)
    return '\n'.join(lines + ['}'])


def search(query=None, author=None, category=None, ids=None, max_results=5, sort="relevance", output_format="text"):
    if output_format not in {'text', 'bibtex'}:
        raise ArxivError('--format must be text or bibtex')
    if not isinstance(max_results, int) or isinstance(max_results, bool) or not 1 <= max_results <= 2000:
        raise ArxivError("--max must be an integer from 1 to 2000")
    if sort not in SORT_MAP:
        raise ArxivError("--sort must be relevance, date, or updated")
    params = {}
    if ids and ids.strip():
        params['id_list'] = ids.strip()
    else:
        parts = [f'{field}:{value.strip()}' for field, value in
                 [('all', query), ('au', author), ('cat', category)] if value and value.strip()]
        if not parts:
            raise ArxivError("provide a query, --author, --category, or --id")
        params['search_query'] = ' AND '.join(parts)
    params.update(max_results=str(max_results), sortBy=SORT_MAP[sort], sortOrder='descending')
    url = "https://export.arxiv.org/api/query?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={'User-Agent': 'arxiv-skill/1.0'})
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = resp.read()
    except (OSError, http.client.HTTPException) as exc:
        raise ArxivError(f"arXiv request failed: {exc}") from exc
    try:
        root = ET.fromstring(data)
    except ET.ParseError as exc:
        raise ArxivError("arXiv returned invalid XML") from exc
    if root.tag != '{http://www.w3.org/2005/Atom}feed':
        raise ArxivError("arXiv returned an unexpected response (expected an Atom feed)")
    entries = root.findall('a:entry', NS)
    for entry in entries:
        raw_id = _text(entry, 'a:id', '')
        if '/api/errors' in raw_id or _text(entry, 'a:title', '').lower() == 'error':
            raise ArxivError(_text(entry, 'a:summary', 'arXiv API error'))
    if output_format == 'bibtex':
        records = [_bibtex(entry) for entry in entries]
        if records:
            print('\n\n'.join(records))
        return
    if not entries:
        print("No results found.")
        return
    total = root.find('{http://a9.com/-/spec/opensearch/1.1/}totalResults')
    if total is not None and total.text:
        print(f"Found {total.text.strip()} results (showing {len(entries)})\n")
    for i, entry in enumerate(entries, 1):
        title = _text(entry, 'a:title')
        raw_id = _text(entry, 'a:id', '')
        full_id = raw_id.split('/abs/', 1)[-1] if '/abs/' in raw_id else raw_id
        published = _text(entry, 'a:published', '')[:10] or 'Unavailable'
        updated = _text(entry, 'a:updated', '')[:10] or 'Unavailable'
        authors = ', '.join(_text(author, 'a:name') for author in entry.findall('a:author', NS)) or 'Unavailable'
        summary = _text(entry, 'a:summary')
        cats = ', '.join(c.get('term') for c in entry.findall('a:category', NS) if c.get('term')) or 'Unavailable'
        print(f"{i}. {title}")
        print(f"   ID: {full_id or 'Unavailable'} | Published: {published} | Updated: {updated}")
        print(f"   Authors: {authors}")
        print(f"   Categories: {cats}")
        print(f"   Abstract: {summary}")
        if full_id:
            print(f"   Links: https://arxiv.org/abs/{full_id} | https://arxiv.org/pdf/{full_id}")
        else:
            print("   Links: Unavailable")
        print()


def _positive_int(value):
    try:
        number = int(value)
    except ValueError:
        raise argparse.ArgumentTypeError("must be an integer from 1 to 2000") from None
    if not 1 <= number <= 2000:
        raise argparse.ArgumentTypeError("must be an integer from 1 to 2000")
    return number


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Search arXiv by keywords, author, category, or IDs; display metadata, full abstracts, and version-specific links.",
        epilog=__doc__ + "\nLimits: one request returns at most 2000 results; no pagination.\nCallers must leave at least 3 seconds between consecutive API calls.\nExit codes: 0 success (including help or no results), 1 request/response error,\n2 invalid arguments.\n", formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('query', nargs='*', help="keywords to search (combine with author and category using AND)")
    parser.add_argument('--author', help="author name")
    parser.add_argument('--category', help="arXiv category, e.g. cs.AI")
    parser.add_argument('--id', dest='ids', help="comma-separated arXiv IDs, optionally versioned; takes precedence over query/author/category")
    parser.add_argument('--max', dest='max_results', type=_positive_int, default=5, help="maximum results, integer 1-2000 (default: 5)")
    parser.add_argument('--sort', choices=SORT_MAP, default='relevance', help="descending relevance, submission date, or update date (default: relevance)")
    parser.add_argument('--format', choices=['text', 'bibtex'], default='text', help="output format (default: text); bibtex writes only entries to stdout for redirection to .bib, preserves versions, omits unavailable fields, and emits nothing for no results")
    argv = sys.argv[1:] if argv is None else argv
    if not argv:
        parser.print_help()
        return 0
    args = parser.parse_intermixed_args(argv)
    query = ' '.join(args.query).strip() or None
    if not any(value and value.strip() for value in (query, args.author, args.category, args.ids)):
        parser.error("provide a query, --author, --category, or --id")
    try:
        options = {'output_format': args.format} if args.format != 'text' else {}
        search(query=query, author=args.author, category=args.category, ids=args.ids,
               max_results=args.max_results, sort=args.sort, **options)
    except ArxivError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())

"""Lossless review loading and strict salience-score input checks."""

import csv
from numbers import Integral


def _read_csv(filepath):
    try:
        with open(filepath, encoding='utf-8-sig', newline='') as stream:
            reader = csv.DictReader(stream, strict=True)
            headers = reader.fieldnames
            if not headers or any(not name for name in headers) or len(set(headers)) != len(headers):
                raise ValueError('CSV must have nonempty, unique headers')
            rows = []
            for row in reader:
                if None in row or any(value is None for value in row.values()):
                    raise ValueError(f'CSV row ending at line {reader.line_num} has the wrong number of fields')
                rows.append(row)
            return headers, rows
    except (csv.Error, UnicodeError) as exc:
        raise ValueError(f'Invalid UTF-8 CSV: {exc}') from exc


def load_reviews(filepath):
    """Return every nonblank review in input order, preserving its original text."""
    headers, rows = _read_csv(filepath)
    column = next((name for name in ['body', 'Body', 'review', 'text', 'content'] if name in headers), None)
    if column is None:
        raise ValueError(f'No text column found. Headers: {headers}')
    return [row[column] for row in rows if row[column].strip()]


def validate_scores(scores, all_reviews, attrs):
    """Validate exact product/row/catalog alignment; never coerce scores."""
    if not isinstance(scores, dict) or set(scores) != set(all_reviews):
        raise ValueError('Score products must exactly match review products')
    for pid, reviews in all_reviews.items():
        matrix = scores[pid]
        if not isinstance(matrix, (list, tuple)) or len(matrix) != len(reviews):
            raise ValueError(f'{pid}: expected {len(reviews)} score rows')
        for i, row in enumerate(matrix):
            if not isinstance(row, (list, tuple)) or len(row) != len(attrs):
                raise ValueError(f'{pid}[{i}]: expected {len(attrs)} scores')
            for value in row:
                if isinstance(value, bool) or not isinstance(value, Integral) or not 0 <= value <= 7:
                    raise ValueError(f'{pid}[{i}]: {value!r} must be an integer from 0 to 7')


def normalize_batch_scores(data, reviews, attrs):
    """Accept a matrix or {scores: matrix}; service must preserve request order."""
    matrix = data.get('scores') if isinstance(data, dict) else data
    validate_scores({'batch': matrix}, {'batch': reviews}, attrs)
    return matrix


def load_scored_csv(filepath, all_reviews, attrs):
    """Import by exported product_0001 IDs, rejecting partial or duplicate results."""
    headers, rows = _read_csv(filepath)
    columns = [f's{attr[0]}' for attr in attrs]
    if not {'review_id', *columns}.issubset(headers):
        raise ValueError('CSV requires review_id and every catalog score column')
    expected = {f'{pid}_{i+1:04d}': (pid, i)
                for pid, reviews in all_reviews.items() for i in range(len(reviews))}
    if len(expected) != sum(len(reviews) for reviews in all_reviews.values()):
        raise ValueError('Product IDs produce duplicate review IDs')
    result = {pid: [None] * len(reviews) for pid, reviews in all_reviews.items()}
    seen = set()
    for row in rows:
        review_id = row['review_id']
        if review_id not in expected or review_id in seen:
            raise ValueError(f'Unknown or duplicate review_id: {review_id!r}')
        values = [row[column].strip() for column in columns]
        if any(value not in '01234567' or len(value) != 1 for value in values):
            raise ValueError(f'{review_id}: scores must be integer text from 0 to 7')
        pid, index = expected[review_id]
        result[pid][index] = [int(value) for value in values]
        seen.add(review_id)
    if seen != set(expected):
        raise ValueError(f'Missing scores for {len(set(expected) - seen)} reviews')
    validate_scores(result, all_reviews, attrs)
    return result

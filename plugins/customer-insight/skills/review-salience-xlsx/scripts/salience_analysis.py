"""Standardised PCA and size-constrained K-means for scored review rows."""
import math
from numbers import Integral

import numpy as np
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import StandardScaler


def _matrix(values):
    matrix = np.asarray(values, dtype=float)
    if matrix.ndim != 2 or not len(matrix) or not np.isfinite(matrix).all():
        raise ValueError('Expected a nonempty finite two-dimensional matrix')
    return matrix


def fit_salience_pca(X):
    """Return (scores, serializable PCA metadata), without running clustering."""
    X = _matrix(X)
    if not X.shape[1]:
        raise ValueError('PCA requires at least one attribute')
    varying = np.var(X, axis=0) > 0
    result = {'n_reviews': len(X), 'n_components': 0, 'loadings': [[] for _ in X.T],
              'excluded_constant_columns': np.flatnonzero(~varying).tolist(),
              'eigenvalues': [], 'explained_variance_ratio': [], 'cumulative_variance': [],
              'status': 'unavailable', 'reason': 'No between-review variation'}
    if len(X) < 2 or not varying.any():
        return np.empty((len(X), 0)), result
    standard = StandardScaler().fit_transform(X[:, varying])
    pca = PCA(n_components=min(standard.shape), svd_solver='full').fit(standard)
    n = int(np.sum(pca.explained_variance_ > 1))
    selection = 'kaiser_eigenvalue_gt_1'
    if not n:
        n = 1
        selection = 'first_positive_component_fallback'
    scores = pca.transform(standard)[:, :n]
    variance = pca.explained_variance_[:n]
    ratio = pca.explained_variance_ratio_[:n]
    loadings = np.zeros((X.shape[1], n))
    loadings[varying] = pca.components_[:n].T * np.sqrt(variance)
    result.update(n_components=n, status='available', reason=None, selection=selection,
                  loadings=loadings.tolist(),
                  eigenvalues=variance.tolist(), explained_variance_ratio=ratio.tolist(),
                  cumulative_variance=np.cumsum(ratio).tolist())
    return scores, result


def _silhouette(X, labels):
    return float(silhouette_score(X, labels)) if 1 < len(set(labels)) < len(X) else None


def iterative_prune(PC, k_start, min_n, seed=42):
    """Return final fitted model, fitting-row mask, and pruning history.

    Rejected clusters never survive via an old model returned at a forced stop.
    The threshold uses the original corpus, including reassigned reviews.
    """
    PC = _matrix(PC)
    if not PC.shape[1]:
        raise ValueError('No components available for K-means')
    if isinstance(k_start, bool) or int(k_start) != k_start or k_start < 1:
        raise ValueError('k_start must be a positive integer')
    if isinstance(min_n, bool) or int(min_n) != min_n or not 1 <= min_n <= len(PC):
        raise ValueError('min_n must be an integer between 1 and the corpus size')
    active = np.ones(len(PC), dtype=bool)
    history = []
    k = int(k_start)
    while True:
        subset = PC[active]
        k = min(k, len(subset), len(np.unique(subset, axis=0)))
        model = KMeans(n_clusters=k, random_state=seed, n_init=20).fit(subset)
        labels = model.labels_
        unique, counts = np.unique(labels, return_counts=True)
        sizes = {int(c): int(n) for c, n in zip(unique, counts)}
        small = [c for c, n in sizes.items() if n < min_n] if k > 1 else []
        history.append({'k': k, 'n_active': int(active.sum()), 'cluster_sizes': sizes,
                        'silhouette': _silhouette(subset, labels), 'pruned_clusters': small,
                        'pruned_n': sum(sizes[c] for c in small)})
        if not small:
            return model, active, history
        active[np.flatnonzero(active)[np.isin(labels, small)]] = False
        k = max(1, k - len(small))
        if not active.any():
            active[:] = True
            k = 1


def cluster_pc_scores(PC, k_start=5, min_pct=0.05, seed=42):
    """Cluster aligned PC rows only; zero-component rows remain unsegmented."""
    PC = _matrix(PC)
    if not 0 < min_pct <= 1:
        raise ValueError('min_pct must be in (0, 1]')
    min_n = math.ceil(len(PC) * min_pct)
    if PC.shape[1]:
        model, active, history = iterative_prune(PC, k_start, min_n, seed)
        labels = model.predict(PC)
    else:
        active, history, labels = np.ones(len(PC), dtype=bool), [], np.zeros(len(PC), dtype=int)
    unique, counts = np.unique(labels, return_counts=True)
    if np.any(counts < min_n):
        raise RuntimeError('Final assignment failed minimum group size')
    segmented = len(unique) >= 2
    return {'n_total': len(PC), 'min_pct': min_pct, 'min_n': min_n,
            'method': 'iterative pruning, final centroids, all-row assignment',
            'status': 'segmented' if segmented else 'unsegmented',
            'reason': None if segmented else 'No multiple groups satisfying data variation and minimum size',
            'history': history, 'final_k': len(unique), 'final_silhouette': _silhouette(PC, labels),
            'cluster_sizes': {int(c): int(n) for c, n in zip(unique, counts)},
            'final_labels': labels.tolist(), 'active_mask': active.tolist(),
            'pc_centroids': [PC[labels == c].mean(axis=0).tolist() for c in unique]}


def analyze_salience(rows, attr_ids, attr_labels, k_start=5, min_pct=0.05, seed=42):
    """Run both requested stages and retain input order and review IDs."""
    if not rows or not attr_ids or len(attr_ids) != len(attr_labels) or len(set(attr_ids)) != len(attr_ids):
        raise ValueError('Provide rows and unique attributes with matching labels')
    ids = [row['review_id'] for row in rows]
    if any(v is None or str(v).strip() == '' for v in ids) or len(set(ids)) != len(ids):
        raise ValueError('review_id must be nonempty and unique')
    values = [[row[f's{a}'] for a in attr_ids] for row in rows]
    for row in values:
        for value in row:
            if isinstance(value, (bool, np.bool_)) or not isinstance(value, Integral) or not 0 <= value <= 7:
                raise ValueError('Salience scores must be integers from 0 to 7')
    X = np.asarray(values, dtype=float)
    scores, pca = fit_salience_pca(X)
    pca.update(attr_ids=list(attr_ids), attr_labels=list(attr_labels))
    pcs = [dict(review_id=row['review_id'], product=row['product'],
                **{f'PC{j+1:02d}': float(value) for j, value in enumerate(score)})
           for row, score in zip(rows, scores)]
    groups = cluster_pc_scores(scores, k_start, min_pct, seed)
    labels = np.asarray(groups['final_labels'])
    groups.update(review_ids=ids, products=[row['product'] for row in rows], attr_labels=list(attr_labels),
                  attr_centroids=[X[labels == c].mean(axis=0).tolist() for c in sorted(set(labels))])
    return pca, pcs, groups

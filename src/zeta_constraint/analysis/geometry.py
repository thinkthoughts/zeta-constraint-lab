from __future__ import annotations

import numpy as np


def condition_number(X) -> float:
    X = np.asarray(X, dtype=float)
    Xc = X - X.mean(axis=0, keepdims=True)
    _, s, _ = np.linalg.svd(Xc, full_matrices=False)
    s = s[s > 1e-12]
    if len(s) == 0:
        return float("inf")
    return float(s.max() / s.min())


def effective_rank(X) -> float:
    X = np.asarray(X, dtype=float)
    Xc = X - X.mean(axis=0, keepdims=True)
    _, s, _ = np.linalg.svd(Xc, full_matrices=False)
    s = s[s > 1e-12]
    if len(s) == 0:
        return 0.0
    p = s / s.sum()
    return float(np.exp(-np.sum(p * np.log(p + 1e-12))))


def correlation_matrix(X):
    X = np.asarray(X, dtype=float)
    if X.shape[1] == 1:
        return np.ones((1, 1))
    return np.nan_to_num(np.corrcoef(X.T), nan=0.0)

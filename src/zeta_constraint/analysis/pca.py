from __future__ import annotations

import numpy as np


def pca_variance(X):
    X = np.asarray(X, dtype=float)
    Xc = X - X.mean(axis=0, keepdims=True)
    _, S, _ = np.linalg.svd(Xc, full_matrices=False)
    var = S**2 / max(len(X) - 1, 1)
    total = var.sum()
    if total <= 1e-12:
        return np.ones_like(var) / len(var)
    return var / total

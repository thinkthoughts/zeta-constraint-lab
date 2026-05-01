from __future__ import annotations

import math
import numpy as np
import pandas as pd
from sklearn.metrics import mean_squared_error

from zeta_constraint.basis.stats import basis_stats
from zeta_constraint.basis.registry import design_matrix


def fit_template(df: pd.DataFrame, basis_name: str, alpha: float = 1e-6, flow_mode: str | None = None):
    stats = basis_stats(df)
    X, names = design_matrix(df, basis_name, stats=stats, flow_mode=flow_mode)
    y = df["predicted_flow"].to_numpy(dtype=float)

    beta = np.linalg.solve(X.T @ X + alpha * np.eye(X.shape[1]), X.T @ y)
    pred = X @ beta

    row = {
        "n": len(df),
        "template_rmse": math.sqrt(mean_squared_error(y, pred)),
        "basis_terms": "|".join(names),
    }
    for name, coef in zip(names, beta):
        row[f"coef_{name}"] = float(coef)

    return beta, pred, row, stats, names


def predict_with_beta(
    df: pd.DataFrame,
    basis_name: str,
    beta,
    stats: dict | None = None,
    flow_mode: str | None = None,
    columns: list[str] | None = None,
):
    X, names = design_matrix(df, basis_name, stats=stats, flow_mode=flow_mode, columns=columns)
    return X @ np.asarray(beta, dtype=float)

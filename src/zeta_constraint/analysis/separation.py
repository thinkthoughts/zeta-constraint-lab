from __future__ import annotations

import pandas as pd


def regime_separation(coef_df: pd.DataFrame, coef_cols: list[str], group_col: str = "forcing_mode") -> float:
    numeric = coef_df[coef_cols].astype(float)
    total_var = float(numeric.var().sum())
    if total_var <= 1e-12:
        return 0.0

    group_means = coef_df.groupby(group_col)[coef_cols].mean(numeric_only=True)
    between_var = float(group_means.var().sum())
    return between_var / total_var

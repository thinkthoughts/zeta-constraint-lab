from __future__ import annotations

import numpy as np
import pandas as pd
from .stats import basis_stats


def compact_interaction_terms(df: pd.DataFrame, stats: dict | None = None) -> dict[str, np.ndarray]:
    r = df["residual"].to_numpy(dtype=float)
    c = df["condition_coord"].to_numpy(dtype=float)
    return {
        "1": np.ones_like(r),
        "c": c,
        "r": r,
        "r c": r * c,
        "c^3": c**3,
        "r^2": r**2,
    }


def nonlinear_interaction_terms(df: pd.DataFrame, stats: dict | None = None) -> dict[str, np.ndarray]:
    r = df["residual"].to_numpy(dtype=float)
    c = df["condition_coord"].to_numpy(dtype=float)
    if stats is None:
        stats = basis_stats(df)

    alpha = stats.get("alpha_c3_on_c", 0.0)
    beta = stats.get("mean_r2", 0.0)

    return {
        "1": np.ones_like(r),
        "c": c,
        "r": r,
        "r c": r * c,
        "c^3_perp_c": c**3 - alpha * c,
        "r^2_centered": r**2 - beta,
        "r c^2": r * c**2,
        "r^3": r**3,
    }


def block_conditioned_terms(df: pd.DataFrame, stats: dict | None = None, flow_mode: str | None = None) -> dict[str, np.ndarray]:
    if flow_mode is None and "flow_mode" in df.columns:
        values = df["flow_mode"].astype(str).unique()
        flow_mode = values[0] if len(values) else "unknown"

    if str(flow_mode) == "nonlinear":
        return nonlinear_interaction_terms(df, stats)
    return compact_interaction_terms(df, stats)

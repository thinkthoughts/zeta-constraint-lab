from __future__ import annotations

import numpy as np
import pandas as pd
from .stats import basis_stats


def structured_terms(df: pd.DataFrame, stats: dict | None = None) -> dict[str, np.ndarray]:
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
    }

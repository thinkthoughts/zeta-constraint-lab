from __future__ import annotations

import numpy as np
import pandas as pd


def raw_terms(df: pd.DataFrame, stats: dict | None = None) -> dict[str, np.ndarray]:
    r = df["residual"].to_numpy(dtype=float)
    c = df["condition_coord"].to_numpy(dtype=float)
    return {
        "1": np.ones_like(r),
        "c": c,
        "r": r,
        "c^3": c**3,
        "r^2": r**2,
        "r c^2": r * c**2,
    }

from __future__ import annotations

import numpy as np
import pandas as pd


def basis_stats(df: pd.DataFrame) -> dict[str, float]:
    r = df["residual"].to_numpy(dtype=float)
    c = df["condition_coord"].to_numpy(dtype=float)
    return {
        "alpha_c3_on_c": float(np.sum(c**4) / max(np.sum(c**2), 1e-12)),
        "mean_r2": float(np.mean(r**2)),
    }

from __future__ import annotations

import numpy as np
import pandas as pd


COUPLING_MATCHES = {
    "raw_6": ["coef_r c^2", "coef_r^2", "coef_c^3"],
    "structured_interaction": ["coef_r c", "coef_r c^2", "coef_c^3_perp_c", "coef_r^2_centered"],
    "block_conditioned": ["coef_r c", "coef_r c^2", "coef_c^3_perp_c", "coef_r^2_centered", "coef_r^3", "coef_c^3", "coef_r^2"],
}


def coupling_variance_drop(coef_df: pd.DataFrame, coef_cols: list[str], basis_name: str) -> dict:
    drop_terms = COUPLING_MATCHES.get(basis_name, [])
    present = [c for c in drop_terms if c in coef_cols]
    keep_cols = [c for c in coef_cols if c not in present]

    base_var = float(np.var(coef_df[coef_cols].to_numpy(dtype=float)))
    retained_var = float(np.var(coef_df[keep_cols].to_numpy(dtype=float))) if keep_cols else 0.0

    return {
        "base_variance": base_var,
        "retained_variance": retained_var,
        "variance_drop": base_var - retained_var,
        "dropped_terms_present": "|".join(present),
        "n_dropped_present": len(present),
    }

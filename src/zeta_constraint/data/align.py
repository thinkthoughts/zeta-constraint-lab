from __future__ import annotations

import numpy as np
import pandas as pd


def align_schema(df: pd.DataFrame) -> pd.DataFrame:
    alias_groups = {
        "condition_coord": ["condition_coord", "c", "condition", "cond", "condition_coordinate"],
        "residual": ["residual", "r", "resid"],
        "predicted_flow": ["predicted_flow", "flow", "g", "drdc", "delta_residual_per_condition"],
        "next_residual": ["next_residual", "r_next", "next_r"],
        "delta_condition": ["delta_condition", "dc", "delta_c"],
        "forcing_mode": ["forcing_mode", "forcing", "forcing_gap", "mode"],
    }
    rename = {}
    for canonical, aliases in alias_groups.items():
        for alias in aliases:
            if alias in df.columns and alias != canonical:
                rename[alias] = canonical
                break
    df = df.rename(columns=rename).copy()

    if "next_residual" not in df.columns and {"residual", "predicted_flow", "delta_condition"}.issubset(df.columns):
        df["next_residual"] = df["residual"] + df["predicted_flow"] * df["delta_condition"]

    if "delta_condition" not in df.columns and "condition_coord" in df.columns:
        df = df.sort_values(["condition_coord"]).copy()
        df["delta_condition"] = np.gradient(df["condition_coord"].to_numpy())

    defaults = {
        "system": "unknown_system",
        "task": "unknown_task",
        "forcing_mode": "unknown_forcing",
        "k": 5,
        "flow_mode": "unknown_flow",
        "sample_id": np.arange(len(df)),
        "path_id": 0,
        "window_id": np.arange(len(df)),
    }
    for key, value in defaults.items():
        if key not in df.columns:
            df[key] = value

    required = ["condition_coord", "residual", "predicted_flow"]
    missing = [c for c in required if c not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns after alignment: {missing}")

    return df

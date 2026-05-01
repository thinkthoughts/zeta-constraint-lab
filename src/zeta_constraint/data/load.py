from __future__ import annotations

import glob
import os
from pathlib import Path
import numpy as np
import pandas as pd


def autodetect_data_path(search_dirs=(".", "data", "outputs")) -> str | None:
    patterns = [
        "*residual*flow*.parquet", "*residual*flow*.csv",
        "*governing*flow*.parquet", "*governing*flow*.csv",
        "*.parquet", "*.csv", "*.pkl", "*.pickle",
    ]
    candidates: list[str] = []
    for directory in search_dirs:
        for pattern in patterns:
            candidates.extend(glob.glob(str(Path(directory) / pattern)))
    candidates = [c for c in candidates if os.path.isfile(c)]
    return candidates[0] if candidates else None


def load_dataframe(path: str | os.PathLike) -> pd.DataFrame:
    path = str(path)
    ext = os.path.splitext(path)[1].lower()
    if ext == ".parquet":
        return pd.read_parquet(path)
    if ext in [".pkl", ".pickle"]:
        return pd.read_pickle(path)
    return pd.read_csv(path)


def synthetic_dataset(seed: int = 42) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    systems = ["entropy", "unevenness"]
    tasks = ["zeta_vs_gue", "zeta_vs_poisson"]
    forcing_modes = ["capacity_gap", "feature_gap", "condition_gap"]
    ks = [3, 5, 7]
    flow_modes = ["linear", "nonlinear"]

    rows = []
    sample_id = 0
    for system in systems:
        for task in tasks:
            for forcing_mode in forcing_modes:
                for k in ks:
                    for flow_mode in flow_modes:
                        c_grid = np.linspace(-1.25, 1.05, 42)
                        sys_shift = 0.06 if system == "entropy" else -0.04
                        task_shift = 0.05 if task == "zeta_vs_gue" else -0.03
                        force_shift = {"capacity_gap": 0.00, "feature_gap": 0.03, "condition_gap": 0.08}[forcing_mode]
                        k_shift = {3: -0.05, 5: 0.02, 7: 0.06}[k]
                        flow_shift = 0.05 if flow_mode == "nonlinear" else -0.02
                        nl_gain = 1.0 if flow_mode == "nonlinear" else 0.55

                        for path_id in range(14):
                            r = -0.75 + 0.10 * path_id + 0.05 * np.sin(0.7 * path_id)
                            for window_id, c in enumerate(c_grid):
                                g = (
                                    0.58 * np.tanh(1.35 * c)
                                    + 0.42 * c
                                    - 0.78 * r
                                    + 0.20 * r**2
                                    + nl_gain * 0.07 * c**2
                                    + nl_gain * 0.10 * r * c
                                    - nl_gain * 0.025 * r**3
                                    + sys_shift + task_shift + force_shift + k_shift + flow_shift
                                )
                                if forcing_mode == "condition_gap":
                                    g += 0.06 * np.sin(2.3 * c)
                                if system == "entropy":
                                    g += 0.03 * np.cos(1.2 * c)
                                if task == "zeta_vs_poisson":
                                    g -= 0.015 * c
                                if flow_mode == "linear":
                                    g -= 0.09 * r**2
                                    g += 0.015 * c * r

                                dc = c_grid[min(window_id + 1, len(c_grid)-1)] - c if window_id < len(c_grid)-1 else c - c_grid[max(window_id-1, 0)]
                                noise = 0.012 * rng.standard_normal()
                                next_r = r + (g + noise) * dc

                                rows.append({
                                    "system": system,
                                    "task": task,
                                    "forcing_mode": forcing_mode,
                                    "k": k,
                                    "flow_mode": flow_mode,
                                    "condition_coord": c,
                                    "residual": r,
                                    "predicted_flow": g + noise,
                                    "next_residual": next_r,
                                    "delta_condition": dc,
                                    "sample_id": sample_id,
                                    "path_id": path_id,
                                    "window_id": window_id,
                                })
                                r = next_r
                                sample_id += 1
    return pd.DataFrame(rows)

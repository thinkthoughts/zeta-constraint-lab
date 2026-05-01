from __future__ import annotations

import math
import numpy as np
import pandas as pd
from sklearn.metrics import mean_squared_error

from zeta_constraint.model.fit import predict_with_beta


def rmse(y_true, y_pred) -> float:
    return math.sqrt(mean_squared_error(y_true, y_pred))


def trajectory_gap(
    df: pd.DataFrame,
    basis_name: str,
    beta_ref,
    beta_cmp,
    stats_ref: dict | None = None,
    stats_cmp: dict | None = None,
    flow_mode: str | None = None,
    columns: list[str] | None = None,
    n_r0: int = 15,
) -> float:
    cmin, cmax = df["condition_coord"].min(), df["condition_coord"].max()
    rmin, rmax = df["residual"].min(), df["residual"].max()
    cgrid = np.linspace(cmin, cmax, 40)
    r0s = np.linspace(np.quantile(df["residual"], 0.05), np.quantile(df["residual"], 0.95), n_r0)
    flow_cap = max(1.0, 2.5 * np.quantile(np.abs(df["predicted_flow"]), 0.995))

    def integrate(beta, stats, r0):
        r = float(np.clip(r0, rmin, rmax))
        traj = [r]
        for i in range(len(cgrid) - 1):
            c = cgrid[i]
            dc = float(cgrid[i + 1] - cgrid[i])
            row = pd.DataFrame({"residual": [r], "condition_coord": [c]})
            g = float(np.clip(
                predict_with_beta(row, basis_name, beta, stats=stats, flow_mode=flow_mode, columns=columns)[0],
                -flow_cap,
                flow_cap,
            ))
            r = float(np.clip(r + g * dc, rmin - 0.5, rmax + 0.5))
            traj.append(r)
        return np.array(traj)

    return float(np.mean([
        rmse(integrate(beta_ref, stats_ref, r0), integrate(beta_cmp, stats_cmp, r0))
        for r0 in r0s
    ]))

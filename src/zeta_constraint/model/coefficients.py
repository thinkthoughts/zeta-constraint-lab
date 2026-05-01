from __future__ import annotations

import pandas as pd

from .fit import fit_template


def build_coef_table(df: pd.DataFrame, basis_name: str, min_rows: int = 30):
    group_cols = ["system", "task", "forcing_mode", "k", "flow_mode"]
    rows, subsets, stats_map, names_map = [], {}, {}, {}

    for vals, sub in df.groupby(group_cols):
        if len(sub) < min_rows:
            continue

        flow_mode = vals[4]
        beta, pred, stats_row, stats, names = fit_template(sub.copy(), basis_name, flow_mode=flow_mode)
        kval = int(vals[3]) if float(vals[3]).is_integer() else vals[3]
        regime_id = f"{vals[0]}|{vals[1]}|{vals[2]}|k={kval}|{vals[4]}"

        row = {
            "regime_id": regime_id,
            "system": vals[0],
            "task": vals[1],
            "forcing_mode": vals[2],
            "k": float(vals[3]),
            "flow_mode": vals[4],
        }
        row.update(stats_row)

        rows.append(row)
        subsets[regime_id] = sub.copy()
        stats_map[regime_id] = stats
        names_map[regime_id] = names

    coef_df = pd.DataFrame(rows).reset_index(drop=True)
    coef_cols = [c for c in coef_df.columns if c.startswith("coef_")]

    if coef_cols:
        coef_df[coef_cols] = coef_df[coef_cols].fillna(0.0)

    return coef_df, coef_cols, subsets, stats_map, names_map

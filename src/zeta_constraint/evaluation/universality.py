from __future__ import annotations

import numpy as np
import pandas as pd


def universality_scores(eval_df: pd.DataFrame, group_col: str = "basis", metric: str = "traj_rmse", tolerance: float = 0.05):
    block_summary = eval_df.groupby(["block", group_col])[metric].mean().reset_index()
    rows = []

    for block, sub in block_summary.groupby("block"):
        best = sub[metric].min()
        for _, row in sub.iterrows():
            rows.append({
                "block": block,
                group_col: row[group_col],
                "metric": metric,
                "value": row[metric],
                "best": best,
                "within_tolerance": bool(row[metric] <= (1 + tolerance) * best),
                "is_best": bool(np.isclose(row[metric], best) or row[metric] == best),
            })

    by_block = pd.DataFrame(rows)
    score = by_block.groupby(group_col).agg(
        universality_score=("within_tolerance", "mean"),
        win_rate=("is_best", "mean"),
        mean_metric=("value", "mean"),
        n_blocks=("block", "nunique"),
    ).reset_index().sort_values(["universality_score", "win_rate", "mean_metric"], ascending=[False, False, True])

    return score, by_block

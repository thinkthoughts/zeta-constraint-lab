from __future__ import annotations

import pandas as pd


def coefficient_table(term_names: list[str], beta) -> pd.DataFrame:
    return pd.DataFrame({"term": term_names, "coefficient": beta})


def model_summary_table(rows: list[dict]) -> pd.DataFrame:
    return pd.DataFrame(rows)

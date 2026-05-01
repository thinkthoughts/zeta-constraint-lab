from __future__ import annotations

import pandas as pd


def equation_markdown(coef_table: pd.DataFrame, coef_col: str = "coefficient", term_col: str = "term", precision: int = 4) -> str:
    pieces = [f"{row[coef_col]:.{precision}f}*{row[term_col]}" for _, row in coef_table.iterrows()]
    return "g(c,r) = " + " + ".join(pieces)


def equation_latex(coef_table: pd.DataFrame, coef_col: str = "coefficient", term_col: str = "term", precision: int = 3) -> str:
    pieces = [f"{row[coef_col]:.{precision}f}\\,{row[term_col]}" for _, row in coef_table.iterrows()]
    return "g(c,r)=" + " + ".join(pieces)

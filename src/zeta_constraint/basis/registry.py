from __future__ import annotations

import numpy as np
import pandas as pd

from .stats import basis_stats
from .raw import raw_terms
from .structured import structured_terms
from .block_conditioned import block_conditioned_terms

BASIS_REGISTRY = {
    "raw_6": raw_terms,
    "structured_interaction": structured_terms,
    "block_conditioned": block_conditioned_terms,
}

PRIMARY_BASIS = "structured_interaction"


def get_basis_terms(df: pd.DataFrame, basis_name: str, stats: dict | None = None, flow_mode: str | None = None) -> dict[str, np.ndarray]:
    if basis_name not in BASIS_REGISTRY:
        raise ValueError(f"Unknown basis: {basis_name}")
    fn = BASIS_REGISTRY[basis_name]
    if basis_name == "block_conditioned":
        return fn(df, stats=stats, flow_mode=flow_mode)
    return fn(df, stats=stats)


def design_matrix(
    df: pd.DataFrame,
    basis_name: str,
    stats: dict | None = None,
    flow_mode: str | None = None,
    columns: list[str] | None = None,
) -> tuple[np.ndarray, list[str]]:
    if stats is None:
        stats = basis_stats(df)
    terms = get_basis_terms(df, basis_name, stats=stats, flow_mode=flow_mode)

    if columns is None:
        columns = list(terms.keys())

    X = np.column_stack([terms.get(col, np.zeros(len(df))) for col in columns])
    return X, columns

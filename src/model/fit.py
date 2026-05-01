def fit_template(df, basis_fn):
    stats = compute_stats(df)
    terms = basis_fn(df, stats)

    X = np.column_stack(list(terms.values()))
    y = df["predicted_flow"].values

    beta = np.linalg.solve(X.T @ X, X.T @ y)

    return beta, list(terms.keys())

def structured_terms(df, stats):
    r = df["residual"].values
    c = df["condition_coord"].values

    alpha = stats["alpha_c3_on_c"]
    beta = stats["mean_r2"]

    return {
        "1": np.ones_like(r),
        "c": c,
        "r": r,
        "rc": r * c,
        "c3_perp": c**3 - alpha * c,
        "r2_centered": r**2 - beta,
        "rc2": r * c**2,
    }

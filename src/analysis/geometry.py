def condition_number(X):
    _, s, _ = np.linalg.svd(X, full_matrices=False)
    return s.max() / s.min()

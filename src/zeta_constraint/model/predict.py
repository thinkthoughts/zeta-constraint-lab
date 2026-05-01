from __future__ import annotations

import numpy as np
import pandas as pd
from sklearn.linear_model import Ridge, LassoCV
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import KFold, LeaveOneOut


def build_metadata_features(df_in: pd.DataFrame, columns: list[str] | None = None) -> pd.DataFrame:
    X = pd.get_dummies(df_in[["forcing_mode", "flow_mode", "system", "task"]], drop_first=False)
    X["k"] = df_in["k"].astype(float).values
    X["k2"] = df_in["k"].astype(float).values ** 2

    ff = df_in["forcing_mode"].astype(str) + "__x__" + df_in["flow_mode"].astype(str)
    sf = df_in["system"].astype(str) + "__x__" + df_in["forcing_mode"].astype(str)

    X = pd.concat([
        X,
        pd.get_dummies(ff, prefix="ff"),
        pd.get_dummies(sf, prefix="sf"),
        pd.get_dummies(df_in["forcing_mode"].astype(str), prefix="fk").multiply(
            df_in["k"].astype(float).to_numpy().reshape(-1, 1)
        ),
    ], axis=1)

    if columns is not None:
        X = X.reindex(columns=columns, fill_value=0.0)

    return X.astype(float)


def build_symbolic_features(df_in: pd.DataFrame, columns: list[str] | None = None, reduced_terms: list[str] | None = None):
    X = build_metadata_features(df_in, columns=columns)
    if reduced_terms is not None:
        X = X.reindex(columns=reduced_terms, fill_value=0.0)
    return X.astype(float)


def term_stability_table(coef_df: pd.DataFrame, coef_cols: list[str], n_splits: int = 8, threshold: float = 1e-4):
    n = len(coef_df)
    splitter = LeaveOneOut() if n <= 12 else KFold(n_splits=min(n_splits, n), shuffle=True, random_state=42)
    all_features = build_symbolic_features(coef_df).columns.tolist()
    stability = {coef: {feat: 0 for feat in all_features} for coef in coef_cols}
    fold_count = 0

    for train_idx, _ in splitter.split(coef_df):
        train_df = coef_df.iloc[train_idx].reset_index(drop=True)
        X_train = build_symbolic_features(train_df, columns=all_features)

        for coef in coef_cols:
            y = train_df[coef].to_numpy(dtype=float)
            scaler = StandardScaler()
            Xs = scaler.fit_transform(X_train)
            model = LassoCV(cv=min(5, len(train_df)), random_state=fold_count + 1, max_iter=30000)
            model.fit(Xs, y)

            for feat, val in zip(all_features, model.coef_):
                if abs(val) > threshold:
                    stability[coef][feat] += 1

        fold_count += 1

    return pd.DataFrame([
        {
            "coefficient": coef,
            "term": feat,
            "frequency": stability[coef][feat] / max(fold_count, 1),
            "count": stability[coef][feat],
            "folds": fold_count,
        }
        for coef in coef_cols for feat in all_features
    ])


def stable_terms_by_coefficient(coef_df: pd.DataFrame, coef_cols: list[str], threshold: float = 0.5):
    stability_df = term_stability_table(coef_df, coef_cols)
    terms_by_coef = {}
    for coef in coef_cols:
        sub = stability_df[(stability_df["coefficient"] == coef) & (stability_df["frequency"] >= threshold)]
        terms_by_coef[coef] = sub["term"].tolist()
    return terms_by_coef, stability_df


def predict_symbolic_coefficients(train_df, test_df, coef_cols, terms_by_coef):
    yhat = np.zeros((len(test_df), len(coef_cols)), dtype=float)

    for j, coef in enumerate(coef_cols):
        terms = terms_by_coef.get(coef, [])
        if not terms:
            yhat[:, j] = train_df[coef].mean()
            continue

        X_train = build_symbolic_features(train_df, reduced_terms=terms)
        X_test = build_symbolic_features(test_df, columns=X_train.columns, reduced_terms=terms)

        y_train = train_df[coef].to_numpy(dtype=float)
        scaler = StandardScaler()
        Xtr = scaler.fit_transform(X_train)
        Xte = scaler.transform(X_test)

        model = Ridge(alpha=1.0)
        model.fit(Xtr, y_train)
        yhat[:, j] = model.predict(Xte)

    return yhat

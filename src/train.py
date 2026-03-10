from __future__ import annotations

import argparse
import json
from pathlib import Path

import joblib
import pandas as pd
import yaml
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import average_precision_score, f1_score, roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder


def load_config(path: str) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def build_preprocessor(df: pd.DataFrame, target_col: str):
    feature_df = df.drop(columns=[target_col])
    cat_cols = feature_df.select_dtypes(include=["object"]).columns.tolist()
    num_cols = [c for c in feature_df.columns if c not in cat_cols]

    numeric_transformer = Pipeline(
        steps=[("imputer", SimpleImputer(strategy="median"))]
    )
    categorical_transformer = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="most_frequent")),
            ("onehot", OneHotEncoder(handle_unknown="ignore")),
        ]
    )

    return ColumnTransformer(
        transformers=[
            ("num", numeric_transformer, num_cols),
            ("cat", categorical_transformer, cat_cols),
        ]
    ), num_cols, cat_cols


def main(config_path: str):
    cfg = load_config(config_path)
    csv_path = Path(cfg["data"]["prepared_csv_path"])
    target_col = cfg["data"]["target_col"]

    if not csv_path.exists():
        raise FileNotFoundError("Dataset bulunamadı. Önce: python -m src.data.prepare_dataset")

    df = pd.read_csv(csv_path)
    X = df.drop(columns=[target_col])
    y = df[target_col]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=float(cfg.get("test_size", 0.2)),
        random_state=int(cfg.get("seed", 42)),
        stratify=y,
    )

    preprocessor, _, _ = build_preprocessor(df, target_col)

    candidates = {}
    lr_cfg = cfg["model"]["logistic_regression"]
    rf_cfg = cfg["model"]["random_forest"]

    candidates["logistic_regression"] = LogisticRegression(
        C=float(lr_cfg["C"]),
        max_iter=int(lr_cfg["max_iter"]),
        class_weight=lr_cfg["class_weight"],
        solver=lr_cfg["solver"],
    )
    candidates["random_forest"] = RandomForestClassifier(
        n_estimators=int(rf_cfg["n_estimators"]),
        max_depth=int(rf_cfg["max_depth"]),
        min_samples_leaf=int(rf_cfg["min_samples_leaf"]),
        class_weight=rf_cfg["class_weight"],
        random_state=int(rf_cfg["random_state"]),
    )

    comparison = []
    best_name = None
    best_score = -1
    best_pipeline = None
    best_metrics = None

    for name in cfg["training"]["candidate_models"]:
        clf = candidates[name]
        pipe = Pipeline(steps=[("preprocessor", preprocessor), ("model", clf)])
        pipe.fit(X_train, y_train)

        probs = pipe.predict_proba(X_test)[:, 1]
        preds = (probs >= float(cfg["threshold"]["default"])).astype(int)

        metrics = {
            "roc_auc": float(roc_auc_score(y_test, probs)),
            "pr_auc": float(average_precision_score(y_test, probs)),
            "f1_score": float(f1_score(y_test, preds)),
        }
        selection_score = (metrics["roc_auc"] + metrics["pr_auc"] + metrics["f1_score"]) / 3
        comparison.append({
            "model": name,
            **metrics,
            "selection_score": float(selection_score),
        })

        if selection_score > best_score:
            best_score = selection_score
            best_name = name
            best_pipeline = pipe
            best_metrics = metrics

    Path("models").mkdir(exist_ok=True)
    Path("reports").mkdir(exist_ok=True)

    joblib.dump(best_pipeline, "models/credit_risk_pipeline.joblib")
    Path("reports/model_meta.json").write_text(
        json.dumps({"best_model": best_name}, indent=2),
        encoding="utf-8",
    )
    Path("reports/model_comparison.json").write_text(
        json.dumps(comparison, indent=2),
        encoding="utf-8",
    )
    Path("reports/metrics.json").write_text(
        json.dumps(best_metrics, indent=2),
        encoding="utf-8",
    )

    # crude feature importance
    feature_items = []
    model = best_pipeline.named_steps["model"]
    pre = best_pipeline.named_steps["preprocessor"]
    feature_names = pre.get_feature_names_out().tolist()

    if hasattr(model, "feature_importances_"):
        importances = model.feature_importances_.tolist()
    elif hasattr(model, "coef_"):
        importances = [abs(v) for v in model.coef_[0].tolist()]
    else:
        importances = [0.0] * len(feature_names)

    pairs = sorted(zip(feature_names, importances), key=lambda x: x[1], reverse=True)[:15]
    total = sum(v for _, v in pairs) or 1.0
    feature_items = [{"feature": name, "importance": float(val / total)} for name, val in pairs]

    Path("reports/feature_importance.json").write_text(
        json.dumps(feature_items, indent=2),
        encoding="utf-8",
    )

    print(f"[OK] Best model: {best_name}")
    print(json.dumps(best_metrics, indent=2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="configs/config.yaml")
    args = parser.parse_args()
    main(args.config)

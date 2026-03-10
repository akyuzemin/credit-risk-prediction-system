from __future__ import annotations

import argparse
import json
from pathlib import Path

import joblib
import pandas as pd
import yaml
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.model_selection import train_test_split


def load_config(path: str) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def main(config_path: str):
    cfg = load_config(config_path)
    csv_path = Path(cfg["data"]["prepared_csv_path"])
    model_path = Path("models/credit_risk_pipeline.joblib")

    if not csv_path.exists():
        raise FileNotFoundError("Dataset bulunamadı. Önce: python -m src.data.prepare_dataset")
    if not model_path.exists():
        raise FileNotFoundError("Model bulunamadı. Önce: python -m src.train --config configs/config.yaml")

    df = pd.read_csv(csv_path)
    target_col = cfg["data"]["target_col"]
    X = df.drop(columns=[target_col])
    y = df[target_col]

    _, X_test, _, y_test = train_test_split(
        X, y,
        test_size=float(cfg.get("test_size", 0.2)),
        random_state=int(cfg.get("seed", 42)),
        stratify=y,
    )

    model = joblib.load(model_path)
    preds = model.predict(X_test)

    report = classification_report(y_test, preds, output_dict=True)
    cm = confusion_matrix(y_test, preds).tolist()

    Path("reports").mkdir(exist_ok=True)
    Path("reports/evaluation.json").write_text(
        json.dumps({"classification_report": report, "confusion_matrix": cm}, indent=2),
        encoding="utf-8",
    )

    print("[OK] Evaluation saved to reports/evaluation.json")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="configs/config.yaml")
    args = parser.parse_args()
    main(args.config)

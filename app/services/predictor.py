from pathlib import Path
import json
import joblib
import pandas as pd

MODEL_PATH = Path("models/credit_risk_pipeline.joblib")
MODEL_META_PATH = Path("reports/model_meta.json")


def _load_model():
    if not MODEL_PATH.exists():
        raise FileNotFoundError(
            "Model bulunamadı. Önce: python -m src.train --config configs/config.yaml"
        )
    return joblib.load(MODEL_PATH)


def predict_one(payload: dict) -> float:
    model = _load_model()
    df = pd.DataFrame([payload])
    return float(model.predict_proba(df)[:, 1][0])


def predict_df(df: pd.DataFrame):
    model = _load_model()
    return model.predict_proba(df)[:, 1]


def get_model_name() -> str:
    if MODEL_META_PATH.exists():
        meta = json.loads(MODEL_META_PATH.read_text(encoding="utf-8"))
        return meta.get("best_model", "unknown")
    return "unknown"

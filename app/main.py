from __future__ import annotations

import io
import json
from pathlib import Path

import pandas as pd
from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.core.settings import get_prediction_threshold
from app.schemas import (
    BatchPredictResponse,
    BatchPredictionItem,
    BatchPredictionSummary,
    CreditApplicant,
    DashboardSummary,
    PredictResponse,
)
from app.services.actions import build_underwriting_action, get_risk_level, recommend_action
from app.services.explainer import explain_one, get_global_feature_importance
from app.services.predictor import get_model_name, predict_df, predict_one

app = FastAPI(title="Credit Risk Prediction API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="app/static"), name="static")


@app.get("/")
def index():
    return {
        "message": "Credit Risk API çalışıyor",
        "docs": "/docs",
        "health": "/health"
    }


@app.get("/health")
def health():
    return {"status": "ok", "service": "credit-risk-api"}


@app.get("/meta")
def meta():
    return {
        "threshold": get_prediction_threshold(),
        "select_options": {
            "checking_status": [
                {"value": "A11", "label": "Düşük bakiyeli / sorunlu vadesiz hesap"},
                {"value": "A12", "label": "200 DM altı vadesiz hesap bakiyesi"},
                {"value": "A13", "label": "200 DM ve üzeri vadesiz hesap bakiyesi"},
                {"value": "A14", "label": "Vadesiz hesap yok"},
            ],
            "credit_history": [
                {"value": "A30", "label": "Daha önce kredi kullanmadı / tüm ödemeler düzenli"},
                {"value": "A31", "label": "Önceki krediler tamamen düzenli ödendi"},
                {"value": "A32", "label": "Mevcut krediler düzenli ödendi"},
                {"value": "A33", "label": "Kredi ödemelerinde gecikme geçmişi var"},
                {"value": "A34", "label": "Kritik hesap / başka kredi kayıtları mevcut"},
            ],
            "purpose": [
                {"value": "A40", "label": "Yeni araç"},
                {"value": "A41", "label": "İkinci el araç"},
                {"value": "A42", "label": "Mobilya / ev eşyası"},
                {"value": "A43", "label": "Elektronik ürün / televizyon"},
                {"value": "A44", "label": "Ev aletleri"},
                {"value": "A45", "label": "Tamir / bakım"},
                {"value": "A46", "label": "Eğitim"},
                {"value": "A47", "label": "Tatil"},
                {"value": "A48", "label": "Mesleki yeniden eğitim"},
                {"value": "A49", "label": "İş / ticari amaç"},
                {"value": "A410", "label": "Diğer"},
            ],
            "savings_status": [
                {"value": "A61", "label": "100 DM altı birikim"},
                {"value": "A62", "label": "100–500 DM arası birikim"},
                {"value": "A63", "label": "500–1000 DM arası birikim"},
                {"value": "A64", "label": "1000 DM üzeri birikim"},
                {"value": "A65", "label": "Birikim hesabı yok / bilinmiyor"},
            ],
            "employment_since": [
                {"value": "A71", "label": "İşsiz"},
                {"value": "A72", "label": "1 yıldan az süredir çalışıyor"},
                {"value": "A73", "label": "1–4 yıldır çalışıyor"},
                {"value": "A74", "label": "4–7 yıldır çalışıyor"},
                {"value": "A75", "label": "7 yıldan uzun süredir çalışıyor"},
            ],
            "personal_status_sex": [
                {"value": "A91", "label": "Erkek, boşanmış / ayrı"},
                {"value": "A92", "label": "Kadın, boşanmış / evli"},
                {"value": "A93", "label": "Erkek, bekar"},
                {"value": "A94", "label": "Erkek, evli / dul"},
            ],
            "other_debtors": [
                {"value": "A101", "label": "Yok"},
                {"value": "A102", "label": "Ortak başvuru sahibi var"},
                {"value": "A103", "label": "Kefil var"},
            ],
            "property": [
                {"value": "A121", "label": "Gayrimenkul"},
                {"value": "A122", "label": "Birikimli sigorta / yapı tasarrufu"},
                {"value": "A123", "label": "Araç veya diğer varlık"},
                {"value": "A124", "label": "Varlık bilgisi yok"},
            ],
            "other_installment_plans": [
                {"value": "A141", "label": "Banka"},
                {"value": "A142", "label": "Mağaza"},
                {"value": "A143", "label": "Yok"},
            ],
            "housing": [
                {"value": "A151", "label": "Kiracı"},
                {"value": "A152", "label": "Ev sahibi"},
                {"value": "A153", "label": "Kira ödemiyor"},
            ],
            "job": [
                {"value": "A171", "label": "İşsiz / vasıfsız"},
                {"value": "A172", "label": "Vasıfsız çalışan"},
                {"value": "A173", "label": "Nitelikli çalışan / memur"},
                {"value": "A174", "label": "Yönetici / serbest meslek / yüksek nitelikli"},
            ],
            "own_telephone": [
                {"value": "A191", "label": "Telefon yok"},
                {"value": "A192", "label": "Telefon var"},
            ],
            "foreign_worker": [
                {"value": "A201", "label": "Evet"},
                {"value": "A202", "label": "Hayır"},
            ],
        },
    }


@app.get("/dashboard-summary", response_model=DashboardSummary)
def dashboard_summary():
    metrics = _load_json("reports/metrics.json")
    model_comparison = _load_json("reports/model_comparison.json", default=[])
    feature_importance = _load_json("reports/feature_importance.json", default=[])
    return DashboardSummary(
        threshold=get_prediction_threshold(),
        available_model=get_model_name(),
        latest_metrics=metrics,
        model_comparison=model_comparison,
        feature_importance=feature_importance,
    )


@app.post("/predict", response_model=PredictResponse)
def predict(features: CreditApplicant):
    payload = features.model_dump()
    prob = predict_one(payload)
    threshold = get_prediction_threshold()
    risk_score = int(round(prob * 100))
    pred = 1 if prob >= threshold else 0
    risk_level = get_risk_level(prob)

    return PredictResponse(
        prediction=pred,
        default_probability=prob,
        risk_score=risk_score,
        risk_level=risk_level,
        recommended_action=recommend_action(prob, payload),
        top_drivers=explain_one(payload),
        underwriting_action=build_underwriting_action(payload, prob),
    )


@app.post("/predict/batch", response_model=BatchPredictResponse)
def batch_predict(file: UploadFile = File(...)):
    if not file.filename.lower().endswith(".csv"):
        raise HTTPException(status_code=400, detail="Lütfen CSV dosyası yükleyin.")

    content = file.file.read()
    try:
        df = pd.read_csv(io.BytesIO(content))
    except Exception as exc:
        raise HTTPException(status_code=400, detail=f"CSV okunamadı: {exc}") from exc

    probs = predict_df(df)
    items = []
    high = medium = low = 0

    for idx, (row, prob) in enumerate(zip(df.to_dict(orient="records"), probs), start=1):
        score = int(round(float(prob) * 100))
        level = get_risk_level(float(prob))
        high += level == "high"
        medium += level == "medium"
        low += level == "low"

        items.append(
            BatchPredictionItem(
                row_id=idx,
                applicant_id=row.get("applicant_id"),
                default_probability=float(prob),
                risk_score=score,
                risk_level=level,
                recommended_action=recommend_action(float(prob), row),
            )
        )

    summary = BatchPredictionSummary(
        total_rows=len(items),
        high_risk_count=int(high),
        medium_risk_count=int(medium),
        low_risk_count=int(low),
        average_risk_score=round(
            sum(item.risk_score for item in items) / len(items), 2
        ) if items else 0.0,
    )
    return BatchPredictResponse(summary=summary, predictions=items)


@app.get("/feature-importance")
def feature_importance():
    return {"items": get_global_feature_importance()}


def _load_json(path: str, default=None):
    file_path = Path(path)
    if not file_path.exists():
        return {} if default is None else default
    return json.loads(file_path.read_text(encoding="utf-8"))
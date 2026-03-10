# Credit Risk Prediction System

End-to-end ML project for loan default risk scoring.

## Features
- Single applicant risk prediction
- Batch CSV scoring
- FastAPI backend
- Simple frontend dashboard
- Training and evaluation pipeline
- Feature importance and model comparison reports

## Quick start

```bash
python -m venv .venv
.venv\Scripts\activate   # Windows
pip install -r requirements.txt

python -m src.data.prepare_dataset
python -m src.train --config configs/config.yaml
python -m src.evaluate --config configs/config.yaml

uvicorn app.main:app --reload
```

Open:
- http://127.0.0.1:8000
- http://127.0.0.1:8000/docs

## Expected raw file

Place the downloaded German Credit file at:

`data/raw/german_credit.data`

The prepare step converts it into `data/raw/credit_risk.csv`.

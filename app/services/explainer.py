from pathlib import Path
import json

FEATURE_PATH = Path("reports/feature_importance.json")


def get_global_feature_importance():
    if not FEATURE_PATH.exists():
        return []
    return json.loads(FEATURE_PATH.read_text(encoding="utf-8"))


def explain_one(payload: dict):
    rules = []
    if payload.get("checking_status") in {"A11", "A12"}:
        rules.append({"feature": "checking_status", "impact": "high", "direction": "risk_up"})
    if float(payload.get("credit_amount", 0)) >= 5000:
        rules.append({"feature": "credit_amount", "impact": "medium", "direction": "risk_up"})
    if int(payload.get("duration_months", 0)) >= 36:
        rules.append({"feature": "duration_months", "impact": "medium", "direction": "risk_up"})
    if int(payload.get("age", 0)) >= 35:
        rules.append({"feature": "age", "impact": "low", "direction": "risk_down"})
    return rules[:4]

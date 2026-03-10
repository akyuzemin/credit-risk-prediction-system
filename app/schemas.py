from typing import Any
from pydantic import BaseModel


class CreditApplicant(BaseModel):
    checking_status: str
    duration_months: int
    credit_history: str
    purpose: str
    credit_amount: float
    savings_status: str
    employment_since: str
    installment_rate: int
    personal_status_sex: str
    other_debtors: str
    present_residence_since: int
    property: str
    age: int
    other_installment_plans: str
    housing: str
    existing_credits: int
    job: str
    num_dependents: int
    own_telephone: str
    foreign_worker: str


class DriverItem(BaseModel):
    feature: str
    impact: str
    direction: str


class RiskAction(BaseModel):
    decision: str
    note: str


class PredictResponse(BaseModel):
    prediction: int
    default_probability: float
    risk_score: int
    risk_level: str
    recommended_action: str
    top_drivers: list[DriverItem]
    underwriting_action: RiskAction


class BatchPredictionItem(BaseModel):
    row_id: int
    applicant_id: str | None = None
    default_probability: float
    risk_score: int
    risk_level: str
    recommended_action: str


class BatchPredictionSummary(BaseModel):
    total_rows: int
    high_risk_count: int
    medium_risk_count: int
    low_risk_count: int
    average_risk_score: float


class BatchPredictResponse(BaseModel):
    summary: BatchPredictionSummary
    predictions: list[BatchPredictionItem]


class DashboardSummary(BaseModel):
    threshold: float
    available_model: str
    latest_metrics: dict[str, Any]
    model_comparison: list[dict[str, Any]]
    feature_importance: list[dict[str, Any]]

const API_BASE = import.meta.env.VITE_API_URL || "http://localhost:8000";

export interface SelectOption {
  value: string;
  label: string;
}

export interface MetaResponse {
  threshold: number;
  select_options: Record<string, SelectOption[]>;
}

export interface DashboardMetricMap {
  roc_auc?: number;
  pr_auc?: number;
  f1_score?: number;
  [key: string]: number | undefined;
}

export interface ModelComparisonItem {
  model: string;
  roc_auc: number;
  pr_auc: number;
  f1_score: number;
  selection_score: number;
}

export interface FeatureImportanceItem {
  feature: string;
  importance: number;
}

export interface DashboardSummary {
  threshold: number;
  available_model: string;
  latest_metrics: DashboardMetricMap;
  model_comparison: ModelComparisonItem[];
  feature_importance: FeatureImportanceItem[];
}

export interface PredictRequest {
  checking_status: string;
  duration_months: number;
  credit_history: string;
  purpose: string;
  credit_amount: number;
  savings_status: string;
  employment_since: string;
  installment_rate: number;
  personal_status_sex: string;
  other_debtors: string;
  present_residence_since: number;
  property: string;
  age: number;
  other_installment_plans: string;
  housing: string;
  existing_credits: number;
  job: string;
  num_dependents: number;
  own_telephone: string;
  foreign_worker: string;
}

export interface DriverItem {
  feature: string;
  impact: string;
  direction: string;
}

export interface UnderwritingAction {
  decision: string;
  note: string;
}

export interface PredictResponse {
  prediction: number;
  default_probability: number;
  risk_score: number;
  risk_level: "low" | "medium" | "high";
  recommended_action: string;
  top_drivers: DriverItem[];
  underwriting_action: UnderwritingAction;
}

export async function fetchMeta(): Promise<MetaResponse> {
  const res = await fetch(`${API_BASE}/meta`);
  if (!res.ok) throw new Error("Failed to fetch metadata");
  return res.json();
}

export async function fetchDashboardSummary(): Promise<DashboardSummary> {
  const res = await fetch(`${API_BASE}/dashboard-summary`);
  if (!res.ok) throw new Error("Failed to fetch dashboard summary");
  return res.json();
}

export async function predict(data: PredictRequest): Promise<PredictResponse> {
  const res = await fetch(`${API_BASE}/predict`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });

  if (!res.ok) {
    const message = await res.text();
    throw new Error(message || "Prediction failed");
  }

  return res.json();
}
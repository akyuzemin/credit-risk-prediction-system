from __future__ import annotations

from pathlib import Path
import pandas as pd
import yaml

COLUMN_NAMES = [
    "checking_status",
    "duration_months",
    "credit_history",
    "purpose",
    "credit_amount",
    "savings_status",
    "employment_since",
    "installment_rate",
    "personal_status_sex",
    "other_debtors",
    "present_residence_since",
    "property",
    "age",
    "other_installment_plans",
    "housing",
    "existing_credits",
    "job",
    "num_dependents",
    "own_telephone",
    "foreign_worker",
    "risk",
]


def load_config(path: str = "configs/config.yaml") -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def main(config_path: str = "configs/config.yaml") -> None:
    cfg = load_config(config_path)
    input_path = Path(cfg["data"]["raw_source_path"])
    output_path = Path(cfg["data"]["prepared_csv_path"])

    if not input_path.exists():
        raise FileNotFoundError(f"Dataset bulunamadı: {input_path}")

    df = pd.read_csv(input_path, sep=r"\s+", header=None, names=COLUMN_NAMES)
    df["default"] = df["risk"].map({1: 0, 2: 1})
    df = df.drop(columns=["risk"])

    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False, encoding="utf-8")

    print(f"[OK] Prepared dataset saved to {output_path}")
    print(df.head())
    print(df["default"].value_counts())


if __name__ == "__main__":
    main()

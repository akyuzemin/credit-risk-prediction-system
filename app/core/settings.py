from pathlib import Path
import yaml


def load_config(path: str = "configs/config.yaml") -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def get_prediction_threshold() -> float:
    cfg = load_config()
    return float(cfg.get("threshold", {}).get("default", 0.5))

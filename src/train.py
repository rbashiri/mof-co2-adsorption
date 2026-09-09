# train.py — Phase 1 (Baseline + Explainability): train RF for all 5 CO2 pressures
# and persist the trained models + metrics for reuse by app.py and later phases.
import argparse
import os
import sys

import pandas as pd
import skops.io as sio

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from mof_models import evaluate_target_columns

DATA_PATH = "/home/susan/mof-co2-adsorption/data/processed/data_clean_v2"
MODELS_DIR = "/home/susan/mof-co2-adsorption/results/models"
METRICS_PATH = "/home/susan/mof-co2-adsorption/results/metrics_all_pressures.csv"

FEATURE_COLUMNS = ["lcd", "pld", "void_fraction", "surface_area_m2g"]
TARGET_COLUMNS = [
    "CO2_uptake_0.01bar_molkg", "CO2_uptake_0.05bar_molkg",
    "CO2_uptake_0.1bar_molkg", "CO2_uptake_0.5bar_molkg",
    "CO2_uptake_2.5bar_molkg",
]
RF_PARAMS = dict(n_estimators=100, max_depth=None, min_samples_split=2,
                 min_samples_leaf=1, max_features="sqrt", random_state=12345, n_jobs=-1)


def train_all_pressures(data_path=DATA_PATH, models_dir=MODELS_DIR, metrics_path=METRICS_PATH):
    """Train one RF per pressure target and save each model + the combined metrics table."""
    df = pd.read_csv(data_path)
    results, summary = evaluate_target_columns(df, FEATURE_COLUMNS, TARGET_COLUMNS, RF_PARAMS)

    os.makedirs(models_dir, exist_ok=True)
    for target, evaluation in results.items():
        model_path = os.path.join(models_dir, f"rf_{target}.skops")
        sio.dump(evaluation["model"], model_path)

    os.makedirs(os.path.dirname(metrics_path), exist_ok=True)
    summary.to_csv(metrics_path, index=False)

    return results, summary


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Train RF models for all CO2 pressure targets.")
    parser.add_argument("--data-path", default=DATA_PATH)
    parser.add_argument("--models-dir", default=MODELS_DIR)
    parser.add_argument("--metrics-path", default=METRICS_PATH)
    args = parser.parse_args()

    _, summary_df = train_all_pressures(args.data_path, args.models_dir, args.metrics_path)
    print(summary_df)

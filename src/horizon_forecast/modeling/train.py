import joblib
from pathlib import Path
import pandas as pd
from xgboost import XGBRegressor
import json

from horizon_forecast.ingestion.adm_load import load_admissions
from horizon_forecast.ingestion.edarr_load import load_ed_arrivals
from horizon_forecast.ingestion.electsurgeries_load import load_elective_surgeries

from horizon_forecast.features.demand_aggregation import build_demand_timeseries
from horizon_forecast.modeling.split import time_split
from horizon_forecast.evaluation.metrics import regression_metrics


def train_model():
    # Load data
    adm = load_admissions()
    ed = load_ed_arrivals()
    elec = load_elective_surgeries()

    # Build modeling dataset
    df = build_demand_timeseries(adm, ed, elec, freq="D")
    df = df.sort_index()

    # Dynamic split
    train_end = df.index[int(len(df) * 0.6)]
    val_end = df.index[int(len(df) * 0.85)]

    train, val, test = time_split(df, train_end, val_end)

    FEATURES = ["ed_arrivals", "elective_surgeries", "dow", "month", "is_weekend"]

    X_train, y_train = train[FEATURES], train["admissions"]
    X_val,   y_val   = val[FEATURES],   val["admissions"]
    X_test,  y_test  = test[FEATURES],  test["admissions"]

    # Train model
    model = XGBRegressor(
        n_estimators=300,
        learning_rate=0.05,
        max_depth=4,
        subsample=0.9,
        colsample_bytree=0.9,
        random_state=42,
    )
    model.fit(X_train, y_train)

    # Save model artifact
    artifacts_dir = Path("artifacts")
    artifacts_dir.mkdir(exist_ok=True, parents=True)
    joblib.dump(model, artifacts_dir / "model.pkl")
    print("Model saved to artifacts/model.pkl")

    # Evaluate
    preds = model.predict(X_test)
    metrics = regression_metrics(y_test, preds)
    print("Test Metrics:", metrics)

    # Save metrics artifact
    with open(artifacts_dir / "metrics.json", "w") as f:
        json.dump(metrics, f, indent=2)


if __name__ == "__main__":
    train_model()
"""
Predict and save to DB:
python ml/predict.py
"""

import time
from pathlib import Path
import sys

import joblib
import pandas as pd
from sqlalchemy import text

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from db.connection import engine, log_pipeline
from ml.features import MODEL_PATH, build_features, load_daily_metrics


def save_predictions() -> int:
    start = time.time()

    if not MODEL_PATH.exists():
        raise FileNotFoundError(f"Model not found: {MODEL_PATH}. Run ml/train.py first.")

    artifact = joblib.load(MODEL_PATH)
    model = artifact["model"]
    features = artifact["feature_columns"]
    version = artifact["model_version"]

    data = build_features(load_daily_metrics())
    test_rows = artifact["test_rows"]
    predict_data = data.tail(test_rows).copy()

    predict_data["predicted_sales"] = model.predict(predict_data[features])
    predict_data["actual_sales"] = predict_data["total_sales"]

    output = predict_data[["metric_date", "predicted_sales", "actual_sales"]].copy()
    output = output.rename(columns={"metric_date": "predict_date"})
    output["model_version"] = version
    output["predict_date"] = output["predict_date"].dt.date

    with engine.begin() as conn:
        conn.execute(
            text("DELETE FROM predictions WHERE model_version = :version"),
            {"version": version},
        )
        output.to_sql("predictions", conn, if_exists="append", index=False)

    duration = int((time.time() - start) * 1000)
    message = f"Saved {len(output)} predictions"
    log_pipeline("predict", "success", message, len(output), duration)

    print(f"[OK] predict: {message} ({duration}ms)")
    print(output.head())
    return len(output)


if __name__ == "__main__":
    save_predictions()

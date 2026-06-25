"""
Model metrics (MAE, RMSE):
python ml/evaluate.py
"""

import time
from pathlib import Path
import sys

import joblib
import numpy as np
from sklearn.metrics import mean_absolute_error, mean_squared_error

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from db.connection import log_pipeline
from ml.features import MODEL_PATH, build_features, load_daily_metrics


def evaluate_model() -> dict:
    start = time.time()

    if not MODEL_PATH.exists():
        raise FileNotFoundError(f"Model not found: {MODEL_PATH}. Run ml/train.py first.")

    artifact = joblib.load(MODEL_PATH)
    model = artifact["model"]
    features = artifact["feature_columns"]

    data = build_features(load_daily_metrics())
    test_rows = artifact["test_rows"]
    test_data = data.tail(test_rows)

    X_test = test_data[features]
    y_test = test_data["total_sales"]
    y_pred = model.predict(X_test)

    mae = mean_absolute_error(y_test, y_pred)
    rmse = float(np.sqrt(mean_squared_error(y_test, y_pred)))

    duration = int((time.time() - start) * 1000)
    message = f"MAE={mae:.2f}, RMSE={rmse:.2f}"
    log_pipeline("evaluate", "success", message, len(test_data), duration)

    print(f"[OK] evaluate: {message} ({duration}ms)")
    print(f"  Test rows: {len(test_data)}")
    return {"mae": mae, "rmse": rmse, "test_rows": len(test_data)}


if __name__ == "__main__":
    evaluate_model()

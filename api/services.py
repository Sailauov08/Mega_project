import joblib
import numpy as np
import pandas as pd
from sklearn.metrics import mean_absolute_error, mean_squared_error
from sqlalchemy import text

from config.settings import settings
from db.connection import engine, get_connection
from ml.features import FEATURE_COLUMNS, MODEL_PATH, build_features, load_daily_metrics


def check_database() -> bool:
    try:
        with get_connection() as conn:
            conn.execute(text("SELECT 1"))
        return True
    except Exception:
        return False


def get_model_info() -> dict:
    if not MODEL_PATH.exists():
        return {"loaded": False, "version": None}

    artifact = joblib.load(MODEL_PATH)
    return {
        "loaded": True,
        "version": artifact.get("model_version", "unknown"),
    }


def compute_metrics() -> dict:
    if not MODEL_PATH.exists():
        raise FileNotFoundError("Model not found. Run: python ml/train.py")

    artifact = joblib.load(MODEL_PATH)
    model = artifact["model"]
    features = artifact["feature_columns"]
    version = artifact["model_version"]
    test_rows = artifact["test_rows"]

    data = build_features(load_daily_metrics())
    test_data = data.tail(test_rows)

    y_test = test_data["total_sales"]
    y_pred = model.predict(test_data[features])

    return {
        "mae": float(mean_absolute_error(y_test, y_pred)),
        "rmse": float(np.sqrt(mean_squared_error(y_test, y_pred))),
        "test_rows": int(len(test_data)),
        "model_version": version,
    }


def get_latest_metrics(limit: int = 10) -> list[dict]:
    df = pd.read_sql(
        text("""
            SELECT metric_date, total_sales, total_profit, total_quantity,
                   order_count, avg_order_value
            FROM daily_metrics
            ORDER BY metric_date DESC
            LIMIT :limit
        """),
        engine,
        params={"limit": limit},
    )
    df["metric_date"] = df["metric_date"].astype(str)
    return df.to_dict(orient="records")


def get_predictions(limit: int = 10) -> list[dict]:
    df = pd.read_sql(
        text("""
            SELECT predict_date, predicted_sales, actual_sales, model_version
            FROM predictions
            ORDER BY predict_date DESC
            LIMIT :limit
        """),
        engine,
        params={"limit": limit},
    )
    df["predict_date"] = df["predict_date"].astype(str)
    return df.to_dict(orient="records")


def predict_sales(payload: dict) -> dict:
    if not MODEL_PATH.exists():
        raise FileNotFoundError("Model not found. Run: python ml/train.py")

    artifact = joblib.load(MODEL_PATH)
    model = artifact["model"]
    features = artifact["feature_columns"]
    version = artifact["model_version"]

    row = pd.DataFrame([{col: payload[col] for col in features}])
    predicted = float(model.predict(row)[0])

    return {
        "predicted_sales": round(predicted, 2),
        "model_version": version,
    }


def predict_from_latest_day() -> dict:
    data = build_features(load_daily_metrics())
    if data.empty:
        raise ValueError("Not enough data for prediction")

    latest = data.iloc[-1]
    payload = {col: latest[col] for col in FEATURE_COLUMNS}
    result = predict_sales(payload)
    result["based_on_date"] = str(latest["metric_date"].date())
    return result

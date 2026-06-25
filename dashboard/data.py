import pandas as pd
from sqlalchemy import text

from db.connection import engine


def load_daily_metrics() -> pd.DataFrame:
    df = pd.read_sql(
        text("""
            SELECT metric_date, total_sales, total_profit, total_quantity,
                   order_count, avg_order_value
            FROM daily_metrics
            ORDER BY metric_date
        """),
        engine,
    )
    df["metric_date"] = pd.to_datetime(df["metric_date"])
    return df


def load_predictions() -> pd.DataFrame:
    df = pd.read_sql(
        text("""
            SELECT predict_date, predicted_sales, actual_sales, model_version
            FROM predictions
            ORDER BY predict_date
        """),
        engine,
    )
    if not df.empty:
        df["predict_date"] = pd.to_datetime(df["predict_date"])
    return df


def load_pipeline_logs(limit: int = 15) -> pd.DataFrame:
    return pd.read_sql(
        text("""
            SELECT step, status, message, rows_count, duration_ms, created_at
            FROM pipeline_logs
            ORDER BY created_at DESC
            LIMIT :limit
        """),
        engine,
        params={"limit": limit},
    )

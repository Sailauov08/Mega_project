from pathlib import Path

import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_DIR = BASE_DIR / "models"
MODEL_PATH = MODEL_DIR / "model_v1.joblib"
MODEL_VERSION = "v1"

FEATURE_COLUMNS = [
    "day_of_week",
    "month",
    "lag_sales_1",
    "lag_sales_7",
    "rolling_mean_7",
    "order_count",
    "total_quantity",
]

TARGET_COLUMN = "total_sales"


def load_daily_metrics() -> pd.DataFrame:
    from db.connection import engine

    df = pd.read_sql(
        """
        SELECT metric_date, total_sales, total_profit, total_quantity, order_count
        FROM daily_metrics
        ORDER BY metric_date
        """,
        engine,
    )
    df["metric_date"] = pd.to_datetime(df["metric_date"])
    return df


def build_features(df: pd.DataFrame) -> pd.DataFrame:
    data = df.copy()
    data["day_of_week"] = data["metric_date"].dt.dayofweek
    data["month"] = data["metric_date"].dt.month
    data["lag_sales_1"] = data["total_sales"].shift(1)
    data["lag_sales_7"] = data["total_sales"].shift(7)
    data["rolling_mean_7"] = data["total_sales"].rolling(7).mean().shift(1)
    data = data.dropna().reset_index(drop=True)
    return data

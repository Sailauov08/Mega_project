import time
from pathlib import Path
import sys

import pandas as pd
from sqlalchemy import text

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from db.connection import engine, log_pipeline


def build_daily_metrics() -> int:
    start = time.time()

    with engine.connect() as conn:
        df = pd.read_sql(
            """
            SELECT order_date, sales, profit, quantity
            FROM clean_sales
            """,
            conn,
        )

    if df.empty:
        log_pipeline("build_metrics", "error", "No data in clean_sales")
        raise ValueError("No data in clean_sales")

    daily = (
        df.groupby("order_date")
        .agg(
            total_sales=("sales", "sum"),
            total_profit=("profit", "sum"),
            total_quantity=("quantity", "sum"),
            order_count=("sales", "count"),
        )
        .reset_index()
    )

    daily["avg_order_value"] = (daily["total_sales"] / daily["order_count"]).round(2)
    daily = daily.rename(columns={"order_date": "metric_date"})

    with engine.begin() as conn:
        conn.execute(text("TRUNCATE TABLE daily_metrics RESTART IDENTITY"))
        daily.to_sql("daily_metrics", conn, if_exists="append", index=False)

    duration = int((time.time() - start) * 1000)
    log_pipeline(
        "build_metrics",
        "success",
        f"Built {len(daily)} daily records",
        len(daily),
        duration,
    )
    print(f"[OK] build_metrics: {len(daily)} days ({duration}ms)")
    return len(daily)


if __name__ == "__main__":
    build_daily_metrics()

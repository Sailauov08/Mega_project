import time
from pathlib import Path
import sys

import pandas as pd
from sqlalchemy import text

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from db.connection import engine, log_pipeline


def clean_data() -> int:
    start = time.time()

    with engine.connect() as conn:
        df = pd.read_sql("SELECT * FROM raw_sales", conn)

    before = len(df)

    df["order_date"] = pd.to_datetime(df["order_date"], errors="coerce")
    df["product"] = df["product"].astype(str).str.strip()
    df["category"] = df["category"].astype(str).str.strip()
    df["region"] = df["region"].astype(str).str.strip()
    df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce")
    df["sales"] = pd.to_numeric(df["sales"], errors="coerce")
    df["profit"] = pd.to_numeric(df["profit"], errors="coerce")

    df = df.dropna(subset=["order_date", "product", "category", "region", "quantity", "sales"])
    df = df.drop_duplicates()
    df = df[df["quantity"] > 0]
    df = df[df["sales"] >= 0]
    df = df[df["order_date"] <= pd.Timestamp.today()]

    df = df[["order_date", "product", "category", "region", "quantity", "sales", "profit"]]
    df["order_date"] = df["order_date"].dt.date

    with engine.begin() as conn:
        conn.execute(text("TRUNCATE TABLE clean_sales RESTART IDENTITY"))
        df.to_sql("clean_sales", conn, if_exists="append", index=False)

    duration = int((time.time() - start) * 1000)
    removed = before - len(df)
    log_pipeline(
        "clean",
        "success",
        f"Cleaned {len(df)} rows, removed {removed}",
        len(df),
        duration,
    )
    print(f"[OK] clean: {len(df)} rows kept, {removed} removed ({duration}ms)")
    return len(df)


if __name__ == "__main__":
    clean_data()

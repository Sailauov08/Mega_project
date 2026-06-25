import time
from pathlib import Path
import sys

import pandas as pd
from sqlalchemy import text

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from config.settings import settings
from db.connection import engine, log_pipeline

REQUIRED_COLUMNS = [
    "order_date",
    "product",
    "category",
    "region",
    "quantity",
    "sales",
    "profit",
]


def load_raw_csv() -> int:
    start = time.time()
    csv_path = Path(settings.raw_data_path)

    if not csv_path.exists():
        msg = f"CSV not found: {csv_path}"
        log_pipeline("load_raw", "error", msg)
        raise FileNotFoundError(msg)

    df = pd.read_csv(csv_path)
    df.columns = df.columns.str.strip().str.lower()

    missing = set(REQUIRED_COLUMNS) - set(df.columns)
    if missing:
        msg = f"Missing columns: {missing}"
        log_pipeline("load_raw", "error", msg)
        raise ValueError(msg)

    df = df[REQUIRED_COLUMNS]

    with engine.begin() as conn:
        conn.execute(text("TRUNCATE TABLE raw_sales RESTART IDENTITY"))
        df.to_sql("raw_sales", conn, if_exists="append", index=False)

    duration = int((time.time() - start) * 1000)
    log_pipeline("load_raw", "success", f"Loaded {len(df)} rows", len(df), duration)
    print(f"[OK] load_raw: {len(df)} rows ({duration}ms)")
    return len(df)


if __name__ == "__main__":
    load_raw_csv()

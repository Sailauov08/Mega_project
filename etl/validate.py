import time
from pathlib import Path
import sys

import pandas as pd
from sqlalchemy import text

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from db.connection import engine, log_pipeline


def validate_data() -> bool:
    start = time.time()
    errors = []
    warnings = []

    with engine.connect() as conn:
        df = pd.read_sql("SELECT * FROM clean_sales", conn)

    if df.empty:
        errors.append("clean_sales is empty")

    if not df.empty:
        if (df["quantity"] <= 0).any():
            errors.append("Found quantity <= 0")

        if (df["sales"] < 0).any():
            errors.append("Found negative sales")

        if df.duplicated().any():
            warnings.append(f"Found {df.duplicated().sum()} duplicates")

        null_count = int(df.isnull().sum().sum())
        if null_count > 0:
            warnings.append(f"Found {null_count} null values")

        date_range = (df["order_date"].max() - df["order_date"].min()).days
        if date_range < 30:
            warnings.append(f"Date range only {date_range} days")

    duration = int((time.time() - start) * 1000)

    if errors:
        log_pipeline("validate", "error", "; ".join(errors), len(df), duration)
        print(f"[ERROR] validate failed: {errors}")
        return False

    status = "warning" if warnings else "success"
    message = "; ".join(warnings) if warnings else f"Validated {len(df)} rows OK"
    log_pipeline("validate", status, message, len(df), duration)
    print(f"[OK] validate: {message} ({duration}ms)")
    return True


if __name__ == "__main__":
    validate_data()

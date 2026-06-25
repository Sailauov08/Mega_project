"""
Толық ETL pipeline:
python etl/run_etl.py
"""

import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from db.connection import log_pipeline
from etl.build_metrics import build_daily_metrics
from etl.clean import clean_data
from etl.load_raw import load_raw_csv
from etl.validate import validate_data


def run_etl() -> bool:
    start = time.time()
    print("=" * 50)
    print("ETL Pipeline Started")
    print("=" * 50)

    try:
        load_raw_csv()
        clean_data()

        if not validate_data():
            log_pipeline("run_etl", "error", "Validation failed")
            return False

        build_daily_metrics()

        duration = int((time.time() - start) * 1000)
        log_pipeline("run_etl", "success", "ETL completed", duration_ms=duration)
        print("=" * 50)
        print(f"[OK] ETL completed in {duration}ms")
        print("=" * 50)
        return True

    except Exception as e:
        duration = int((time.time() - start) * 1000)
        log_pipeline("run_etl", "error", str(e), duration_ms=duration)
        print(f"[ERROR] ETL failed: {e}")
        return False


if __name__ == "__main__":
    success = run_etl()
    sys.exit(0 if success else 1)

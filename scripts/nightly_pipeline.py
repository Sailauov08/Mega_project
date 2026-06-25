"""
Түнгі pipeline (03:00):
python scripts/nightly_pipeline.py
"""

import sys
import time
import traceback
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from api.services import check_database, compute_metrics
from bot.telegram_notifier import send_error, send_success, send_warning
from db.connection import log_pipeline
from etl.run_etl import run_etl
from ml.run_ml import run_ml

MAE_WARNING_THRESHOLD = 5000


def run_nightly_pipeline() -> bool:
    start = time.time()
    started_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print("=" * 50)
    print(f"Nightly Pipeline Started: {started_at}")
    print("=" * 50)

    try:
        if not check_database():
            raise RuntimeError("Database connection failed")

        if not run_etl():
            raise RuntimeError("ETL pipeline failed")

        if not run_ml():
            raise RuntimeError("ML pipeline failed")

        metrics = compute_metrics()
        duration_sec = round(time.time() - start, 1)

        message = (
            f"<b>Nightly run OK</b>\n"
            f"Time: {started_at}\n"
            f"Duration: {duration_sec}s\n"
            f"MAE: {metrics['mae']:.2f}\n"
            f"RMSE: {metrics['rmse']:.2f}\n"
            f"Model: {metrics['model_version']}"
        )

        if metrics["mae"] > MAE_WARNING_THRESHOLD:
            send_warning(
                message + f"\n\nMAE is high (>{MAE_WARNING_THRESHOLD}). Consider retraining."
            )
        else:
            send_success(message)

        log_pipeline("nightly", "success", f"Completed in {duration_sec}s", duration_ms=duration_sec * 1000)
        print(f"[OK] Nightly pipeline completed in {duration_sec}s")
        return True

    except Exception as e:
        duration_sec = round(time.time() - start, 1)
        error_text = traceback.format_exc()
        log_pipeline("nightly", "error", str(e), duration_ms=duration_sec * 1000)

        send_error(
            f"<b>Nightly run FAILED</b>\n"
            f"Time: {started_at}\n"
            f"Error: {e}\n\n"
            f"<pre>{error_text[-500:]}</pre>"
        )
        print(f"[ERROR] Nightly pipeline failed: {e}")
        return False


if __name__ == "__main__":
    success = run_nightly_pipeline()
    sys.exit(0 if success else 1)

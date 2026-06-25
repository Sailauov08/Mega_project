"""
Толық ML pipeline:
python ml/run_ml.py
"""

import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from db.connection import log_pipeline
from ml.evaluate import evaluate_model
from ml.predict import save_predictions
from ml.train import train_model


def run_ml() -> bool:
    start = time.time()
    print("=" * 50)
    print("ML Pipeline Started")
    print("=" * 50)

    try:
        train_model()
        metrics = evaluate_model()
        rows = save_predictions()

        duration = int((time.time() - start) * 1000)
        log_pipeline(
            "run_ml",
            "success",
            f"ML completed. MAE={metrics['mae']:.2f}, RMSE={metrics['rmse']:.2f}",
            rows,
            duration,
        )
        print("=" * 50)
        print(f"[OK] ML completed in {duration}ms")
        print(f"  MAE:  {metrics['mae']:.2f}")
        print(f"  RMSE: {metrics['rmse']:.2f}")
        print("=" * 50)
        return True

    except Exception as e:
        duration = int((time.time() - start) * 1000)
        log_pipeline("run_ml", "error", str(e), duration_ms=duration)
        print(f"[ERROR] ML failed: {e}")
        return False


if __name__ == "__main__":
    success = run_ml()
    sys.exit(0 if success else 1)

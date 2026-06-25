"""
Model train:
python ml/train.py
"""

import time
from pathlib import Path
import sys

import joblib
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from db.connection import log_pipeline
from ml.features import (
    FEATURE_COLUMNS,
    MODEL_DIR,
    MODEL_PATH,
    MODEL_VERSION,
    TARGET_COLUMN,
    build_features,
    load_daily_metrics,
)


def train_model(test_size: float = 0.2, random_state: int = 42) -> dict:
    start = time.time()

    df = load_daily_metrics()
    if len(df) < 30:
        raise ValueError(f"Need at least 30 days of data, got {len(df)}")

    data = build_features(df)
    X = data[FEATURE_COLUMNS]
    y = data[TARGET_COLUMN]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, shuffle=False, random_state=random_state
    )

    model = RandomForestRegressor(
        n_estimators=100,
        max_depth=10,
        random_state=random_state,
        n_jobs=-1,
    )
    model.fit(X_train, y_train)

    MODEL_DIR.mkdir(parents=True, exist_ok=True)
    artifact = {
        "model": model,
        "feature_columns": FEATURE_COLUMNS,
        "target_column": TARGET_COLUMN,
        "model_version": MODEL_VERSION,
        "train_rows": len(X_train),
        "test_rows": len(X_test),
    }
    joblib.dump(artifact, MODEL_PATH)

    duration = int((time.time() - start) * 1000)
    message = f"Trained on {len(X_train)} rows, test {len(X_test)} rows"
    log_pipeline("train", "success", message, len(X_train), duration)

    print(f"[OK] train: {message} ({duration}ms)")
    print(f"[OK] model saved -> {MODEL_PATH}")
    return artifact


if __name__ == "__main__":
    train_model()

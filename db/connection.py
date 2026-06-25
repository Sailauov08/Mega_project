from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

from config.settings import settings

engine = create_engine(settings.database_url, echo=False, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine)


def get_connection():
    return engine.connect()


def execute_sql_file(filepath: str) -> None:
    with open(filepath, "r", encoding="utf-8") as f:
        sql = f.read()

    with engine.begin() as conn:
        conn.execute(text(sql))

    print(f"[OK] SQL file executed: {filepath}")


def log_pipeline(
    step: str,
    status: str,
    message: str,
    rows_count: int | None = None,
    duration_ms: int | None = None,
) -> None:
    with engine.begin() as conn:
        conn.execute(
            text("""
                INSERT INTO pipeline_logs (step, status, message, rows_count, duration_ms)
                VALUES (:step, :status, :message, :rows_count, :duration_ms)
            """),
            {
                "step": step,
                "status": status,
                "message": message,
                "rows_count": rows_count,
                "duration_ms": duration_ms,
            },
        )

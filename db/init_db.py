"""
DB инициализация:
python db/init_db.py
"""

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from sqlalchemy import text

from db.connection import execute_sql_file, get_connection, log_pipeline


def init_database() -> None:
    schema_path = Path(__file__).parent / "schema.sql"
    execute_sql_file(str(schema_path))

    with get_connection() as conn:
        tables = conn.execute(
            text("""
                SELECT table_name
                FROM information_schema.tables
                WHERE table_schema = 'public'
                ORDER BY table_name
            """)
        ).fetchall()

    print("\n[INFO] Created tables:")
    for (name,) in tables:
        print(f"  - {name}")

    log_pipeline("init_db", "success", f"Database initialized. Tables: {len(tables)}")
    print("\n[OK] Database ready!")


if __name__ == "__main__":
    init_database()

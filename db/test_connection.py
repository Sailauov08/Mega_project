"""
DB connection test:
python db/test_connection.py
"""

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import psycopg2

from config.settings import settings


def test_connection() -> None:
    print("Testing PostgreSQL connection...")
    print(f"  host: {settings.db_host}")
    print(f"  port: {settings.db_port}")
    print(f"  db:   {settings.db_name}")
    print(f"  user: {settings.db_user}")

    try:
        conn = psycopg2.connect(
            host=settings.db_host,
            port=settings.db_port,
            dbname=settings.db_name,
            user=settings.db_user,
            password=settings.db_password,
            connect_timeout=5,
        )
        conn.close()
        print("\n[OK] Connection successful!")
        return

    except UnicodeDecodeError:
        pwd_len = len(settings.db_password)
        print(
            "\n[ERROR] Connection failed (Windows hides the real error).\n"
            f"Loaded password length: {pwd_len} characters.\n"
            "If you see 18 -> .env is NOT saved (still your_password_here).\n"
            "Fix: Ctrl+S on .env, then run again."
        )
        sys.exit(1)

    except psycopg2.OperationalError as e:
        print(f"\n[ERROR] {e}")
        sys.exit(1)


if __name__ == "__main__":
    test_connection()

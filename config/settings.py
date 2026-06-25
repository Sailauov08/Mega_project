from pathlib import Path
from urllib.parse import quote_plus

from pydantic import field_validator
from pydantic_settings import BaseSettings

BASE_DIR = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    db_host: str = "localhost"
    db_port: int = 5432
    db_name: str = "sales_db"
    db_user: str = "postgres"
    db_password: str = "your_password_here"
    raw_data_path: str = "data/raw/sales.csv"
    api_key: str = ""
    api_host: str = "127.0.0.1"
    api_port: int = 8000
    telegram_bot_token: str = ""
    telegram_chat_id: str = ""

    @field_validator(
        "db_password", "db_user", "db_host", "db_name", "raw_data_path",
        "api_key", "telegram_bot_token", "telegram_chat_id",
    )
    @classmethod
    def strip_strings(cls, value: str) -> str:
        return value.strip()

    class Config:
        env_file = BASE_DIR / ".env"
        env_file_encoding = "utf-8"

    @property
    def database_url(self) -> str:
        user = quote_plus(self.db_user)
        password = quote_plus(self.db_password)
        return (
            f"postgresql+psycopg2://{user}:{password}"
            f"@{self.db_host}:{self.db_port}/{self.db_name}"
        )


settings = Settings()

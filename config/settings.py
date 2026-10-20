import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class Settings:
    base_url: str = os.getenv("BASE_URL", "")
    timeout: int = int(os.getenv("API_TIMEOUT", "10"))
    token: str = os.getenv("TOKEN", "")
    username: str = os.getenv("USER_NAME")
    password: str = os.getenv("PASSWORD")
    db_host: str = os.getenv("DB_HOST", "")
    db_port: int = int(os.getenv("DB_PORT", ""))
    db_user: str = os.getenv("DB_USER", "")
    db_password: str = os.getenv("DB_PASSWORD", "")
    db_name: str = os.getenv("DB_NAME", "")


settings = Settings()

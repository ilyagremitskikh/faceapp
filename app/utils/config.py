from dataclasses import dataclass
from os import environ
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv


@dataclass
class DBConfig:
    db_host: Optional[str]
    db_user: Optional[str]
    db_pass: Optional[str]
    db_database: Optional[str]


@dataclass
class ApiConfig:
    secret_api_key: Optional[str]


@dataclass
class Config:
    db: DBConfig
    api: ApiConfig


def load_config():
    load_dotenv(Path.cwd() / ".env")
    config = Config(
        db=DBConfig(
            db_host=environ.get("DB_HOST"),
            db_user=environ.get("DB_USER"),
            db_pass=environ.get("DB_PASS"),
            db_database=environ.get("DB_DATABASE"),
        ),
        api=ApiConfig(secret_api_key=environ.get("API_SECRET_KEY")),
    )
    return config

import logging
from typing import Optional

from domain.core.utils import get_env_path
from pydantic import BaseSettings


class Settings(BaseSettings):
    app_port: str
    token_algorithm: str
    access_token_expire_minutes: str
    refresh_token_expire_minutes: str
    postgres_db: str
    postgres_user: str
    postgres_password: str
    postgres_host: str
    postgres_port: str
    redis_host: str
    redis_port: str
    ALGORITHM: str
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: float
    REFRESH_TOKEN_EXPIRE_MINUTES: float
    DATABASE_PORT_INT: int
    cors_data: str

    log_file: Optional[str] = 'app.log'
    log_level: Optional[int] = logging.INFO

    class Config:
        env_file = get_env_path()
        env_file_encoding = 'utf-8'


config = Settings()

logging.basicConfig(filename=config.log_file,
                    level=config.log_level,
                    format="%(asctime)s %(levelname)s %(message)s")

logger = logging.getLogger(__name__)

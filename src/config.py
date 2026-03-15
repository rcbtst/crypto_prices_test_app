from typing import Literal

from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy import URL


class EnvSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_nested_delimiter="__",
        extra="ignore",
        nested_model_default_partial_update=True,
    )

    LOG_LEVEL: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = "INFO"

    DB_HOST: str
    DB_PORT: int
    DB_NAME: str
    DB_USERNAME: str
    DB_PASSWORD: SecretStr
    DB_DRIVER: str = "postgresql+asyncpg"

    CELERY_BROKER_URL: str
    CELERY_RESULT_BACKEND: str
    CELERY_TICKER_WORKER_EXTRA_CONFIG: dict[str, object] = Field(default_factory=dict)

    APP_TICKER_UPDATE_TASK_SCHEDULE_INTERVAL: int = Field(default=60, gt=0)
    APP_TICKERS_TO_UPDATE: tuple[str, ...] = ("btc_usd", "eth_usd")

    def build_db_url(self) -> URL:
        return URL.create(
            drivername=self.DB_DRIVER,
            username=self.DB_USERNAME,
            password=self.DB_PASSWORD.get_secret_value(),
            host=self.DB_HOST,
            port=self.DB_PORT,
            database=self.DB_NAME,
        )


settings = EnvSettings()

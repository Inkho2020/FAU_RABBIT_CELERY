import logging
from pathlib import Path
from typing import Literal

from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
)
from pydantic import BaseModel

BASE_DIR = Path(__file__).resolve().parent.parent
LOG_DEFAULT_FORMAT = (
    "[%(asctime)s.%(msecs)03d] %(module)10s:%(lineno)-3d %(levelname)-7s - %(message)s"
)


class ApiPrefix(BaseModel):
    prefix: str = "/api"
    v1: str = "/v1"
    auth: str = "/auth"

    @property
    def bearer_token_url(self):
        parts = (self.v1, self.auth, "/login")
        path = "".join(parts)
        return path[1:]


class DatabaseConf(BaseModel):
    url: str
    echo: bool
    max_overflow: int
    pool_size: int


class AccessToken(BaseModel):
    lifetime: int
    reset_password_token: str
    verification_token: str


class LoggingConfig(BaseModel):
    log_level: Literal[
        "debug",
        "info",
        "warning",
        "error",
        "critical",
    ] = "info"
    log_format: str = LOG_DEFAULT_FORMAT

    @property
    def log_level_value(self) -> int:
        return logging.getLevelNamesMapping()[self.log_level.upper()]


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(BASE_DIR / ".env"),
        case_sensitive=False,
        env_nested_delimiter="__",
        env_prefix="APP__",
    )

    db: DatabaseConf
    access_token: AccessToken
    api: ApiPrefix
    logging: LoggingConfig = LoggingConfig()


settings = Settings()
UserIDType = int

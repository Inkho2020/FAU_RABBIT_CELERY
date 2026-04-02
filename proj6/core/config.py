from pathlib import Path

from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
)
from pydantic import BaseModel

BASE_DIR = Path(__file__).resolve().parent.parent


class ApiPrefix(BaseModel):
    prefix: str = "/api"

    @property
    def bearer_token_url(self):
        parts = (self.prefix, "/login")
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


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(BASE_DIR / ".env"),
        case_sensitive=False,
        env_nested_delimiter="__",
        env_prefix="APP__",
    )

    db: DatabaseConf
    access_token: AccessToken


settings = Settings()
UserIDType = int

from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
)
from pydantic import BaseModel


class DatabaseConf(BaseModel):
    url: str
    echo: bool
    max_overflow: int
    pool_size: int


class Setting(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(),
        case_sensitive=False,
        env_nested_delimiter="__",
        env_prefix="APP__",
    )

    db: DatabaseConf


settings = Setting()

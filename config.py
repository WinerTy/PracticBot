from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import PostgresDsn, BaseModel


class DataBaseConfig(BaseModel):
    url: PostgresDsn
    echo: bool = False
    echo_pool: bool = False
    max_overflow: int = 10
    pool_size: int = 50


class BotConfig(BaseModel):
    token: str


class AppConfig(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        env_nested_delimiter="__",
        env_prefix="APP_CONFIG__",
    )
    bot: BotConfig
    db: DataBaseConfig


config: AppConfig = AppConfig()

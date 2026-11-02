from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    app_name: str = "issuescope"
    environment: str = "local"  # local | ci | production

    # LLM
    openai_api_key: str = "sk-placeholder"
    openai_model: str = "gpt-4o-mini"
    fallback_model: str = "gpt-3.5-turbo"

    # Cost per 1 000 tokens (USD)
    primary_cost_per_1k_input: float = 0.000150
    primary_cost_per_1k_output: float = 0.000600
    fallback_cost_per_1k_input: float = 0.000050
    fallback_cost_per_1k_output: float = 0.000150

    # Postgres (Week 3+)
    database_url: str = "postgresql+asyncpg://issuescope:issuescope@db:5432/issuescope"


@lru_cache
def get_settings() -> Settings:
    return Settings()

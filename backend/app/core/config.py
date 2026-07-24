from functools import lru_cache

from pydantic import Field, PostgresDsn, RedisDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # Application
    app_name: str = "AI Incident Investigator"
    environment: str = "development"
    debug: bool = False
    api_v1_prefix: str = "/api/v1"

    # Security / JWT
    secret_key: str = Field(default="change-me-in-production", min_length=8)
    access_token_expire_minutes: int = 60
    algorithm: str = "HS256"

    # Database
    database_url: PostgresDsn = Field(
        default="postgresql+asyncpg://postgres:postgres@localhost:5432/incident_investigator"
    )
    db_echo: bool = False

    # Redis
    redis_url: RedisDsn = Field(default="redis://localhost:6379/0")

    # OpenSearch / Elasticsearch
    opensearch_url: str = "http://localhost:9200"
    opensearch_log_index: str = "log-entries"

    # LLM (Ollama)
    ollama_base_url: str = "http://localhost:11434"
    ollama_model: str = "llama3"
    ollama_timeout_seconds: int = 120

    # CORS
    cors_origins: list[str] = ["http://localhost:5173", "http://localhost:3000"]

    # Log grouping / correlation
    correlation_window_minutes: int = 15
    grouping_similarity_threshold: float = 0.75


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()

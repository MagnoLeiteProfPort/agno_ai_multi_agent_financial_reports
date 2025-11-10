# core/config.py
"""
Configuration Module

Purpose:
- Centralizes application settings and environment configuration.
- Uses Pydantic for type validation, default management, and .env integration.
- Provides a cached access pattern to ensure consistent configuration across modules.

Usage:
- Import and call `get_settings()` to retrieve an initialized and cached Settings instance.
- Environment variables (e.g., API keys, DB URLs) can be managed through a `.env` file.

Example:
    from core.config import get_settings
    settings = get_settings()
    print(settings.OPENAI_API_KEY)
"""

from functools import lru_cache
from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Application configuration model.

    Attributes:
        OPENAI_API_KEY (str): API key for accessing the language model.
        AGNO_DB_URL (str): Database connection URL (default: SQLite local memory DB).
        ENV (str): Current environment (e.g., "dev", "prod", "test").
        LOG_LEVEL (str): Logging level for the application.
        ALLOWED_WEB_DOMAINS (str): Whitelisted domains for external data access.
        MAX_INPUT_TOKENS (int): Token limit for user inputs.
        MAX_STEPS (int): Maximum reasoning or operation steps per agent.
        MAX_SECONDS (int): Execution time limit (seconds) for each process.
    """

    OPENAI_API_KEY: str = Field(default="", repr=False)
    AGNO_DB_URL: str = Field(default="sqlite:///./agno_memory.db")
    ENV: str = "dev"
    LOG_LEVEL: str = "DEBUG"
    ALLOWED_WEB_DOMAINS: str = (
        "wsj.com,ft.com,reuters.com,bcb.gov.br,sec.gov,investing.com"
    )
    MAX_INPUT_TOKENS: int = 1800
    MAX_STEPS: int = 8
    MAX_SECONDS: int = 45

    class Config:
        """Configuration for environment variable loading and validation."""
        env_file = ".env"
        case_sensitive = True


@lru_cache
def get_settings() -> Settings:
    """
    Retrieve a cached instance of the application settings.

    Returns:
        Settings: A singleton configuration object initialized from environment variables.
    """
    return Settings()

"""Application settings loaded from environment variables."""

from __future__ import annotations

from pathlib import Path

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Configuration for the AI QA Agent."""

    model_config = SettingsConfigDict(
        env_prefix="AI_QA_",
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # LLM provider configuration
    client: str = Field(
        default="placeholder", description="LLM backend: openai, anthropic, or placeholder"
    )
    openai_base_url: str | None = Field(default=None, alias="OPENAI_BASE_URL")
    openai_api_key: str | None = Field(default=None, alias="OPENAI_API_KEY")
    openai_model: str = Field(default="gpt-4o-mini", alias="OPENAI_MODEL")
    anthropic_api_key: str | None = Field(default=None, alias="ANTHROPIC_API_KEY")
    anthropic_model: str = Field(default="claude-3-5-sonnet-20241022", alias="ANTHROPIC_MODEL")

    # Pipeline configuration
    target_module: Path = Field(
        default=Path(__file__).resolve().parent.parent / "code" / "majorization.py"
    )
    generated_tests_dir: Path = Field(default=Path(__file__).resolve().parent / "generated_tests")
    report_path: Path = Field(default=Path(__file__).resolve().parent / "report.md")
    num_workers: int = Field(default=1, ge=1)
    max_retries: int = Field(default=3, ge=0)
    retry_backoff: float = Field(default=1.0, ge=0.0)

    # Logging
    log_level: str = Field(default="INFO")
    json_logs: bool = Field(default=False)

    @field_validator("client")
    @classmethod
    def validate_client(cls, v: str) -> str:
        allowed = {"openai", "anthropic", "placeholder"}
        if v not in allowed:
            raise ValueError(f"client must be one of {allowed}")
        return v

    @field_validator("log_level")
    @classmethod
    def validate_log_level(cls, v: str) -> str:
        allowed = {"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"}
        upper = v.upper()
        if upper not in allowed:
            raise ValueError(f"log_level must be one of {allowed}")
        return upper

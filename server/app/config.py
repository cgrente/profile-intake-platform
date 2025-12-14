"""
Application configuration for the Profile Intake API.

This module defines all runtime configuration using Pydantic settings,
which automatically map environment variables to strongly-typed fields.

Using BaseSettings allows:
- environment-based configuration
- sensible defaults for local development
- centralized configuration management
"""

from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """
    Strongly-typed application settings.

    All fields can be overridden via environment variables.
    Field names are automatically converted to uppercase
    (e.g. `API_TOKEN`, `DATABASE_URL`, etc.).

    Defaults are chosen to support local development while
    remaining production-safe when overridden.
    """

    # API authentication token used for Bearer auth
    api_token: str

    # Database connection URL.
    # Defaults to a local SQLite database for simplicity.
    database_url: str = "sqlite:///./data.db"

    # Directory where uploaded files are stored.
    # This path should be writable by the application container/process.
    upload_dir: str = "./uploads"

    # Allowed file extensions for uploads.
    # Validation is enforced server-side.
    allowed_file_types: list[str] = ["pdf"]

    # Maximum allowed file size (in megabytes).
    # Requests exceeding this limit should be rejected.
    max_file_size_mb: int = 10

    # Enable or disable CORS support.
    # Useful for local development and browser-based clients.
    enable_cors: bool = True

    # List of allowed CORS origins.
    # Default is permissive for development; should be restricted in production.
    cors_origins: list[str] = ["*"]

    # Application log level.
    # Typical values: debug, info, warning, error, critical
    log_level: str = "info"


# Instantiate settings at import time so configuration
# is loaded once and shared across the application.
settings = Settings()

"""
Authentication utilities for the Profile Intake API.

This module provides request-level authentication dependencies
used by FastAPI routes to enforce Bearer token access.
"""

from fastapi import Header, HTTPException

from .config import settings


def require_auth(authorization: str = Header(...)):
    """
    Enforce Bearer token authentication on protected endpoints.

    This dependency validates the `Authorization` header against
    the expected API token configured via environment variables.

    Design notes:
    - Authentication is kept intentionally simple (static Bearer token)
      to reduce operational complexity for this service.
    - The check is centralized here to ensure consistent behavior
      across all protected routes.
    - This function is designed to be used as a FastAPI dependency
      (`Depends(require_auth)`).

    Args:
        authorization: Value of the HTTP Authorization header.

    Raises:
        HTTPException: 401 Unauthorized if the token is missing or invalid.
    """
    expected = f"Bearer {settings.api_token}"

    # Perform a strict comparison against the expected Bearer token.
    # Any mismatch results in an immediate authentication failure.
    if authorization != expected:
        raise HTTPException(status_code=401, detail="Unauthorized")

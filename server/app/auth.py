"""
Authentication utilities for the Profile Intake API.

This module provides request-level authentication dependencies
used by FastAPI routes to enforce Bearer token access.
"""

from __future__ import annotations

from fastapi import HTTPException, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from .config import settings

_bearer_scheme = HTTPBearer(auto_error=False)


def require_auth(
    credentials: HTTPAuthorizationCredentials | None = Security(_bearer_scheme),
) -> None:
    """
    Enforce Bearer token authentication on protected endpoints.

    - Uses FastAPI's Security() + HTTPBearer so OpenAPI/Swagger reflects auth correctly.
    - Returns 401 with a WWW-Authenticate header, which is standard for Bearer auth.
    """
    if credentials is None or credentials.scheme.lower() != "bearer":
        raise HTTPException(
            status_code=401,
            detail="Unauthorized",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if credentials.credentials != settings.api_token:
        raise HTTPException(
            status_code=401,
            detail="Unauthorized",
            headers={"WWW-Authenticate": "Bearer"},
        )

"""
Pytest fixtures for the Profile Intake API.

This module defines shared test fixtures responsible for:
- configuring an isolated test environment
- setting environment variables before app import
- providing a FastAPI test client
- supplying authenticated request headers

The fixtures are designed to keep tests deterministic,
fast, and independent of external state.
"""

import importlib
import os

import pytest
from fastapi.testclient import TestClient


@pytest.fixture(scope="session")
def test_env(tmp_path_factory: pytest.TempPathFactory):
    """
    Configure environment variables for the test session.

    This fixture:
    - creates a temporary directory for test artifacts
    - provisions a temporary SQLite database
    - sets a dedicated upload directory
    - injects environment variables BEFORE the application is imported

    Using a session-scoped fixture ensures:
    - consistent configuration across all tests
    - minimal filesystem setup overhead
    """
    tmp_dir = tmp_path_factory.mktemp("profile_intake_test")

    # Temporary database path for this test session
    db_path = tmp_dir / "test.db"

    # Temporary upload directory for file-related tests
    upload_dir = tmp_dir / "uploads"
    upload_dir.mkdir(parents=True, exist_ok=True)

    # Configure environment variables expected by the application
    os.environ["API_TOKEN"] = "test-token"
    os.environ["DATABASE_URL"] = f"sqlite:///{db_path}"
    os.environ["UPLOAD_DIR"] = str(upload_dir)

    return {
        "db_path": db_path,
        "upload_dir": upload_dir,
    }


@pytest.fixture()
def client(test_env):
    """
    Provide a FastAPI TestClient instance.

    The application modules are explicitly reloaded AFTER environment
    variables are set to ensure that Pydantic settings and database
    configuration are picked up correctly.

    This pattern avoids configuration leakage between test runs
    and mirrors how the app would start in a fresh process.
    """
    # Import modules explicitly so they can be reloaded
    import app.config
    import app.database
    import app.main

    # Reload modules to force re-evaluation of environment-based settings
    importlib.reload(app.config)
    importlib.reload(app.database)
    importlib.reload(app.main)

    # Import the FastAPI application instance after reload
    from app.main import app  # noqa: E402

    return TestClient(app)


@pytest.fixture()
def auth_headers():
    """
    Provide Authorization headers for authenticated requests.

    This fixture centralizes authentication configuration so
    individual tests do not need to duplicate header logic.
    """
    return {"Authorization": "Bearer test-token"}

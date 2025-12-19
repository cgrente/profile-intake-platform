"""
Pytest fixtures for the Profile Intake API.
"""

from __future__ import annotations

import importlib
from pathlib import Path

import pytest
from fastapi.testclient import TestClient


@pytest.fixture()
def test_env(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    """
    Function scope => every test gets its own temp dir + its own SQLite DB.
    """
    db_path = tmp_path / "test.db"

    upload_dir = tmp_path / "uploads"
    upload_dir.mkdir(parents=True, exist_ok=True)

    monkeypatch.setenv("API_TOKEN", "test-token")
    monkeypatch.setenv("DATABASE_URL", f"sqlite:///{db_path}")
    monkeypatch.setenv("UPLOAD_DIR", str(upload_dir))

    return {"db_path": db_path, "upload_dir": upload_dir}


@pytest.fixture()
def client(test_env):
    """
    Reload config/database/routes/main so routes re-import the fresh get_db + SessionLocal.
    """
    import app.config as app_config
    import app.database as app_database
    import app.main as app_main
    import app.models as app_models
    import app.routes as app_routes

    # Order matters: config -> database -> models -> routes -> main
    importlib.reload(app_config)
    importlib.reload(app_database)
    importlib.reload(app_models)
    importlib.reload(app_routes)
    importlib.reload(app_main)

    from app.main import app as fastapi_app  # noqa: E402

    return TestClient(fastapi_app)


@pytest.fixture()
def auth_headers():
    return {"Authorization": "Bearer test-token"}

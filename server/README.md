# Profile Intake Server

The **Profile Intake Server** is a FastAPI-based backend service that owns the full
profile submission and document intake workflow.

This service is intentionally designed to resemble a **real internal API service**:
it owns all business rules, state transitions, and persistence, while clients and
CLI tools remain thin and reusable.

---

## What This Service Does

- Authenticated REST APIs
- Profile creation
- PDF upload and validation
- Submission lifecycle management
- Asynchronous processing simulation
- Persistent storage via SQLAlchemy
- Full test coverage and CI support

This server exists to demonstrate **API ownership**, **workflow modeling**, and
**production-shaped backend architecture**.

---

## Tech Stack

- **Python 3.12**
- **FastAPI** – API framework
- **Uvicorn** – ASGI server
- **SQLAlchemy 2.x** – ORM
- **Pydantic v2** – validation & settings
- **SQLite** – local persistence (swappable)
- **Pytest** – testing
- **Ruff** – linting & formatting
- **Mypy** – static typing
- **Docker** – containerization

---

## Project Structure

```
app/
├── auth.py        # Authentication dependency
├── config.py      # Environment-based configuration
├── database.py    # Database engine & session
├── models.py      # ORM models
├── schemas.py     # Request / response schemas
├── services.py    # Business logic
├── routes.py      # HTTP endpoints
├── processing.py  # Background processing
└── main.py        # Application entrypoint
```

All **business rules live in the server**.  
Clients and the CLI never encode workflow logic.

---

## API Overview

All endpoints are versioned under:

```
/api/v1
```

### Health Check

```
GET /healthz
```

Returns:

```json
{ "ok": true }
```

### Profiles

```
POST /api/v1/profiles
```

Creates a new profile entity.

### Submissions

```
POST /api/v1/submissions
POST /api/v1/submissions/{id}/submit
GET  /api/v1/submissions/{id}
```

Handles document upload and submission lifecycle transitions.

Full API documentation:
```
docs/api.md
```

---

## Authentication

All API endpoints (except `/healthz`) require a Bearer token:

```
Authorization: Bearer <API_TOKEN>
```

The token is configured via environment variables.

---

## Configuration

The server is configured **entirely via environment variables**.

Typical configuration:

```env
API_TOKEN=dev-token-change-me
DATABASE_URL=sqlite:///./data.db
UPLOAD_DIR=./uploads
```

A full example is provided in:

```
.env.example
```

> When running via Docker or `make`, the **root `.env` file is the single source of truth**.

---

## Running Locally

### Without Docker

```bash
cd server
pip install -e ".[dev]"
uvicorn app.main:app --reload
```

Server will be available at:

```
http://localhost:8000
```

### With Docker

```bash
docker build -t profile-intake-server .
docker run --env-file ../.env -p 8000:8000 profile-intake-server
```

---

## Testing

Run the full test suite:

```bash
pytest
```

Tests cover:

- Authentication enforcement
- Health endpoint
- PDF validation
- Full submission workflow
- Asynchronous processing behavior
- Database isolation per test

---

## Design Principles

- Explicit workflow modeling
- Server-owned business logic
- Environment-driven configuration
- Deterministic, isolated tests
- Minimal but realistic architecture
- No unnecessary infrastructure

---

## Notes

- Asynchronous processing is simulated using FastAPI background tasks
- SQLite is used for portability and ease of review
- The storage layer can be replaced with PostgreSQL with minimal changes
- Schema migrations are intentionally omitted to keep scope focused

---

## License

MIT License. See the repository root for details.

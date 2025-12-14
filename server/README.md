# Profile Intake Server

The **Profile Intake Server** is a FastAPI-based backend service that owns the full
profile submission and document intake workflow.

It provides:
- authenticated REST APIs
- profile creation
- PDF upload and validation
- submission lifecycle management
- asynchronous processing simulation
- persistent storage via SQLAlchemy
- full test coverage and CI support

This service is designed to demonstrate **API ownership**, **workflow modeling**,
and **production-shaped backend architecture**.

---

## Tech Stack

- **Python 3.12**
- **FastAPI** – API framework
- **Uvicorn** – ASGI server
- **SQLAlchemy 2.x** – ORM
- **Pydantic v2** – validation & settings
- **SQLite** – local persistence
- **Pytest** – testing
- **Docker** – containerization

---

## Architecture Overview

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

Business rules live in the server.  
Clients and CLI tools are intentionally thin.

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

Creates a new profile.

### Submissions

```
POST /api/v1/submissions
POST /api/v1/submissions/{id}/submit
GET  /api/v1/submissions/{id}
```

Manages document uploads and submission lifecycle.

Full endpoint documentation is available in:
```
docs/api.md
```

---

## Authentication

All API endpoints (except `/healthz`) require a Bearer token.

```
Authorization: Bearer <API_TOKEN>
```

The token is configured via environment variables.

---

## Configuration

The server is configured entirely via environment variables.

Example:

```bash
API_TOKEN=dev-token
DATABASE_URL=sqlite:///./data.db
UPLOAD_DIR=./uploads
```

A sample configuration is provided in `.env.example`.

---

## Running Locally

### Using Python

```bash
cd server
pip install -e ".[dev]"
uvicorn app.main:app --reload
```

### Using Docker

```bash
docker build -t profile-intake-server .
docker run -p 8000:8000 profile-intake-server
```

---

## Testing

Run the full test suite:

```bash
pytest
```

Tests include:
- authentication enforcement
- health endpoint
- file validation
- full submission workflow
- async processing behavior

---

## Design Principles

- Explicit workflow modeling
- Server-owned business logic
- Minimal client assumptions
- Environment-driven configuration
- Test-first development
- Production-shaped structure

---

## Notes

- Asynchronous processing is simulated using FastAPI background tasks
- SQLite is used for portability; can be replaced with PostgreSQL easily
- Schema migrations are intentionally omitted for simplicity

---

## License

MIT License. See the repository root for details.

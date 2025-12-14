# Profile Intake Platform

The **Profile Intake Platform** is a small, production-shaped monorepo that demonstrates
**API ownership**, **workflow modeling**, and **end‑to‑end backend development**.

It includes:
- a FastAPI backend that owns business logic and data
- a reusable Python client SDK
- a CLI built on top of the client
- full test coverage and CI
- Docker-based local development

This repository is intentionally scoped to remain clear, explicit, and easy to reason about.

---

## Repository Structure

```
profile-intake-platform/
├── client/                 # Python SDK + CLI
├── server/                 # FastAPI backend service
├── docs/                   # API & architecture documentation
├── .github/workflows/      # CI pipeline
├── docker-compose.yml      # Local orchestration
├── Makefile                # Common developer commands
├── .env.example            # Environment configuration template
├── CONTRIBUTING.md         # Contribution guidelines
├── SECURITY.md             # Security policy
└── README.md               # This file
```

---

## High-Level Architecture

```
CLI / Scripts
     │
     ▼
Client SDK (Python)
     │  HTTP
     ▼
FastAPI Server
     │
     ▼
SQLite Database + File Storage
```

- The **server** owns all business rules and state transitions
- The **client** is intentionally thin and reusable
- The **CLI** is a convenience layer on top of the client

More details:
- `docs/architecture.md`
- `docs/api.md`

---

## Features

- Bearer-token authenticated REST API
- Profile creation
- PDF upload and validation
- Submission lifecycle management
- Asynchronous processing simulation
- SQLite persistence (portable & simple)
- Dockerized development
- CI with linting, typing, and tests

---

## Quick Start (Docker)

### 1. Create environment file

```bash
cp .env.example .env
```

Edit `.env` and set at least:

```env
API_TOKEN=dev-token-change-me
```

### 2. Start the service

```bash
docker compose up --build
```

The API will be available at:

```
http://localhost:8000
```

Health check:

```bash
curl http://localhost:8000/healthz
```

---

## Local Development (without Docker)

### Install dependencies

```bash
make install
```

### Run the server

```bash
make dev
```

### Run tests

```bash
make test
```

---

## Client & CLI

The `client/` directory contains:
- a Python SDK (`IntakeClient`)
- a CLI tool (`intake`)

Example usage:

```bash
export INTAKE_API_TOKEN=dev-token-change-me
intake status <submission_id>
```

See:
- `client/README.md`

---

## Testing & Quality

This repository uses:

- **Pytest** for testing
- **Ruff** for linting & formatting
- **Mypy** for static typing
- **GitHub Actions** for CI

Run all checks locally:

```bash
make check
make test
```

---

## Design Principles

- Explicit over implicit
- Server-owned business logic
- Minimal but realistic architecture
- Clear separation of concerns
- Testability first
- Avoid unnecessary infrastructure

This project is intentionally designed to resemble a real internal service,
without introducing complexity that does not serve the core problem.

---

## Security

Please see `SECURITY.md` for vulnerability reporting guidelines.

---

## License

This project is licensed under the MIT License.
See the `LICENSE` file for details.

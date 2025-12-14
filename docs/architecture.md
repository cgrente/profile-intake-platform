# Profile Intake Platform – Architecture

This document describes the high-level architecture and design decisions
behind the **Profile Intake Platform**.

---

## Overview

The platform is designed as a small, self-contained backend system that
demonstrates real-world API ownership and workflow modeling.

It consists of:
- a FastAPI-based backend service
- a reusable Python client SDK
- a CLI built on top of the SDK
- a lightweight persistence layer
- Dockerized deployment

---

## High-Level Architecture

```
┌────────────┐
│   CLI /    │
│   Scripts  │
└─────┬──────┘
      │
      ▼
┌────────────┐
│ Intake SDK │
│ (client)   │
└─────┬──────┘
      │ HTTP
      ▼
┌────────────┐
│ FastAPI    │
│ Server     │
├────────────┤
│ Auth       │
│ Routes     │
│ Services   │
│ Models     │
└─────┬──────┘
      │
      ▼
┌────────────┐
│ SQLite DB  │
└────────────┘
```

---

## Server Responsibilities

The server owns all business rules:

- authentication and authorization
- profile creation
- document validation
- submission lifecycle enforcement
- asynchronous processing
- status transitions

The client and CLI do **not** implement business logic.

---

## Layered Design (Server)

```
app/
├── auth.py        # Authentication logic
├── config.py      # Environment-based configuration
├── database.py    # Database setup
├── models.py      # ORM models
├── schemas.py     # Request/response schemas
├── services.py    # Business logic
├── routes.py      # HTTP endpoints
├── processing.py  # Background processing
└── main.py        # Application entrypoint
```

This separation keeps the system testable, maintainable, and easy to extend.

---

## Submission Lifecycle

1. Profile is created
2. PDF document is uploaded (`UPLOADED`)
3. Submission is locked and processed (`PROCESSING`)
4. Processing completes (`COMPLETED`)

Invalid transitions (e.g. resubmission) are rejected.

---

## Asynchronous Processing

Processing is performed using FastAPI background tasks.
This simulates real asynchronous workflows without introducing
external infrastructure (e.g. message queues).

---

## Persistence

- SQLite is used for simplicity and portability
- ORM models are abstracted from business logic
- Swapping to PostgreSQL requires minimal changes

---

## Security Considerations

- Bearer-token authentication
- No secrets committed to the repository
- Environment-based configuration
- Upload validation enforced server-side

---

## Deployment

- Dockerized server
- Docker Compose for local orchestration
- CI pipeline runs linting, type checks, and tests

---

## Design Goals

- Clarity over cleverness
- Explicit workflow modeling
- Low operational complexity
- Easy local development
- Production-shaped architecture


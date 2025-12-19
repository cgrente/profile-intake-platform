# Profile Intake Client

A lightweight Python SDK and CLI for interacting with the **Profile Intake Platform API**.

This package provides:
- a reusable HTTP client (`IntakeClient`)
- a command-line interface (`intake`) for common workflows
- environment-based configuration (no hardcoded secrets)

The client is intentionally **thin by design**.  
All business rules, validation, and workflow state transitions are owned by the server.

---

## Features

- Bearer-token authentication
- Profile creation
- PDF document upload
- Submission lifecycle management
- Status retrieval
- Reusable SDK + thin CLI wrapper
- Minimal runtime dependencies

---

## Installation

From the repository root:

```bash
pip install -e client
```

For development (tests, linting, CLI tooling):

```bash
pip install -e "client[dev]"
```

---

## Configuration

The client is configured via environment variables.

### Required

```bash
export INTAKE_API_TOKEN=<your-api-token>
```

### Optional

```bash
export INTAKE_API_URL=http://localhost:8000/api/v1
```

If `INTAKE_API_URL` is not set, the client defaults to a local server.

When used inside the monorepo, the root `.env` file is the canonical source of configuration.

---

## SDK Usage

```python
from intake_client.client import IntakeClient

client = IntakeClient(
    base_url="http://localhost:8000/api/v1",
    token="your-api-token",
)

profile = client.create_profile({
    "first_name": "John",
    "last_name": "Smith",
    "email": "john.smith@test.com",
    "github_url": "github.com/johnsmith",
})

submission = client.upload_pdf(profile["id"], "./resume.pdf")

client.submit(submission["id"])

status = client.status(submission["id"])
print(status)
```

---

## CLI Usage

The CLI is exposed as the `intake` command.

### Create a profile

```bash
intake create-profile \
  --first-name John \
  --last-name Smith \
  --email john.smith@test.com \
  --github-url github.com/johnsmith
```

### Upload a PDF document

```bash
intake upload <profile_id> ./resume.pdf
```

### Submit a document for processing

```bash
intake submit <submission_id>
```

### Check submission status

```bash
intake status <submission_id>
```

All commands output structured JSON by default, making them suitable for scripting and automation.

---

## Development

### Run tests

```bash
pytest
```

### Lint and format

```bash
ruff check .
ruff format .
```

### Type checking

```bash
mypy .
```

---

## Design Notes

- The client contains **no business logic**
- All validation and workflow rules are enforced by the server
- The CLI is a thin wrapper around the SDK
- HTTP sessions are reused for efficiency
- Responses are returned as raw JSON for flexibility

---

## License

MIT License. See the repository root for details.

# Contributing

Thank you for your interest in contributing to the **Profile Intake Platform** 🎉  
Contributions are welcome and appreciated.

This document outlines the guidelines and expectations for contributing to this repository.

---

## Project Scope

This project is intentionally kept **small, explicit, and production-shaped**.  
The primary goals are:

- clear API ownership
- explicit workflow modeling
- clean separation of concerns
- strong test coverage
- minimal operational complexity

Please keep these goals in mind when proposing changes.

---

## Getting Started

### Prerequisites

- Python **3.12+**
- `pip`
- Docker (optional, but recommended)

### Setup

```bash
git clone https://github.com/<your-org-or-username>/profile-intake-platform.git
cd profile-intake-platform

pip install -e "server[dev]"
pip install -e "client[dev]"
```

Run the test suite to ensure everything works:

```bash
pytest
```

---

## Development Guidelines

### Code Style

This project uses automated tooling to enforce style and consistency:

- **Ruff** for linting and formatting
- **Mypy** for static typing
- **Pytest** for testing

Before submitting a change, please run:

```bash
ruff format .
ruff check .
mypy .
pytest
```

CI will enforce these checks on pull requests.

---

### Testing

All new features or bug fixes **must include tests**.

Tests should be:
- deterministic
- isolated
- readable
- focused on behavior, not implementation details

Avoid introducing flaky or timing-sensitive tests unless strictly necessary.

---

## Pull Requests

When opening a pull request, please ensure:

- the change has a clear purpose
- tests pass locally
- new behavior is covered by tests
- existing behavior is not broken
- documentation is updated if needed

A good pull request includes:
- a concise description of the change
- reasoning behind design decisions
- any relevant tradeoffs or limitations

---

## What Not to Add

To keep the project focused, please avoid:

- adding unnecessary abstractions
- introducing heavy infrastructure (queues, caches, auth providers)
- adding features without a clear use case
- refactoring purely for stylistic reasons

If in doubt, open an issue first to discuss.

---

## Security

If you discover a security issue, **do not open a public issue**.

Please report it privately by contacting the repository maintainer.

---

## License

By contributing, you agree that your contributions will be licensed under the same license as this project.

---

## Final Note

This project is maintained with clarity and simplicity in mind.  
Thoughtful, well-scoped contributions are always welcome.

Thank you for taking the time to contribute 🚀

# Monorepo Makefile (server + client)
# Usage:
#   make help
#   make dev
#   make test
#   make docker-up

SHELL := /bin/bash
.DEFAULT_GOAL := help

PYTHON ?= python3
PIP ?= pip

SERVER_DIR := server
CLIENT_DIR := client

.PHONY: help
help: ## Show available commands
	@awk 'BEGIN {FS = ":.*##"; printf "\nAvailable targets:\n\n"} /^[a-zA-Z0-9_.-]+:.*##/ {printf "  \033[36m%-22s\033[0m %s\n", $$1, $$2} END {printf "\n"}' $(MAKEFILE_LIST)

# -------------------------------------------------------------------
# Setup
# -------------------------------------------------------------------
.PHONY: install
install: ## Install server+client (dev deps)
	$(PIP) install -e "$(SERVER_DIR)[dev]"
	$(PIP) install -e "$(CLIENT_DIR)[dev]"

.PHONY: install-server
install-server: ## Install server only (dev deps)
	$(PIP) install -e "$(SERVER_DIR)[dev]"

.PHONY: install-client
install-client: ## Install client only (dev deps)
	$(PIP) install -e "$(CLIENT_DIR)[dev]"

# -------------------------------------------------------------------
# Formatting / linting / typing
# -------------------------------------------------------------------
.PHONY: format
format: ## Format code with ruff (server+client)
	cd $(SERVER_DIR) && ruff format .
	cd $(CLIENT_DIR) && ruff format .

.PHONY: lint
lint: ## Lint code with ruff (server+client)
	cd $(SERVER_DIR) && ruff check .
	cd $(CLIENT_DIR) && ruff check .

.PHONY: typecheck
typecheck: ## Type-check with mypy (server+client)
	cd $(SERVER_DIR) && mypy .
	cd $(CLIENT_DIR) && mypy .

.PHONY: check
check: format lint typecheck ## Run format + lint + typecheck

# -------------------------------------------------------------------
# Tests
# -------------------------------------------------------------------
.PHONY: test
test: ## Run all tests (server+client)
	cd $(SERVER_DIR) && pytest
	cd $(CLIENT_DIR) && pytest

.PHONY: test-server
test-server: ## Run server tests only
	cd $(SERVER_DIR) && pytest

.PHONY: test-client
test-client: ## Run client tests only
	cd $(CLIENT_DIR) && pytest

# -------------------------------------------------------------------
# Run locally
# -------------------------------------------------------------------
.PHONY: dev
dev: ## Run server locally with reload (requires local env vars)
	cd $(SERVER_DIR) && uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# -------------------------------------------------------------------
# Docker / Compose
# -------------------------------------------------------------------
.PHONY: docker-build
docker-build: ## Build server Docker image
	docker build -t profile-intake-server ./$(SERVER_DIR)

.PHONY: docker-run
docker-run: ## Run server Docker image (port 8000)
	docker run --rm -p 8000:8000 profile-intake-server

.PHONY: docker-up
docker-up: ## Start services with docker compose
	docker compose up --build

.PHONY: docker-up-d
docker-up-d: ## Start services with docker compose (detached)
	docker compose up --build -d

.PHONY: docker-down
docker-down: ## Stop services
	docker compose down

.PHONY: docker-logs
docker-logs: ## Tail compose logs
	docker compose logs -f

# -------------------------------------------------------------------
# Cleanup
# -------------------------------------------------------------------
.PHONY: clean
clean: ## Remove caches and local artifacts
	rm -rf $(SERVER_DIR)/.pytest_cache $(SERVER_DIR)/.mypy_cache $(SERVER_DIR)/.ruff_cache
	rm -rf $(CLIENT_DIR)/.pytest_cache $(CLIENT_DIR)/.mypy_cache $(CLIENT_DIR)/.ruff_cache
	find . -type d -name "__pycache__" -prune -exec rm -rf {} \; 2>/dev/null || true

.PHONY: reset-data
reset-data: ## Remove local server data (SQLite DB + uploads if mounted locally)
	rm -rf $(SERVER_DIR)/.data

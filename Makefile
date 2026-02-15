SHELL := /bin/bash

.PHONY: setup run test lint format clean docker-up docker-down

PY_BIN ?= python3.12

setup:
	@set -e; \
	if command -v python3.12 >/dev/null 2>&1; then PY=python3.12; \
	elif command -v python3.11 >/dev/null 2>&1; then PY=python3.11; \
	else PY=python3; fi; \
	echo "Using $$PY"; \
	cd backend && $$PY -m venv .venv; \
	cd backend && source .venv/bin/activate && pip install --upgrade pip setuptools wheel && pip install -r requirements.txt; \
	echo "Done. Activate with: source backend/.venv/bin/activate"

run:
	@cd backend && source .venv/bin/activate && uvicorn app.main:app --reload --port 8000

test:
	@cd backend && source .venv/bin/activate && pytest -q

lint:
	@cd backend && source .venv/bin/activate && ruff check .

format:
	@cd backend && source .venv/bin/activate && ruff format .

clean:
	@rm -rf backend/.venv backend/.pytest_cache backend/.ruff_cache

docker-up:
	@docker compose up --build

docker-down:
	@docker compose down

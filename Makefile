-include .env

APP_HOST ?= 0.0.0.0
APP_PORT ?= 8080

.PHONY: run debug test test-coverage lint lint-fix

run:
	npm run start

debug:
	uv run uvicorn main:app --reload --host $(APP_HOST) --port $(APP_PORT)

test:
	APP_ENV=test uv run pytest

test-coverage:
	APP_ENV=test uv run pytest --cov

test-doc:
	APP_ENV=test uv run python -i -c "from fastapi.testclient import TestClient; from main import app; client = TestClient(app)"

lint:
	uv run ruff check .

lint-fix:
	uv run ruff check . --fix

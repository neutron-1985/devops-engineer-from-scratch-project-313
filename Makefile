-include .env

APP_HOST ?= 0.0.0.0
APP_PORT ?= 8080

.PHONY: run debug test test-coverage lint lint-fix

run:
	uv run uvicorn main:app --host $(APP_HOST) --port $(APP_PORT)

debug:
	uv run uvicorn main:app --reload --host $(APP_HOST) --port $(APP_PORT)

test:
	uv run pytest

test-coverage:
	uv run pytest --cov

lint:
	uv run ruff check .

lint-fix:
	uv run ruff check . --fix

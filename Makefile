run:
	uv run flask --app main:app run --host 0.0.0.0 --port 8080

debug:
	uv run flask --app main:app run --debug --host 0.0.0.0 --port 8080

test:
	uv run pytest

test-coverage:
	uv run pytest $$(find . -path ./.venv -prune -o -type d -name tests -print) \
	$$(find . -path ./.venv -prune -o -type d -name src -print | sed 's/^/--cov=/') \
	--cov-report=term-missing

lint:
	uv run ruff check .

lint-fix:
	uv run ruff check . --fix



run:
	uv run flask --app main:app run --host 0.0.0.0 --port 8080

debug:
	uv run flask --app main:app run --debug --host 0.0.0.0 --port 8080
	
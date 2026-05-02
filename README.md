### Hexlet tests and linter status:
[![Actions Status](https://github.com/neutron-1985/devops-engineer-from-scratch-project-313/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/neutron-1985/devops-engineer-from-scratch-project-313/actions)

[![Code Quality](https://github.com/neutron-1985/devops-engineer-from-scratch-project-313/actions/workflows/ci.yml/badge.svg)](https://github.com/neutron-1985/devops-engineer-from-scratch-project-313/actions/workflows/ci.yml)

# DevOps Engineer From Scratch Project 313

This is a Hexlet educational FastAPI application for managing short links.
The application uses SQLModel with PostgreSQL, creates database tables on
startup, and provides CRUD endpoints for links.

## Deployed Application

The application is deployed on Render:

```text
https://devops-engineer-from-scratch-project-313-2p80.onrender.com/ping
```

## Requirements

- Python `3.14` or higher
- `uv`
- `make`
- PostgreSQL

## Installation

Clone the repository and install the dependencies:

```bash
git clone https://github.com/neutron-1985/devops-engineer-from-scratch-project-313.git
cd devops-engineer-from-scratch-project-313
uv sync
```

Create a local environment file:

```bash
cp .env.example .env
```

Configure the database connection in `.env`:

```text
DATABASE_URL=postgres://postgres:password@localhost:5432/appdb?sslmode=disable
SHORT_URL_BASE=https://short.io/r
```

## Usage

Run the application:

```bash
make run
```

Run the application in debug mode:

```bash
make debug
```

The application will be available at:

```text
http://localhost:8080
```

Database tables are created automatically when the application starts.

## Health Check

Check that the application is running:

```bash
curl http://localhost:8080/ping
```

Expected response:

```text
pong
```

## Links API

List all links:

```bash
curl http://localhost:8080/api/links
```

Create a link:

```bash
curl -X POST http://localhost:8080/api/links \
  -H 'Content-Type: application/json' \
  -d '{"original_url":"https://example.com/long-url","short_name":"exmpl"}'
```

Get a link by id:

```bash
curl http://localhost:8080/api/links/1
```

Update a link:

```bash
curl -X PUT http://localhost:8080/api/links/1 \
  -H 'Content-Type: application/json' \
  -d '{"original_url":"https://example.com/new-url","short_name":"new-name"}'
```

Delete a link:

```bash
curl -X DELETE http://localhost:8080/api/links/1
```

The `short_name` field must be unique. The `short_url` field is generated from
`SHORT_URL_BASE` and `short_name`.

## Tests

Run tests and lint checks:

```bash
uv run pytest
uv run ruff check .
```

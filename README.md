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
https://devops-engineer-from-scratch-project-313-2p80.onrender.com
```

## Requirements

- `Python 3.14` or higher
- `uv`
- `make`
- `Node.js` and `npm`
- `PostgreSQL`

## Installation

Clone the repository and install the dependencies:

```bash
git clone https://github.com/neutron-1985/devops-engineer-from-scratch-project-313.git
cd devops-engineer-from-scratch-project-313
uv sync
npm install
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

Run the backend and frontend in development mode:

```bash
make run
```

Run the application in debug mode:

```bash
make debug
```

The backend will be available at:

```text
http://localhost:8080
```

The frontend will be available at:

```text
http://localhost:5173
```

Build and run the production Docker image:

```bash
docker build -t devops-engineer-from-scratch-project-313 .
docker run --rm -p 8088:80 --env-file .env devops-engineer-from-scratch-project-313
```

The application will be available through Nginx at:

```text
http://localhost:8088
```

In production, Nginx listens on port `80`, serves the built frontend from
`/app/public`, and proxies `/api/` requests to the backend on port `8080`.

For Render deployment, set the application port:

```text
PORT=80
```

Database tables are created automatically when the application starts.

## Health Check

Check that the backend is running in development mode:

```bash
curl http://localhost:8080/ping
```

Expected response:

```text
pong
```

## Links API

In development, use `http://localhost:8080`. In Docker, use the Nginx port,
for example `http://localhost:8088`.

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

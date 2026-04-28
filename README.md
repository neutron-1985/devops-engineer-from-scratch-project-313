### Hexlet tests and linter status:
[![Actions Status](https://github.com/neutron-1985/devops-engineer-from-scratch-project-313/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/neutron-1985/devops-engineer-from-scratch-project-313/actions)

# DevOps Engineer From Scratch Project 313

This is a Hexlet educational project with a minimal Flask web application.
The application starts an HTTP server on port `8080` and provides a `/ping`

## Requirements

- Python `3.14` or higher
- `uv`
- `make`

## Installation

Clone the repository and install the dependencies:

```bash
git clone https://github.com/neutron-1985/devops-engineer-from-scratch-project-313.git
cd devops-engineer-from-scratch-project-313
uv sync
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

## Health Check

Check that the application is running:

```bash
curl http://localhost:8080/ping
```

Expected response:

```text
pong
```

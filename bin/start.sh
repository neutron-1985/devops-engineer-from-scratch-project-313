#!/usr/bin/env bash

set -e

uv run --no-sync uvicorn main:app --host 0.0.0.0 --port 8080 &

nginx -g "daemon off;"

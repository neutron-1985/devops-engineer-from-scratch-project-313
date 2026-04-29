#!/usr/bin/env bash

set -e

COMMAND="uv run --no-sync flask --app main:app run --host 0.0.0.0 --port 8080"

echo $COMMAND
eval $COMMAND

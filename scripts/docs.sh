#!/usr/bin/env bash

set -x

uv run mkdocs serve --dev-addr 127.0.0.1:8001

# mkdocs build
# pip-compile docs/requirements.in

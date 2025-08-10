#!/usr/bin/env bash

set -e
set -x

# Inline --asyncio-mode=auto argument for compatibility with GitHub Actions
uv run --extra dev coverage run -m pytest --asyncio-mode=auto tests
uv run --extra dev coverage combine
uv run --extra dev coverage report --show-missing
uv run --extra dev coverage html

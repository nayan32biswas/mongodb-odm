#!/usr/bin/env bash

set -e
set -x

uv run --extra dev coverage run -m pytest
uv run --extra dev coverage combine
uv run --extra dev coverage report --show-missing
uv run --extra dev coverage html

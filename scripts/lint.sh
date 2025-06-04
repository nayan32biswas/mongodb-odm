#!/usr/bin/env bash

set -e
set -x

uv run --extra dev mypy mongodb_odm
uv run --extra dev ruff check mongodb_odm tests docs_src scripts
uv run --extra dev ruff format mongodb_odm tests docs_src --check

#!/usr/bin/env bash

set -x

uv pip compile pyproject.toml --extra docs -o docs/requirements.txt
uv run --extra docs mkdocs build

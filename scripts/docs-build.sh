#!/usr/bin/env bash

set -x

uv run pip-compile docs/requirements.in
uv run mkdocs build

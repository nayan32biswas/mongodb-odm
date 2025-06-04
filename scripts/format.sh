#!/usr/bin/env bash

set -x

uv run --extra dev ruff check mongodb_odm tests docs_src scripts --fix
uv run --extra dev ruff format mongodb_odm tests docs_src scripts

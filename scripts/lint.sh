#!/usr/bin/env bash

set -e
set -x

mypy mongodb_odm
ruff mongodb_odm tests docs_src scripts
ruff format mongodb_odm tests docs_src --check

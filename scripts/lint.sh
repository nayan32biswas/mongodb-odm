#!/usr/bin/env bash

set -e
set -x

mypy mongodb_odm
flake8 mongodb_odm tests docs_src
black mongodb_odm tests docs_src --check
isort mongodb_odm tests docs_src scripts --check-only

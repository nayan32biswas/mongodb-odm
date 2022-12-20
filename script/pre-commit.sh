#!/usr/bin/env bash

set -x

# poetry run pre-commit install
poetry run pre-commit run --all-files

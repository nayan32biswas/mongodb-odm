#!/usr/bin/env bash

set -e
set -x

poetry run coverage run -m pytest tests
poetry run coverage combine
poetry run coverage report --show-missing

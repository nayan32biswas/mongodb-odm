#!/usr/bin/env bash

set -e

# poetry config pypi-token.pypi <your-api-token>
poetry publish --build --skip-existing

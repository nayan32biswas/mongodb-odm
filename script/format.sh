#!/usr/bin/env bash

set -x

poetry run autoflake --remove-all-unused-imports --recursive --remove-unused-variables --in-place mongodb_odm tests --exclude=__init__.py

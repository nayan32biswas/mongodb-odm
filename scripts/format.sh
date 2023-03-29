#!/usr/bin/env bash

set -x

autoflake --remove-all-unused-imports --recursive --remove-unused-variables --in-place mongodb_odm tests --exclude=__init__.py
black mongodb_odm tests docs_src
isort mongodb_odm tests docs_src

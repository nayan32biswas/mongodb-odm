#!/usr/bin/env bash

set -x

ruff check mongodb_odm tests docs_src scripts --fix
ruff format mongodb_odm tests docs_src scripts

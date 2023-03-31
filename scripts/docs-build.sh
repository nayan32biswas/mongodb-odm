#!/usr/bin/env bash

set -x

pip-compile docs/requirements.in
mkdocs build

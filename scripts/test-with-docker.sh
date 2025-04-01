#!/usr/bin/env bash

set -x

<<comment
docker run -d --rm --name mongo -p 27017:27017 mongo
uv run scripts/test.sh
docker stop mongo
comment

<<comment
# Up mongodb container
docker compose up -d mongodb && docker compose up mongo-init
export MONGO_URL="mongodb://localhost:27017/testdb"

# Run the test locally with uv
uv run scripts/test.sh
docker compose stop mongodb
comment

<<comment
# Run test for single file with docker
docker-compose -f docker-compose-local.yml run --rm app \
    uv run coverage run -m pytest tests/test__indexes.py
comment

# Run test for all files with docker
docker-compose -f docker-compose-local.yml run --rm app \
    ./scripts/test.sh

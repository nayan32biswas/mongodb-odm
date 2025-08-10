#!/usr/bin/env bash

set -x

<<comment
docker run -d --rm --name mongo -p 27017:27017 mongo
./scripts/test.sh
docker stop mongo
comment

<<comment
# Up mongodb container
docker compose up -d mongodb mongodb_follower && \
    docker compose up init-replica
export MONGO_URL="mongodb://localhost:27017/testdb?directConnection=true&replicaSet=rs0"

# Run the test locally with uv
./scripts/test.sh
docker compose stop mongodb
comment

<<comment
# Run test for single file with docker
docker compose run --rm app \
    uv run --extra dev coverage run -m pytest tests/test__indexes.py
comment

# Run test for all files with docker
docker compose run --rm app \
    ./scripts/test.sh

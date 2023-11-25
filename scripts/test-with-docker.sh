#!/usr/bin/env bash

set -x

<<comment
docker run -d --rm --name mongo -p 27017:27017 mongo
poetry run scripts/test.sh
docker stop mongo
comment

<<comment
docker compose up -d mongodb && docker compose up mongo-init
python -m poetry run bash scripts/test.sh
docker compose stop mongodb
comment

<<comment
# Run test for single file
docker-compose -f docker-compose-local.yml run --rm app \
    python -m poetry run coverage run -m pytest tests/test__indexes.py
comment

docker-compose -f docker-compose-local.yml run --build --rm app \
    python -m poetry run bash scripts/test.sh

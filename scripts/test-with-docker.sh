#!/usr/bin/env bash

set -x

# docker run -d --rm --name mongo -p 27017:27017 mongo
# poetry run scripts/test.sh
# docker stop mongo

# docker compose up -d mongodb && docker compose up mongo-init
# python -m poetry run bash scripts/test.sh
# docker compose stop mongodb

docker-compose -f docker-compose-local.yml run --build --rm app \
    python -m poetry run bash scripts/test.sh

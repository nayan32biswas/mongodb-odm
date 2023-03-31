#!/usr/bin/env bash

set -x

docker run -d --rm --name mongo -p 27017:27017 mongo

poetry run scripts/test.sh

docker stop mongo

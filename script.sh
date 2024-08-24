#! /bin/bash

mv .env.development .env

mv django/.env.development django/.env

source .env

envsubst < docker-compose.yml > docker-compose-test.yml

docker compose -f docker-compose-test.yml up -d
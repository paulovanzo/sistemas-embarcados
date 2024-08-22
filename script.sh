#! /bin/bash

source .env.development

envsubst < docker-compose.yml > docker-compose-test.yml

docker compose -f docker-compose-test.yml up -d
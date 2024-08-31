#! /bin/bash

cp .env.development .env

cp django/.env.development django/.env

source .env

envsubst < alertmanager/config.yml > alertmanager/config-temp.yml && mv alertmanager/config-temp.yml alertmanager/config.yml

envsubst < docker-compose.yml > docker-compose-temp.yml && mv docker-compose-temp.yml docker-compose.yml

docker compose up -d
docker compose exec rabbitmq rabbitmq-plugins enable rabbitmq_mqtt
docker compose restart django-backend
#!/bin/bash

MODE=${1:-dev}
if [ "$MODE" = "prod" ]; then
  docker compose -f docker-compose.yml -f docker-compose.prod.yml down
else
  docker compose -f docker-compose.yml -f docker-compose.dev.yml down
fi

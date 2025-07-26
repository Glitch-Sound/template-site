#!/bin/bash
set -e

MODE=${1:-dev}
if [ "$MODE" = "prod" ]; then
  docker compose -f docker-compose.yml -f docker-compose.prod.yml build --no-cache
  docker compose -f docker-compose.yml -f docker-compose.prod.yml up
else
  docker compose -f docker-compose.yml -f docker-compose.dev.yml build --no-cache
  docker compose -f docker-compose.yml -f docker-compose.dev.yml up
fi

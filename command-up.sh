#!/bin/bash
set -e

MODE=${1:-dev}
if [ "$MODE" = "prod" ]; then
  docker compose -f docker-compose.yml -f docker-compose.prod.yml up --build
else
  docker compose -f docker-compose.yml -f docker-compose.dev.yml up --build
fi

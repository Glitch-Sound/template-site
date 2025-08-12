#!/bin/bash

MODE=${1:-dev}
if [ "$MODE" = "prod" ]; then
  docker compose -f docker-compose.yml -f docker-compose.prod.yml down -v
  rm -f ./backend/app/db.sqlite3
else
  docker compose -f docker-compose.yml -f docker-compose.dev.yml down -v
  rm -f ./backend/app/db.sqlite3
fi




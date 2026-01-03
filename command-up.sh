#!/usr/bin/env bash
set -euo pipefail

# Usage:
#   ./command-up.sh dev
#   ./command-up.sh prod

MODE="${1:-dev}"
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV="${ROOT}/.venv"
REQ="${ROOT}/backend/requirements.txt"

case "${MODE}" in
  dev|prod) ;;
  *) echo "Usage: $0 [dev|prod]"; exit 1 ;;
esac

# Pre-checks.
[[ -f "${ROOT}/docker-compose.yml" ]] || { echo "[error] docker-compose.yml not found"; exit 1; }
[[ -f "${REQ}" ]] || { echo "[error] ${REQ} not found"; exit 1; }

# Docker Compose up.
echo "[compose] Starting services in '${MODE}' mode ..."
if [[ "${MODE}" == "prod" ]]; then
  docker compose -f docker-compose.yml -f docker-compose.prod.yml build
  docker compose -f docker-compose.yml -f docker-compose.prod.yml up
else
  docker compose -f docker-compose.yml -f docker-compose.dev.yml build
  docker compose -f docker-compose.yml -f docker-compose.dev.yml up
fi

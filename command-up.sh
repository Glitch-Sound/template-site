#!/usr/bin/env bash
set -euo pipefail

# Usage:
#   ./command-up.sh dev
#   ./command-up.sh prod
#
# Requirements:
#   sudo apt update
#   sudo apt install -y python3-venv

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

# Safety: do not delete the venv if the current shell is using it.
if [[ "${VIRTUAL_ENV:-}" == "${VENV}" ]]; then
  echo "[venv][error] Current shell is using ${VENV}. Run 'deactivate' and re-run this script."
  exit 1
fi

# Clean & create venv.
if [[ -d "${VENV}" ]]; then
  echo "[venv] Removing existing .venv ..."
  rm -rf "${VENV}"
fi
echo "[venv] Creating .venv ..."
python3 -m venv "${VENV}"

# Install dependencies.
echo "[venv] Upgrading pip ..."
"${VENV}/bin/python" -m pip install -U pip
echo "[venv] Installing dependencies from ${REQ} ..."
"${VENV}/bin/python" -m pip install -r "${REQ}"

# Docker Compose up.
echo "[compose] Starting services in '${MODE}' mode ..."
if [[ "${MODE}" == "prod" ]]; then
  docker compose -f docker-compose.yml -f docker-compose.prod.yml build
  docker compose -f docker-compose.yml -f docker-compose.prod.yml up
else
  docker compose -f docker-compose.yml -f docker-compose.dev.yml build
  docker compose -f docker-compose.yml -f docker-compose.dev.yml up
fi

#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
MIGRATION_DB="$(mktemp /tmp/creaty_verify_XXXXXX.db)"

cleanup() {
  rm -f "$MIGRATION_DB" "$MIGRATION_DB-journal"
}
trap cleanup EXIT

cd "$ROOT_DIR"

PYTHONPATH=backend python -m pytest backend/tests -v
PYTHONPATH=backend python -m compileall backend/app backend/tests

cd "$ROOT_DIR/backend"
CDOS_DATABASE_URL="sqlite:///$MIGRATION_DB" PYTHONPATH=. alembic upgrade head

#!/usr/bin/env bash
set -euo pipefail

# Usage: scripts/pg_restore.sh postgresql://user:pass@host:5432/db in.sql.gz
CONN_STR=${1:-}
IN=${2:-}
if [ -z "$CONN_STR" ] || [ -z "$IN" ]; then
  echo "Usage: $0 <DATABASE_URL> <in.sql.gz>" >&2
  exit 1
fi

gunzip -c "$IN" | psql "$CONN_STR"
echo "Restored from $IN"



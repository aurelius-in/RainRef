#!/usr/bin/env bash
set -euo pipefail

# Usage: scripts/pg_backup.sh postgresql://user:pass@host:5432/db out.sql.gz
CONN_STR=${1:-}
OUT=${2:-backup.sql.gz}
if [ -z "$CONN_STR" ]; then
  echo "Usage: $0 <DATABASE_URL> [out.sql.gz]" >&2
  exit 1
fi

pg_dump "$CONN_STR" | gzip -9 > "$OUT"
echo "Wrote $OUT"



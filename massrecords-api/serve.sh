#!/usr/bin/env bash
# Ensures the local capture API is running on :8787. Safe to call repeatedly —
# no-ops if it's already up. Creates the venv on first run.
set -euo pipefail
cd "$(dirname "$0")"

if [ ! -d .venv ]; then
  echo "Creating venv + installing deps..." >&2
  python3 -m venv .venv
  .venv/bin/pip install -q -r requirements.txt
fi

if curl -sf http://localhost:8787/health >/dev/null 2>&1; then
  echo "already-running"
  exit 0
fi

nohup .venv/bin/uvicorn api:app --port 8787 >> api.log 2>&1 &
disown

for _ in $(seq 1 30); do
  sleep 0.2
  if curl -sf http://localhost:8787/health >/dev/null 2>&1; then
    echo "started"
    exit 0
  fi
done

echo "failed-to-start — check api.log" >&2
exit 1

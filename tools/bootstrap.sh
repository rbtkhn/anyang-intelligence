#!/usr/bin/env sh
set -eu

ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
VENV="$ROOT/.venv"

if [ "${1:-}" = "--refresh" ] && [ -d "$VENV" ]; then
  rm -rf "$VENV"
fi

if [ ! -x "$VENV/bin/python" ]; then
  python3 -m venv "$VENV"
fi

"$VENV/bin/python" -m pip install --disable-pip-version-check PyYAML pytest
printf 'Persistent repository environment ready: %s\n' "$VENV/bin/python"

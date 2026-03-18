#!/usr/bin/env bash

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="$ROOT_DIR/.venv-macos"

if [[ ! -x "$VENV_DIR/bin/python" ]]; then
  echo "Ambiente macOS nao encontrado em $VENV_DIR"
  echo "Crie-o com:"
  echo "  /opt/homebrew/bin/python3.13 -m venv .venv-macos"
  echo "  ./.venv-macos/bin/python -m pip install -r requirements.txt"
  exit 1
fi

exec "$VENV_DIR/bin/python" "$ROOT_DIR/main.py"

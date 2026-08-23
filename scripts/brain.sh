#!/usr/bin/env bash
# Stable AIBrain public launcher. All v1 commands remain available through v2.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYTHON="${AIBRAIN_PYTHON:-}"

if [ -z "$PYTHON" ]; then
    if command -v python3 >/dev/null 2>&1; then
        PYTHON="$(command -v python3)"
    elif command -v python >/dev/null 2>&1; then
        PYTHON="$(command -v python)"
    else
        echo "error: AIBrain v2 requires Python 3.9+" >&2
        exit 1
    fi
fi

exec "$PYTHON" "$SCRIPT_DIR/aibrain.py" "$@"

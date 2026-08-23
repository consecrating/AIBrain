#!/usr/bin/env bash
# Refresh live package evidence using the AIBrain v2 stdlib runtime.
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYTHON="${AIBRAIN_PYTHON:-$(command -v python3 || command -v python || true)}"
if [ -z "$PYTHON" ]; then
    echo "error: refresh requires Python 3.9+" >&2
    exit 1
fi

case "${1:-all}" in
    --python) shift; exec "$PYTHON" "$SCRIPT_DIR/refresh.py" python "$@" ;;
    --node) shift; exec "$PYTHON" "$SCRIPT_DIR/refresh.py" node "$@" ;;
    all|python|node) exec "$PYTHON" "$SCRIPT_DIR/refresh.py" "$@" ;;
    *) exec "$PYTHON" "$SCRIPT_DIR/refresh.py" "$@" ;;
esac

#!/usr/bin/env bash
# Install AIBrain v2 into the active Kiro configuration.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
AIBRAIN_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"

if [ -n "${KIRO_DIR:-}" ]; then
    TARGET="$KIRO_DIR"
elif [ -d "/projects/.kiro" ]; then
    TARGET="/projects/.kiro"
elif [ -d "$HOME/.kiro" ]; then
    TARGET="$HOME/.kiro"
else
    TARGET="/projects/.kiro"
fi

PYTHON="${AIBRAIN_PYTHON:-$(command -v python3 || command -v python || true)}"
if [ -z "$PYTHON" ]; then
    echo "error: AIBrain v2 requires Python 3.9+" >&2
    exit 1
fi
if ! "$PYTHON" -c 'import sys; raise SystemExit(sys.version_info < (3, 9))'; then
    echo "error: AIBrain v2 requires Python 3.9+" >&2
    exit 1
fi

chmod +x "$AIBRAIN_DIR/scripts/"*.sh "$AIBRAIN_DIR/scripts/"*.py

# Validate and initialize the source before replacing installed integration files.
AIBRAIN_ROOT="$AIBRAIN_DIR" AIBRAIN_PYTHON="$PYTHON" "$AIBRAIN_DIR/scripts/brain.sh" init >/dev/null
AIBRAIN_ROOT="$AIBRAIN_DIR" AIBRAIN_PYTHON="$PYTHON" "$AIBRAIN_DIR/scripts/brain.sh" doctor >/dev/null

printf '✓ Installing AIBrain v2 into %s\n' "$TARGET"
AIBRAIN_PYTHON="$PYTHON" "$PYTHON" "$AIBRAIN_DIR/scripts/install_integration.py" \
    --root "$AIBRAIN_DIR" \
    --target "$TARGET"

# Verify the installed pointer resolves and the source remains healthy.
KIRO_DIR="$TARGET" AIBRAIN_PYTHON="$PYTHON" "$AIBRAIN_DIR/scripts/brain.sh" doctor

printf '\n✅ AIBrain v2 installed successfully.\n'
printf 'Brain: %s\n' "$AIBRAIN_DIR"
printf 'CLI:   %s/scripts/brain.sh\n' "$AIBRAIN_DIR"

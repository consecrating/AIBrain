#!/usr/bin/env bash
# Canonical AIBrain v2 integrity check.
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
exec "$SCRIPT_DIR/brain.sh" doctor "$@"

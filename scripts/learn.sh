#!/usr/bin/env bash
# ---------------------------------------------------------------------------
# learn.sh — Capture a learning from the current session
#
# Learnings are captured quickly, then classified and promoted later.
# This is the "inbox" approach — fast capture, deliberate promotion.
#
# Usage:
#   ./scripts/learn.sh add "Never use sync requests in async code"
#   ./scripts/learn.sh add "httpx timeout default is too short for scraping" --scope repo
#   ./scripts/learn.sh list
#   ./scripts/learn.sh promote 3
#   ./scripts/learn.sh clear
# ---------------------------------------------------------------------------
set -euo pipefail

BRAIN_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
INBOX="$BRAIN_DIR/memory/learnings-inbox.md"
MEMORY="$BRAIN_DIR/memory"

NOW="$(date -u +%Y-%m-%dT%H:%M:%S)"

# Ensure inbox exists
if [ ! -f "$INBOX" ]; then
    cat > "$INBOX" << 'EOF'
# Learnings Inbox

> Quick-captured learnings. Review and promote to brain/ or rules/ periodically.
> Format: [timestamp] #N | scope | learning text

EOF
fi

cmd_add() {
    local text="${1:-}"
    local scope="${2:-global}"
    if [ -z "$text" ]; then
        echo "Usage: learn.sh add <learning> [scope: global|repo|task]"
        exit 1
    fi
    
    local num=$(grep -c "^[0-9]" "$INBOX" 2>/dev/null || echo "0")
    num=$((num + 1))
    
    echo "$num. [$NOW] | $scope | $text" >> "$INBOX"
    echo "- [$NOW] [LEARNED] #$num: $text" >> "$MEMORY/journal.md"
    
    echo "✓ Learning #$num captured (scope: $scope)"
    echo "  Run 'learn.sh promote $num' to move to permanent storage"
}

cmd_list() {
    if [ -f "$INBOX" ]; then
        echo ""
        echo "📚 Learnings Inbox:"
        echo ""
        grep "^[0-9]" "$INBOX" 2>/dev/null || echo "  (empty)"
    fi
}

cmd_promote() {
    local num="${1:-}"
    if [ -z "$num" ]; then
        echo "Usage: learn.sh promote <number>"
        echo "  This guides you on where to place the learning permanently."
        exit 1
    fi
    
    local entry=$(grep "^$num\." "$INBOX" 2>/dev/null || echo "")
    if [ -z "$entry" ]; then
        echo "Learning #$num not found"
        exit 1
    fi
    
    echo ""
    echo "📋 Learning to promote:"
    echo "  $entry"
    echo ""
    echo "🎯 Promotion targets (cheapest first):"
    echo ""
    echo "  1. brain/stack/registry.md   — if it's about a package choice"
    echo "  2. brain/stack/banned.md     — if it's about avoiding something"
    echo "  3. brain/patterns/           — if it's a code pattern to reuse"
    echo "  4. rules/code-style.md       — if it's about how to write code"
    echo "  5. rules/anti-patterns.md    — if it's a mistake to never make"
    echo "  6. memory/corrections.md     — if it was a user correction"
    echo "  7. brain/decisions/          — if it's an architectural decision"
    echo ""
    echo "  After placing it, remove from inbox with: learn.sh done $num"
}

cmd_done() {
    local num="${1:-}"
    if [ -z "$num" ]; then
        echo "Usage: learn.sh done <number>"
        exit 1
    fi
    sed -i "/^$num\./d" "$INBOX" 2>/dev/null
    echo "✓ Learning #$num removed from inbox (assumed promoted)"
}

cmd_clear() {
    > "$INBOX"
    cat > "$INBOX" << 'EOF'
# Learnings Inbox

> Quick-captured learnings. Review and promote to brain/ or rules/ periodically.
> Format: [timestamp] #N | scope | learning text

EOF
    echo "✓ Inbox cleared"
}

# ─── Main ────────────────────────────────────────────────────────────────────

case "${1:-list}" in
    add)     shift; cmd_add "$@" ;;
    list)    cmd_list ;;
    promote) shift; cmd_promote "$@" ;;
    done)    shift; cmd_done "$@" ;;
    clear)   cmd_clear ;;
    *)       echo "Usage: learn.sh [add|list|promote|done|clear]" ;;
esac

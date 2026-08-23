#!/usr/bin/env bash
# ---------------------------------------------------------------------------
# brain.sh — AIBrain CLI
#
# Query, add to, and manage the brain's knowledge graph.
# Zero external dependencies — bash + coreutils only.
#
# Usage:
#   brain.sh <command> [args...]
#
# Commands:
#   status          — show brain health + active task
#   recall <topic>  — search the brain for relevant knowledge
#   decide <text>   — record a new decision
#   correct <text>  — record a correction (mistake to never repeat)
#   pattern add     — add a new code pattern
#   stack add       — add approved package
#   stack ban       — ban a package
#   journal <text>  — append to session journal
#   next <text>     — update the "next action" in active-task
#   validate        — check brain integrity
#   stats           — knowledge base statistics
# ---------------------------------------------------------------------------
set -euo pipefail

BRAIN_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
BRAIN="$BRAIN_DIR/brain"
MEMORY="$BRAIN_DIR/memory"
RULES="$BRAIN_DIR/rules"
FEEDS="$BRAIN_DIR/feeds"

NOW="$(date -u +%Y-%m-%dT%H:%M:%S)"
TODAY="$(date -u +%Y-%m-%d)"

# ─── Helpers ─────────────────────────────────────────────────────────────────

_color() { printf "\033[%sm%s\033[0m" "$1" "$2"; }
_green()  { _color "32" "$1"; }
_yellow() { _color "33" "$1"; }
_red()    { _color "31" "$1"; }
_blue()   { _color "34" "$1"; }
_bold()   { _color "1" "$1"; }

# ─── Commands ────────────────────────────────────────────────────────────────

cmd_status() {
    echo ""
    _bold "🧠 AIBrain Status"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    
    # Active task
    if [ -f "$MEMORY/active-task.md" ]; then
        _blue "📋 Active Task:"
        grep "^\- \*\*Goal:\*\*" "$MEMORY/active-task.md" 2>/dev/null | sed 's/.*\*\*Goal:\*\* /  /' || echo "  (none)"
        grep "^\- \*\*Status:\*\*" "$MEMORY/active-task.md" 2>/dev/null | sed 's/.*\*\*Status:\*\* /  /' || echo "  (unknown)"
        grep "^\- \*\*Next Action:\*\*" "$MEMORY/active-task.md" 2>/dev/null | sed 's/.*\*\*Next Action:\*\* /  /' || true
    fi
    echo ""
    
    # Knowledge stats
    _blue "📊 Knowledge Base:"
    local decisions=$(grep -c "^| [0-9]" "$BRAIN/decisions/_index.md" 2>/dev/null || echo "0")
    local patterns=$(grep -c "^| [A-Z]" "$BRAIN/patterns/_index.md" 2>/dev/null || echo "0")
    local approved=$(grep -c "^| " "$BRAIN/stack/registry.md" 2>/dev/null || echo "0")
    local banned=$(grep -c "^| " "$BRAIN/stack/banned.md" 2>/dev/null || echo "0")
    local corrections=$(grep -c "^### \[" "$MEMORY/corrections.md" 2>/dev/null || echo "0")
    
    printf "  Decisions: %s | Patterns: %s | Approved pkgs: %s | Banned: %s | Corrections: %s\n" \
        "$decisions" "$patterns" "$approved" "$banned" "$corrections"
    echo ""
    
    # Recent corrections (antibodies)
    if [ "$corrections" -gt 0 ]; then
        _yellow "⚠️  Active Corrections (never repeat):"
        grep "^\- \*\*What I did wrong:\*\*" "$MEMORY/corrections.md" 2>/dev/null | head -3 | sed 's/.*\*\*What I did wrong:\*\* /  ❌ /'
    fi
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
}

cmd_recall() {
    local query="${1:-}"
    if [ -z "$query" ]; then
        echo "Usage: brain.sh recall <topic>"
        exit 1
    fi
    
    echo ""
    _bold "🔍 Recalling: $query"
    echo ""
    
    # Search across all brain files
    local found=0
    
    # Decisions
    local hits=$(grep -il "$query" "$BRAIN/decisions/"*.md 2>/dev/null || true)
    if [ -n "$hits" ]; then
        _blue "📋 Decisions:"
        grep -i "$query" "$BRAIN/decisions/_index.md" 2>/dev/null | head -5 | sed 's/^/  /'
        found=1
    fi
    
    # Stack
    local stack_hits=$(grep -i "$query" "$BRAIN/stack/"*.md 2>/dev/null || true)
    if [ -n "$stack_hits" ]; then
        echo ""
        _blue "📦 Stack Knowledge:"
        echo "$stack_hits" | head -5 | sed 's/^/  /'
        found=1
    fi
    
    # Patterns
    local pattern_hits=$(grep -i "$query" "$BRAIN/patterns/"*.md 2>/dev/null || true)
    if [ -n "$pattern_hits" ]; then
        echo ""
        _blue "🔧 Patterns:"
        echo "$pattern_hits" | head -5 | sed 's/^/  /'
        found=1
    fi
    
    # Rules
    local rule_hits=$(grep -i "$query" "$RULES/"*.md 2>/dev/null || true)
    if [ -n "$rule_hits" ]; then
        echo ""
        _blue "📏 Rules:"
        echo "$rule_hits" | head -5 | sed 's/^/  /'
        found=1
    fi
    
    # Corrections
    local correction_hits=$(grep -i "$query" "$MEMORY/corrections.md" 2>/dev/null || true)
    if [ -n "$correction_hits" ]; then
        echo ""
        _yellow "⚠️  Related Corrections:"
        echo "$correction_hits" | head -3 | sed 's/^/  /'
        found=1
    fi
    
    if [ "$found" -eq 0 ]; then
        echo "  No knowledge found for '$query'"
        echo "  Consider adding with: brain.sh decide/pattern/stack"
    fi
}

cmd_decide() {
    local decision="${1:-}"
    local reason="${2:-}"
    if [ -z "$decision" ]; then
        echo "Usage: brain.sh decide <decision> [reason]"
        exit 1
    fi
    
    # Get next decision number
    local last_num=$(grep -oP "^\| \K[0-9]+" "$BRAIN/decisions/_index.md" 2>/dev/null | tail -1 || echo "0")
    local next_num=$(printf "%03d" $((10#$last_num + 1)))
    
    # Append to index
    echo "| $next_num | $TODAY | $decision | ✅ Active | ${reason:-pending rationale} |" >> "$BRAIN/decisions/_index.md"
    
    # Journal
    echo "- [$NOW] [DECISION] DEC-$next_num: $decision" >> "$MEMORY/journal.md"
    
    _green "✓ Decision #$next_num recorded: $decision"
}

cmd_correct() {
    local mistake="${1:-}"
    local fix="${2:-}"
    if [ -z "$mistake" ]; then
        echo "Usage: brain.sh correct <what-went-wrong> [what-to-do-instead]"
        exit 1
    fi
    
    local num=$(grep -c "^### \[" "$MEMORY/corrections.md" 2>/dev/null || echo "0")
    num=$((num + 1))
    
    cat >> "$MEMORY/corrections.md" << EOF

### [$TODAY] Correction #$num
- **What I did wrong:** $mistake
- **What to do instead:** ${fix:-TBD — fill in the correct behavior}
- **Why:** (add rationale)
- **Scope:** always
EOF
    
    echo "- [$NOW] [CORRECTION] #$num: $mistake" >> "$MEMORY/journal.md"
    _yellow "⚠️  Correction #$num recorded. Never repeat: $mistake"
}

cmd_stack_add() {
    local pkg="${1:-}"
    local version="${2:->=latest}"
    local reason="${3:-}"
    if [ -z "$pkg" ]; then
        echo "Usage: brain.sh stack add <package> [version] [reason]"
        exit 1
    fi
    
    echo "| $pkg | $version | ${reason:-approved} | — |" >> "$BRAIN/stack/registry.md"
    echo "- [$NOW] [STACK] Added: $pkg $version" >> "$MEMORY/journal.md"
    _green "✓ Added to registry: $pkg $version"
}

cmd_stack_ban() {
    local pkg="${1:-}"
    local reason="${2:-}"
    local alt="${3:-}"
    if [ -z "$pkg" ]; then
        echo "Usage: brain.sh stack ban <package> [reason] [alternative]"
        exit 1
    fi
    
    echo "| $pkg | ${reason:-banned} | ${alt:-find alternative} |" >> "$BRAIN/stack/banned.md"
    echo "- [$NOW] [STACK] Banned: $pkg (${reason:-no reason given})" >> "$MEMORY/journal.md"
    _red "✗ Banned: $pkg → use ${alt:-alternative TBD}"
}

cmd_journal() {
    local entry="${1:-}"
    if [ -z "$entry" ]; then
        # Show recent journal
        tail -20 "$MEMORY/journal.md"
        return
    fi
    echo "- [$NOW] [NOTE] $entry" >> "$MEMORY/journal.md"
    _green "✓ Journaled"
}

cmd_next() {
    local action="${1:-}"
    if [ -z "$action" ]; then
        grep "^## Next Action" -A 2 "$MEMORY/active-task.md" 2>/dev/null
        return
    fi
    
    # Update the next action in active-task.md
    if [ -f "$MEMORY/active-task.md" ]; then
        sed -i "s|^## Next Action.*|## Next Action\n\n$action|" "$MEMORY/active-task.md" 2>/dev/null || true
    fi
    echo "- [$NOW] [NEXT] $action" >> "$MEMORY/journal.md"
    _blue "→ Next: $action"
}

cmd_validate() {
    _bold "🔍 Validating brain integrity..."
    local errors=0
    
    # Check required files exist
    for f in "$BRAIN/identity.md" "$BRAIN/decisions/_index.md" "$BRAIN/stack/registry.md" \
             "$BRAIN/stack/banned.md" "$MEMORY/active-task.md" "$MEMORY/corrections.md"; do
        if [ ! -f "$f" ]; then
            _red "  ✗ Missing: $f"
            errors=$((errors + 1))
        fi
    done
    
    # Check for empty required files
    for f in "$BRAIN/identity.md" "$BRAIN/stack/registry.md"; do
        if [ -f "$f" ] && [ ! -s "$f" ]; then
            _yellow "  ⚠ Empty: $f"
            errors=$((errors + 1))
        fi
    done
    
    if [ "$errors" -eq 0 ]; then
        _green "  ✓ Brain integrity OK"
    else
        _red "  ✗ $errors issue(s) found"
    fi
    return $errors
}

cmd_stats() {
    echo ""
    _bold "📊 AIBrain Statistics"
    echo ""
    echo "  Brain files:      $(find "$BRAIN" -name "*.md" | wc -l)"
    echo "  Memory files:     $(find "$MEMORY" -name "*.md" | wc -l)"
    echo "  Rule files:       $(find "$RULES" -name "*.md" | wc -l)"
    echo "  Total knowledge:  $(find "$BRAIN_DIR" -name "*.md" | wc -l) files"
    echo "  Total size:       $(du -sh "$BRAIN_DIR" 2>/dev/null | cut -f1)"
    echo ""
    echo "  Decisions:        $(grep -c "^| [0-9]" "$BRAIN/decisions/_index.md" 2>/dev/null || echo 0)"
    echo "  Patterns:         $(grep -c "^| [A-Z]" "$BRAIN/patterns/_index.md" 2>/dev/null || echo 0)"
    echo "  Stack approved:   $(grep -c "^| [a-z]" "$BRAIN/stack/registry.md" 2>/dev/null || echo 0)"
    echo "  Stack banned:     $(grep -c "^| [a-z]" "$BRAIN/stack/banned.md" 2>/dev/null || echo 0)"
    echo "  Corrections:      $(grep -c "^### \[" "$MEMORY/corrections.md" 2>/dev/null || echo 0)"
    echo "  Journal entries:  $(grep -c "^\- \[" "$MEMORY/journal.md" 2>/dev/null || echo 0)"
}

# ─── Main ────────────────────────────────────────────────────────────────────

case "${1:-status}" in
    status)     cmd_status ;;
    recall)     shift; cmd_recall "$@" ;;
    decide)     shift; cmd_decide "$@" ;;
    correct)    shift; cmd_correct "$@" ;;
    stack)
        shift
        case "${1:-}" in
            add) shift; cmd_stack_add "$@" ;;
            ban) shift; cmd_stack_ban "$@" ;;
            *) echo "Usage: brain.sh stack [add|ban] <args>" ;;
        esac
        ;;
    journal)    shift; cmd_journal "$@" ;;
    next)       shift; cmd_next "$@" ;;
    validate)   cmd_validate ;;
    stats)      cmd_stats ;;
    help|--help|-h)
        echo "AIBrain CLI — manage your persistent intelligence"
        echo ""
        echo "Commands:"
        echo "  status          Brain health + active task summary"
        echo "  recall <topic>  Search all knowledge for a topic"
        echo "  decide <text>   Record a decision"
        echo "  correct <text>  Record a mistake to never repeat"
        echo "  stack add <pkg> Add approved package"
        echo "  stack ban <pkg> Ban a package"
        echo "  journal [text]  View or append to journal"
        echo "  next <action>   Set next action"
        echo "  validate        Check brain integrity"
        echo "  stats           Knowledge base statistics"
        ;;
    *)
        echo "Unknown command: $1 (try: brain.sh help)"
        exit 1
        ;;
esac

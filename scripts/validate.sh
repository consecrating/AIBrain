#!/usr/bin/env bash
# ---------------------------------------------------------------------------
# validate.sh — Check AIBrain integrity
#
# Ensures: no broken references, no stale entries, required files exist,
# no contradictions between registry and banned lists.
# ---------------------------------------------------------------------------
set -euo pipefail

BRAIN_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
BRAIN="$BRAIN_DIR/brain"
MEMORY="$BRAIN_DIR/memory"
RULES="$BRAIN_DIR/rules"

errors=0
warnings=0

echo "🔍 Validating AIBrain..."
echo ""

# ─── Required files ──────────────────────────────────────────────────────────

echo "📁 Required files:"
required_files=(
    "$BRAIN/identity.md"
    "$BRAIN/decisions/_index.md"
    "$BRAIN/patterns/_index.md"
    "$BRAIN/stack/registry.md"
    "$BRAIN/stack/banned.md"
    "$BRAIN/stack/alternatives.md"
    "$BRAIN/context/repos.md"
    "$BRAIN/context/environments.md"
    "$MEMORY/active-task.md"
    "$MEMORY/corrections.md"
    "$MEMORY/journal.md"
    "$MEMORY/scratchpad.md"
    "$RULES/response-quality.md"
    "$RULES/dependency-policy.md"
    "$RULES/code-style.md"
    "$RULES/anti-patterns.md"
)

for f in "${required_files[@]}"; do
    if [ ! -f "$f" ]; then
        echo "  ✗ MISSING: $f"
        errors=$((errors + 1))
    elif [ ! -s "$f" ]; then
        echo "  ⚠ EMPTY: $f"
        warnings=$((warnings + 1))
    fi
done
echo "  ✓ Checked ${#required_files[@]} required files"
echo ""

# ─── Contradiction check ─────────────────────────────────────────────────────

echo "🔀 Contradiction check (registry vs banned):"
while IFS='|' read -r _ pkg _; do
    pkg=$(echo "$pkg" | tr -d ' ')
    if [ -n "$pkg" ] && grep -q "^| $pkg |" "$BRAIN/stack/banned.md" 2>/dev/null; then
        echo "  ✗ CONTRADICTION: '$pkg' is in BOTH registry and banned!"
        errors=$((errors + 1))
    fi
done < <(grep "^| [a-z]" "$BRAIN/stack/registry.md" 2>/dev/null || true)
if [ "$errors" -eq 0 ]; then echo "  ✓ No contradictions"; fi
echo ""

# ─── Decision log integrity ──────────────────────────────────────────────────

echo "📋 Decision log:"
local_decisions=$(grep -c "^| [0-9]" "$BRAIN/decisions/_index.md" 2>/dev/null || echo "0")
if [ "$local_decisions" -eq 0 ]; then
    echo "  ⚠ No decisions recorded yet"
    warnings=$((warnings + 1))
else
    echo "  ✓ $local_decisions decisions logged"
fi
echo ""

# ─── Memory integrity ────────────────────────────────────────────────────────

echo "🧠 Memory integrity:"
if grep -q "## Current State" "$MEMORY/active-task.md" 2>/dev/null; then
    echo "  ✓ Active task has structure"
else
    echo "  ⚠ Active task may be malformed"
    warnings=$((warnings + 1))
fi

corrections=$(grep -c "^### \[" "$MEMORY/corrections.md" 2>/dev/null || echo "0")
echo "  ✓ $corrections corrections recorded"
echo ""

# ─── Summary ─────────────────────────────────────────────────────────────────

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
if [ "$errors" -eq 0 ] && [ "$warnings" -eq 0 ]; then
    echo "✅ Brain integrity: PERFECT"
elif [ "$errors" -eq 0 ]; then
    echo "⚠️  Brain integrity: OK ($warnings warnings)"
else
    echo "❌ Brain integrity: FAILED ($errors errors, $warnings warnings)"
fi
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

exit $errors

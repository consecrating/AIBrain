#!/usr/bin/env bash
# ---------------------------------------------------------------------------
# install.sh — Install AIBrain into the active Kiro workspace
#
# This installs:
#   1. The AIBrain steering file (always-on) → /projects/.kiro/steering/
#   2. The AIBrain skill → /projects/.kiro/skills/aibrain/
#   3. Symlinks the brain to a discoverable location
#
# Usage:
#   ./scripts/install.sh
#   KIRO_DIR=/custom/path ./scripts/install.sh
# ---------------------------------------------------------------------------
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
AIBRAIN_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"

# Detect Kiro config directory
if [ -n "${KIRO_DIR:-}" ]; then
    TARGET="$KIRO_DIR"
elif [ -d "/projects/.kiro" ]; then
    TARGET="/projects/.kiro"
elif [ -d "$HOME/.kiro" ]; then
    TARGET="$HOME/.kiro"
else
    TARGET="/projects/.kiro"
fi

echo "🧠 Installing AIBrain into: $TARGET"
echo ""

# 1. Install steering file
mkdir -p "$TARGET/steering"
cp "$AIBRAIN_DIR/.kiro/steering/aibrain.md" "$TARGET/steering/aibrain.md"
echo "✓ Steering: $TARGET/steering/aibrain.md"

# 2. Install skill
mkdir -p "$TARGET/skills/aibrain"
cp "$AIBRAIN_DIR/.kiro/skills/aibrain/SKILL.md" "$TARGET/skills/aibrain/SKILL.md"
echo "✓ Skill: $TARGET/skills/aibrain/SKILL.md"

# 3. Create a pointer so scripts know where the brain is
echo "$AIBRAIN_DIR" > "$TARGET/.aibrain-path"
echo "✓ Brain path: $TARGET/.aibrain-path → $AIBRAIN_DIR"

# 4. Make all scripts executable
chmod +x "$AIBRAIN_DIR/scripts/"*.sh
echo "✓ Scripts: executable"

# 4b. Seed private working memory from templates on first run.
# The live files are gitignored (this repo is public), so a fresh clone has the
# *.template.md seeds only. Copy them into place if missing — never overwrite an
# existing file, which would destroy accumulated memory.
seed_from_template() {
    local live="$1" template="$2"
    if [ -f "$AIBRAIN_DIR/$live" ]; then
        echo "  · $live (exists — preserved)"
    elif [ -f "$AIBRAIN_DIR/$template" ]; then
        cp "$AIBRAIN_DIR/$template" "$AIBRAIN_DIR/$live"
        echo "  ✓ $live (seeded from template)"
    else
        echo "  ⚠ $live (no template found at $template)"
    fi
}

echo "🌱 Seeding private working memory:"
seed_from_template "memory/active-task.md"      "memory/active-task.template.md"
seed_from_template "memory/corrections.md"      "memory/corrections.template.md"
seed_from_template "memory/journal.md"          "memory/journal.template.md"
seed_from_template "brain/decisions/_index.md"  "brain/decisions/_index.template.md"

# 4c. Install the secret-scanning pre-commit hook. This repo is public and the
# protocol writes memory on every event — the hook is the tripwire.
if [ -x "$AIBRAIN_DIR/scripts/scan-secrets.sh" ] && [ -d "$AIBRAIN_DIR/.git" ]; then
    "$AIBRAIN_DIR/scripts/scan-secrets.sh" --install >/dev/null 2>&1 \
        && echo "✓ Secret scanner: pre-commit hook installed" \
        || echo "⚠ Secret scanner: hook install failed"
fi

# 5. Quick validation
"$AIBRAIN_DIR/scripts/brain.sh" validate && echo "" && echo "✅ AIBrain installed and validated" || echo "⚠️  Installed with warnings"

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "AIBrain is now active. It will:"
echo "  • Load identity + active task at session start"
echo "  • Check banned/approved packages before suggesting deps"
echo "  • Use your proven patterns before generating new code"
echo "  • Never repeat corrected mistakes"
echo "  • Record decisions automatically"
echo ""
echo "Quick commands:"
echo "  $AIBRAIN_DIR/scripts/brain.sh status"
echo "  $AIBRAIN_DIR/scripts/brain.sh recall <topic>"
echo "  $AIBRAIN_DIR/scripts/brain.sh decide <decision>"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

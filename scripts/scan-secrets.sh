#!/usr/bin/env bash
# ---------------------------------------------------------------------------
# scan-secrets.sh — Refuse to let credentials reach a public repository.
#
# AIBrain is PUBLIC and its own protocol tells the agent to write facts into
# memory/ on every significant event. That is a direct path from "remember
# this" to "published on the internet". This script is the tripwire.
#
# Scans STAGED content by default (use as a pre-commit hook), or --all to scan
# every tracked file, or --history to scan the entire git history.
#
# Usage:
#   ./scripts/scan-secrets.sh              # staged changes (pre-commit)
#   ./scripts/scan-secrets.sh --all        # all tracked files
#   ./scripts/scan-secrets.sh --history    # full history
#   ./scripts/scan-secrets.sh --install    # install as a git pre-commit hook
#
# Exit 0 = clean, Exit 1 = secrets found (blocks the commit).
# ---------------------------------------------------------------------------
set -uo pipefail

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_DIR" || exit 1

# Each pattern is "label|regex". Kept deliberately tight to limit false
# positives — a noisy scanner gets disabled, and a disabled scanner is useless.
PATTERNS=(
  'WordPress application password|[A-Za-z0-9]{4}( [A-Za-z0-9]{4}){5}'
  'curl basic auth|curl[^|]*-u +[A-Za-z0-9._%+-]+:[^ '"'"'"]+'
  'FTP/SFTP URL with password|(ftp|ftps|sftp|ssh)://[A-Za-z0-9._%+-]+:[^@/ ]+@'
  'OpenAI-style key|sk-[A-Za-z0-9_-]{20,}'
  'Anthropic key|sk-ant-[A-Za-z0-9_-]{20,}'
  'GitHub token|gh[pousr]_[A-Za-z0-9]{20,}'
  'AWS access key|AKIA[0-9A-Z]{16}'
  'Google API key|AIza[0-9A-Za-z_-]{35}'
  'Slack token|xox[baprs]-[0-9A-Za-z-]{10,}'
  'Private key block|BEGIN [A-Z ]*PRIVATE KEY'
  'JWT|eyJ[A-Za-z0-9_-]{10,}\.eyJ[A-Za-z0-9_-]{10,}\.'
  'Generic assigned secret|(password|passwd|secret|api_key|apikey|access_token|auth_token)[ ]*[:=][ ]*['"'"'"][^'"'"'"]{8,}['"'"'"]'
)

# Strings that look like secrets but are deliberate documentation placeholders.
#
# Deliberately NARROW. An earlier version allowlisted the bare word "EXAMPLE",
# which suppressed the entire matching line — so an ftp:// URL carrying a real
# password went undetected purely because the host happened to be example.net.
# Never allowlist a token that can appear incidentally alongside a real secret;
# match the placeholder itself instead.
ALLOWLIST_REGEX='(user%40domain:password@ftp\.host\.com|USER:APP_PASSWORD|AKIAIOSFODNN7EXAMPLE|<[A-Za-z_-]+>|YOUR_[A-Z_]+|EXAMPLE_[A-Z_]+|PLACEHOLDER|xxxx|XXXX|\*\*\*\*|foo:bar|\.template\.md)'

MODE="${1:-staged}"
FOUND=0

_scan_text() {
    local label="$1" regex="$2" text="$3" source="$4"
    local hits
    hits="$(printf '%s' "$text" | grep -nIiE "$regex" 2>/dev/null | grep -vIiE "$ALLOWLIST_REGEX" 2>/dev/null)"
    if [ -n "$hits" ]; then
        echo ""
        echo "  ✗ $label  ($source)"
        printf '%s\n' "$hits" | head -5 | sed 's/^/      /'
        FOUND=$((FOUND + 1))
    fi
}

echo ""
echo "🔒 AIBrain secret scan — mode: $MODE"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

case "$MODE" in
  --install)
      mkdir -p .git/hooks
      cat > .git/hooks/pre-commit <<'HOOK'
#!/usr/bin/env bash
exec "$(git rev-parse --show-toplevel)/scripts/scan-secrets.sh" staged
HOOK
      chmod +x .git/hooks/pre-commit
      echo "  ✓ installed .git/hooks/pre-commit"
      echo ""
      exit 0
      ;;
  --all)
      while IFS= read -r f; do
          [ -f "$f" ] || continue
          case "$f" in *.template.md) continue ;; esac
          content="$(cat "$f" 2>/dev/null)"
          for p in "${PATTERNS[@]}"; do
              _scan_text "${p%%|*}" "${p#*|}" "$content" "$f"
          done
      done < <(git ls-files)
      ;;
  --history)
      content="$(git log -p --all 2>/dev/null)"
      for p in "${PATTERNS[@]}"; do
          _scan_text "${p%%|*}" "${p#*|}" "$content" "git history"
      done
      ;;
  staged|*)
      content="$(git diff --cached 2>/dev/null)"
      if [ -z "$content" ]; then
          echo "  (nothing staged)"
          echo ""
          exit 0
      fi
      for p in "${PATTERNS[@]}"; do
          _scan_text "${p%%|*}" "${p#*|}" "$content" "staged diff"
      done
      ;;
esac

echo ""
if [ "$FOUND" -eq 0 ]; then
    echo "✅ Clean — no credential-shaped strings found."
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    exit 0
fi

echo "❌ BLOCKED — $FOUND pattern(s) matched. This repo is PUBLIC."
echo ""
echo "   Credentials belong in the private vault, never in the brain."
echo "   If a match is a documentation placeholder, add it to ALLOWLIST_REGEX"
echo "   in scripts/scan-secrets.sh — do not delete the check."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
exit 1

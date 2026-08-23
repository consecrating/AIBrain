#!/usr/bin/env bash
# ---------------------------------------------------------------------------
# refresh.sh — Update live feeds from package registries
#
# Checks current versions of approved packages against npm/pypi
# and flags anything deprecated or significantly outdated.
#
# Usage:
#   ./scripts/refresh.sh              # full refresh
#   ./scripts/refresh.sh --python     # Python packages only
#   ./scripts/refresh.sh --node       # Node packages only
# ---------------------------------------------------------------------------
set -euo pipefail

BRAIN_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
FEEDS="$BRAIN_DIR/feeds"
REGISTRY="$BRAIN_DIR/brain/stack/registry.md"

mkdir -p "$FEEDS"

echo "🔄 Refreshing live feeds..."
echo ""

# ─── Check Python packages on PyPI ───────────────────────────────────────────

refresh_python() {
    echo "📦 Checking Python packages on PyPI..."
    local snapshot="$FEEDS/python-versions.json"
    echo "{" > "$snapshot"
    local first=true
    
    # Extract Python packages from registry
    grep "^| " "$REGISTRY" | grep -A1000 "## Python" | grep -B1000 "## JavaScript" | \
        grep "^| [a-z]" | awk -F'|' '{print $2}' | tr -d ' ' | while read -r pkg; do
        if [ -z "$pkg" ]; then continue; fi
        
        # Query PyPI
        local info
        info=$(curl -sf "https://pypi.org/pypi/$pkg/json" 2>/dev/null || echo "")
        if [ -n "$info" ]; then
            local version=$(echo "$info" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('info',{}).get('version','unknown'))" 2>/dev/null || echo "unknown")
            local released=$(echo "$info" | python3 -c "import sys,json; d=json.load(sys.stdin); urls=d.get('urls',[]); print(urls[0]['upload_time'][:10] if urls else 'unknown')" 2>/dev/null || echo "unknown")
            
            if [ "$first" = true ]; then first=false; else echo "," >> "$snapshot"; fi
            printf '  "%s": {"version": "%s", "released": "%s"}' "$pkg" "$version" "$released" >> "$snapshot"
            
            # Check if stale (> 1 year since last release)
            if [ "$released" != "unknown" ]; then
                local release_ts=$(date -d "$released" +%s 2>/dev/null || echo "0")
                local now_ts=$(date +%s)
                local age_days=$(( (now_ts - release_ts) / 86400 ))
                if [ "$age_days" -gt 365 ]; then
                    echo "  ⚠️  $pkg: last release $released ($age_days days ago)"
                else
                    echo "  ✓ $pkg: $version (released $released)"
                fi
            else
                echo "  ? $pkg: $version (release date unknown)"
            fi
        else
            echo "  ✗ $pkg: not found on PyPI"
        fi
    done
    
    echo "" >> "$snapshot"
    echo "}" >> "$snapshot"
    echo ""
}

# ─── Check Node packages on npm ──────────────────────────────────────────────

refresh_node() {
    echo "📦 Checking Node packages on npm..."
    local snapshot="$FEEDS/node-versions.json"
    echo "{" > "$snapshot"
    local first=true
    
    # Extract JS/TS packages from registry
    grep "^| " "$REGISTRY" | grep -A1000 "## JavaScript" | grep -B1000 "## Infrastructure" | \
        grep "^| [a-z@]" | awk -F'|' '{print $2}' | tr -d ' ' | while read -r pkg; do
        if [ -z "$pkg" ]; then continue; fi
        
        # Query npm
        local info
        info=$(curl -sf "https://registry.npmjs.org/$pkg/latest" 2>/dev/null || echo "")
        if [ -n "$info" ]; then
            local version=$(echo "$info" | python3 -c "import sys,json; print(json.load(sys.stdin).get('version','unknown'))" 2>/dev/null || echo "unknown")
            
            if [ "$first" = true ]; then first=false; else echo "," >> "$snapshot"; fi
            printf '  "%s": {"version": "%s"}' "$pkg" "$version" >> "$snapshot"
            echo "  ✓ $pkg: $version"
        else
            echo "  ✗ $pkg: not found on npm"
        fi
    done
    
    echo "" >> "$snapshot"
    echo "}" >> "$snapshot"
    echo ""
}

# ─── Check for deprecated packages ──────────────────────────────────────────

check_deprecated() {
    echo "🚨 Checking for newly deprecated packages..."
    local deprecated_file="$FEEDS/deprecated.json"
    echo "[]" > "$deprecated_file"
    
    # Known deprecated packages to always flag
    local known_deprecated=("moment" "request" "create-react-app" "enzyme" "node-sass" "tslint" "bower" "gulp")
    
    for pkg in "${known_deprecated[@]}"; do
        if grep -qi "$pkg" "$REGISTRY" 2>/dev/null; then
            echo "  🚨 WARNING: '$pkg' is in registry but DEPRECATED"
        fi
    done
    echo ""
}

# ─── Main ────────────────────────────────────────────────────────────────────

case "${1:-all}" in
    --python)  refresh_python ;;
    --node)    refresh_node ;;
    all|*)
        refresh_python
        refresh_node
        check_deprecated
        echo "✅ Feeds refreshed at $(date -u +%Y-%m-%dT%H:%M:%SZ)"
        echo "   Snapshots saved to: $FEEDS/"
        ;;
esac

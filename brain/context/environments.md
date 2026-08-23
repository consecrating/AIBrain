# Environments & Runtime Knowledge

> Facts about our runtime that prevent stupid mistakes.

## Kiro Web Sandbox

- **Python:** 3.11.15 at `/root/.pyenv/versions/3.11.15/bin`
- **Node:** v22 via nvm
- **Network:** OPEN_INTERNET (full access)
- **Git:** pre-configured (HTTPS, gh CLI authenticated)
- **Package managers:** pip, uv, pnpm, npm, yarn
- **ALWAYS prefix:** `export PATH="/root/.pyenv/versions/3.11.15/bin:$PATH"`

## What Works in Kiro Web

- ✅ All bash commands
- ✅ pip install (any package)
- ✅ git push, gh api (authenticated)
- ✅ Web fetch (any URL)
- ✅ File read/write
- ✅ MCP tools (playwright, 21st.dev, etc.)
- ✅ Sub-agents

## What Does NOT Work in Kiro Web

- ❌ `gh pr create` (use `gh api repos/.../pulls` instead)
- ❌ Interactive commands (use --yes, --non-interactive flags)
- ❌ Long-running processes (no dev servers, use --run for tests)
- ❌ `.kiro/agents/` (not read on Web — use skills instead)
- ❌ `.kiro/hooks/` agent actions (consume credits — use command actions)
- ❌ Model pinning in Autonomous mode

## Environment Variables (set by connect-all.sh)

```bash
export PATH="/root/.pyenv/versions/3.11.15/bin:$PATH"
export GOAAISEO_ROOT="/projects/sandbox/goaaiseo"
export GSA_SINK="jsonfile"
export GSA_SINK_PATH="/projects/sandbox/goaaiseo-seo-adapter/out/site.graph.json"
export SCRAPETOOL_OUTPUT="/projects/sandbox/ScrapeToolAi/output"
export KIRO_SKILLS_DIR="/projects/.kiro/skills"
```

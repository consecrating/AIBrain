# 🧠 AIBrain

**Persistent intelligence layer for Kiro** — solves the three problems that make AI coding assistants unreliable:

1. **Memory Loss** — Kiro forgets decisions, preferences, and context after compaction
2. **Poor Response Quality** — no curated knowledge base of proven patterns and your actual stack
3. **Outdated Dependencies** — defaults to training-data libraries instead of current, battle-tested ones

AIBrain is NOT another prompt engineering repo. It's a **structured knowledge graph** that Kiro reads at session start and queries during work — making every session as informed as your best session.

---

## The Problem (in detail)

| Symptom | Root Cause | AIBrain Fix |
|---------|-----------|-------------|
| "I already told you to use X" | Context compaction deletes old turns | Persistent decision log survives any session |
| Generates generic/bad code | No knowledge of YOUR patterns, stack, preferences | Curated pattern library with your proven solutions |
| Suggests deprecated packages | Training data is stale; doesn't check current state | Live registry with pinned versions + freshness checks |
| Forgets what files it changed | Memory is conversation-only | Change journal persisted to disk |
| Re-debates settled decisions | Rationale lost in compaction | Decision records with WHY, never re-litigated |
| Uses wrong coding style | No durable style enforcement | Executable style rules, not suggestions |

---

## Architecture

```
AIBrain/
├── brain/                          # The knowledge graph (the core)
│   ├── identity.md                 # WHO: your role, stack, preferences, non-negotiables
│   ├── decisions/                  # WHAT was decided and WHY (append-only log)
│   │   ├── _index.md              # Decision log with dates + status
│   │   └── *.md                   # Individual decision records
│   ├── patterns/                   # HOW: proven code patterns from YOUR repos
│   │   ├── _index.md              # Pattern catalog
│   │   └── *.md                   # Pattern files (problem → solution → usage)
│   ├── stack/                      # WITH WHAT: your approved technology stack
│   │   ├── registry.md            # Master dependency registry (pinned versions)
│   │   ├── banned.md              # Libraries/patterns explicitly rejected
│   │   └── alternatives.md        # "If you'd suggest X, use Y instead"
│   └── context/                    # WHERE: project-specific knowledge
│       ├── repos.md               # All repos, their purpose, how they connect
│       └── environments.md        # Runtime details, deploy targets, env vars
│
├── memory/                         # Session-persistent memory (survives compaction)
│   ├── active-task.md             # Current goal + constraints + next action
│   ├── journal.md                 # Append-only log of significant events
│   ├── corrections.md            # Things the user corrected (never repeat)
│   └── scratchpad.md              # Working memory for current session
│
├── rules/                          # Executable rules (not suggestions)
│   ├── response-quality.md        # Rules for generating better responses
│   ├── dependency-policy.md       # How to choose/validate packages
│   ├── code-style.md             # Your actual coding conventions
│   └── anti-patterns.md          # Specific mistakes to never make
│
├── feeds/                          # Live knowledge (refreshed periodically)
│   ├── registry-snapshot.json     # Current versions of approved packages
│   ├── deprecated.json            # Known deprecated packages to avoid
│   └── update-feeds.sh           # Script to refresh from npm/pypi/github
│
├── scripts/                        # Automation
│   ├── brain.sh                   # CLI: query, add, search the brain
│   ├── learn.sh                   # Capture a learning from this session
│   ├── refresh.sh                 # Update live feeds
│   ├── validate.sh               # Check brain integrity
│   └── install.sh                # Install AIBrain into any Kiro workspace
│
├── .kiro/                          # Kiro integration
│   ├── steering/
│   │   └── aibrain.md            # Always-on steering that loads the brain
│   └── skills/
│       └── aibrain/
│           └── SKILL.md          # The skill that powers brain queries
│
└── tests/                          # Self-tests
    └── validate-brain.sh          # Ensures no broken refs, no stale data
```

---

## How It Solves Each Problem

### 1. Memory Loss → Persistent Knowledge Graph

**Before:** Kiro forgets your decisions after ~30 turns (compaction).
**After:** Decisions live in `brain/decisions/`, read at session start.

```bash
# Record a decision
./scripts/brain.sh decide "Use Supabase not Firebase" \
  --reason "RLS, pgvector, self-hostable, OSS" \
  --context "goaaiseo database choice" \
  --alternatives "Firebase (vendor lock), PlanetScale (no vector)"

# At session start, Kiro reads:
# brain/decisions/_index.md → knows all settled decisions
# memory/active-task.md → knows what was in progress
# memory/corrections.md → knows what NOT to do again
```

### 2. Poor Responses → Curated Pattern Library

**Before:** Kiro generates generic boilerplate that doesn't match your codebase.
**After:** It checks `brain/patterns/` first and uses YOUR proven solutions.

```bash
# Add a pattern you've proven works
./scripts/brain.sh pattern add "api-error-handling" \
  --problem "Consistent error responses across FastAPI services" \
  --solution "patterns/api-error-handling.md" \
  --repos "goaaiseo,goaaiseo-seo-adapter"

# When Kiro generates API code, it checks patterns/ first
# and uses YOUR error handling shape, not a random tutorial's
```

### 3. Outdated Deps → Live Registry + Policy

**Before:** Kiro suggests `requests` (old) instead of `httpx` (current, async).
**After:** Registry pins what to use; banned list blocks what to avoid.

```markdown
<!-- brain/stack/registry.md -->
| Package | Version | Why | Replaces |
|---------|---------|-----|----------|
| httpx | >=0.25 | async, HTTP/2, modern | requests |
| lxml | >=4.9 | fast XML/HTML parsing | html.parser |
| pydantic | >=2.0 | validation + serialization | dataclasses for APIs |
| ruff | >=0.4 | replaces flake8+isort+black | flake8, black, isort |

<!-- brain/stack/banned.md -->
| Package | Reason | Use Instead |
|---------|--------|-------------|
| requests | sync-only, no HTTP/2 | httpx |
| flask | sync, no typing | FastAPI |
| moment.js | deprecated, huge | date-fns or dayjs |
| create-react-app | deprecated | Vite or Next.js |
```

---

## The Steering File (what makes it work)

`AIBrain/.kiro/steering/aibrain.md` is an always-on file that instructs Kiro:

1. **At session start:** Read `brain/identity.md` + `memory/active-task.md` + `brain/decisions/_index.md`
2. **Before choosing a library:** Check `brain/stack/registry.md` and `brain/stack/banned.md`
3. **Before writing code:** Check `brain/patterns/` for an existing pattern that applies
4. **After any decision:** Append to `brain/decisions/_index.md`
5. **When corrected:** Append to `memory/corrections.md` and classify for promotion
6. **Before reporting done:** Verify against `memory/active-task.md` criteria

---

## Quick Start

```bash
# Clone into your workspace
git clone https://github.com/consecrating/AIBrain.git
cd AIBrain

# Initialize with your identity
./scripts/brain.sh init

# Install into active Kiro workspace
./scripts/install.sh

# Add your first decisions
./scripts/brain.sh decide "Python 3.11+ for all services"
./scripts/brain.sh decide "Use httpx not requests"
./scripts/brain.sh decide "FastAPI for all Python APIs"

# Add your stack
./scripts/brain.sh stack add httpx ">=0.25" --replaces requests
./scripts/brain.sh stack ban requests --reason "sync-only" --use httpx

# Refresh live feeds
./scripts/refresh.sh
```

---

## Integration with Existing Repos

AIBrain connects to your workspace repos:

```
AIBrain (knowledge layer)
   │
   ├── informs → GOAAISEO (architecture decisions, API patterns)
   ├── informs → goaaiseo-seo-adapter (coding patterns, dep choices)
   ├── informs → ScrapeToolAi (stealth patterns, dep policy)
   ├── powered by → Claude-Power (engineering skills read brain)
   └── powered by → All-Skills (design skills read brand identity)
```

---

## Design Principles

1. **Files > conversation** — anything important lives on disk, not in chat history
2. **Append-only decisions** — never silently reverse; log reversals with rationale
3. **Executable rules** — not "try to remember", but "check this file before acting"
4. **Minimal always-on cost** — index files are tiny; detail loads on demand
5. **Human-readable** — every file is Markdown you can read and edit directly
6. **Self-validating** — `validate.sh` catches broken refs and stale entries

---

## vs. Claude-Power's context-durability

Claude-Power's `context-durability` skill handles **within-task** memory (one feature, one PR).
AIBrain handles **cross-session, cross-project** memory (your entire development identity).

| | context-durability | AIBrain |
|---|---|---|
| Scope | One task | All tasks, all repos |
| Lifespan | Until task completes | Permanent |
| Content | Task state, next action | Decisions, patterns, stack, identity |
| Trigger | Long session | Every session |
| Location | `.kiro/.memory/` | `AIBrain/brain/` |

They complement each other: context-durability saves task progress, AIBrain saves everything else.

---

## License

MIT

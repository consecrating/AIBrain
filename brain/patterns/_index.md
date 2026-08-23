# Pattern Library Index

> Proven patterns from OUR codebases. Check here BEFORE generating new code.
> Each pattern is battle-tested and should be used as-is unless there's a specific reason not to.

## Python Patterns

| ID | Pattern | Source Repo | File |
|----|---------|-------------|------|
| PY-001 | Stealth HTTP fetching with auto-escalation | ScrapeToolAi | `patterns/py-stealth-fetch.md` |
| PY-002 | stdlib-only adapter with pluggable sinks | goaaiseo-seo-adapter | `patterns/py-adapter-sinks.md` |
| PY-003 | Pydantic v2 models with validation | goaaiseo-seo-adapter | `patterns/py-pydantic-models.md` |
| PY-004 | FastAPI service with health check + graceful shutdown | GOAAISEO | `patterns/py-fastapi-service.md` |
| PY-005 | CLI with argparse subcommands | goaaiseo-seo-adapter | `patterns/py-cli-argparse.md` |

## TypeScript Patterns

| ID | Pattern | Source Repo | File |
|----|---------|-------------|------|
| TS-001 | Next.js 15 App Router page with RSC | GOAAISEO | `patterns/ts-nextjs-page.md` |
| TS-002 | TanStack Query with optimistic updates | GOAAISEO | `patterns/ts-tanstack-query.md` |
| TS-003 | Zod schema → type → validation pipeline | GOAAISEO | `patterns/ts-zod-pipeline.md` |

## Architecture Patterns

| ID | Pattern | Source Repo | File |
|----|---------|-------------|------|
| AR-001 | Graph sink protocol (pluggable persistence) | goaaiseo-seo-adapter | `patterns/ar-graph-sink.md` |
| AR-002 | 3-tier escalation with domain caching | ScrapeToolAi | `patterns/ar-escalation.md` |
| AR-003 | Confidence-gated action candidates | goaaiseo-seo-adapter | `patterns/ar-confidence-gate.md` |
| AR-004 | Closed-loop feedback (act → measure → learn) | GOAAISEO | `patterns/ar-closed-loop.md` |

## How to Add a Pattern

```bash
./scripts/brain.sh pattern add "pattern-name" \
  --problem "What problem does this solve" \
  --solution "The code/approach (or path to file)" \
  --source "Which repo it's from" \
  --when "When to apply this pattern"
```

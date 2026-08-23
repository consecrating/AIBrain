---
name: aibrain
description: "AIBrain v2 local intelligence runtime — durable structured memory, ranked recall, compact context packs, dependency evidence, project profiles, super-skill routing, snapshots, and self-healing diagnostics. Activate for session startup, knowledge retrieval, package selection, architecture decisions, cross-repo work, corrections, or context recovery."
metadata:
  version: "2.0"
  author: consecrating
---

# AIBrain v2

AIBrain is a local-first intelligence runtime. Its core uses only Python's standard library and keeps every result inspectable and attributable.

## Start here

```bash
KIRO_ROOT="${KIRO_DIR:-/projects/.kiro}"
BRAIN_ROOT="${AIBRAIN_ROOT:-$(cat "$KIRO_ROOT/.aibrain-path" 2>/dev/null)}"
BRAIN="$BRAIN_ROOT/scripts/brain.sh"
$BRAIN status
$BRAIN context "the current task" --profile auto
$BRAIN skills route "the current task"
```

## Durable knowledge

```bash
$BRAIN remember "Use tenant-scoped query keys" --kind preference --scope goaaiseo --tags react,security
$BRAIN forget mem-123456789abc --reason "Superseded by DEC-014"
$BRAIN decide "Keep the adapter core stdlib-only" --reason "Portable ingestion" --context "gsa"
$BRAIN correct "Used an unverified package" --do-instead "Check registry evidence first" --scope always
$BRAIN ingest ./research.md --kind reference --scope goaaiseo --tags seo,evidence
```

## Retrieval and routing

```bash
$BRAIN recall "tenant isolation" --limit 8
$BRAIN context "add a crawl scheduler" --profile auto --budget 1800
$BRAIN profile auto /projects/sandbox/ScrapeToolAi
$BRAIN skills route "resolve dependency conflict"
$BRAIN index build
```

## Health and recovery

```bash
$BRAIN doctor
$BRAIN snapshot create before-migration
$BRAIN snapshot verify before-migration
$BRAIN stats --json
```

## Compatibility

All v1 commands and positional forms remain supported: `status`, `recall`, `decide`, `correct`, `stack add`, `stack ban`, `journal`, `next`, `validate`, and `stats`.

## Operating contract

1. Retrieve before regenerating.
2. Cite the source of recalled knowledge.
3. Keep time-sensitive facts scoped and expiring.
4. Never silently delete or promote knowledge.
5. Resolve contradictions explicitly and preserve history.
6. Run doctor before claiming the brain is healthy.

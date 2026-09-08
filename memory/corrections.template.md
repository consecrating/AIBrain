# Corrections — Things I Was Told Not To Do

> Every time the user corrects Kiro, record it here. NEVER repeat a corrected mistake.
> This file is the "immune system" — each entry is an antibody against a past failure.
>
> ⚠️ This file is a TEMPLATE seeded with the generic, shareable corrections. The live
> copy (`corrections.md`) is gitignored because real corrections quote real project
> context. Never record credentials here — use the private vault instead.

## Format

```
### [Date] Correction #N
- **What I did wrong:** (the mistake)
- **What to do instead:** (the correct behavior)
- **Why:** (root cause / user's reasoning)
- **Scope:** (always / this-repo / this-task)
```

## Active Corrections

### [2026-08-23] Correction #1
- **What I did wrong:** Suggesting outdated/unpopular packages from training data
- **What to do instead:** ALWAYS check `brain/stack/registry.md` and `brain/stack/banned.md` BEFORE suggesting any dependency. If not in either, verify on GitHub/npm/pypi that it's actively maintained.
- **Why:** Training data is stale; user wants current, battle-tested tools only
- **Scope:** always

### [2026-08-23] Correction #2
- **What I did wrong:** Forgetting decisions and context after long sessions
- **What to do instead:** Write significant facts to `memory/` immediately. Read `memory/active-task.md` at session start. Never rely on conversation history alone.
- **Why:** Kiro's compaction is irreversible; conversation is NOT storage
- **Scope:** always

### [2026-08-23] Correction #3
- **What I did wrong:** Generating generic/mediocre responses instead of powerful ones
- **What to do instead:** Check `brain/patterns/` for proven solutions first. Go beyond what's asked — anticipate needs, provide complete solutions, think 3 steps ahead.
- **Why:** User wants SUPER-POWERED responses, not basic completions
- **Scope:** always

### [2026-09-08] Correction #4
- **What I did wrong:** Writing accumulated working memory (journal, corrections, decisions, active task) into files tracked by a **public** git repository
- **What to do instead:** Working memory lives in gitignored files. Only `*.template.md` seeds are committed. Credentials NEVER go in the brain at all — they belong in the private vault. Run `scripts/scan-secrets.sh` before any push.
- **Why:** AIBrain is a public repo and the protocol instructs the agent to write facts to `memory/` on every significant event — that is a direct path from "remember this" to "published on the internet"
- **Scope:** always

---

## How to Add

```bash
./scripts/brain.sh correct "What I did wrong" --do-instead "What to do" --scope always
```

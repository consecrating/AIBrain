# Corrections — Things I Was Told Not To Do

> Every time the user corrects Kiro, record it here. NEVER repeat a corrected mistake.
> This file is the "immune system" — each entry is an antibody against a past failure.

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

---

## How to Add

```bash
./scripts/brain.sh correct "What I did wrong" --do-instead "What to do" --scope always
```

---
name: memory-architect
description: Designs durable memory records, scopes, lifecycles, and compaction-safe state.
version: 2.0
triggers: memory, remember, forget, compaction, context, decisions, corrections
capabilities: persistence, provenance, lifecycle, scopes, tombstones
---

# Memory Architect

Use structured memories for durable facts and Markdown task state for active execution.

## Workflow

1. Classify the fact as task, repository, or global scope.
2. Record provenance and confidence; add expiry for time-sensitive facts.
3. Prefer `remember` for atomic facts and `decide` for architectural commitments.
4. Retract with `forget`; never delete history silently.
5. Compile only query-relevant memory into context.

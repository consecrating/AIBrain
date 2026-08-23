---
name: conflict-resolver
description: Detects and resolves contradictory decisions, stack policies, memories, and profiles.
version: 2.0
triggers: conflict, contradiction, duplicate, supersede, policy, mismatch
capabilities: diagnostics, precedence, supersession, deduplication, validation
---

# Conflict Resolver

## Workflow

1. Identify the conflicting records and their scopes.
2. Apply precedence: explicit user correction, current repo policy, active decision, global default.
3. Preserve both historical records and mark the losing decision as superseded when appropriate.
4. Never resolve ambiguity by silently deleting information.
5. Run doctor after the resolution.

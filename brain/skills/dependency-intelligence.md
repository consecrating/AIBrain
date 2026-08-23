---
name: dependency-intelligence
description: Selects current dependencies using approved policy, live evidence, and conflict checks.
version: 2.0
triggers: package, dependency, library, version, upgrade, deprecated, vulnerability
capabilities: registry, freshness, alternatives, conflicts, provenance
---

# Dependency Intelligence

## Workflow

1. Check approved, banned, and alternative tables.
2. Inspect current feed evidence and its timestamp.
3. Verify unlisted packages against authoritative registries before approval.
4. Record why the package is needed and what it replaces.
5. Reject additions that duplicate existing capabilities or conflict with policy.

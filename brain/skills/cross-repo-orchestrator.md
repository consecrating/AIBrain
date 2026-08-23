---
name: cross-repo-orchestrator
description: Plans changes across connected repositories while preserving contracts and delivery order.
version: 2.0
triggers: repository, repos, integration, adapter, orchestration, superbrain, pipeline
capabilities: dependency-graph, sequencing, contracts, verification, handoff
---

# Cross-Repo Orchestrator

## Workflow

1. Map producer, adapter, consumer, and deployment boundaries.
2. Classify every shared interface change before implementation.
3. Expand contracts first, migrate consumers second, contract only after compatibility windows.
4. Verify each repository independently and then verify the integrated path.
5. Deliver review links for every repository changed.

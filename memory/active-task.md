# Active Task

> Updated at every significant state change. Read at session start to resume.
> This is the FIRST file to check when starting a new session.

## Current State

- **Goal:** Upgrade AIBrain to v2 with durable structured memory, ranked recall, project profiles, knowledge ingestion, conflict/freshness checks, and routable super skills
- **Status:** 🚀 Ready to Ship — implementation, profile-boundary hardening, and final verification complete
- **Started:** 2026-08-23
- **Last Updated:** 2026-08-23

## Constraints

1. Preserve all v1 CLI commands and positional forms
2. Keep the core standard-library only and local-first
3. Preserve Markdown knowledge as a human-readable source of truth
4. Remain compatible with Kiro Web and SuperBrain's fixed install paths
5. Use safe, atomic writes for mutable state
6. Do not silently execute remote content or promote corrections globally

## Acceptance Criteria

- [x] Current architecture and compatibility contracts mapped
- [x] Additive v2 architecture documented
- [x] Stable `brain.sh` launcher backed by a stdlib Python intelligence core
- [x] Ranked recall and compact context compilation operational
- [x] Structured remember/forget/ingest memory store operational
- [x] Project profile detection and super-skill routing operational
- [x] Doctor detects conflicts, stale state, invalid schemas, and dangling references
- [x] Refresh and install flows use atomic writes and propagate failures
- [x] Kiro skill/steering and README document implemented behavior
- [x] Focused command verification passes
- [ ] Feature branch pushed with a reviewable pull request

## Next Action

Stage the reviewed files explicitly, commit the v2 upgrade, push `feat/aibrain-v2`, and open the pull request

## Decisions Made

- Retain `brain.sh` as the public entry point and delegate to `scripts/aibrain.py`
- Use deterministic weighted lexical retrieval instead of a mandatory embedding dependency
- Store structured memories as append-only JSONL events with tombstones
- Keep local file ingestion in core; fetch externally, then ingest
- Treat SuperBrain paths and installed Kiro artifact names as public contracts

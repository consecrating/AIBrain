---
inclusion: always
description: AIBrain v2 — persistent memory, ranked context, dependency evidence, profiles, skills, and self-healing diagnostics.
---

# AIBrain v2 Protocol

Resolve the brain from `AIBRAIN_ROOT`, the active Kiro `.aibrain-path`, or the repository containing `scripts/brain.sh`.

## Session start

1. Run `scripts/brain.sh status`.
2. Read `brain/identity.md`, `memory/active-task.md`, and `memory/corrections.md`.
3. Compile task context with `scripts/brain.sh context "<task>" --profile auto` for non-trivial work.
4. If status reports a stale index, run `scripts/brain.sh index build`.

## Before dependencies

Check `brain/stack/registry.md`, `banned.md`, and `alternatives.md`, then inspect current feed evidence. Verify unlisted packages against an authoritative source before approval.

## Before code

Route the task with `scripts/brain.sh skills route "<task>"`, inspect relevant local patterns, and follow the detected project profile.

## Durable writes

- Fact or preference: `brain.sh remember ...`
- Architectural commitment: `brain.sh decide ...`
- User correction: `brain.sh correct ...`
- Proven implementation: `brain.sh pattern add ...`
- Local research artifact: `brain.sh ingest FILE ...`

Use the CLI instead of editing structured stores directly; it provides locking, provenance, escaping, and atomic writes.

## Completion

Run `scripts/brain.sh doctor`, verify the acceptance criteria in `memory/active-task.md`, and report anything that remains unverified.

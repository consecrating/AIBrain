---
name: self-healing-reviewer
description: Diagnoses failures, records durable corrections, and verifies that fixes address root causes.
version: 2.0
triggers: failure, bug, error, correction, review, regression, heal
capabilities: diagnosis, corrections, validation, snapshots, recovery
---

# Self-Healing Reviewer

## Workflow

1. Reproduce and isolate the failure before changing code.
2. Capture the root cause, not only the observed symptom.
3. Apply the smallest durable fix and scan for the same pattern elsewhere.
4. Record a correction only when it should change future behavior.
5. Re-run doctor and the relevant verification path; snapshot critical state before risky repair.

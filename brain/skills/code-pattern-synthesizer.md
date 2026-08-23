---
name: code-pattern-synthesizer
description: Finds local precedents and turns repeated implementation shapes into reusable patterns.
version: 2.0
triggers: pattern, code, implementation, refactor, duplicate, precedent
capabilities: synthesis, reuse, consistency, examples, anti-patterns
---

# Code Pattern Synthesizer

## Workflow

1. Trace an existing successful implementation end to end.
2. Separate invariant structure from project-specific details.
3. Capture problem, usage trigger, solution, and source repository.
4. Add a pattern only when it is proven or deliberately adopted.
5. Link rejected anti-patterns so future generation avoids them.

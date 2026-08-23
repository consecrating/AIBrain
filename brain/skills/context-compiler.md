---
name: context-compiler
description: Builds compact task-specific context from profiles, ranked knowledge, decisions, and corrections.
version: 2.0
triggers: context, prompt, token, compact, resume, profile, task
capabilities: ranking, budgeting, profiles, citations, compression
---

# Context Compiler

## Workflow

1. Auto-detect the project profile from repository markers.
2. Retrieve relevant corrections, decisions, stack policy, and patterns.
3. Rank by query fit, source authority, confidence, and freshness.
4. Enforce a context budget and preserve source citations.
5. Exclude scratch data and unrelated knowledge.

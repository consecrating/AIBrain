# Active Task

> Updated at every significant state change. Read at session start to resume.
> This is the FIRST file to check when starting a new session.

## Current State

- **Goal:** Build AIBrain as a super-powered intelligence layer for Kiro
- **Status:** 🔨 In Progress — Core structure built, scripts needed
- **Started:** 2026-08-23
- **Last Updated:** 2026-08-23

## Constraints

1. Must work in Kiro Web sandbox (no IDE features)
2. Must survive context compaction (everything on disk)
3. Must be installable into any workspace
4. Must be super-powered — autonomous execution, live intelligence, self-healing

## Acceptance Criteria

- [ ] Brain structure complete (identity, decisions, patterns, stack, context)
- [ ] Memory system working (active-task, journal, corrections, scratchpad)
- [ ] Rules engine complete (response quality, dep policy, code style, anti-patterns)
- [ ] Live feeds system (registry snapshots, deprecated detection)
- [ ] Scripts operational (brain.sh, learn.sh, refresh.sh, validate.sh, install.sh)
- [ ] Kiro integration (steering + skill that reads the brain)
- [ ] Super-powers: autonomous multi-step execution
- [ ] Super-powers: live web intelligence (verify before suggesting)
- [ ] Super-powers: self-healing (detect and fix own mistakes)
- [ ] Super-powers: cross-repo orchestration
- [ ] Pushed to GitHub

## Next Action

Build the super-power scripts and rules engine

## Decisions Made

- AIBrain is a repo, not just config files (portable, versioned, shareable)
- Complements Claude-Power's context-durability (that's per-task, this is cross-session)
- Markdown-first for human readability + AI parsability
- Scripts use bash for zero-dep execution

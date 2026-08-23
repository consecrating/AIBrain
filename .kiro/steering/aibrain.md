---
inclusion: always
description: AIBrain — persistent intelligence layer. Prevents memory loss, ensures response quality, blocks outdated dependencies.
---

# AIBrain Protocol

You have a persistent brain at `/projects/sandbox/AIBrain`. It survives sessions.

## At Session Start (ALWAYS do this)

1. Read `AIBrain/memory/active-task.md` — know what was in progress
2. Read `AIBrain/memory/corrections.md` — know what NOT to repeat
3. Skim `AIBrain/brain/decisions/_index.md` — know what's settled

## Before Suggesting ANY Package/Library

1. Check `AIBrain/brain/stack/registry.md` — is it approved? Use that version.
2. Check `AIBrain/brain/stack/banned.md` — is it banned? Use the alternative.
3. Check `AIBrain/brain/stack/alternatives.md` — is there a better modern option?
4. If not in any list: verify on the web that it's current + maintained before suggesting

## Before Writing Code

1. Check `AIBrain/brain/patterns/` — does a proven pattern exist for this?
2. Follow `AIBrain/rules/code-style.md` — types, async, naming conventions
3. Scan `AIBrain/rules/anti-patterns.md` — don't make the Fatal Fifteen mistakes
4. Apply `AIBrain/rules/response-quality.md` — be SUPER-POWERED, not basic

## After Any Decision

Append to `AIBrain/brain/decisions/_index.md` or run:
```bash
/projects/sandbox/AIBrain/scripts/brain.sh decide "the decision" "the reason"
```

## When Corrected by the User

Append to `AIBrain/memory/corrections.md` or run:
```bash
/projects/sandbox/AIBrain/scripts/brain.sh correct "what went wrong" "what to do instead"
```

## Before Reporting Done

Check `AIBrain/memory/active-task.md` acceptance criteria — every one must be verified.

## The Quality Bar

Every response must be:
- **Complete** — no `...` or `TODO` or missing pieces
- **Current** — only actively maintained packages/patterns
- **Correct** — verified it actually works (run it, test it)
- **Contextual** — uses OUR patterns, not generic ones
- **Super-powered** — anticipates next needs, connects dots, saves hours

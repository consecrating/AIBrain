---
inclusion: always
description: AIBrain — persistent intelligence layer. Prevents memory loss, ensures response quality, blocks outdated dependencies.
---

# AIBrain Protocol

You have a persistent brain at `/projects/sandbox/AIBrain`. It survives sessions.

## 🔒 NEVER Put Secrets In The Brain (read this first)

**This repository is PUBLIC.** Every instruction below tells you to persist facts to
disk — which makes this the single highest-risk rule in the protocol.

1. **NEVER** write credentials, passwords, application passwords, API keys, tokens,
   FTP/SSH/SFTP logins, or connection strings into ANY brain file. Not into memory,
   not into decisions, not into journal, not "temporarily".
2. Credentials belong in the **private vault**, never here. Reference them by
   name only — e.g. "WP app password for sanctify.in is in the vault", never the value.
3. Live working memory (`memory/*.md`, `brain/decisions/_index.md`) is **gitignored**.
   Only `*.template.md` seeds are committed. Never `git add -f` a live memory file.
4. Before any `git push` from this repo, run:
   ```bash
   bash /projects/sandbox/AIBrain/scripts/scan-secrets.sh --all
   ```
5. Treat client names, hostnames, and internal URLs as sensitive-by-default. Prefer
   "the client's staging site" over a real subdomain in anything committed.

If you are ever unsure whether something is safe to persist: **do not persist it**,
and ask the user.

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

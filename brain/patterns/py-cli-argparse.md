# Backward-Compatible Argparse CLI

- **ID:** PY-005
- **Problem:** A CLI must add capabilities without breaking existing scripts.
- **Use when:** Extending a public command surface.
- **Source:** AIBrain / goaaiseo-seo-adapter

## Solution

Retain command names, positional forms, defaults, and exit semantics. Add optional flags and subcommands additively, validate at the boundary, emit stable structured JSON when requested, and keep human output concise.

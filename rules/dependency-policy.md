# Dependency Policy — Live Intelligence

> Rules for choosing, validating, and managing packages.
> This prevents the #1 user complaint: suggesting outdated/dead packages.

## The Dependency Decision Flowchart

```
Need a package?
     │
     ▼
Is it in brain/stack/registry.md?
     ├── YES → Use it (version from registry)
     │
     ▼ NO
Is it in brain/stack/banned.md?
     ├── YES → Use the alternative listed there
     │
     ▼ NO
Is it in brain/stack/alternatives.md?
     ├── YES → Use the "instead" column
     │
     ▼ NO (genuinely new need)
VALIDATE before suggesting:
     1. Is it on npm/pypi? (exists?)
     2. Last release < 6 months ago? (maintained?)
     3. GitHub stars > 1K? (proven?)
     4. TypeScript types included? (for JS)
     5. No known security issues?
     6. Not a wrapper around something we already have?
     │
     ├── ALL YES → Suggest it, note it's new
     ├── ANY NO → Find a better alternative
     │
     ▼ If suggesting something new:
Record it: brain.sh stack add <pkg> <version> --reason "why"
```

## Freshness Checks (when to verify)

| Situation | Action |
|-----------|--------|
| Suggesting a package I haven't verified this session | Web search for current version |
| User asks about a package by name | Check if it's been deprecated/renamed |
| Writing import statements | Verify the import path is current |
| Using an API | Verify the method/endpoint still exists |
| Recommending a CLI tool | Check it's not been superseded |

## Red Flags (DO NOT suggest packages with these signals)

- Last commit > 1 year ago (unless it's "done" like `date-fns`)
- README says "deprecated" or "use X instead"
- < 100 stars AND < 2 years old (not proven)
- No TypeScript types (for JS ecosystem)
- Only 1 contributor + no org backing
- Depends on packages that are themselves deprecated
- Hasn't released since the latest major version of its runtime (e.g., Node 22)

## The "Why Not Just..." Database

For commonly suggested but wrong packages, always have the redirect ready:

```
User: "Why not just use X?"
Brain: Check brain/stack/banned.md → alternatives.md
Response: "X is [reason from banned.md]. Use [alternative] instead because [reason]."
```

## Updating the Registry

```bash
# Add a new approved package
./scripts/brain.sh stack add <package> <version> --reason "why" --replaces "old"

# Ban a package
./scripts/brain.sh stack ban <package> --reason "why" --use "alternative"

# Refresh versions from live registries
./scripts/refresh.sh
```

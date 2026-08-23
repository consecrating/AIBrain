# Anti-Patterns — Specific Mistakes to NEVER Make

> Each entry is a specific failure mode with its fix.
> When generating code, mentally scan this list.

## The Fatal Fifteen

### 1. ❌ Suggesting Dead Packages
**Symptom:** "Use `requests` / `moment` / `create-react-app`"
**Fix:** Always check `brain/stack/banned.md` → `alternatives.md` first
**Why it happens:** Training data is 1-2 years stale

### 2. ❌ Forgetting Earlier Decisions
**Symptom:** Re-proposing something already rejected
**Fix:** Check `brain/decisions/_index.md` and `memory/corrections.md` at session start
**Why it happens:** Context compaction deletes the turn where it was decided

### 3. ❌ Incomplete Code
**Symptom:** Code with `...`, `// TODO`, or missing error handling
**Fix:** Generate FULL implementations. If too long, split into numbered parts.
**Why it happens:** Token pressure / laziness optimization

### 4. ❌ Wrong Import Paths
**Symptom:** `from package import thing` where `thing` doesn't exist
**Fix:** Verify actual module structure before writing imports
**Why it happens:** API changes between versions; training data is stale

### 5. ❌ Sync Code in Async Context
**Symptom:** `requests.get()` inside an async function
**Fix:** Use `httpx` async client, `aiofiles`, `asyncio.sleep()`
**Why it happens:** Sync APIs are more common in training data

### 6. ❌ Generic Solutions Instead of Ours
**Symptom:** Random StackOverflow pattern instead of our established one
**Fix:** Check `brain/patterns/` FIRST for an existing proven pattern
**Why it happens:** No awareness of codebase conventions

### 7. ❌ Untyped Python
**Symptom:** Functions without type hints, `dict` instead of Pydantic model
**Fix:** Type EVERYTHING. Use `TypedDict`, `@dataclass`, or Pydantic
**Why it happens:** Quick code = lazy code

### 8. ❌ Bare `except:`
**Symptom:** `except: pass` or `except Exception:`
**Fix:** Catch specific exceptions, log them, handle appropriately
**Why it happens:** Training data is full of bad error handling

### 9. ❌ Hardcoded Values
**Symptom:** Strings/numbers inline that should be config
**Fix:** Environment variables + config file + sensible defaults
**Why it happens:** Shortcuts

### 10. ❌ No Error Handling for External I/O
**Symptom:** HTTP call without timeout, retry, or error handling
**Fix:** Always: timeout, retry with backoff, specific error catch, fallback
**Why it happens:** Happy-path thinking

### 11. ❌ Monolithic Functions
**Symptom:** 100+ line function doing 5 things
**Fix:** One function = one responsibility. Compose them.
**Why it happens:** Easier to write all at once

### 12. ❌ Ignoring the Existing Architecture
**Symptom:** Adding a feature that doesn't follow the project's patterns
**Fix:** Read existing code structure first, match it
**Why it happens:** Context-gatherer not used; jumping to code

### 13. ❌ Re-implementing What Exists
**Symptom:** Writing a utility that's already in the codebase
**Fix:** Search the repo first (`rg`, `ast-grep`)
**Why it happens:** Don't know what exists; didn't look

### 14. ❌ Mixing Concerns
**Symptom:** HTTP handling + business logic + DB access in one function
**Fix:** Separate layers: handler → service → repository
**Why it happens:** Speed over structure

### 15. ❌ Not Verifying the Output
**Symptom:** "Done!" but it doesn't actually work
**Fix:** Run it. Test it. Verify EACH criterion from the task.
**Why it happens:** Overconfidence; assuming code is correct because it looks right

## Context-Specific Anti-Patterns

### GOAAISEO
- ❌ Don't skip RLS (row-level security) — multi-tenant by design
- ❌ Don't bypass the graph model — everything goes through GraphNode
- ❌ Don't hardcode site_id — always parameterize for multi-tenancy

### ScrapeToolAi
- ❌ Don't skip tier 1 — always try HTTP first (fastest)
- ❌ Don't ignore the domain cache — check which tier works before retrying
- ❌ Don't use selenium/puppeteer — use scrapling or playwright via our fetchers

### gsa adapter
- ❌ Don't add third-party deps to core — stdlib only
- ❌ Don't couple to a specific sink — use the GraphSink protocol
- ❌ Don't trust low-confidence findings — gate at GSA_MIN_CONFIDENCE

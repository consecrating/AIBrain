# Decision Log

> Append-only. Never silently reverse a decision. To change one, add a new entry
> that explicitly supersedes it with rationale.

| # | Date | Decision | Status | Context |
|---|------|----------|--------|---------|
| 001 | 2024-08 | Use Supabase (Postgres+pgvector) as primary database | ✅ Active | GOAAISEO — need RLS, vector search, OSS-compatible |
| 002 | 2024-08 | Python 3.11+ for all backend services | ✅ Active | Performance (task groups), typing (Self, TypeVarTuple) |
| 003 | 2024-08 | httpx over requests for all HTTP | ✅ Active | Async, HTTP/2, modern API |
| 004 | 2024-08 | FastAPI for all Python API services | ✅ Active | Async, typing, auto-docs, Pydantic v2 |
| 005 | 2024-08 | Next.js 15 (App Router) for frontend | ✅ Active | RSC, server actions, streaming |
| 006 | 2024-08 | stdlib-only core for gsa adapter | ✅ Active | Zero dep install for normalization layer |
| 007 | 2024-08 | 3-tier fetch escalation (HTTP→Stealth→Playwright) | ✅ Active | ScrapeToolAi — balance speed vs. bypass |
| 008 | 2024-08 | Kiro skills split: All-Skills (design) + Claude-Power (engineering) | ✅ Active | Separation of concerns, independent updates |

## Decision Template

```markdown
### DEC-NNN: [Title]
- **Date:** YYYY-MM-DD
- **Status:** Active / Superseded by DEC-XXX / Rejected
- **Context:** Why this decision was needed
- **Decision:** What was decided
- **Alternatives rejected:**
  - Option B — why not
  - Option C — why not
- **Consequences:** What this enables/constrains going forward
```

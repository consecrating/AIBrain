# Code Style Rules

> Enforceable conventions. Not preferences — RULES.
> Kiro must follow these in ALL generated code.

## Python Style

```python
# ✅ YES — Type hints on everything
def process_report(report: SeoReport, *, site_id: str) -> IngestResult:
    """Process a report into normalized graph nodes."""
    ...

# ❌ NO — Untyped functions
def process_report(report, site_id):
    ...

# ✅ YES — Keyword-only args after *
def fetch(url: str, *, timeout: float = 30, follow_redirects: bool = True) -> Response:
    ...

# ✅ YES — Dataclasses/Pydantic for models, not plain dicts
@dataclass
class GraphNode:
    node_id: str
    node_type: str
    properties: dict[str, Any]

# ❌ NO — Dict as a data model
node = {"node_id": "...", "node_type": "...", "properties": {...}}

# ✅ YES — Async for I/O
async def fetch_page(url: str) -> str:
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        return response.text

# ❌ NO — Sync I/O in async codebase
def fetch_page(url: str) -> str:
    return requests.get(url).text

# ✅ YES — Context managers for resources
async with httpx.AsyncClient() as client:
    ...

# ✅ YES — f-strings, not format() or %
msg = f"Processed {count} nodes for site {site_id}"

# ✅ YES — pathlib, not os.path
path = Path(__file__).parent / "data" / "output.json"

# ✅ YES — Specific exceptions
except httpx.HTTPStatusError as e:
    logger.error(f"HTTP {e.response.status_code}: {e.request.url}")

# ❌ NO — Bare except
except:
    pass
```

## TypeScript Style

```typescript
// ✅ YES — Explicit return types on exports
export function calculateScore(metrics: PageMetrics): ScoreResult {
  ...
}

// ✅ YES — Zod for runtime validation, infer types
const PageSchema = z.object({
  url: z.string().url(),
  title: z.string().min(1),
  score: z.number().min(0).max(100),
});
type Page = z.infer<typeof PageSchema>;

// ✅ YES — const assertions for literals
const TIERS = ['http', 'stealth', 'browser'] as const;
type Tier = typeof TIERS[number];

// ❌ NO — enums (use union types or const assertions)
enum Tier { Http, Stealth, Browser }

// ✅ YES — Discriminated unions for state
type FetchResult =
  | { status: 'success'; data: Page; cached: boolean }
  | { status: 'blocked'; tier: Tier; retryAfter?: number }
  | { status: 'error'; error: Error; recoverable: boolean };

// ✅ YES — Server components by default (Next.js 15)
// Only add "use client" when you need interactivity

// ✅ YES — Suspense boundaries for async
<Suspense fallback={<Skeleton />}>
  <AsyncComponent />
</Suspense>
```

## File Organization

```
# Python
- One class per file (unless tightly coupled)
- __init__.py exports public API only
- _private.py for internal helpers (underscore prefix)
- tests/ mirrors src/ structure

# TypeScript
- Colocate components with their styles/tests
- page.tsx, layout.tsx, loading.tsx, error.tsx (Next.js conventions)
- lib/ for shared utilities
- No barrel files (index.ts re-exports)
```

## Naming

| Thing | Convention | Example |
|-------|-----------|---------|
| Python files | snake_case | `http_fetcher.py` |
| Python classes | PascalCase | `GraphNode` |
| Python functions | snake_case | `ingest_seo_report` |
| Python constants | UPPER_SNAKE | `MAX_RETRIES` |
| TS files | kebab-case | `use-fetch-page.ts` |
| TS components | PascalCase | `ScoreCard.tsx` |
| TS functions | camelCase | `calculateScore` |
| TS types/interfaces | PascalCase | `PageMetrics` |
| CSS classes | Tailwind utilities | `className="flex items-center gap-2"` |
| Env vars | UPPER_SNAKE | `GSA_MIN_CONFIDENCE` |
| CLI commands | kebab-case | `gsa ingest`, `scrapetool fetch` |

## Comments

```python
# ✅ YES — explain WHY, not WHAT
# Tier cache expires after 1h because Cloudflare rotates challenges
_CACHE_TTL = 3600

# ❌ NO — obvious comments
# Increment counter
counter += 1

# ✅ YES — TODO with context
# TODO(consecrating): Replace with pgvector sink when GOAAISEO DB is ready

# ❌ NO — Vague TODOs
# TODO: fix this later
```

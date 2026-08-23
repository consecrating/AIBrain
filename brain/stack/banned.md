# Banned Packages & Patterns

> If Kiro would suggest any of these, it MUST use the alternative instead.
> Each ban has a reason — this prevents re-debating settled decisions.

## Python — Banned

| Package | Reason | Use Instead |
|---------|--------|-------------|
| requests | Sync-only, no HTTP/2, no async | `httpx` |
| flask | Sync-only, no native typing, no auto-docs | `fastapi` |
| django-rest-framework | Heavy, sync-first | `fastapi` |
| selenium | Slow, detectable, no stealth | `scrapling` or `playwright` |
| beautifulsoup4 (without lxml) | Must always specify `lxml` as parser for speed | `BeautifulSoup(html, "lxml")` |
| nose / nose2 | Dead project | `pytest` |
| pylint | Slow, noisy | `ruff` |
| black + isort + flake8 | Three tools, one job | `ruff` (does all three) |
| pipenv | Slow, abandoned feel | `uv` or plain `pip` + `pyproject.toml` |
| setup.py | Legacy | `pyproject.toml` |

## JavaScript — Banned

| Package | Reason | Use Instead |
|---------|--------|-------------|
| create-react-app | Deprecated, unmaintained | `vite` or `next` |
| moment.js | Deprecated, 300KB+ | `date-fns` or `dayjs` |
| lodash (full) | Tree-shaking issues, mostly native now | Native methods or `lodash-es` (specific imports) |
| express | No async errors, manual typing | `fastify` or `hono` (for non-Next APIs) |
| jest | Slow in Vite/ESM projects | `vitest` |
| enzyme | Dead, React 18+ incompatible | React Testing Library |
| redux (for server state) | Overkill for API cache | `@tanstack/react-query` |
| axios | Unnecessary wrapper over fetch | Native `fetch` or `ky` |
| classnames | Tailwind makes it unnecessary | `cn()` from shadcn/ui utils |
| styled-components | Runtime CSS-in-JS is dead | Tailwind CSS |

## Patterns — Banned

| Pattern | Reason | Do Instead |
|---------|--------|-----------|
| `any` type in TypeScript | Defeats the type system | Proper typing, `unknown` if truly unknown |
| Barrel files (`index.ts` re-exports) | Breaks tree-shaking, circular deps | Direct imports |
| God classes | Untestable, violates SRP | Composition of small functions |
| Mutation in reducers | Bugs | Immutable updates or Immer |
| `console.log` for observability | Not structured, lost in prod | Proper logging (structlog/pino) |
| Sync file I/O in async code | Blocks event loop | `aiofiles` or async alternatives |
| `time.sleep()` in async code | Blocks the loop | `asyncio.sleep()` |
| Wildcard imports (`from x import *`) | Namespace pollution | Explicit imports |

## How to Challenge a Ban

If you think a banned package/pattern is actually the right choice:
1. State the specific use case
2. Explain why the alternative doesn't work here
3. Add a decision record if we agree to make an exception
4. The exception is scoped — it doesn't lift the general ban

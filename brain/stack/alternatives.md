# Smart Alternatives Map

> When Kiro's training data suggests package X, this file intercepts and redirects
> to the CURRENT best option. Updated by `refresh.sh`.

## The Redirection Table

| If you'd suggest... | Use this instead | Why (one line) |
|---------------------|-----------------|----------------|
| requests | httpx | Async, HTTP/2, drop-in API compatible |
| Flask | FastAPI | Async, typed, auto-docs, 10x perf |
| Django REST | FastAPI + SQLAlchemy 2.0 | Lighter, faster, more flexible |
| express.js | Hono or Fastify | Type-safe, 5x faster, modern |
| create-react-app | Vite + React or Next.js | CRA is dead (deprecated 2023) |
| Webpack | Vite | 100x faster HMR, zero config |
| Jest (in Vite project) | Vitest | Native ESM, shared config, 3x faster |
| moment.js | date-fns v3 | Tree-shakeable, 5KB vs 300KB |
| lodash | Native JS + lodash-es (specific) | Most lodash is native since ES2022 |
| Mongoose | Drizzle ORM or Prisma | Type-safe, SQL-first, no magic |
| Redux (for API state) | TanStack Query v5 | Caching, dedup, background refresh built-in |
| styled-components | Tailwind CSS + cn() | Zero runtime, JIT compiled |
| Puppeteer | Playwright | Multi-browser, better API, auto-wait |
| Selenium | Playwright or Scrapling | Stealth, faster, modern API |
| pip install + requirements.txt | uv + pyproject.toml | 10-100x faster, lockfile, standards |
| virtualenv | uv venv | Faster, integrated with uv |
| pylint + flake8 + black | ruff | One tool, 100x faster, all rules |
| SQLAlchemy 1.x patterns | SQLAlchemy 2.0 style | Typed, async, new query API |
| celery (simple jobs) | arq | Lighter, async-native, Redis-only |
| Pandas (for ETL) | Polars | 10x faster, less memory, Rust-based |
| NumPy (for data processing) | Polars (if tabular) | Lazy eval, multi-threaded |
| Docker Compose v1 | Docker Compose v2 | Built into Docker CLI now |
| yarn v1 | pnpm | Faster, disk-efficient, strict |
| npm | pnpm | 3x faster installs, phantom dep prevention |

## Framework Decisions (pre-made)

| Category | Our Choice | Runner-up | Why not runner-up |
|----------|-----------|-----------|-------------------|
| Python web | FastAPI | Litestar | Smaller ecosystem, less docs |
| JS fullstack | Next.js 15 | Nuxt 4 | React ecosystem bigger, RSC |
| CSS | Tailwind + shadcn/ui | Panda CSS | shadcn/ui component library |
| Database | PostgreSQL + pgvector | Turso (SQLite) | Need pgvector + RLS + joins |
| ORM (Python) | SQLAlchemy 2.0 | Prisma (Python) | Prisma Python is beta |
| ORM (JS) | Drizzle | Prisma | Edge-compatible, SQL-first |
| Auth | Supabase Auth | NextAuth/Auth.js | Integrated with our DB |
| Queue | BullMQ (Node) / arq (Python) | SQS | Self-hostable, Redis reuse |
| Search | pgvector + pg_trgm | Meilisearch | Fewer moving parts |
| Monitoring | OpenTelemetry | Datadog | Vendor-neutral, OSS |

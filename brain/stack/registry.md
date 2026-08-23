# Approved Stack Registry

> Before suggesting ANY dependency, check this file first.
> If it's listed here, use the specified version range.
> If it's not listed, check `banned.md` to make sure it's not banned,
> then verify it's actively maintained (>1 release in last 6 months, >1K GitHub stars).

## Python

| Package | Version | Purpose | Replaces |
|---------|---------|---------|----------|
| httpx | >=0.25 | HTTP client (async, HTTP/2) | requests |
| fastapi | >=0.110 | Web framework | Flask, Django REST |
| pydantic | >=2.0 | Validation + serialization | marshmallow, attrs (for APIs) |
| uvicorn | >=0.29 | ASGI server | gunicorn (for async) |
| lxml | >=4.9 | XML/HTML parsing (fast) | html.parser, html5lib |
| beautifulsoup4 | >=4.12 | HTML parsing (flexible) | — |
| pillow | >=10.0 | Image processing | — |
| ruff | >=0.4 | Linting + formatting (all-in-one) | flake8, black, isort |
| pytest | >=7.0 | Testing | unittest |
| sqlalchemy | >=2.0 | ORM (async support) | peewee, tortoise |
| celery | >=5.3 | Task queue (Python) | rq (for complex needs) |
| arq | >=0.25 | Lightweight task queue | — |
| scrapling | >=0.3 | Stealth browser fetching | selenium |

## JavaScript / TypeScript

| Package | Version | Purpose | Replaces |
|---------|---------|---------|----------|
| next | >=15.0 | React framework | create-react-app, Gatsby |
| react | >=19.0 | UI library | — |
| typescript | >=5.4 | Type system | — |
| tailwindcss | >=3.4 | Utility CSS | styled-components, CSS modules |
| @tanstack/react-query | >=5.0 | Server state | SWR, Redux for API |
| zod | >=3.22 | Schema validation | yup, joi |
| date-fns | >=3.0 | Date utilities | moment.js, luxon |
| bullmq | >=5.0 | Job queue (Node) | bull, agenda |
| vitest | >=1.0 | Testing | jest (for Vite projects) |
| drizzle-orm | >=0.30 | TypeScript ORM | Prisma (for edge), TypeORM |

## Infrastructure

| Tool | Version | Purpose |
|------|---------|---------|
| docker | >=24 | Containerization |
| node | >=20 LTS | JS runtime |
| python | >=3.11 | Python runtime |
| postgresql | >=16 | Primary database |
| redis | >=7 | Cache + queue backend |
| supabase | latest | BaaS (auth, storage, realtime) |

## Freshness Policy

- Check npm/pypi for latest version before pinning a NEW package
- If the latest version is >1 year old with no commits, it's likely abandoned
- Prefer packages with: TypeScript types, async support, active maintenance, >1K stars
- Run `./scripts/refresh.sh` monthly to update this registry

# Identity — Who I Am Building For

> This file is read at every session start. Keep it under 50 lines.
> It tells Kiro WHO you are, WHAT you build, and HOW you think.

## Developer Profile

- **Name:** (your name)
- **Role:** Full-stack developer / SEO platform architect
- **Primary languages:** Python, TypeScript
- **Work style:** Ship fast, iterate, prefer working code over perfect abstractions

## Stack DNA

- **Backend:** Python 3.11+ (FastAPI, async-first, type-annotated)
- **Frontend:** Next.js 15 + React 19 + TypeScript + Tailwind + shadcn/ui
- **Database:** PostgreSQL + pgvector (via Supabase) + TimescaleDB
- **Infra:** Docker, GitHub Actions, Vercel (web), Fly.io (services)
- **AI:** Claude API, OpenAI, Google Gemini — model-agnostic design
- **Scraping:** httpx + lxml + Playwright (3-tier escalation)

## Non-Negotiables

1. Never suggest deprecated libraries (check `brain/stack/banned.md` first)
2. Async-first for all I/O operations
3. Type annotations on all function signatures
4. No classes where a function will do (unless it's a clear domain model)
5. Tests verify behavior, not implementation details
6. Every decision has a recorded WHY

## Communication Preferences

- Be direct, skip disclaimers
- Show code first, explain after (if needed)
- When unsure between options, state tradeoffs in a table, let me decide
- Never regenerate what already works — extend it

## Active Projects

See `brain/context/repos.md` for the full map. Key ones:
- GOAAISEO — autonomous SEO operating system
- ScrapeToolAi — stealth web scraping framework
- goaaiseo-seo-adapter — bridges claude-seo analysis into GOAAISEO

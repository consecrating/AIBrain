# Repository Map

> All repos, how they connect, what each one does. Read at session start.

## Active Repositories

### GOAAISEO — The Autonomous SEO Operating System
- **Path:** `/projects/sandbox/goaaiseo`
- **GitHub:** `consecrating/goaaiseo`
- **Status:** Blueprint/Architecture phase
- **Stack:** Next.js 15 + NestJS + FastAPI + PostgreSQL/pgvector + Redis + BullMQ
- **Purpose:** Closed-loop SEO platform (crawl → analyze → act → measure → learn)
- **Blueprint:** 13 phases in `docs/blueprint/`
- **Key insight:** The moat is the closed loop between GSC ground truth ↔ site graph ↔ entity model ↔ autonomous action

### goaaiseo-seo-adapter (gsa)
- **Path:** `/projects/sandbox/goaaiseo-seo-adapter`
- **GitHub:** `consecrating/goaaiseo-seo-adapter`
- **Status:** Functional (v0.1.0 installed)
- **Stack:** Python stdlib-only (zero deps for core)
- **Purpose:** Normalizes claude-seo reports → GOAAISEO graph model
- **CLI:** `gsa ingest`, `gsa analyze`, `gsa doctor`, `gsa serve`
- **Key insight:** Adapter pattern — GOAAISEO doesn't re-implement analysis, just consumes it

### ScrapeToolAi
- **Path:** `/projects/sandbox/ScrapeToolAi`
- **GitHub:** `consecrating/ScrapeToolAi`
- **Status:** Core functional (v1.0.0 installed)
- **Stack:** Python (httpx, lxml, bs4, pillow) + optional (scrapling, scrapy, playwright)
- **Purpose:** Stealth scraping with 3-tier escalation + AI extraction + data organizer
- **CLI:** `scrapetool fetch`, `scrapetool extract`, `scrapetool crawl`, `scrapetool mcp-server`
- **Key insight:** Auto-escalation (HTTP→Stealth→Playwright) per domain, cached

### Claude-Power
- **Path:** `/projects/sandbox/Claude-Power`
- **GitHub:** `consecrating/Claude-Power`
- **Status:** Active (16 packaged skills)
- **Purpose:** Engineering skills for Kiro (token efficiency, memory, debugging, etc.)
- **Combined ownership:** Canonical owner of the `token-efficiency` overlap

### All-Skills
- **Path:** `/projects/sandbox/All-Skills`
- **GitHub:** `consecrating/All-Skills`
- **Status:** Active (45 packaged; combined v2 receipt owns 44)
- **Purpose:** Design/UX/WordPress skills bundle
- **Combined ownership:** One catalog-declared external owner: `token-efficiency` → Claude-Power
- **Current sources:** `/projects/sandbox/All-Skills/catalog/skills.json` and `/projects/.kiro/all-skills-integration.json`
- **Note:** All-Skills standalone installation still owns all 45; counts are informational, not health checks

### AIBrain (this repo)
- **Path:** `/projects/sandbox/AIBrain`
- **GitHub:** `consecrating/AIBrain`
- **Status:** Under construction
- **Purpose:** Persistent intelligence layer — memory, patterns, stack knowledge, autonomy

## Connection Graph

```
                    AIBrain (intelligence layer)
                         │
         ┌───────────────┼───────────────────────┐
         │               │                       │
         ▼               ▼                       ▼
   ┌──────────┐   ┌───────────┐          ┌────────────┐
   │ GOAAISEO │◄──│    gsa    │◄── claude-seo (external)
   │ (system) │   │ (adapter) │
   └────┬─────┘   └───────────┘
        │
        ▼
   ┌──────────────┐
   │ ScrapeToolAi │ ← powers the crawler engine
   └──────────────┘

   ┌──────────────┐   ┌──────────────┐
   │ Claude-Power │ + │  All-Skills  │ → 60 Kiro skills
   └──────────────┘   └──────────────┘
```

## Data Flow

1. **ScrapeToolAi** crawls sites → raw HTML + structured data
2. **gsa adapter** normalizes analysis reports → GraphNode, IssueRecord, ActionCandidate
3. **GOAAISEO** persists to ground-truth graph → reasons over it → acts → measures
4. **AIBrain** remembers decisions, patterns, and learnings across ALL of this

# 📚 Learnings Index

> **Purpose:** Structured knowledge base of proven approaches, discovered during real project execution.  
> **Scope:** Cross-project, cross-domain insights that improve future AI-assisted development.  
> **Policy:** Append-only. Each learning is immutable once recorded. To update, add a superseding entry.  
> **Consumption:** Any AI agent reading this repository gains contextual intelligence for similar tasks.

---

## Schema

Every learning file follows this structure:

```markdown
# LRN-{category}-{NNN}: {Title}

## Metadata
- **Date:** YYYY-MM-DD
- **Category:** {category}
- **Subcategory:** {subcategory}
- **Source Project:** {repo or project name}
- **Confidence:** High | Medium | Low
- **Reusability:** Universal | Domain-Specific | Project-Specific

## Context
{What was being built, what constraints existed}

## Learning
{The key insight — what was discovered, validated, or proven}

## Evidence
{Concrete example, code snippet, or result that proves this works}

## Application Rules
{When to apply this learning, and when NOT to}

## Related
- LRN-xxx-xxx (if connected to other learnings)
- DEC-xxx (if connected to decisions)
- Pattern: XX-xxx (if evolved into a pattern)
```

---

## Category Taxonomy

| Category | Directory | Description |
|----------|-----------|-------------|
| **web-development** | `learnings/web-development/` | Frontend/fullstack patterns, frameworks, responsive design |
| **design-systems** | `learnings/design-systems/` | UI/UX insights, color theory, typography, visual hierarchy |
| **deployment** | `learnings/deployment/` | Hosting, CI/CD, FTP, static export, server configuration |
| **tooling** | `learnings/tooling/` | Build systems, dev tools, package management, CLI workflows |
| **ai-patterns** | `learnings/ai-patterns/` | AI-assisted development patterns, prompt engineering, automation |
| **seo** | `learnings/seo/` | Search optimization, crawling, indexing, performance |
| **hospitality** | `learnings/hospitality/` | Domain-specific: hotel industry, tourism, F&B sector knowledge |

---

## Master Ledger

| ID | Date | Title | Category | Confidence | Source |
|----|------|-------|----------|------------|--------|
| LRN-WEB-001 | 2026-08-23 | Next.js 16 Static Export for Shared Hosting | web-development | High | TES-Krishna |
| LRN-WEB-002 | 2026-08-23 | Tailwind v4 Custom Theme Tokens for Brand Systems | web-development | High | TES-Krishna |
| LRN-WEB-003 | 2026-08-23 | Glassmorphism + Dark Gradients for Premium Feel | web-development | High | TES-Krishna |
| LRN-DES-001 | 2026-08-23 | Color Contrast Requirements for Dark Backgrounds | design-systems | High | TES-Krishna |
| LRN-DES-002 | 2026-08-23 | PDF-to-Website Color Extraction Pipeline | design-systems | High | TES-Krishna |
| LRN-DES-003 | 2026-08-23 | Section Density vs Empty Space — Modern Approach | design-systems | High | TES-Krishna |
| LRN-DEP-001 | 2026-08-23 | FTP Deployment Pipeline for Static Next.js Sites | deployment | High | TES-Krishna |
| LRN-DEP-002 | 2026-08-23 | Apache .htaccess for SPA/Static Export Routing | deployment | High | TES-Krishna |
| LRN-AI-001 | 2026-08-23 | PDF Content Extraction for Website Generation | ai-patterns | High | TES-Krishna |
| LRN-AI-002 | 2026-08-23 | Iterative Redesign: Feedback Loop Pattern | ai-patterns | High | TES-Krishna |
| LRN-HOS-001 | 2026-08-23 | Hotel Industry Website Structure & Content Model | hospitality | High | TES-Krishna |

---

## How to Add a Learning

```bash
# Via CLI (if brain.sh supports it)
./scripts/brain.sh learn "Title of learning" \
  --category "web-development" \
  --source "project-name" \
  --confidence "High"

# Or manually:
# 1. Create file in learnings/{category}/LRN-{CAT}-{NNN}.md
# 2. Add entry to this _index.md ledger
# 3. Commit with message: "learn: {title}"
```

---

## Consumption Protocol (for AI agents)

1. **At session start:** Scan `learnings/_index.md` for relevant entries based on current task
2. **Before generating code:** Check if any learning in the relevant category applies
3. **After completing work:** Record new learnings discovered during execution
4. **Cross-reference:** Link learnings to `brain/decisions/` and `brain/patterns/` where applicable
5. **Confidence decay:** If a learning hasn't been validated in 6+ months, treat as Medium confidence

---

## Promotion Rules

- A **Learning** that proves universally useful across 3+ projects → promote to **Pattern** in `brain/patterns/`
- A **Learning** that establishes a permanent choice → promote to **Decision** in `brain/decisions/`
- A **Learning** that identifies something to avoid → add to `rules/anti-patterns.md`

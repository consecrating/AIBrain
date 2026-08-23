# LRN-AI-002: Iterative Redesign — Feedback Loop Pattern

## Metadata
- **Date:** 2026-08-23
- **Category:** ai-patterns
- **Subcategory:** iteration, feedback-loop, quality-assurance
- **Source Project:** TES-Krishna (TES Hospitality website)
- **Confidence:** High
- **Reusability:** Universal

## Context
First version of TES Hospitality site was deployed and received client feedback: "too basic, visibility issues, not modern, empty spaces." Needed a systematic approach to redesign without starting from scratch.

## Learning
The optimal AI-assisted website redesign follows a **diagnose → transform → verify** loop:

### The Feedback Loop

```
┌─────────────────────────────────────────────┐
│  1. DEPLOY V1 (functional, content-complete) │
└─────────────────────┬───────────────────────┘
                      ▼
┌─────────────────────────────────────────────┐
│  2. COLLECT FEEDBACK (specific complaints)   │
│     - "text visibility issues"               │
│     - "colors not good"                      │
│     - "too basic layout"                     │
│     - "many empty spaces"                    │
└─────────────────────┬───────────────────────┘
                      ▼
┌─────────────────────────────────────────────┐
│  3. CATEGORIZE (map complaints → systems)    │
│     - visibility → contrast system           │
│     - colors → palette refinement            │
│     - basic → visual effects + density       │
│     - empty → layout composition             │
└─────────────────────┬───────────────────────┘
                      ▼
┌─────────────────────────────────────────────┐
│  4. TRANSFORM (systematic, not piecemeal)    │
│     - Rewrite CSS system (globals.css)       │
│     - Rewrite ALL components (not patch)     │
│     - Validate contrast on every section     │
└─────────────────────┬───────────────────────┘
                      ▼
┌─────────────────────────────────────────────┐
│  5. DEPLOY V2 + VERIFY                       │
│     - Build passes                           │
│     - Live site returns 200                  │
│     - Each complaint addressed               │
└─────────────────────────────────────────────┘
```

### Key Principles

1. **V1 is for content validation** — get the structure and words right
2. **V2 is for design quality** — upgrade the visual system wholesale
3. **Never patch** — when feedback is systemic ("too basic"), rewrite the design system, don't add effects piecemeal
4. **Preserve content** — redesign means changing HOW it looks, not WHAT it says
5. **Address ALL feedback points** — partial fixes lead to V3 requests

### Complaint → Solution Mapping

| Common Complaint | Root Cause | Solution Category |
|-----------------|------------|-------------------|
| "Can't read text" | Low contrast | LRN-DES-001 |
| "Looks basic/average" | Flat design, no effects | LRN-WEB-003 |
| "Too much empty space" | Low density layout | LRN-DES-003 |
| "Colors are off" | Direct PDF colors without refinement | LRN-DES-002 |
| "Not modern" | Missing: gradients, glass, animations | LRN-WEB-003 |
| "Doesn't feel premium" | All of the above combined | Full redesign |

## Evidence
TES-Krishna V1 → V2 transformation:
- Addressed 4 specific complaints in single iteration
- No V3 requested for the design system (only a minor tonal adjustment to one section)
- Build remained clean (no regressions)
- Deployed in single session

## Application Rules
**Apply when:**
- Received design feedback on a deployed site
- Feedback is about look/feel not content/structure
- Multiple visual issues mentioned (systemic problem)

**Do NOT apply when:**
- Feedback is about content (wrong text, missing sections) — that's content editing
- Single specific issue (just fix that one thing)
- Client wants a completely different design direction (start fresh)

## Related
- LRN-DES-001 (Contrast fix methodology)
- LRN-DES-003 (Density improvement toolkit)
- LRN-WEB-003 (Premium effects library)

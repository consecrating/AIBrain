# LRN-DES-001: Color Contrast Requirements for Dark Backgrounds

## Metadata
- **Date:** 2026-08-23
- **Category:** design-systems
- **Subcategory:** accessibility, contrast, readability
- **Source Project:** TES-Krishna (TES Hospitality website)
- **Confidence:** High
- **Reusability:** Universal

## Context
First version of TES Hospitality site had severe text visibility issues on teal/dark sections. White text on teal (#0D8D93), gold text on teal, and light text on gold backgrounds all failed readability.

## Learning
Dark/colored backgrounds require a deliberate text opacity hierarchy to maintain readability while establishing visual weight:

### The Opacity Hierarchy (dark backgrounds)

| Element Type | Minimum Opacity | Example |
|-------------|----------------|---------|
| Headings (H1-H3) | `text-white` (100%) | Always full white for anchors |
| Body text (primary) | `text-white/80` (80%) | Main paragraphs |
| Body text (secondary) | `text-white/65` (65%) | Descriptions, sub-text |
| Labels / micro-copy | `text-white/50` (50%) | Tags, timestamps, hints |
| Disabled / decorative | `text-white/30` (30%) | Minimum for any visible text |

### Critical Failures to Avoid

| ❌ Bad | ✅ Fixed | Why |
|--------|----------|-----|
| `text-white/50` for body | `text-white/65` minimum | 50% is too faint on teal |
| Gold text on teal bg | Gold text on dark bg only | Insufficient contrast ratio |
| White text on gold bg | Dark text on gold bg | Gold is mid-tone, needs dark text |
| `text-white/40` for labels | `text-white/50` minimum | Below 40% is invisible |

### Background Darkness Rule
For text sections requiring readability:
- **Teal backgrounds:** Darken to `#042d2f` – `#053e41` (not the raw `#0D8D93`)
- **Gold backgrounds:** Use dark text (`text-tes-dark`) not white
- **Glass cards:** Ensure `bg-white/[0.08]` minimum on dark backgrounds

## Evidence
HowItWorks section was flagged for poor readability. After darkening gradient from `#085558→#0B7A80→#10A3AB` to `#042d2f→#053e41→#063a3c` and increasing card opacity from `0.05` to `0.08`, all text became clearly legible.

## Application Rules
**Apply when:**
- Any dark or colored section with text content
- Using semi-transparent text (opacity-based approach)
- Designing glassmorphism or overlay-heavy layouts

**Validation method:**
- Squint test: if you squint and can't read it, increase opacity
- Screenshot → grayscale → check if text is still distinguishable
- WCAG 2.1 AA: 4.5:1 ratio for normal text, 3:1 for large text

## Related
- LRN-WEB-003 (Glassmorphism requires careful contrast)
- LRN-DES-003 (Dense sections need strong text hierarchy)

# LRN-WEB-003: Glassmorphism + Dark Gradients for Premium Feel

## Metadata
- **Date:** 2026-08-23
- **Category:** web-development
- **Subcategory:** visual-effects, premium-ui
- **Source Project:** TES-Krishna (TES Hospitality website)
- **Confidence:** High
- **Reusability:** Universal

## Context
Initial site version was "too basic and average." Client feedback explicitly cited: basic layout, poor visibility, not modern UI/UX, too many empty spaces. Needed to transform from generic to premium without changing content.

## Learning
The combination of **dark gradient backgrounds + glassmorphism cards + subtle grid patterns** creates an immediate premium feel. This stack of visual techniques upgrades any section from "basic" to "modern" with minimal content changes:

**The Premium Stack (in order of impact):**

1. **Dark gradient backgrounds** — replace flat colors with 2-3 stop gradients
   ```css
   .gradient-dark {
     background: linear-gradient(180deg, #111827 0%, #1F2937 100%);
   }
   ```

2. **Glass cards** — semi-transparent with backdrop blur and subtle borders
   ```css
   .glass-card {
     background: rgba(255, 255, 255, 0.08);
     backdrop-filter: blur(12px);
     border: 1px solid rgba(255, 255, 255, 0.15);
   }
   ```

3. **Grid pattern overlay** — subtle lines that add texture without distraction
   ```css
   .grid-pattern {
     background-image:
       linear-gradient(rgba(255,255,255,0.03) 1px, transparent 1px),
       linear-gradient(90deg, rgba(255,255,255,0.03) 1px, transparent 1px);
     background-size: 60px 60px;
   }
   ```

4. **Hover-lift effect** — cards that rise with enhanced shadow on hover
   ```css
   .hover-lift:hover {
     transform: translateY(-4px);
     box-shadow: 0 20px 40px -12px rgba(0, 0, 0, 0.15);
   }
   ```

5. **Colored glow blurs** — large absolutely-positioned circles with blur
   ```tsx
   <div className="absolute top-1/4 left-0 w-[400px] h-[400px] bg-teal/8 rounded-full blur-[100px]" />
   ```

## Evidence
TES-Krishna V2 redesign received no negative feedback after applying these techniques. The Strengths section (dark bg + glass cards + grid), HowItWorks section (dark teal gradient + numbered steps), and Contact section (dark + form glass card) all demonstrate this pattern.

## Application Rules
**Apply when:**
- Client says current design is "too basic" or "average"
- Building premium/luxury brand websites
- Dark sections need visual depth
- Sections feel flat or unfinished

**Do NOT apply when:**
- Target is minimalist/clean aesthetic (too busy)
- Performance budget is very tight (backdrop-filter is expensive)
- Target audience uses older browsers without backdrop-filter support
- Content itself is the hero (blog posts, documentation)

**Performance note:** `backdrop-filter: blur()` causes composite layer creation. Limit to 3-5 elements per viewport. Never apply to large scrolling areas.

## Related
- LRN-DES-001 (Contrast requirements — glass must have sufficient opacity)
- LRN-DES-003 (Section density approach)

# LRN-WEB-002: Tailwind v4 Custom Theme Tokens for Brand Systems

## Metadata
- **Date:** 2026-08-23
- **Category:** web-development
- **Subcategory:** css-architecture, design-tokens
- **Source Project:** TES-Krishna (TES Hospitality website)
- **Confidence:** High
- **Reusability:** Universal

## Context
Needed to implement a precise brand color system (Gold #D4920F, Teal #0B7A80, Red #B91C1C) with multiple tints/shades as first-class Tailwind utilities — not just arbitrary values.

## Learning
Tailwind CSS v4 uses `@theme inline` blocks to define custom design tokens that become native utilities. This is superior to the v3 `extend` approach because:

1. Tokens are type-safe and auto-suggested
2. They compose with all Tailwind modifiers (`hover:`, `focus:`, responsive)
3. They work in `bg-`, `text-`, `border-`, `shadow-` etc. automatically
4. They use CSS custom properties under the hood (easy to override/theme)

**Implementation pattern:**
```css
@theme inline {
  --color-brand-gold: #D4920F;
  --color-brand-gold-light: #F5B731;
  --color-brand-gold-dark: #A36E08;
  --color-brand-gold-50: #FEF9EC;   /* backgrounds */
  --color-brand-gold-100: #FDF0C8;  /* hover states */

  --color-brand-teal: #0B7A80;
  --color-brand-teal-light: #10A3AB;
  --color-brand-teal-dark: #085558;
  --color-brand-teal-50: #EDFCFD;
  --color-brand-teal-100: #D2F7F9;
}
```

**Usage in components:**
```tsx
<div className="bg-brand-gold-50 text-brand-gold-dark border-brand-gold/20">
  {/* Fully native Tailwind — autocomplete, responsive, all modifiers */}
</div>
```

## Evidence
TES-Krishna site uses 15+ custom color tokens across all components. Every color utility autocompletes in IDE, works with opacity modifiers (`bg-tes-gold/15`), and responds to all pseudo-classes.

## Application Rules
**Apply when:**
- Building a branded website with specific color requirements
- Need multiple tints/shades of brand colors
- Team needs consistent color usage across components
- Project uses Tailwind CSS v4+

**Do NOT apply when:**
- Using Tailwind v3 (use `theme.extend` in config instead)
- Only need 1-2 custom colors (arbitrary values `bg-[#D4920F]` are simpler)
- Colors change dynamically at runtime (use CSS variables directly)

## Related
- LRN-DES-001 (Color contrast on dark backgrounds)
- LRN-DES-002 (PDF color extraction pipeline)

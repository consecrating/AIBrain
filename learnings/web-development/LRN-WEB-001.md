# LRN-WEB-001: Next.js 16 Static Export for Shared Hosting

## Metadata
- **Date:** 2026-08-23
- **Category:** web-development
- **Subcategory:** static-export, hosting-compatibility
- **Source Project:** TES-Krishna (TES Hospitality website)
- **Confidence:** High
- **Reusability:** Universal

## Context
Built a hospitality consulting website using Next.js 16 (App Router, React 19, Tailwind CSS 4) that needed to be deployed on traditional shared hosting (cPanel/Apache) via FTP — not Vercel or any Node.js hosting.

## Learning
Next.js 16 supports `output: "export"` in `next.config.ts` which generates a fully static site in `/out` directory. Combined with `images: { unoptimized: true }`, the output is pure HTML/CSS/JS that works on ANY web server including cheap shared hosting with only Apache/Nginx.

**Key configuration:**
```typescript
// next.config.ts
const nextConfig: NextConfig = {
  output: "export",
  images: { unoptimized: true },
};
```

**Constraints of static export:**
- No API routes (use external APIs instead)
- No Server Actions
- No ISR/SSR — all pages pre-rendered at build time
- No `next/image` optimization (images served as-is)
- Route-based pages work, but dynamic routes need `generateStaticParams`

## Evidence
Successfully deployed TES Hospitality site to `demo2.sanctify.co` via FTP. Build output: `out/` directory with `index.html`, `404.html`, `_next/static/` assets. Apache served it with 200 status, no Node.js runtime required.

## Application Rules
**Apply when:**
- Client uses shared hosting (cPanel, Plesk, Apache without Node)
- Project is primarily a marketing/brochure site (no server logic)
- Client needs simple FTP-based deployment
- Budget doesn't justify Vercel/AWS

**Do NOT apply when:**
- Site needs server-side rendering or dynamic API routes
- Site uses authentication or server actions
- Site needs incremental static regeneration
- Site has dynamic content that changes frequently

## Related
- LRN-DEP-001 (FTP deployment pipeline)
- LRN-DEP-002 (Apache .htaccess configuration)

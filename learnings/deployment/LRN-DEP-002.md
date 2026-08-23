# LRN-DEP-002: Apache .htaccess for SPA/Static Export Routing

## Metadata
- **Date:** 2026-08-23
- **Category:** deployment
- **Subcategory:** apache, routing, server-config
- **Source Project:** TES-Krishna (TES Hospitality website)
- **Confidence:** High
- **Reusability:** Universal

## Context
Next.js static export generates `/index.html`, `/404.html`, and `_next/` assets. On Apache shared hosting, direct URL access to routes (bookmarks, refreshes) returns 404 unless properly configured.

## Learning
Complete `.htaccess` for static SPAs on Apache shared hosting:

```apache
RewriteEngine On
RewriteBase /

# 1. SPA Routing — serve index.html for all non-file, non-directory requests
RewriteCond %{REQUEST_FILENAME} !-f
RewriteCond %{REQUEST_FILENAME} !-d
RewriteRule ^(.*)$ /index.html [L]

# 2. GZIP Compression — reduce transfer size 60-80%
<IfModule mod_deflate.c>
  AddOutputFilterByType DEFLATE text/html text/css application/javascript application/json image/svg+xml
</IfModule>

# 3. Browser Caching — static assets cached for 1 year (cache-busted by filename hash)
<IfModule mod_expires.c>
  ExpiresActive On
  ExpiresByType text/css "access plus 1 year"
  ExpiresByType application/javascript "access plus 1 year"
  ExpiresByType image/png "access plus 1 year"
  ExpiresByType image/jpeg "access plus 1 year"
  ExpiresByType image/svg+xml "access plus 1 year"
  ExpiresByType font/woff2 "access plus 1 year"
</IfModule>

# 4. Security Headers
<IfModule mod_headers.c>
  Header set X-Content-Type-Options "nosniff"
  Header set X-Frame-Options "SAMEORIGIN"
  Header set Referrer-Policy "strict-origin-when-cross-origin"
</IfModule>
```

### Why This Works for Next.js Static Export
- `_next/static/chunks/` files have content-hash in filename → safe to cache forever
- `index.html` has no cache header → always fresh
- Client-side JS handles routing after initial load
- 404 falls through to `index.html` which can show a client-rendered 404 page

### Multi-page Static Export (no SPA)
If using `generateStaticParams` for multiple pages (e.g., `/about.html`, `/services.html`):
```apache
# Remove .html extension from URLs
RewriteCond %{REQUEST_FILENAME} !-f
RewriteCond %{REQUEST_FILENAME} !-d
RewriteCond %{REQUEST_FILENAME}.html -f
RewriteRule ^(.*)$ $1.html [L]
```

## Evidence
Deployed to `demo2.sanctify.co` — site loads correctly on direct URL access, assets are GZIP-compressed, and `_next/static/` files are cached by browser.

## Application Rules
**Apply when:**
- Deploying any SPA or static export to Apache
- Using Next.js `output: "export"`, Vite, Astro (static), Gatsby
- Shared hosting with `.htaccess` support

**Do NOT apply when:**
- Using Nginx (use `try_files` directive instead)
- Server-rendered app (needs reverse proxy config)
- `.htaccess` is disabled by host (check `AllowOverride All`)

## Related
- LRN-DEP-001 (FTP deployment pipeline)
- LRN-WEB-001 (Next.js static export setup)

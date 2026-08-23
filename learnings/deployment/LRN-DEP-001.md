# LRN-DEP-001: FTP Deployment Pipeline for Static Next.js Sites

## Metadata
- **Date:** 2026-08-23
- **Category:** deployment
- **Subcategory:** ftp, shared-hosting, automation
- **Source Project:** TES-Krishna (TES Hospitality website)
- **Confidence:** High
- **Reusability:** Universal

## Context
Client's hosting is traditional shared hosting (cPanel, Apache) with only FTP access. No SSH, no Node.js runtime, no Vercel integration. Need a reliable automated deployment pipeline.

## Learning
Complete pipeline for deploying Next.js static exports via FTP:

### Pipeline Steps

```bash
# 1. Build static export
npm run build  # with output: "export" in next.config.ts

# 2. Deploy via lftp (supports mirror, TLS, resume)
lftp -c "
set ftp:ssl-allow yes
set ssl:verify-certificate no
open ftp://user%40domain:password@ftp.host.com:21
mirror --reverse --delete --only-newer ./out /
bye
"
```

### Key Flags
| Flag | Purpose |
|------|---------|
| `--reverse` | Upload local → remote (not download) |
| `--delete` | Remove remote files not in local (clean deploy) |
| `--only-newer` | Skip unchanged files (faster) |
| `--verbose` | Show progress (for debugging) |

### Gotchas Discovered
1. **URL-encode credentials:** `@` in username → `%40` (e.g., `user%40domain`)
2. **Special chars in password:** Shell-escape `$`, `(`, `)`, `{`, `}` in passwords
3. **`.ftpquota` file:** Server-managed file that can't be deleted (causes exit 1 but deploy succeeds)
4. **SSL issues:** Many shared hosts have self-signed certs → `set ssl:verify-certificate no`
5. **No `.htaccess` in build:** Must create separately and upload (Next.js doesn't generate it)

### Required .htaccess
```apache
RewriteEngine On
RewriteBase /
RewriteCond %{REQUEST_FILENAME} !-f
RewriteCond %{REQUEST_FILENAME} !-d
RewriteRule ^(.*)$ /index.html [L]
```

## Evidence
Successfully deployed TES-Krishna to `demo2.sanctify.co` via this exact pipeline. FTP credentials with `@` in username worked after URL-encoding. Mirror completed in under 10 seconds for ~30 files.

## Application Rules
**Apply when:**
- Client has shared hosting (cPanel, Plesk, DirectAdmin)
- Only FTP/SFTP access available
- Static site or static export from Next.js/Gatsby/Astro
- Need automated/repeatable deployments

**Do NOT apply when:**
- SSH available → use rsync instead (faster, resumable)
- CI/CD pipeline exists → use GitHub Actions
- Dynamic site → needs Node.js hosting (Vercel, Railway, Fly.io)

**Security note:** Never commit FTP credentials. Use environment variables or secrets manager.

## Related
- LRN-WEB-001 (Next.js static export configuration)
- LRN-DEP-002 (.htaccess for routing)

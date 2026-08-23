# Stealth HTTP Fetching with Escalation

- **ID:** PY-001
- **Problem:** Fetch public pages efficiently while handling JavaScript or bot challenges.
- **Use when:** A crawler needs the fastest viable retrieval method.
- **Source:** ScrapeToolAi

## Solution

Try plain HTTP with realistic headers and bounded timeouts first. Escalate only on explicit blocking signals to a stealth browser, then to full browser automation. Cache the successful tier per domain with an expiry and retain the final URL, status, and tier as provenance.

# Graph Sink Protocol

- **ID:** AR-001
- **Problem:** Normalized graph writes must support local files and production databases.
- **Use when:** Persistence is owned by the consuming platform.
- **Source:** goaaiseo-seo-adapter

## Solution

Normalize into stable graph records, then depend on a minimal sink interface. Keep tenant enforcement and transaction boundaries inside the production sink while preserving idempotent identities in the shared model.

# TanStack Query Mutation with Recovery

- **ID:** TS-002
- **Problem:** Client mutations need responsive updates without corrupting cached server state.
- **Use when:** A client component changes remote data.
- **Source:** GOAAISEO

## Solution

Cancel affected queries, snapshot prior cache, apply an optimistic update, restore on error, and invalidate authoritative queries on settlement. Keep query keys centralized and tenant-scoped.

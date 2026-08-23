# Zod Boundary Pipeline

- **ID:** TS-003
- **Problem:** TypeScript types disappear at runtime while external data remains untrusted.
- **Use when:** Parsing forms, environment variables, APIs, or queued events.
- **Source:** GOAAISEO

## Solution

Define one Zod schema at the boundary, infer the TypeScript type from it, parse before business logic, and map validation failures to stable field-level errors. Avoid maintaining a duplicate handwritten interface.

# Pydantic v2 Boundary Models

- **ID:** PY-003
- **Problem:** External payloads require runtime validation and typed internal use.
- **Use when:** Data enters an API or service boundary.
- **Source:** GOAAISEO

## Solution

Validate once at the boundary with explicit Pydantic v2 models, reject invalid fields with actionable errors, and pass typed objects into business logic. Keep persistence models separate when their lifecycle differs from API contracts.

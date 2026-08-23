# FastAPI Service Lifecycle

- **ID:** PY-004
- **Problem:** A Python service needs typed endpoints, health checks, and clean resource management.
- **Use when:** Building an async API or worker control plane.
- **Source:** GOAAISEO

## Solution

Use an application lifespan context to initialize and close shared clients. Expose distinct liveness and readiness checks, validate request models at the edge, return stable error codes, and keep handlers thin by delegating to typed services.

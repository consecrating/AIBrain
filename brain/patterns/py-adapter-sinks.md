# Standard-Library Adapter with Pluggable Sinks

- **ID:** PY-002
- **Problem:** Normalize external data without coupling the core to persistence infrastructure.
- **Use when:** An integration layer feeds multiple storage backends.
- **Source:** goaaiseo-seo-adapter

## Solution

Keep parsing and normalization in a dependency-free core. Define a small sink protocol around `write(result) -> metadata`; provide memory and file implementations, and let the host application inject database-backed sinks.

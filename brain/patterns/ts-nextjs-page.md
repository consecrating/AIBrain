# Next.js App Router Server Page

- **ID:** TS-001
- **Problem:** A page needs data without shipping unnecessary client JavaScript.
- **Use when:** Building a Next.js App Router route.
- **Source:** GOAAISEO

## Solution

Use a server component by default, fetch data near the route, wrap slow regions in Suspense, and introduce a client boundary only for stateful browser interaction. Keep authentication and tenant checks on the server.

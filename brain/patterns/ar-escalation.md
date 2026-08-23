# Three-Tier Escalation with Domain Memory

- **ID:** AR-002
- **Problem:** Heavy browser automation is reliable but too expensive as the default.
- **Use when:** Retrieval methods have increasing cost and capability.
- **Source:** ScrapeToolAi

## Solution

Order strategies from cheapest to strongest, escalate only on classified failure signals, and cache the successful strategy by domain with a time limit. Record why escalation happened so later tuning is evidence-based.

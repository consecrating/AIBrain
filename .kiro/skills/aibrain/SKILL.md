---
name: aibrain
description: "Super-powered intelligence layer — persistent memory, live dependency verification, proven patterns, cross-repo orchestration, self-healing. Activate when: starting a session, choosing packages, writing code patterns, making architectural decisions, or when previous responses were subpar. Provides recall, decide, correct, validate commands via brain.sh."
metadata:
  version: "1.0"
  author: consecrating
---

# AIBrain — Super-Powered Intelligence

You have a persistent intelligence layer that makes you dramatically better than
a vanilla AI assistant. Use it.

## Super Powers

### 🧠 Power 1: Perfect Memory
You never forget. Decisions, corrections, patterns, and context live on disk.
```bash
# Query the brain
/projects/sandbox/AIBrain/scripts/brain.sh recall "topic"
/projects/sandbox/AIBrain/scripts/brain.sh status
```

### 📦 Power 2: Live Dependency Intelligence
You never suggest outdated packages. The registry is YOUR truth.
```bash
# Check before suggesting
cat /projects/sandbox/AIBrain/brain/stack/registry.md    # approved
cat /projects/sandbox/AIBrain/brain/stack/banned.md      # never suggest
cat /projects/sandbox/AIBrain/brain/stack/alternatives.md # redirections
```

### 🔧 Power 3: Pattern Reuse
You never reinvent what already works. Proven patterns first.
```bash
cat /projects/sandbox/AIBrain/brain/patterns/_index.md
```

### ⚡ Power 4: Autonomous Multi-Step Execution
You can chain complex operations across all repos:
- Scrape with ScrapeToolAi → analyze with gsa → feed GOAAISEO
- Search the web for current info → verify → apply
- Read patterns → generate code → validate → commit

### 🔄 Power 5: Self-Healing
When something goes wrong:
1. Record the mistake: `brain.sh correct "what happened"`
2. Check corrections before repeating: read `memory/corrections.md`
3. Validate your own output against the quality rules

### 🌐 Power 6: Live Web Intelligence
Before suggesting ANYTHING from training data:
- Web search for current version/status
- Verify the package isn't deprecated
- Check if there's a newer/better alternative
- Validate API endpoints still exist

### 🔗 Power 7: Cross-Repo Orchestration
You understand how all 6 repos connect:
```bash
cat /projects/sandbox/AIBrain/brain/context/repos.md
```
And can execute operations that span multiple repos in one flow.

## When to Activate

- ✅ Starting any session (load context)
- ✅ Before suggesting a package
- ✅ Before generating non-trivial code
- ✅ After being corrected
- ✅ When a response was rejected
- ✅ When making a decision with long-term impact
- ✅ Before claiming "done"

## Command Reference

```bash
BRAIN=/projects/sandbox/AIBrain/scripts/brain.sh
LEARN=/projects/sandbox/AIBrain/scripts/learn.sh

$BRAIN status                    # health + active task
$BRAIN recall "authentication"   # search all knowledge
$BRAIN decide "Use X over Y"    # record decision
$BRAIN correct "bad thing"      # never do again
$BRAIN stack add pkg version    # approve a package
$BRAIN stack ban pkg reason     # ban a package
$BRAIN journal "important note" # append to log
$BRAIN next "next thing to do"  # set next action
$BRAIN validate                 # check integrity
$BRAIN stats                    # knowledge stats

$LEARN add "lesson learned"     # quick capture
$LEARN list                     # review inbox
$LEARN promote 3                # promote to permanent
```

## The Contract

1. I will NEVER suggest a banned package
2. I will ALWAYS check the registry before recommending dependencies
3. I will ALWAYS check patterns before writing new code
4. I will NEVER repeat a recorded correction
5. I will ALWAYS record significant decisions
6. I will ALWAYS verify current state before claiming something works
7. I will write complete, typed, production-quality code
8. I will anticipate needs 2-3 steps ahead
9. I will connect dots across repositories
10. I will be SUPER-POWERED — not basic

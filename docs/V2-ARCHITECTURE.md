# AIBrain v2 Architecture

## Goal

Turn AIBrain from a Markdown knowledge bundle into a local-first intelligence runtime while preserving every v1 command and installed Kiro path.

## Design principles

1. **Local first:** all core behavior uses the Python standard library; no API key or hosted service is required.
2. **Additive contracts:** existing `brain.sh` positional commands, Markdown headings, journal rows, steering paths, and SuperBrain install paths remain valid.
3. **Evidence over recall:** every result identifies its source file and freshness metadata.
4. **Append-only memory:** structured memories are JSONL events; retraction creates a tombstone rather than deleting history.
5. **Compact context:** context packs are ranked and budgeted instead of dumping the knowledge base into the model context.
6. **Safe writes:** mutable Markdown and JSONL state use file locks, escaping, temporary files, and atomic replacement.
7. **Inspectable intelligence:** profiles, skill routing, conflicts, freshness, and index state are visible through CLI commands.

## Runtime layers

```text
brain.sh (stable public launcher)
  -> scripts/aibrain.py (stdlib CLI)
       -> scripts/aibrain_core/{paths,store,index,markdown,profiles}.py
            -> Markdown knowledge graph (human source of truth)
            -> memory/store.jsonl (append-only structured memory)
            -> .aibrain/index.json (generated weighted search index)
            -> brain/profiles/*.json (project context policies)
            -> brain/skills/*.md (routable super-skill definitions)
```

## New capabilities

### Hybrid ranked recall

`brain.sh recall QUERY` searches identity, decisions, patterns, stack policy, context, rules, task state, corrections, and structured memories. Ranking combines exact phrase matches, token frequency, title matches, source priority, confidence, and freshness. Results include file/record citations.

### Structured durable memory

`brain.sh remember TEXT [--kind KIND] [--scope SCOPE] [--tags a,b] [--confidence 0..1] [--source SOURCE] [--expires YYYY-MM-DD]`

Each event receives a stable ID, timestamp, content hash, provenance, scope, confidence, and optional expiry. `forget ID --reason TEXT` appends a tombstone.

### Context compiler

`brain.sh context QUERY [--profile NAME] [--budget N] [--json]` produces a compact, ranked context packet containing relevant memories, decisions, corrections, stack policy, patterns, and project profile rules.

### Project profiles

Profiles make repository-specific behavior explicit. `profile auto PATH` selects the best profile from path markers; `profile show NAME` renders it. Initial profiles cover AIBrain, GOAAISEO, ScrapeToolAi, and a default workspace.

### Super-skill router

`skills route TASK` ranks local super skills by triggers and capabilities. Skills are declarative Markdown documents with machine-readable metadata, allowing AIBrain to recommend workflows without loading every skill body.

### Knowledge ingestion

`ingest FILE [--kind reference] [--scope global] [--tags ...]` fingerprints a local document, stores provenance, indexes its sections, and avoids duplicate ingestion. Network ingestion is intentionally excluded from core v2; callers can fetch with approved tools and ingest the resulting local artifact.

### Doctor and conflict engine

`doctor` validates schemas, duplicate IDs, table placement, dangling pattern references, package conflicts, expired memories, stale feeds, installed Kiro artifacts, and index freshness.

### Snapshot and recovery

`snapshot create [NAME]` writes an atomic manifest of mutable state and content hashes. `snapshot list` and `snapshot verify NAME` support recovery checks without silently restoring files.

## Compatibility contract

| v1 contract | v2 behavior |
|---|---|
| `brain.sh` executable | retained as stable launcher |
| no-arg command runs `status` | retained |
| `status`, `recall`, `decide`, `correct`, `stack`, `journal`, `next`, `validate`, `stats` | retained; behavior corrected and expanded |
| positional arguments | retained; documented long options added |
| `.kiro/skills/aibrain/SKILL.md` | retained, metadata upgraded |
| `.kiro/steering/aibrain.md` | retained, root resolution documented |
| `scripts/install.sh` | retained, now initializes runtime state and propagates validation failures |
| `/projects/.kiro/.aibrain-path` | retained and now consumed by root resolution |
| SuperBrain `AIBRAIN_ROOT` | retained and honored |

## Deliberate exclusions

- No embeddings package or vector database in core. The index is deterministic and offline.
- No automatic execution of fetched code.
- No destructive restore command in v2. Snapshots verify and expose recovery material; restoration remains explicit.
- No silent promotion of user corrections into global policy.

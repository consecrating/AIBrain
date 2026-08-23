# AIBrain v2

**A local-first intelligence runtime for Kiro:** durable memory, ranked knowledge retrieval, compact context compilation, project profiles, dependency evidence, routable super skills, and self-healing diagnostics.

AIBrain keeps human-readable Markdown as the knowledge source while adding a standard-library Python runtime for safe writes and explainable retrieval. It does not require an embedding service, database, API key, or third-party Python package.

## What v2 solves

| Failure mode | AIBrain v2 capability |
|---|---|
| Context compaction loses decisions | Append-only decisions and structured memory events |
| The assistant rereads or regenerates known work | Ranked `recall` with file/record citations |
| Too much context lowers response quality | Budgeted, profile-aware `context` packets |
| Outdated packages are suggested | Approved/banned policy plus atomic PyPI/npm evidence feeds |
| Repository conventions are mixed together | Auto-detected project profiles |
| Skills are loaded without task fit | Metadata-based super-skill routing |
| Knowledge contradicts itself | `doctor` conflict, schema, freshness, and reference checks |
| Risky edits damage memory | Locked atomic writes and verifiable snapshots |

## Core capabilities

### 1. Ranked local recall

AIBrain indexes Markdown sections and active structured memories. Ranking combines phrase matches, token relevance, title matches, source authority, confidence, and scope.

```bash
./scripts/brain.sh index build
./scripts/brain.sh recall "tenant isolation" --limit 8
./scripts/brain.sh recall "http client" --kind stack --json
```

Every result identifies its source; no opaque vector store is required.

### 2. Durable structured memory

```bash
./scripts/brain.sh remember \
  "Use tenant-scoped query keys" \
  --kind preference \
  --scope goaaiseo \
  --tags react,security \
  --confidence 0.95 \
  --source user

./scripts/brain.sh forget mem-123456789abc \
  --reason "Superseded by DEC-014"
```

Memories are append-only JSONL events. Forgetting writes a tombstone instead of deleting history. Duplicate active memories are detected by content hash.

### 3. Compact context compiler

```bash
./scripts/brain.sh context \
  "add a distributed crawl scheduler" \
  --profile auto \
  --budget 1800
```

The compiler detects the current project, includes its rules, retrieves relevant decisions/corrections/patterns, and stops at the requested approximate token budget.

### 4. Project profiles

```bash
./scripts/brain.sh profile list
./scripts/brain.sh profile auto /projects/sandbox/ScrapeToolAi
./scripts/brain.sh profile show goaaiseo --json
```

Included profiles: `default`, `aibrain`, `goaaiseo`, and `scrapetoolai`. Profiles are plain JSON validated by `doctor`.

### 5. Routable super skills

```bash
./scripts/brain.sh skills list
./scripts/brain.sh skills route "resolve a dependency policy conflict"
./scripts/brain.sh skills show conflict-resolver
```

Included super skills:

- `memory-architect`
- `dependency-intelligence`
- `evidence-research`
- `code-pattern-synthesizer`
- `context-compiler`
- `conflict-resolver`
- `cross-repo-orchestrator`
- `self-healing-reviewer`

### 6. Local knowledge ingestion

```bash
./scripts/brain.sh ingest ./research.md \
  --kind reference \
  --scope goaaiseo \
  --tags seo,evidence
```

Ingestion accepts local text artifacts, fingerprints them, records provenance, avoids duplicates, and adds them to ranked retrieval. Fetch external sources with an approved tool first; AIBrain never executes ingested content.

### 7. Dependency evidence

```bash
./scripts/refresh.sh             # PyPI + npm
./scripts/refresh.sh --python
./scripts/refresh.sh --node --strict
```

Snapshots are written atomically under `feeds/` and include lookup status, current version, registry URL metadata, refresh time, and deprecation signals. Generated feeds remain local and are ignored by Git.

### 8. Doctor and snapshots

```bash
./scripts/brain.sh doctor
./scripts/brain.sh snapshot create before-migration
./scripts/brain.sh snapshot list
./scripts/brain.sh snapshot verify before-migration
```

Doctor checks required files, JSONL validity, duplicate/contradictory package policy, dangling patterns, profile and skill metadata, feed JSON/freshness, installed Kiro artifacts, and index freshness.

Snapshots copy mutable brain state and record SHA-256 hashes. v2 intentionally provides verification rather than an automatic destructive restore.

## Install

```bash
git clone https://github.com/consecrating/AIBrain.git
cd AIBrain
bash scripts/install.sh
```

The installer:

1. requires Python 3.9 or newer;
2. installs `.kiro/steering/aibrain.md` and `.kiro/skills/aibrain/SKILL.md`;
3. transactionally publishes the steering, skill, and active-root pointer with rollback;
4. initializes runtime files and the local index;
5. runs the canonical doctor and fails if integrity errors remain.

Override locations when needed:

```bash
KIRO_DIR=/custom/.kiro AIBRAIN_PYTHON=python3.12 bash scripts/install.sh
```

Root discovery order is `AIBRAIN_ROOT`, the active Kiro `.aibrain-path`, then the repository containing the runtime.

## CLI reference

```text
status [--json]                       Brain and active-task state
recall QUERY [filters]                Ranked cited retrieval
decide TEXT [REASON] [options]        Architectural decision
correct MISTAKE [FIX] [options]       Durable correction
remember TEXT [metadata]              Structured memory event
forget ID --reason TEXT               Memory tombstone
ingest FILE [metadata]                Fingerprinted local reference
context QUERY [profile/budget]        Compact context packet
pattern add NAME [options]            Proven pattern registration
stack add|ban PACKAGE [options]       Dependency policy
profile list|show|auto                Project profile operations
skills list|show|route                Super-skill operations
index build|status                    Local search index
snapshot create|list|verify           State snapshot operations
journal [TEXT]                        Append or inspect journal
next [ACTION]                         Read or set next action
doctor / validate                     Integrity and freshness checks
stats [--json]                        Knowledge statistics
init                                  Initialize runtime state
```

Run `./scripts/brain.sh COMMAND --help` for exact options.

## Backward compatibility

AIBrain v2 preserves the v1 executable, installed paths, no-argument `status`, and all v1 positional commands:

```bash
./scripts/brain.sh decide "Use X over Y" "Reason"
./scripts/brain.sh correct "What went wrong" "What to do instead"
./scripts/brain.sh stack add httpx ">=0.25" "Modern async HTTP"
./scripts/brain.sh stack ban requests "Sync only" httpx
./scripts/brain.sh journal "Important observation"
./scripts/brain.sh next "Implement the adapter"
./scripts/brain.sh validate
```

Long options are additive; no existing positional form was removed.

## Architecture

```text
scripts/brain.sh                  stable launcher
scripts/aibrain.py                stdlib CLI and command contracts
scripts/aibrain_core/             paths, safe I/O, index, doctor, profiles, skills, snapshots
brain/
  identity.md                     developer and stack identity
  decisions/                      append-only architectural decisions
  patterns/                       proven implementation patterns
  profiles/                       repository-specific policies
  skills/                         routable super-skill definitions
  schemas/                        JSON schemas for structured records
  stack/                          approved, banned, and alternative dependencies
  references/                     locally ingested knowledge (ignored by default)
memory/
  active-task.md                  resumable task state
  corrections.md                 durable behavioral corrections
  journal.md                     append-only event journal
  store.jsonl                    generated structured memory events
feeds/                            generated package evidence
.aibrain/                         generated index, locks, and snapshots
```

Detailed design and compatibility rationale: [`docs/V2-ARCHITECTURE.md`](docs/V2-ARCHITECTURE.md).

## Security and privacy

- Generated structured memory, ingested references, feeds, indexes, locks, and snapshots are ignored by Git by default.
- Deliberately promoted knowledge—decisions, corrections, active-task state, journal entries, patterns, and stack policy—is tracked and reviewable. Do not write secrets to those files.
- Ingestion reads local files only and enforces a configurable size limit.
- Fetched content is never executed by AIBrain.
- Package refresh contacts only PyPI and npm registry endpoints derived from approved package names.
- Review any runtime knowledge before deliberately committing it.

## Integration with SuperBrain

AIBrain v2 preserves SuperBrain's existing AIBrain contracts:

- `scripts/install.sh` remains the installation entry point and validates before publishing integration files.
- `scripts/brain.sh` remains executable.
- `.kiro/skills/aibrain/SKILL.md` and `.kiro/steering/aibrain.md` retain their paths.
- `AIBRAIN_ROOT=/projects/sandbox/AIBrain` remains supported.

SuperBrain v1 can install and verify AIBrain v2 without a manifest change. A future SuperBrain hardening should preserve the installer's exit status instead of filtering it through `grep ... || true`; AIBrain's own installer does propagate failures.

## License

MIT

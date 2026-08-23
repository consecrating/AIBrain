"""Deterministic local index and weighted ranked retrieval."""

from __future__ import annotations

import hashlib
import json
import math
import re
from collections import Counter
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Any

from .io_utils import atomic_write, read_jsonl
from .paths import BrainPaths

TOKEN_RE = re.compile(r"[a-z0-9][a-z0-9_+.-]*", re.IGNORECASE)
HEADING_RE = re.compile(r"^(#{1,4})\s+(.+)$", re.MULTILINE)
SOURCE_WEIGHTS = {
    "correction": 2.2,
    "decision": 2.0,
    "stack": 1.8,
    "pattern": 1.7,
    "profile": 1.6,
    "skill": 1.5,
    "memory": 1.5,
    "rule": 1.4,
    "context": 1.3,
    "identity": 1.3,
    "task": 1.2,
    "reference": 1.0,
}


def tokenize(text: str) -> list[str]:
    return [token.lower() for token in TOKEN_RE.findall(text) if len(token) > 1]


def _kind(relative: str) -> str:
    if "corrections" in relative:
        return "correction"
    if "decisions/" in relative:
        return "decision"
    if "stack/" in relative:
        return "stack"
    if "patterns/" in relative:
        return "pattern"
    if "profiles/" in relative:
        return "profile"
    if "skills/" in relative:
        return "skill"
    if relative.startswith("rules/"):
        return "rule"
    if "context/" in relative:
        return "context"
    if relative.endswith("identity.md"):
        return "identity"
    if relative.endswith("active-task.md"):
        return "task"
    if "references/" in relative:
        return "reference"
    return "knowledge"


def _markdown_documents(paths: BrainPaths) -> list[dict[str, Any]]:
    files = [*paths.brain.rglob("*.md"), *paths.profiles.glob("*.json"), *paths.rules.rglob("*.md")]
    files.extend(path for path in paths.memory.glob("*.md") if path.name != "scratchpad.md")
    ingest_metadata = {
        str(record.get("target")): record
        for record in read_jsonl(paths.ingest_log)
        if record.get("event") == "ingest" and record.get("target")
    }
    documents: list[dict[str, Any]] = []
    for path in sorted(set(files)):
        text = path.read_text(encoding="utf-8", errors="replace")
        relative = str(path.relative_to(paths.root))
        metadata = ingest_metadata.get(relative, {})
        headings = list(HEADING_RE.finditer(text))
        if not headings:
            headings = [re.match(r"", "")]
        for index, heading in enumerate(headings):
            if heading is None:
                continue
            start = heading.start() if heading.group(0) else 0
            end = headings[index + 1].start() if index + 1 < len(headings) else len(text)
            title = heading.group(2).strip() if heading.group(0) else path.stem
            body = text[start:end].strip()
            if not body:
                continue
            doc_id = hashlib.sha256(f"{relative}:{title}:{start}".encode()).hexdigest()[:16]
            documents.append(
                {
                    "id": f"doc-{doc_id}",
                    "kind": metadata.get("kind") or _kind(relative),
                    "title": title,
                    "text": body,
                    "source": relative,
                    "updated": metadata.get("created_at") or datetime.fromtimestamp(path.stat().st_mtime, timezone.utc).isoformat(),
                    "confidence": 1.0,
                    "scope": metadata.get("scope", "global"),
                    "tags": metadata.get("tags", []),
                }
            )
    return documents


def active_memories(paths: BrainPaths) -> list[dict[str, Any]]:
    records = read_jsonl(paths.store)
    tombstones = {str(record.get("target_id")) for record in records if record.get("event") == "forget"}
    today = date.today().isoformat()
    memories: list[dict[str, Any]] = []
    for record in records:
        if record.get("event") != "remember" or record.get("id") in tombstones:
            continue
        expires = str(record.get("expires") or "")
        if expires and expires < today:
            continue
        memories.append(record)
    return memories


def build_index(paths: BrainPaths) -> dict[str, Any]:
    documents = _markdown_documents(paths)
    for record in active_memories(paths):
        documents.append(
            {
                "id": record["id"],
                "kind": record.get("kind", "memory"),
                "title": record.get("title") or str(record.get("text", ""))[:72],
                "text": record.get("text", ""),
                "source": record.get("source", "memory/store.jsonl"),
                "updated": record.get("created_at"),
                "confidence": record.get("confidence", 1.0),
                "scope": record.get("scope", "global"),
                "tags": record.get("tags", []),
            }
        )
    payload = {
        "schema_version": 2,
        "built_at": datetime.now(timezone.utc).isoformat(),
        "document_count": len(documents),
        "documents": documents,
    }
    atomic_write(paths.index, json.dumps(payload, indent=2, ensure_ascii=False) + "\n")
    return payload


def index_is_stale(paths: BrainPaths) -> bool:
    if not paths.index.exists():
        return True
    index_mtime = paths.index.stat().st_mtime
    sources = [*paths.brain.rglob("*.md"), *paths.profiles.glob("*.json"), *paths.rules.rglob("*.md")]
    sources.extend(path for path in paths.memory.glob("*.md") if path.name != "scratchpad.md")
    if paths.store.exists():
        sources.append(paths.store)
    return any(path.stat().st_mtime > index_mtime for path in sources)


def load_index(paths: BrainPaths, rebuild: bool = False) -> dict[str, Any]:
    if rebuild or index_is_stale(paths):
        return build_index(paths)
    try:
        payload = json.loads(paths.index.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return build_index(paths)
    return payload if isinstance(payload, dict) else build_index(paths)


def search(
    paths: BrainPaths,
    query: str,
    *,
    limit: int = 8,
    kind: str | None = None,
    scope: str | None = None,
) -> list[dict[str, Any]]:
    payload = load_index(paths)
    documents = list(payload.get("documents", []))
    query_terms = tokenize(query)
    if not query_terms:
        return []
    document_frequency: Counter[str] = Counter()
    tokenized: list[tuple[dict[str, Any], list[str]]] = []
    for document in documents:
        tokens = tokenize(f"{document.get('title', '')} {document.get('text', '')}")
        tokenized.append((document, tokens))
        document_frequency.update(set(tokens))
    total = max(len(documents), 1)
    phrase = query.lower().strip()
    ranked: list[dict[str, Any]] = []
    for document, tokens in tokenized:
        if kind and document.get("kind") != kind:
            continue
        if scope and document.get("scope") not in {scope, "global"}:
            continue
        counts = Counter(tokens)
        title = str(document.get("title", "")).lower()
        body = str(document.get("text", "")).lower()
        score = 0.0
        for term in query_terms:
            if not counts[term]:
                continue
            inverse = math.log((total + 1) / (document_frequency[term] + 1)) + 1
            score += (1 + math.log(counts[term])) * inverse
            if term in title:
                score += 3.0
        if phrase and phrase in body:
            score += 8.0
        if all(term in counts for term in query_terms):
            score += 4.0
        score *= SOURCE_WEIGHTS.get(str(document.get("kind")), 1.0)
        score *= float(document.get("confidence", 1.0))
        updated = str(document.get("updated") or "")
        try:
            updated_at = datetime.fromisoformat(updated.replace("Z", "+00:00"))
            if updated_at.tzinfo is None:
                updated_at = updated_at.replace(tzinfo=timezone.utc)
            age_days = max((datetime.now(timezone.utc) - updated_at).days, 0)
            score *= max(0.85, 1.0 - min(age_days, 3650) / 24333)
        except ValueError:
            pass
        if score > 0:
            ranked.append({**document, "score": round(score, 3)})
    return sorted(ranked, key=lambda item: (-float(item["score"]), str(item.get("source"))))[:limit]

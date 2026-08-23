#!/usr/bin/env python3
"""AIBrain v2 CLI — local-first memory, retrieval, routing, and diagnostics."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import uuid
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Any

from aibrain_core import __version__
from aibrain_core.doctor import run_doctor
from aibrain_core.index import active_memories, build_index, index_is_stale, load_index, search
from aibrain_core.io_utils import (
    append_jsonl,
    append_line,
    atomic_write,
    content_id,
    insert_before,
    markdown_cell,
    read_jsonl,
    replace_markdown_section,
    safe_slug,
    write_lock,
)
from aibrain_core.paths import BrainPaths
from aibrain_core.profiles import auto_profile, get_profile, load_profiles
from aibrain_core.skills import load_skills, route_skills
from aibrain_core.snapshots import create_snapshot, list_snapshots, verify_snapshot

NOW = lambda: datetime.now(timezone.utc).replace(microsecond=0).isoformat()
TODAY = lambda: date.today().isoformat()


def emit(value: Any, *, as_json: bool = False) -> None:
    if as_json:
        print(json.dumps(value, indent=2, ensure_ascii=False))
    elif isinstance(value, str):
        print(value)
    else:
        print(json.dumps(value, indent=2, ensure_ascii=False))


def count(pattern: str, path: Path) -> int:
    if not path.exists():
        return 0
    return sum(bool(re.search(pattern, line)) for line in path.read_text(encoding="utf-8").splitlines())


def journal(paths: BrainPaths, category: str, message: str) -> None:
    append_line(paths.memory / "journal.md", f"- [{NOW()}] [{category}] {message}")


def next_decision_number(path: Path) -> int:
    numbers = [int(match.group(1)) for match in re.finditer(r"(?m)^\|\s*(\d+)\s*\|", path.read_text(encoding="utf-8"))]
    return max(numbers, default=0) + 1


def command_status(paths: BrainPaths, args: argparse.Namespace) -> int:
    active_task = (paths.memory / "active-task.md").read_text(encoding="utf-8")
    fields = dict(re.findall(r"(?m)^- \*\*(Goal|Status|Started|Last Updated):\*\*\s*(.+)$", active_task))
    next_match = re.search(r"(?ms)^## Next Action\s*\n+(.+?)(?=^##\s|\Z)", active_task)
    payload = {
        "version": __version__,
        "root": str(paths.root),
        "goal": fields.get("Goal"),
        "status": fields.get("Status"),
        "next_action": next_match.group(1).strip() if next_match else None,
        "decisions": count(r"^\|\s*\d+\s*\|", paths.brain / "decisions/_index.md"),
        "patterns": count(r"^\|\s*[A-Z]{2}-\d+\s*\|", paths.brain / "patterns/_index.md"),
        "memories": len(active_memories(paths)),
        "profiles": len(load_profiles(paths)),
        "skills": len(load_skills(paths)),
        "index_stale": index_is_stale(paths),
    }
    if args.json:
        emit(payload, as_json=True)
    else:
        print(f"AIBrain {__version__}")
        print(f"Root: {payload['root']}")
        print(f"Goal: {payload['goal'] or '(none)'}")
        print(f"Status: {payload['status'] or '(unknown)'}")
        print(f"Next: {payload['next_action'] or '(none)'}")
        print(
            "Knowledge: "
            f"{payload['decisions']} decisions | {payload['patterns']} patterns | "
            f"{payload['memories']} memories | {payload['profiles']} profiles | {payload['skills']} skills"
        )
        print(f"Index: {'stale' if payload['index_stale'] else 'current'}")
    return 0


def command_recall(paths: BrainPaths, args: argparse.Namespace) -> int:
    query = " ".join(args.query)
    results = search(paths, query, limit=args.limit, kind=args.kind, scope=args.scope)
    if args.json:
        emit({"query": query, "results": results}, as_json=True)
        return 0
    print(f"Recall: {query}")
    if not results:
        print("No matching knowledge found.")
        return 0
    for index, result in enumerate(results, 1):
        snippet = " ".join(str(result.get("text", "")).split())[:240]
        print(f"{index}. [{result['kind']}] {result['title']} (score {result['score']})")
        print(f"   {result['source']}")
        print(f"   {snippet}")
    return 0


def command_decide(paths: BrainPaths, args: argparse.Namespace) -> int:
    reason = args.reason_option or args.reason or "pending rationale"
    decision = markdown_cell(args.decision)
    with write_lock(paths.runtime):
        index_path = paths.brain / "decisions/_index.md"
        number = next_decision_number(index_path)
        row = f"| {number:03d} | {TODAY()} | {decision} | ✅ Active | {markdown_cell(reason)} |"
        insert_before(index_path, "## Decision Template", row)
        if args.context or args.alternatives:
            detail = [
                f"# DEC-{number:03d}: {args.decision}",
                "",
                f"- **Date:** {TODAY()}",
                "- **Status:** Active",
                f"- **Context:** {args.context or reason}",
                f"- **Decision:** {args.decision}",
                f"- **Alternatives rejected:** {args.alternatives or 'Not recorded'}",
                f"- **Consequences:** {reason}",
            ]
            atomic_write(paths.brain / "decisions" / f"{number:03d}-{safe_slug(args.decision)}.md", "\n".join(detail) + "\n")
        journal(paths, "DECISION", f"DEC-{number:03d}: {args.decision}")
    print(f"Decision #{number:03d} recorded: {args.decision}")
    return 0


def command_correct(paths: BrainPaths, args: argparse.Namespace) -> int:
    corrections = paths.memory / "corrections.md"
    fix = markdown_cell(args.do_instead or args.fix or "TBD — fill in the correct behavior")
    why = markdown_cell(args.why or "User correction")
    mistake = markdown_cell(args.mistake)
    scope = args.scope
    with write_lock(paths.runtime):
        existing = corrections.read_text(encoding="utf-8")
        numbers = [int(value) for value in re.findall(r"Correction #(\d+)", existing)]
        number = max(numbers, default=0) + 1
        block = (
            f"### [{TODAY()}] Correction #{number}\n"
            f"- **What I did wrong:** {mistake}\n"
            f"- **What to do instead:** {fix}\n"
            f"- **Why:** {why}\n"
            f"- **Scope:** {scope}\n"
        )
        marker = "---\n\n## How to Add"
        if marker in existing:
            insert_before(corrections, marker, block)
        else:
            append_line(corrections, "\n" + block)
        journal(paths, "CORRECTION", f"#{number}: {mistake}")
    print(f"Correction #{number} recorded: {mistake}")
    return 0


def _insert_table_row(
    path: Path,
    heading: str,
    header: str,
    separator: str,
    marker: str,
    row: str,
) -> None:
    text = path.read_text(encoding="utf-8")
    if heading not in text:
        block = f"{heading}\n\n{header}\n{separator}\n{row}\n\n"
        if marker not in text:
            raise ValueError(f"Insertion marker not found in {path}: {marker}")
        atomic_write(path, text.replace(marker, block + marker, 1))
        return
    start = text.index(heading)
    following = re.search(r"(?m)^##\s", text[start + len(heading) :])
    end = start + len(heading) + following.start() if following else len(text)
    section = text[start:end].rstrip() + f"\n{row}\n\n"
    atomic_write(path, text[:start] + section + text[end:])


def command_stack_add(paths: BrainPaths, args: argparse.Namespace) -> int:
    registry = paths.brain / "stack/registry.md"
    banned = paths.brain / "stack/banned.md"
    version = args.version or ">=latest"
    reason = args.reason_option or args.reason or "approved"
    heading = "## Custom Approved (Python)" if args.ecosystem == "python" else "## Custom Approved (Node)"
    with write_lock(paths.runtime):
        if re.search(rf"(?mi)^\|\s*{re.escape(args.package)}\s*\|", banned.read_text(encoding="utf-8")):
            raise ValueError(f"Package is banned; resolve the conflict first: {args.package}")
        current = registry.read_text(encoding="utf-8")
        if re.search(rf"(?mi)^\|\s*{re.escape(args.package)}\s*\|", current):
            raise ValueError(f"Package already approved: {args.package}")
        row = (
            f"| {markdown_cell(args.package)} | {markdown_cell(version)} | "
            f"{markdown_cell(reason)} | {markdown_cell(args.replaces or '—')} |"
        )
        _insert_table_row(
            registry,
            heading,
            "| Package | Version | Purpose | Replaces |",
            "|---------|---------|---------|----------|",
            "## Freshness Policy",
            row,
        )
        journal(paths, "STACK", f"Approved ({args.ecosystem}): {args.package} {version}")
    print(f"Approved ({args.ecosystem}): {args.package} {version}")
    return 0


def command_stack_ban(paths: BrainPaths, args: argparse.Namespace) -> int:
    registry = paths.brain / "stack/registry.md"
    banned = paths.brain / "stack/banned.md"
    reason = args.reason_option or args.reason or "banned"
    alternative = args.use or args.alternative or "find alternative"
    with write_lock(paths.runtime):
        if re.search(rf"(?mi)^\|\s*{re.escape(args.package)}\s*\|", registry.read_text(encoding="utf-8")):
            raise ValueError(f"Package is approved; resolve the conflict first: {args.package}")
        current = banned.read_text(encoding="utf-8")
        if re.search(rf"(?mi)^\|\s*{re.escape(args.package)}\s*\|", current):
            raise ValueError(f"Package already banned: {args.package}")
        row = f"| {markdown_cell(args.package)} | {markdown_cell(reason)} | {markdown_cell(alternative)} |"
        _insert_table_row(
            banned,
            "## Custom Bans",
            "| Package | Reason | Use Instead |",
            "|---------|--------|-------------|",
            "## How to Challenge a Ban",
            row,
        )
        journal(paths, "STACK", f"Banned: {args.package}; use {alternative}")
    print(f"Banned: {args.package}; use {alternative}")
    return 0


def command_journal(paths: BrainPaths, args: argparse.Namespace) -> int:
    if not args.text:
        lines = (paths.memory / "journal.md").read_text(encoding="utf-8").splitlines()
        print("\n".join(lines[-args.limit :]))
        return 0
    text = " ".join(args.text)
    with write_lock(paths.runtime):
        journal(paths, args.category.upper(), text)
    print("Journal entry recorded.")
    return 0


def command_next(paths: BrainPaths, args: argparse.Namespace) -> int:
    task = paths.memory / "active-task.md"
    if not args.action:
        text = task.read_text(encoding="utf-8")
        match = re.search(r"(?ms)^## Next Action\s*\n+(.+?)(?=^##\s|\Z)", text)
        print(match.group(1).strip() if match else "(none)")
        return 0
    action = " ".join(args.action)
    with write_lock(paths.runtime):
        replace_markdown_section(task, "## Next Action", action)
        journal(paths, "NEXT", action)
    print(f"Next: {action}")
    return 0


def command_remember(paths: BrainPaths, args: argparse.Namespace) -> int:
    text = " ".join(args.text)
    if not 0 <= args.confidence <= 1:
        raise ValueError("--confidence must be between 0 and 1")
    if args.expires:
        try:
            date.fromisoformat(args.expires)
        except ValueError as error:
            raise ValueError("--expires must use YYYY-MM-DD") from error
    digest = hashlib.sha256(f"{args.kind}\x1f{args.scope}\x1f{text}".encode()).hexdigest()
    with write_lock(paths.runtime):
        existing = active_memories(paths)
        for record in existing:
            if record.get("content_hash") == digest:
                print(f"Already remembered: {record['id']}")
                return 0
        existing_ids = {str(record.get("id")) for record in read_jsonl(paths.store)}
        memory_id = f"mem-{uuid.uuid4().hex[:12]}"
        while memory_id in existing_ids:
            memory_id = f"mem-{uuid.uuid4().hex[:12]}"
        record = {
            "schema_version": 2,
            "event": "remember",
            "id": memory_id,
            "created_at": NOW(),
            "kind": args.kind,
            "scope": args.scope,
            "tags": [tag.strip() for tag in args.tags.split(",") if tag.strip()],
            "confidence": args.confidence,
            "source": args.source,
            "expires": args.expires,
            "text": text,
            "content_hash": digest,
        }
        append_jsonl(paths.store, record)
        journal(paths, "MEMORY", f"Remembered {record['id']}: {text[:96]}")
    emit(record, as_json=args.json)
    return 0


def command_forget(paths: BrainPaths, args: argparse.Namespace) -> int:
    with write_lock(paths.runtime):
        active = {record["id"] for record in active_memories(paths)}
        if args.memory_id not in active:
            raise KeyError(f"Active memory not found: {args.memory_id}")
        record = {
            "schema_version": 2,
            "event": "forget",
            "id": content_id("evt", NOW(), args.memory_id, uuid.uuid4().hex),
            "target_id": args.memory_id,
            "created_at": NOW(),
            "reason": markdown_cell(args.reason),
        }
        append_jsonl(paths.store, record)
        journal(paths, "MEMORY", f"Forgot {args.memory_id}: {record['reason']}")
    emit(record, as_json=args.json)
    return 0


def command_ingest(paths: BrainPaths, args: argparse.Namespace) -> int:
    source = Path(args.file).expanduser().resolve()
    if not source.is_file():
        raise FileNotFoundError(source)
    if source.stat().st_size > args.max_bytes:
        raise ValueError(f"File exceeds --max-bytes ({args.max_bytes}): {source}")
    raw = source.read_bytes()
    digest = hashlib.sha256(raw).hexdigest()
    text = raw.decode("utf-8", errors="replace")
    ingestion_id = content_id("ing", digest, args.scope, args.kind)
    target = paths.references / f"{ingestion_id}-{safe_slug(source.stem)}.md"
    title = args.title or source.stem.replace("-", " ").title()
    metadata = (
        f"# {title}\n\n"
        f"> Ingested from `{source}` on {TODAY()}; SHA-256 `{digest}`.\n\n"
        f"<!-- kind: {args.kind}; scope: {args.scope}; tags: {args.tags} -->\n\n"
    )
    with write_lock(paths.runtime):
        records = read_jsonl(paths.ingest_log)
        if any(
            record.get("sha256") == digest
            and record.get("scope") == args.scope
            and record.get("kind") == args.kind
            for record in records
        ):
            existing = next(
                record
                for record in records
                if record.get("sha256") == digest
                and record.get("scope") == args.scope
                and record.get("kind") == args.kind
            )
            print(f"Already ingested in {args.scope}: {existing['id']} -> {existing['target']}")
            return 0
        if target.exists():
            raise ValueError(f"Ingestion target already exists without provenance: {target}")
        atomic_write(target, metadata + text)
        record = {
            "schema_version": 1,
            "event": "ingest",
            "id": ingestion_id,
            "created_at": NOW(),
            "source": str(source),
            "target": str(target.relative_to(paths.root)),
            "sha256": digest,
            "kind": args.kind,
            "scope": args.scope,
            "tags": [tag.strip() for tag in args.tags.split(",") if tag.strip()],
        }
        append_jsonl(paths.ingest_log, record)
        journal(paths, "INGEST", f"{source} -> {record['target']}")
    emit(record, as_json=args.json)
    return 0


def command_context(paths: BrainPaths, args: argparse.Namespace) -> int:
    query = " ".join(args.query)
    if args.profile == "auto":
        profile, profile_score = auto_profile(paths, Path(args.path or Path.cwd()))
    else:
        profile, profile_score = get_profile(paths, args.profile), 100
    effective_scope = args.scope or str(profile.get("scope") or "global")
    results = search(paths, query, limit=args.limit, scope=effective_scope)
    packet = {
        "schema_version": 2,
        "query": query,
        "profile": profile.get("name"),
        "scope": effective_scope,
        "profile_score": profile_score,
        "rules": profile.get("rules", []),
        "knowledge": [],
    }
    remaining = max(args.budget * 4, 400)
    for result in results:
        excerpt = " ".join(str(result.get("text", "")).split())
        excerpt = excerpt[: min(remaining, args.excerpt_chars)]
        if not excerpt:
            continue
        item = {
            "kind": result["kind"],
            "title": result["title"],
            "source": result["source"],
            "score": result["score"],
            "excerpt": excerpt,
        }
        packet["knowledge"].append(item)
        remaining -= len(excerpt)
        if remaining <= 0:
            break
    if args.json:
        emit(packet, as_json=True)
    else:
        print(f"# AIBrain Context: {query}\n")
        print(f"Profile: {packet['profile']}\n")
        if packet["rules"]:
            print("## Profile Rules")
            for rule in packet["rules"]:
                print(f"- {rule}")
            print()
        print("## Relevant Knowledge")
        for item in packet["knowledge"]:
            print(f"### [{item['kind']}] {item['title']}")
            print(f"Source: `{item['source']}` | Score: {item['score']}")
            print(item["excerpt"] + "\n")
    return 0


def command_pattern_add(paths: BrainPaths, args: argparse.Namespace) -> int:
    index_path = paths.brain / "patterns/_index.md"
    prefix = args.category.upper()
    slug = safe_slug(args.name)
    relative = f"patterns/{slug}.md"
    target = paths.brain / relative
    with write_lock(paths.runtime):
        text = index_path.read_text(encoding="utf-8")
        if target.exists() or re.search(rf"(?mi)^\|[^|]+\|\s*{re.escape(args.name)}\s*\|", text):
            raise ValueError(f"Pattern already exists: {args.name}")
        existing = [int(value) for value in re.findall(rf"\|\s*{re.escape(prefix)}-(\d+)\s*\|", text)]
        number = max(existing, default=0) + 1
        pattern_id = f"{prefix}-{number:03d}"
        body = (
            f"# {args.name}\n\n"
            f"- **ID:** {pattern_id}\n"
            f"- **Problem:** {args.problem}\n"
            f"- **Use when:** {args.when}\n"
            f"- **Source:** {args.source}\n\n"
            f"## Solution\n\n{args.solution}\n"
        )
        atomic_write(target, body)
        try:
            row = f"| {pattern_id} | {markdown_cell(args.name)} | {markdown_cell(args.source)} | `{relative}` |"
            insert_before(index_path, "## How to Add a Pattern", row)
        except BaseException:
            target.unlink(missing_ok=True)
            raise
        journal(paths, "PATTERN", f"Added {pattern_id}: {args.name}")
    print(f"Pattern {pattern_id} added: {relative}")
    return 0


def command_profiles(paths: BrainPaths, args: argparse.Namespace) -> int:
    if args.profile_command == "list":
        values = [{key: value for key, value in profile.items() if key != "_path"} for profile in load_profiles(paths)]
        emit(values, as_json=args.json)
    elif args.profile_command == "show":
        emit(get_profile(paths, args.name), as_json=True if args.json else False)
    else:
        profile, score = auto_profile(paths, Path(args.path))
        emit({"profile": profile, "score": score}, as_json=args.json)
    return 0


def command_skills(paths: BrainPaths, args: argparse.Namespace) -> int:
    if args.skills_command == "list":
        values = [{key: value for key, value in skill.items() if key not in {"body", "path"}} for skill in load_skills(paths)]
        emit(values, as_json=args.json)
    elif args.skills_command == "show":
        match = next((skill for skill in load_skills(paths) if skill.get("name") == args.name), None)
        if not match:
            raise KeyError(f"Unknown skill: {args.name}")
        emit(match if args.json else match["body"], as_json=args.json)
    else:
        task = " ".join(args.task)
        results = route_skills(paths, task, limit=args.limit)
        if args.json:
            emit({"task": task, "skills": results}, as_json=True)
        else:
            print(f"Skill route: {task}")
            for item in results:
                print(f"- {item['name']} (score {item['score']}): {item.get('description', '')}")
    return 0


def command_index(paths: BrainPaths, args: argparse.Namespace) -> int:
    if args.index_command == "build":
        payload = build_index(paths)
        emit({"built_at": payload["built_at"], "documents": payload["document_count"]}, as_json=args.json)
    else:
        payload = load_index(paths)
        emit(
            {
                "path": str(paths.index),
                "stale": index_is_stale(paths),
                "built_at": payload.get("built_at"),
                "documents": payload.get("document_count", 0),
            },
            as_json=args.json,
        )
    return 0


def command_doctor(paths: BrainPaths, args: argparse.Namespace) -> int:
    report = run_doctor(paths)
    if args.json:
        emit(report, as_json=True)
    else:
        print(f"AIBrain doctor: {'HEALTHY' if report['ok'] else 'UNHEALTHY'}")
        print(f"Errors: {report['errors']} | Warnings: {report['warnings']}")
        for issue in report["issues"]:
            print(f"- {issue['severity'].upper()} [{issue['code']}] {issue['message']}")
    return 0 if report["ok"] else 1


def command_stats(paths: BrainPaths, args: argparse.Namespace) -> int:
    payload = load_index(paths)
    data = {
        "version": __version__,
        "brain_files": len(list(paths.brain.rglob("*.md"))),
        "rule_files": len(list(paths.rules.rglob("*.md"))),
        "memories": len(active_memories(paths)),
        "ingested": len(read_jsonl(paths.ingest_log)),
        "profiles": len(load_profiles(paths)),
        "skills": len(load_skills(paths)),
        "indexed_documents": payload.get("document_count", 0),
        "snapshots": len(list_snapshots(paths)),
    }
    emit(data, as_json=args.json)
    return 0


def command_snapshot(paths: BrainPaths, args: argparse.Namespace) -> int:
    if args.snapshot_command == "create":
        emit(create_snapshot(paths, args.name), as_json=args.json)
    elif args.snapshot_command == "list":
        emit(list_snapshots(paths), as_json=args.json)
    else:
        result = verify_snapshot(paths, args.name)
        emit(result, as_json=args.json)
        return 0 if result["ok"] else 1
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="brain.sh", description="AIBrain v2 local intelligence runtime")
    parser.add_argument("--version", action="version", version=f"AIBrain {__version__}")
    sub = parser.add_subparsers(dest="command")

    status = sub.add_parser("status", help="show brain and active-task state")
    status.add_argument("--json", action="store_true")

    recall = sub.add_parser("recall", help="rank relevant knowledge")
    recall.add_argument("query", nargs="+")
    recall.add_argument("--limit", type=int, default=8)
    recall.add_argument("--kind")
    recall.add_argument("--scope")
    recall.add_argument("--json", action="store_true")

    decide = sub.add_parser("decide", help="record an architectural decision")
    decide.add_argument("decision")
    decide.add_argument("reason", nargs="?")
    decide.add_argument("--reason", dest="reason_option")
    decide.add_argument("--context")
    decide.add_argument("--alternatives")

    correct = sub.add_parser("correct", help="record a correction")
    correct.add_argument("mistake")
    correct.add_argument("fix", nargs="?")
    correct.add_argument("--do-instead")
    correct.add_argument("--why")
    correct.add_argument("--scope", default="always", choices=("always", "repo", "task"))

    stack = sub.add_parser("stack", help="manage dependency policy")
    stack_sub = stack.add_subparsers(dest="stack_command", required=True)
    stack_add = stack_sub.add_parser("add")
    stack_add.add_argument("package")
    stack_add.add_argument("version", nargs="?")
    stack_add.add_argument("reason", nargs="?")
    stack_add.add_argument("--reason", dest="reason_option")
    stack_add.add_argument("--replaces")
    stack_add.add_argument("--ecosystem", choices=("python", "node"), default="python")
    stack_ban = stack_sub.add_parser("ban")
    stack_ban.add_argument("package")
    stack_ban.add_argument("reason", nargs="?")
    stack_ban.add_argument("alternative", nargs="?")
    stack_ban.add_argument("--reason", dest="reason_option")
    stack_ban.add_argument("--use")

    journal_parser = sub.add_parser("journal", help="view or append journal entries")
    journal_parser.add_argument("text", nargs="*")
    journal_parser.add_argument("--category", default="NOTE")
    journal_parser.add_argument("--limit", type=int, default=20)

    next_parser = sub.add_parser("next", help="view or set the next action")
    next_parser.add_argument("action", nargs="*")

    remember = sub.add_parser("remember", help="store structured durable memory")
    remember.add_argument("text", nargs="+")
    remember.add_argument("--kind", default="fact")
    remember.add_argument("--scope", default="global")
    remember.add_argument("--tags", default="")
    remember.add_argument("--confidence", type=float, default=1.0)
    remember.add_argument("--source", default="user")
    remember.add_argument("--expires")
    remember.add_argument("--json", action="store_true")

    forget = sub.add_parser("forget", help="retract a structured memory")
    forget.add_argument("memory_id")
    forget.add_argument("--reason", required=True)
    forget.add_argument("--json", action="store_true")

    ingest = sub.add_parser("ingest", help="ingest a local knowledge document")
    ingest.add_argument("file")
    ingest.add_argument("--title")
    ingest.add_argument("--kind", default="reference")
    ingest.add_argument("--scope", default="global")
    ingest.add_argument("--tags", default="")
    ingest.add_argument("--max-bytes", type=int, default=2_000_000)
    ingest.add_argument("--json", action="store_true")

    context = sub.add_parser("context", help="compile a compact context packet")
    context.add_argument("query", nargs="+")
    context.add_argument("--profile", default="auto")
    context.add_argument("--path")
    context.add_argument("--scope")
    context.add_argument("--budget", type=int, default=1800, help="approximate token budget")
    context.add_argument("--limit", type=int, default=12)
    context.add_argument("--excerpt-chars", type=int, default=900)
    context.add_argument("--json", action="store_true")

    pattern = sub.add_parser("pattern", help="manage proven patterns")
    pattern_sub = pattern.add_subparsers(dest="pattern_command", required=True)
    pattern_add = pattern_sub.add_parser("add")
    pattern_add.add_argument("name")
    pattern_add.add_argument("--problem", required=True)
    pattern_add.add_argument("--solution", required=True)
    pattern_add.add_argument("--source", default="AIBrain")
    pattern_add.add_argument("--when", default="When the described problem occurs")
    pattern_add.add_argument("--category", default="AR", choices=("PY", "TS", "AR", "AI"))

    profile = sub.add_parser("profile", help="inspect project profiles")
    profile_sub = profile.add_subparsers(dest="profile_command", required=True)
    profile_list = profile_sub.add_parser("list")
    profile_list.add_argument("--json", action="store_true")
    profile_show = profile_sub.add_parser("show")
    profile_show.add_argument("name")
    profile_show.add_argument("--json", action="store_true")
    profile_auto = profile_sub.add_parser("auto")
    profile_auto.add_argument("path")
    profile_auto.add_argument("--json", action="store_true")

    skills = sub.add_parser("skills", help="discover and route super skills")
    skills_sub = skills.add_subparsers(dest="skills_command", required=True)
    skills_list = skills_sub.add_parser("list")
    skills_list.add_argument("--json", action="store_true")
    skills_show = skills_sub.add_parser("show")
    skills_show.add_argument("name")
    skills_show.add_argument("--json", action="store_true")
    skills_route = skills_sub.add_parser("route")
    skills_route.add_argument("task", nargs="+")
    skills_route.add_argument("--limit", type=int, default=5)
    skills_route.add_argument("--json", action="store_true")

    index = sub.add_parser("index", help="manage local search index")
    index_sub = index.add_subparsers(dest="index_command", required=True)
    index_build = index_sub.add_parser("build")
    index_build.add_argument("--json", action="store_true")
    index_status = index_sub.add_parser("status")
    index_status.add_argument("--json", action="store_true")

    doctor = sub.add_parser("doctor", help="run integrity and freshness diagnostics")
    doctor.add_argument("--json", action="store_true")
    validate = sub.add_parser("validate", help="alias for doctor")
    validate.add_argument("--json", action="store_true")

    stats = sub.add_parser("stats", help="show knowledge statistics")
    stats.add_argument("--json", action="store_true")

    snapshot = sub.add_parser("snapshot", help="create and verify state snapshots")
    snapshot_sub = snapshot.add_subparsers(dest="snapshot_command", required=True)
    snapshot_create = snapshot_sub.add_parser("create")
    snapshot_create.add_argument("name", nargs="?")
    snapshot_create.add_argument("--json", action="store_true")
    snapshot_list = snapshot_sub.add_parser("list")
    snapshot_list.add_argument("--json", action="store_true")
    snapshot_verify = snapshot_sub.add_parser("verify")
    snapshot_verify.add_argument("name")
    snapshot_verify.add_argument("--json", action="store_true")

    sub.add_parser("init", help="initialize runtime state and build index")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    paths = BrainPaths.discover()
    paths.initialize()
    command = args.command or "status"
    if command == "status":
        if not hasattr(args, "json"):
            args.json = False
        return command_status(paths, args)
    dispatch = {
        "recall": command_recall,
        "decide": command_decide,
        "correct": command_correct,
        "journal": command_journal,
        "next": command_next,
        "remember": command_remember,
        "forget": command_forget,
        "ingest": command_ingest,
        "context": command_context,
        "profile": command_profiles,
        "skills": command_skills,
        "index": command_index,
        "doctor": command_doctor,
        "validate": command_doctor,
        "stats": command_stats,
        "snapshot": command_snapshot,
    }
    if command == "stack":
        return command_stack_add(paths, args) if args.stack_command == "add" else command_stack_ban(paths, args)
    if command == "pattern":
        return command_pattern_add(paths, args)
    if command == "init":
        payload = build_index(paths)
        print(f"AIBrain initialized: {payload['document_count']} indexed documents")
        return 0
    return dispatch[command](paths, args)


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (FileNotFoundError, KeyError, RuntimeError, ValueError) as error:
        print(f"error: {error}", file=sys.stderr)
        raise SystemExit(1)

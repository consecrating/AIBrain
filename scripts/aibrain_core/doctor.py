"""AIBrain integrity, conflict, freshness, and integration diagnostics."""

from __future__ import annotations

import json
import os
import re
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Any

from .index import index_is_stale
from .io_utils import read_jsonl
from .paths import BrainPaths
from .skills import load_skills

TABLE_ROW = re.compile(r"^\|\s*([^|]+?)\s*\|")
PATTERN_FILE = re.compile(r"`(patterns/[^`]+\.md)`")
MEMORY_ID = re.compile(r"^(mem|evt)-[a-f0-9]{12}$")


def _table_names(path: Path) -> list[str]:
    names: list[str] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        match = TABLE_ROW.match(line)
        if not match:
            continue
        name = match.group(1).strip().lower()
        if name not in {"package", "tool", "if you'd suggest...", "category", "#", "---"} and not set(name) <= {"-", ":"}:
            names.append(name)
    return names


def _kiro_dirs() -> list[Path]:
    candidates: list[Path] = []
    if configured := os.environ.get("KIRO_DIR"):
        candidates.append(Path(configured).expanduser())
    if Path("/projects/.kiro").is_dir():
        candidates.append(Path("/projects/.kiro"))
    candidates.append(Path.home() / ".kiro")
    return list(dict.fromkeys(path.resolve() for path in candidates if path.exists()))


def run_doctor(paths: BrainPaths) -> dict[str, Any]:
    issues: list[dict[str, str]] = []

    def add(severity: str, code: str, message: str) -> None:
        issues.append({"severity": severity, "code": code, "message": message})

    required = [
        paths.brain / "identity.md",
        paths.brain / "decisions/_index.md",
        paths.brain / "patterns/_index.md",
        paths.brain / "stack/registry.md",
        paths.brain / "stack/banned.md",
        paths.brain / "stack/alternatives.md",
        paths.brain / "context/repos.md",
        paths.brain / "context/environments.md",
        paths.memory / "active-task.md",
        paths.memory / "corrections.md",
        paths.memory / "journal.md",
        paths.memory / "scratchpad.md",
        paths.rules / "response-quality.md",
        paths.rules / "dependency-policy.md",
        paths.rules / "code-style.md",
        paths.rules / "anti-patterns.md",
        paths.brain / "schemas/memory.schema.json",
        paths.brain / "schemas/profile.schema.json",
        paths.brain / "schemas/skill.schema.json",
    ]
    for path in required:
        if not path.exists():
            add("error", "missing-file", str(path.relative_to(paths.root)))
        elif not path.stat().st_size:
            add("error", "empty-file", str(path.relative_to(paths.root)))

    for schema_path in paths.brain.glob("schemas/*.json"):
        try:
            schema = json.loads(schema_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as error:
            add("error", "schema-json", f"{schema_path.name}: {error.msg}")
            continue
        if not isinstance(schema, dict) or schema.get("type") != "object" or not schema.get("required"):
            add("error", "schema-definition", schema_path.name)

    active_task = paths.memory / "active-task.md"
    if active_task.exists():
        text = active_task.read_text(encoding="utf-8")
        for heading in ("## Current State", "## Constraints", "## Acceptance Criteria", "## Next Action"):
            if heading not in text:
                add("error", "active-task-schema", f"Missing heading: {heading}")

    memory_records: list[dict[str, Any]] = []
    for jsonl in (paths.store, paths.ingest_log):
        try:
            records = read_jsonl(jsonl)
            if jsonl == paths.store:
                memory_records = records
        except ValueError as error:
            add("error", "invalid-jsonl", str(error))

    seen_ids: set[str] = set()
    remembered_ids: set[str] = set()
    today = date.today().isoformat()
    for number, record in enumerate(memory_records, 1):
        event = record.get("event")
        record_id = str(record.get("id", ""))
        if record_id in seen_ids:
            add("error", "duplicate-memory-id", record_id)
        seen_ids.add(record_id)
        if not MEMORY_ID.fullmatch(record_id):
            add("error", "memory-schema", f"Record {number}: invalid id {record_id!r}")
        if record.get("schema_version") != 2 or event not in {"remember", "forget"} or not record.get("created_at"):
            add("error", "memory-schema", f"Record {number}: missing core fields")
            continue
        if event == "remember":
            remembered_ids.add(record_id)
            confidence = record.get("confidence")
            if not isinstance(confidence, (int, float)) or not 0 <= float(confidence) <= 1:
                add("error", "memory-schema", f"{record_id}: confidence must be 0..1")
            for field in ("kind", "scope", "text", "content_hash"):
                if not record.get(field):
                    add("error", "memory-schema", f"{record_id}: missing {field}")
            expires = record.get("expires")
            if expires:
                try:
                    date.fromisoformat(str(expires))
                    if str(expires) < today:
                        add("warning", "expired-memory", f"{record_id}: expired {expires}")
                except ValueError:
                    add("error", "memory-schema", f"{record_id}: invalid expiry {expires}")
        elif not record.get("target_id") or not record.get("reason"):
            add("error", "memory-schema", f"{record_id}: forget event requires target_id and reason")
    for record in memory_records:
        if record.get("event") == "forget" and record.get("target_id") not in remembered_ids:
            add("warning", "orphan-tombstone", str(record.get("target_id")))

    registry = paths.brain / "stack/registry.md"
    banned = paths.brain / "stack/banned.md"
    if registry.exists() and banned.exists():
        approved = _table_names(registry)
        rejected = set(_table_names(banned))
        for duplicate in sorted({name for name in approved if approved.count(name) > 1}):
            add("warning", "duplicate-package", f"Approved package appears more than once: {duplicate}")
        for conflict in sorted(set(approved) & rejected):
            add("error", "stack-conflict", f"Package is both approved and banned: {conflict}")

    decisions = paths.brain / "decisions/_index.md"
    if decisions.exists():
        text = decisions.read_text(encoding="utf-8")
        numbers = re.findall(r"(?m)^\|\s*(\d+)\s*\|", text)
        for duplicate in sorted({number for number in numbers if numbers.count(number) > 1}):
            add("error", "duplicate-decision", duplicate)
        marker = text.find("## Decision Template")
        if marker >= 0 and re.search(r"(?m)^\|\s*\d+\s*\|", text[marker:]):
            add("error", "table-placement", "Decision rows found after Decision Template")

    corrections = paths.memory / "corrections.md"
    if corrections.exists():
        numbers = re.findall(r"Correction #(\d+)", corrections.read_text(encoding="utf-8"))
        for duplicate in sorted({number for number in numbers if numbers.count(number) > 1}):
            add("error", "duplicate-correction", duplicate)

    patterns_index = paths.brain / "patterns/_index.md"
    if patterns_index.exists():
        for relative in PATTERN_FILE.findall(patterns_index.read_text(encoding="utf-8")):
            if not (paths.brain / relative).exists():
                add("error", "dangling-pattern", relative)

    profile_names: set[str] = set()
    profile_files = sorted(paths.profiles.glob("*.json"))
    for profile_path in profile_files:
        try:
            profile = json.loads(profile_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as error:
            add("error", "profile-json", f"{profile_path.name}: {error.msg}")
            continue
        if not isinstance(profile, dict):
            add("error", "profile-schema", f"object: {profile_path.name}")
            continue
        name = profile.get("name")
        if (
            profile.get("schema_version") != 1
            or not isinstance(name, str)
            or not name.strip()
            or not isinstance(profile.get("description"), str)
            or not profile.get("description", "").strip()
        ):
            add("error", "profile-schema", profile_path.name)
        if isinstance(name, str) and name.strip():
            if name in profile_names:
                add("error", "duplicate-profile", name)
            profile_names.add(name)
        marker_fields = ("path_markers", "file_markers", "priorities", "rules", "required_context", "skill_preferences")
        if not isinstance(profile.get("scope"), str):
            add("error", "profile-schema", f"scope: {profile_path.name}")
        for field in marker_fields:
            value = profile.get(field)
            if not isinstance(value, list) or not all(isinstance(item, str) for item in value):
                add("error", "profile-schema", f"{field}: {profile_path.name}")
    if "default" not in profile_names:
        add("error", "missing-default-profile", "brain/profiles/default.json")

    skill_files = sorted(paths.skills.glob("*.md"))
    loaded_skills = load_skills(paths)
    if len(loaded_skills) != len(skill_files):
        add("error", "skill-frontmatter", "One or more skill files have invalid frontmatter")
    skill_names: set[str] = set()
    for skill in loaded_skills:
        name = str(skill.get("name", ""))
        if not name or not skill.get("description") or not skill.get("triggers") or not skill.get("capabilities"):
            add("error", "skill-schema", str(skill.get("path")))
        if name in skill_names:
            add("error", "duplicate-skill", name)
        skill_names.add(name)
    if not skill_names:
        add("error", "missing-skills", "No routable super skills found")

    for feed in paths.feeds.glob("*.json"):
        try:
            payload = json.loads(feed.read_text(encoding="utf-8"))
        except json.JSONDecodeError as error:
            add("error", "invalid-feed", f"{feed.name}: {error.msg}")
            continue
        age_days = (datetime.now(timezone.utc).timestamp() - feed.stat().st_mtime) / 86400
        if age_days > 45:
            add("warning", "stale-feed", f"{feed.name}: {age_days:.0f} days old")
        packages = payload.get("packages") if isinstance(payload, dict) else None
        if isinstance(packages, dict) and packages:
            statuses = [str(item.get("status", "ok")) for item in packages.values() if isinstance(item, dict)]
            if statuses and all(status == "error" for status in statuses):
                add("error", "unusable-feed", f"{feed.name}: every lookup failed")
            elif any(status in {"error", "stale-cache"} for status in statuses):
                add("warning", "partial-feed", f"{feed.name}: contains failed or cached lookups")

    if paths.index.exists():
        try:
            index_payload = json.loads(paths.index.read_text(encoding="utf-8"))
            if index_payload.get("schema_version") != 2 or not isinstance(index_payload.get("documents"), list):
                add("error", "index-schema", "Generated index has an invalid shape")
        except json.JSONDecodeError as error:
            add("error", "index-json", error.msg)
    if index_is_stale(paths):
        add("warning", "stale-index", "Run: brain.sh index build")

    for kiro_dir in _kiro_dirs():
        pointer = kiro_dir / ".aibrain-path"
        if pointer.exists() and pointer.read_text(encoding="utf-8").strip() == str(paths.root):
            for installed in (kiro_dir / "skills/aibrain/SKILL.md", kiro_dir / "steering/aibrain.md"):
                if not installed.exists():
                    add("warning", "integration-missing", str(installed))

    errors = sum(issue["severity"] == "error" for issue in issues)
    warnings = sum(issue["severity"] == "warning" for issue in issues)
    return {
        "ok": errors == 0,
        "schema_version": 2,
        "errors": errors,
        "warnings": warnings,
        "issues": issues,
    }

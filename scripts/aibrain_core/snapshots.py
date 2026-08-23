"""Atomic AIBrain state snapshots and integrity verification."""

from __future__ import annotations

import hashlib
import json
import re
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .io_utils import atomic_write, safe_slug, write_lock
from .paths import BrainPaths

PATTERN_FILE = re.compile(r"`(patterns/[^`]+\.md)`")


def _digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _snapshot_sources(paths: BrainPaths) -> list[Path]:
    sources = [*paths.brain.rglob("*.md"), *paths.brain.rglob("*.json")]
    sources.extend(paths.memory.glob("*.md"))
    sources.extend(paths.memory.glob("*.jsonl"))
    sources.extend(paths.rules.rglob("*.md"))
    sources.extend(paths.feeds.glob("*.json"))
    return sorted({source for source in sources if source.is_file()})


def create_snapshot(paths: BrainPaths, name: str | None = None) -> dict[str, Any]:
    timestamp = datetime.now(timezone.utc)
    snapshot_name = safe_slug(name or timestamp.strftime("%Y%m%d-%H%M%S"), "snapshot")
    target = paths.snapshots / snapshot_name
    with write_lock(paths.runtime):
        if target.exists():
            raise ValueError(f"Snapshot already exists: {snapshot_name}")
        target.mkdir(parents=True)
        files: list[dict[str, str]] = []
        try:
            for source in _snapshot_sources(paths):
                relative = source.relative_to(paths.root)
                destination = target / relative
                destination.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(source, destination)
                files.append({"path": str(relative), "sha256": _digest(destination)})
            manifest = {
                "schema_version": 2,
                "name": snapshot_name,
                "created_at": timestamp.isoformat(),
                "files": files,
            }
            atomic_write(target / "manifest.json", json.dumps(manifest, indent=2) + "\n")
        except BaseException:
            shutil.rmtree(target, ignore_errors=True)
            raise
    return manifest


def list_snapshots(paths: BrainPaths) -> list[dict[str, Any]]:
    snapshots: list[dict[str, Any]] = []
    for manifest_path in sorted(paths.snapshots.glob("*/manifest.json"), reverse=True):
        try:
            value = json.loads(manifest_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        if isinstance(value, dict):
            snapshots.append(value)
    return snapshots


def verify_snapshot(paths: BrainPaths, name: str) -> dict[str, Any]:
    target = paths.snapshots / safe_slug(name)
    manifest_path = target / "manifest.json"
    if not manifest_path.exists():
        raise KeyError(f"Unknown snapshot: {name}")
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    mismatches: list[str] = []
    for item in manifest.get("files", []):
        snapshot_file = target / item["path"]
        if not snapshot_file.exists() or _digest(snapshot_file) != item["sha256"]:
            mismatches.append(item["path"])

    dangling: list[str] = []
    pattern_index = target / "brain/patterns/_index.md"
    if pattern_index.exists():
        for relative in PATTERN_FILE.findall(pattern_index.read_text(encoding="utf-8")):
            if not (target / "brain" / relative).exists():
                dangling.append(relative)
    return {
        "ok": not mismatches and not dangling,
        "name": name,
        "mismatches": mismatches,
        "dangling_references": dangling,
    }

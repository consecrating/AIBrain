"""Safe writes, JSONL events, and Markdown mutation helpers."""

from __future__ import annotations

import contextlib
import fcntl
import hashlib
import json
import os
import re
import tempfile
from collections.abc import Iterator
from pathlib import Path
from typing import Any


@contextlib.contextmanager
def write_lock(runtime: Path) -> Iterator[None]:
    runtime.mkdir(parents=True, exist_ok=True)
    lock_path = runtime / "write.lock"
    with lock_path.open("a", encoding="utf-8") as handle:
        fcntl.flock(handle.fileno(), fcntl.LOCK_EX)
        try:
            yield
        finally:
            fcntl.flock(handle.fileno(), fcntl.LOCK_UN)


def atomic_write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8") as handle:
            handle.write(text)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
    except BaseException:
        with contextlib.suppress(OSError):
            os.unlink(temporary)
        raise


def append_line(path: Path, line: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(line.rstrip("\n") + "\n")
        handle.flush()
        os.fsync(handle.fileno())


def append_jsonl(path: Path, record: dict[str, Any]) -> None:
    append_line(path, json.dumps(record, ensure_ascii=False, sort_keys=True))


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    records: list[dict[str, Any]] = []
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        try:
            value = json.loads(line)
        except json.JSONDecodeError as error:
            raise ValueError(f"Invalid JSONL at {path}:{line_number}: {error.msg}") from error
        if not isinstance(value, dict):
            raise ValueError(f"Expected object at {path}:{line_number}")
        records.append(value)
    return records


def markdown_cell(value: str) -> str:
    return " ".join(value.replace("|", "\\|").splitlines()).strip()


def safe_slug(value: str, default: str = "item") -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return slug[:64] or default


def content_id(prefix: str, *parts: str, length: int = 12) -> str:
    digest = hashlib.sha256("\x1f".join(parts).encode("utf-8")).hexdigest()[:length]
    return f"{prefix}-{digest}"


def insert_before(path: Path, marker: str, addition: str) -> None:
    text = path.read_text(encoding="utf-8")
    if marker not in text:
        raise ValueError(f"Insertion marker not found in {path}: {marker!r}")
    atomic_write(path, text.replace(marker, addition.rstrip() + "\n\n" + marker, 1))


def replace_markdown_section(path: Path, heading: str, body: str) -> None:
    text = path.read_text(encoding="utf-8")
    pattern = re.compile(
        rf"(?ms)^{re.escape(heading)}\s*\n.*?(?=^##\s|\Z)",
    )
    replacement = f"{heading}\n\n{body.strip()}\n\n"
    if not pattern.search(text):
        raise ValueError(f"Section {heading!r} not found in {path}")
    atomic_write(path, pattern.sub(replacement, text, count=1).rstrip() + "\n")

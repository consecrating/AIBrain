"""Declarative AIBrain super-skill discovery and routing."""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any

from .paths import BrainPaths


def _frontmatter(path: Path) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        return {}
    _, raw, _ = text.split("---", 2)
    data: dict[str, Any] = {}
    for line in raw.splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        key = key.strip()
        value = value.strip().strip('"')
        if key in {"triggers", "capabilities"}:
            data[key] = [item.strip() for item in value.split(",") if item.strip()]
        else:
            data[key] = value
    data["body"] = text.split("---", 2)[2].strip()
    data["path"] = str(path)
    return data


def load_skills(paths: BrainPaths) -> list[dict[str, Any]]:
    return [skill for path in sorted(paths.skills.glob("*.md")) if (skill := _frontmatter(path))]


def route_skills(paths: BrainPaths, task: str, limit: int = 5) -> list[dict[str, Any]]:
    terms = set(re.findall(r"[a-z0-9][a-z0-9_-]+", task.lower()))
    ranked: list[dict[str, Any]] = []
    for skill in load_skills(paths):
        triggers = {str(item).lower() for item in skill.get("triggers", [])}
        capabilities = {str(item).lower() for item in skill.get("capabilities", [])}
        name_terms = set(str(skill.get("name", "")).lower().split("-"))
        score = 4 * len(terms & triggers) + 2 * len(terms & capabilities) + len(terms & name_terms)
        phrase = str(skill.get("description", "")).lower()
        score += sum(1 for term in terms if term in phrase)
        if score:
            ranked.append({**skill, "score": score})
    return sorted(ranked, key=lambda item: (-int(item["score"]), str(item.get("name"))))[:limit]

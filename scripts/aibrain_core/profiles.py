"""Project profile loading and path-based selection."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .paths import BrainPaths


def load_profiles(paths: BrainPaths) -> list[dict[str, Any]]:
    profiles: list[dict[str, Any]] = []
    for profile_path in sorted(paths.profiles.glob("*.json")):
        try:
            profile = json.loads(profile_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        if isinstance(profile, dict):
            profile["_path"] = str(profile_path.relative_to(paths.root))
            profiles.append(profile)
    return profiles


def get_profile(paths: BrainPaths, name: str) -> dict[str, Any]:
    for profile in load_profiles(paths):
        if profile.get("name") == name:
            return profile
    raise KeyError(f"Unknown profile: {name}")


def auto_profile(paths: BrainPaths, target: Path) -> tuple[dict[str, Any], int]:
    target_text = str(target.resolve()).lower()
    profiles = load_profiles(paths)
    default = next((profile for profile in profiles if profile.get("name") == "default"), None)
    best: tuple[dict[str, Any], int] | None = None
    for profile in profiles:
        if profile.get("name") == "default":
            continue
        score = 0
        path_markers = profile.get("path_markers", [])
        file_markers = profile.get("file_markers", [])
        if not isinstance(path_markers, list) or not isinstance(file_markers, list):
            continue
        for marker in path_markers:
            if str(marker).lower() in target_text:
                score += 10
        for marker in file_markers:
            if (target / str(marker)).exists():
                score += 5
        if best is None or score > best[1]:
            best = (profile, score)
    if best and best[1] > 0:
        return best
    if default is not None:
        return default, 0
    raise KeyError("Default profile is missing")

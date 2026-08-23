"""Portable AIBrain path discovery and runtime initialization."""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class BrainPaths:
    root: Path
    brain: Path
    memory: Path
    rules: Path
    feeds: Path
    runtime: Path
    index: Path
    store: Path
    ingest_log: Path
    profiles: Path
    skills: Path
    references: Path
    snapshots: Path

    @classmethod
    def discover(cls) -> "BrainPaths":
        candidates: list[Path] = []
        if configured := os.environ.get("AIBRAIN_ROOT"):
            candidates.append(Path(configured).expanduser())

        kiro_candidates: list[Path] = []
        if configured_kiro := os.environ.get("KIRO_DIR"):
            kiro_candidates.append(Path(configured_kiro).expanduser())
        if Path("/projects/.kiro").is_dir():
            kiro_candidates.append(Path("/projects/.kiro"))
        kiro_candidates.append(Path.home() / ".kiro")
        for kiro_dir in kiro_candidates:
            pointer = kiro_dir / ".aibrain-path"
            if pointer.is_file():
                try:
                    candidates.append(Path(pointer.read_text(encoding="utf-8").strip()))
                except OSError:
                    pass

        candidates.append(Path(__file__).resolve().parents[2])
        for root in candidates:
            resolved = root.resolve()
            if (resolved / "brain").is_dir() and (resolved / "memory").is_dir():
                return cls.from_root(resolved)
        raise RuntimeError("AIBrain root not found; set AIBRAIN_ROOT or install AIBrain")

    @classmethod
    def from_root(cls, root: Path) -> "BrainPaths":
        return cls(
            root=root,
            brain=root / "brain",
            memory=root / "memory",
            rules=root / "rules",
            feeds=root / "feeds",
            runtime=root / ".aibrain",
            index=root / ".aibrain" / "index.json",
            store=root / "memory" / "store.jsonl",
            ingest_log=root / "memory" / "ingested.jsonl",
            profiles=root / "brain" / "profiles",
            skills=root / "brain" / "skills",
            references=root / "brain" / "references",
            snapshots=root / ".aibrain" / "snapshots",
        )

    def initialize(self) -> None:
        for directory in (
            self.runtime,
            self.profiles,
            self.skills,
            self.references,
            self.snapshots,
            self.feeds,
        ):
            directory.mkdir(parents=True, exist_ok=True)
        for file_path in (self.store, self.ingest_log):
            if not file_path.exists():
                file_path.touch()
        scratchpad = self.memory / "scratchpad.md"
        if not scratchpad.exists():
            scratchpad.write_text(
                "# Scratchpad — Working Memory\n\n> Temporary session notes.\n",
                encoding="utf-8",
            )

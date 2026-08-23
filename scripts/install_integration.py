#!/usr/bin/env python3
"""Transactionally publish AIBrain's Kiro integration artifacts."""

from __future__ import annotations

import argparse
import os
import tempfile
from pathlib import Path


def stage_bytes(destination: Path, payload: bytes) -> Path:
    destination.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary = tempfile.mkstemp(prefix=f".{destination.name}.", dir=destination.parent)
    with os.fdopen(descriptor, "wb") as handle:
        handle.write(payload)
        handle.flush()
        os.fsync(handle.fileno())
    return Path(temporary)


def restore(destination: Path, payload: bytes | None) -> None:
    if payload is None:
        destination.unlink(missing_ok=True)
        return
    temporary = stage_bytes(destination, payload)
    os.replace(temporary, destination)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", required=True, type=Path)
    parser.add_argument("--target", required=True, type=Path)
    args = parser.parse_args()

    root = args.root.resolve()
    target = args.target.resolve()
    artifacts = [
        (root / ".kiro/steering/aibrain.md", target / "steering/aibrain.md"),
        (root / ".kiro/skills/aibrain/SKILL.md", target / "skills/aibrain/SKILL.md"),
    ]
    payloads: list[tuple[Path, bytes]] = []
    for source, destination in artifacts:
        payload = source.read_bytes()
        if not payload.strip():
            raise ValueError(f"Refusing to install empty artifact: {source}")
        payloads.append((destination, payload))
    payloads.append((target / ".aibrain-path", f"{root}\n".encode()))

    previous = {destination: destination.read_bytes() if destination.exists() else None for destination, _ in payloads}
    staged = {destination: stage_bytes(destination, payload) for destination, payload in payloads}
    published: list[Path] = []
    try:
        for destination, _ in payloads:
            os.replace(staged[destination], destination)
            published.append(destination)
    except BaseException:
        for destination in reversed(published):
            restore(destination, previous[destination])
        for temporary in staged.values():
            temporary.unlink(missing_ok=True)
        raise

    for destination, payload in payloads:
        if destination.read_bytes() != payload:
            for rollback_destination, previous_payload in previous.items():
                restore(rollback_destination, previous_payload)
            raise RuntimeError(f"Installed artifact verification failed: {destination}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

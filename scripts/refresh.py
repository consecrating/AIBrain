#!/usr/bin/env python3
"""Refresh approved dependency evidence from PyPI and npm using stdlib only."""

from __future__ import annotations

import argparse
import json
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from aibrain_core.io_utils import atomic_write
from aibrain_core.paths import BrainPaths

PACKAGE_RE = re.compile(r"^[@a-zA-Z0-9][@a-zA-Z0-9._/-]*$")


def table_packages(path: Path, heading: str) -> list[str]:
    packages: list[str] = []
    active = False
    for line in path.read_text(encoding="utf-8").splitlines():
        if line == heading:
            active = True
            continue
        if active and line.startswith("## "):
            break
        if not active or not line.startswith("|"):
            continue
        cells = [cell.strip() for cell in line.strip("|").split("|")]
        if not cells or cells[0].lower() in {"package", "tool"} or set(cells[0]) <= {"-", ":"}:
            continue
        if PACKAGE_RE.fullmatch(cells[0]):
            packages.append(cells[0])
    return packages


def fetch_json(url: str, timeout: float) -> dict[str, Any]:
    request = urllib.request.Request(url, headers={"User-Agent": "AIBrain/2.0 dependency-intelligence"})
    with urllib.request.urlopen(request, timeout=timeout) as response:
        value = json.load(response)
    if not isinstance(value, dict):
        raise ValueError("Registry returned a non-object payload")
    return value


def pypi_record(package: str, timeout: float) -> dict[str, Any]:
    payload = fetch_json(f"https://pypi.org/pypi/{urllib.parse.quote(package)}/json", timeout)
    info = payload.get("info", {})
    urls = payload.get("urls", [])
    released = urls[0].get("upload_time_iso_8601") if urls else None
    yanked_reasons = sorted(
        {str(item.get("yanked_reason") or "yanked") for item in urls if item.get("yanked")}
    )
    return {
        "version": info.get("version"),
        "released": released,
        "deprecated": "; ".join(yanked_reasons) or None,
        "project_url": info.get("project_url") or info.get("package_url"),
    }


def npm_record(package: str, timeout: float) -> dict[str, Any]:
    encoded = urllib.parse.quote(package, safe="")
    payload = fetch_json(f"https://registry.npmjs.org/{encoded}/latest", timeout)
    repository = payload.get("repository")
    return {
        "version": payload.get("version"),
        "deprecated": payload.get("deprecated"),
        "project_url": repository.get("url") if isinstance(repository, dict) else None,
    }


def load_previous(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}
    return value if isinstance(value, dict) else {}


def refresh_group(
    packages: list[str],
    registry: str,
    timeout: float,
    previous: dict[str, Any],
) -> tuple[dict[str, Any], int, int]:
    records: dict[str, Any] = {}
    failures = 0
    prior_records = previous.get("packages", {}) if isinstance(previous.get("packages"), dict) else {}
    for package in packages:
        try:
            record = pypi_record(package, timeout) if registry == "pypi" else npm_record(package, timeout)
            record["status"] = "ok"
            print(f"  ✓ {package}: {record.get('version')}")
        except (OSError, ValueError, urllib.error.URLError) as error:
            failures += 1
            prior = prior_records.get(package)
            if isinstance(prior, dict) and prior.get("status") in {"ok", "stale-cache"}:
                record = {**prior, "status": "stale-cache", "refresh_error": str(error)}
                print(f"  ⚠ {package}: using cached {record.get('version')} ({error})")
            else:
                record = {"status": "error", "error": str(error)}
                print(f"  ✗ {package}: {error}")
        records[package] = record
    usable = sum(item.get("status") in {"ok", "stale-cache"} for item in records.values())
    return (
        {
            "schema_version": 2,
            "registry": registry,
            "refreshed_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
            "packages": records,
        },
        failures,
        usable,
    )


def unique(values: list[str]) -> list[str]:
    return list(dict.fromkeys(values))


def main() -> int:
    parser = argparse.ArgumentParser(description="Refresh AIBrain dependency evidence")
    parser.add_argument("mode", nargs="?", default="all", choices=("all", "python", "node"))
    parser.add_argument("--timeout", type=float, default=12.0)
    parser.add_argument("--strict", action="store_true", help="fail if any registry lookup fails")
    args = parser.parse_args()

    paths = BrainPaths.discover()
    paths.initialize()
    registry_path = paths.brain / "stack/registry.md"
    failures = 0
    unusable_groups = 0
    deprecated: list[dict[str, str]] = []
    refreshed_registries: set[str] = set()
    previous_deprecated = load_previous(paths.feeds / "deprecated.json")

    groups = []
    if args.mode in {"all", "python"}:
        groups.append(
            (
                "pypi",
                unique(
                    table_packages(registry_path, "## Python")
                    + table_packages(registry_path, "## Custom Approved (Python)")
                ),
                paths.feeds / "python-versions.json",
            )
        )
    if args.mode in {"all", "node"}:
        groups.append(
            (
                "npm",
                unique(
                    table_packages(registry_path, "## JavaScript / TypeScript")
                    + table_packages(registry_path, "## Custom Approved (Node)")
                ),
                paths.feeds / "node-versions.json",
            )
        )

    for registry, packages, output in groups:
        print(f"{registry}: checking {len(packages)} approved packages")
        payload, group_failures, usable = refresh_group(packages, registry, args.timeout, load_previous(output))
        failures += group_failures
        if packages and usable == 0:
            unusable_groups += 1
            print(f"  ✗ refusing to replace {output.name}: no usable evidence")
            continue
        atomic_write(output, json.dumps(payload, indent=2) + "\n")
        refreshed_registries.add(registry)
        deprecated.extend(
            {"package": name, "registry": registry, "reason": str(item["deprecated"])}
            for name, item in payload["packages"].items()
            if item.get("deprecated")
        )

    prior_signals = previous_deprecated.get("packages", []) if isinstance(previous_deprecated, dict) else []
    if isinstance(prior_signals, list):
        deprecated.extend(
            item
            for item in prior_signals
            if isinstance(item, dict) and item.get("registry") not in refreshed_registries
        )
    unique_deprecated = {
        (str(item.get("registry")), str(item.get("package"))): item
        for item in deprecated
        if item.get("registry") and item.get("package")
    }
    deprecated = list(unique_deprecated.values())

    atomic_write(
        paths.feeds / "deprecated.json",
        json.dumps(
            {
                "schema_version": 2,
                "refreshed_at": datetime.now(timezone.utc).isoformat(),
                "packages": deprecated,
            },
            indent=2,
        )
        + "\n",
    )
    print(
        f"Refresh complete: {failures} lookup failure(s), "
        f"{unusable_groups} unusable group(s), {len(deprecated)} deprecation signal(s)"
    )
    return 1 if unusable_groups or (args.strict and failures) else 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (FileNotFoundError, RuntimeError, ValueError) as error:
        print(f"error: {error}", file=sys.stderr)
        raise SystemExit(1)

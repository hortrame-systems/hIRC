#!/usr/bin/env python3
"""Reproduce the M04-S001 local integrity-core acceptance checks."""

from __future__ import annotations

import ast
import hashlib
import io
import json
import sys
import tempfile
import unittest
from pathlib import Path

from validation_config import FULL_SUITE_TESTS, STORE_TESTS


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
OUTPUT = ROOT / "implementation/m04-s001-validation.json"
sys.path.insert(0, str(SRC))

from hirc.store import DISABLED_CAPABILITIES, EventInput, Store  # noqa: E402


FILES = (
    "pyproject.toml",
    "src/hirc/__init__.py",
    "src/hirc/__main__.py",
    "src/hirc/canonical.py",
    "src/hirc/cli.py",
    "src/hirc/store.py",
    "tests/test_store.py",
    "implementation/README.md",
)
FORBIDDEN_NETWORK_IMPORTS = {"socket", "http", "urllib", "requests", "aiohttp", "subprocess"}


def identity(relative: str) -> dict[str, object]:
    body = (ROOT / relative).read_bytes()
    return {"path": relative, "sha256": hashlib.sha256(body).hexdigest(), "bytes": len(body)}


def imported_roots(path: Path) -> set[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    names: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            names.update(alias.name.split(".", 1)[0] for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            names.add(node.module.split(".", 1)[0])
    return names


def main() -> int:
    stream = io.StringIO()
    suite = unittest.defaultTestLoader.discover(str(ROOT / "tests"), pattern="test_store.py")
    test_result = unittest.TextTestRunner(stream=stream, verbosity=2).run(suite)

    forbidden: dict[str, list[str]] = {}
    for source in sorted((SRC / "hirc").glob("*.py")):
        found = sorted(imported_roots(source) & FORBIDDEN_NETWORK_IMPORTS)
        if found:
            forbidden[source.relative_to(ROOT).as_posix()] = found

    temp_root = ROOT / "tests/.tmp"
    temp_root.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(dir=temp_root) as directory:
        store = Store(Path(directory) / "validation.sqlite3")
        store.initialize()
        appended = store.append(
            EventInput(
                stream_id="work:validation",
                actor_id="actor:validator",
                event_type="work.created",
                category="EVIDENCE",
                foundation_version="foundation:1",
                goal_version="goal:2",
                privacy_class="privacy:owner",
                audience="audience:owner",
                purpose="purpose:validation",
                occurred_at="2026-10-10T00:00:00Z",
                payload={"title": "M04-S001 validation"},
            )
        )
        verification = store.verify()

    checks = {
        "unit_tests": test_result.wasSuccessful(),
        "unit_test_count": test_result.testsRun == STORE_TESTS,
        "network_imports_absent": not forbidden,
        "store_valid": verification["valid"],
        "single_event_observed": verification["event_count"] == 1,
        "head_matches_append": verification["head_hash"] == appended.event_hash,
        "high_risk_capabilities_disabled": verification["disabled_capabilities"] == DISABLED_CAPABILITIES,
    }
    result = {
        "schema": "hirc.m04-s001-validation/1",
        "stone": "M04-S001",
        "status": "PASS" if all(checks.values()) else "FAIL",
        "checks": checks,
        "files": [identity(path) for path in FILES],
        "unit_test_output": stream.getvalue().splitlines(),
        "forbidden_imports": forbidden,
        "smoke": {
            "event_id": appended.event_id,
            "event_hash": appended.event_hash,
            "event_count": verification["event_count"],
        },
        "nonclaim": "Local dependency-free integrity-core evidence only; it does not validate the separate UI, agent execution, network security, production hardening, external-effect or Bridge scopes.",
    }
    OUTPUT.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps(result, indent=2))
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())

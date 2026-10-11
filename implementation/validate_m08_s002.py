#!/usr/bin/env python3
"""Reproduce M08-S002 migration and bounded deterministic hardening checks."""

from __future__ import annotations

import hashlib
import io
import json
import sys
import tempfile
import time
import unittest
from dataclasses import replace
from pathlib import Path

from validation_config import FULL_SUITE_TESTS, MIGRATION_TESTS


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "tests"))

from hirc.migration import migrate_v1_to_v2  # noqa: E402
from hirc.store import EventInput, Store  # noqa: E402
from test_migration_hardening import legacy  # noqa: E402


OUTPUT = ROOT / "implementation/m08-s002-validation.json"
FAILED = ROOT / "implementation/m08-s002-migration-validation-v1-failed.json"
FILES = (
    "implementation/M08_RELEASE_HARDENING_PLAN.md",
    "implementation/README.md",
    "src/hirc/migration.py",
    "src/hirc/store.py",
    "src/hirc/cli.py",
    "tests/test_migration_hardening.py",
    "implementation/m08-s002-migration-validation-v1-failed.json",
)


def identity(relative: str) -> dict[str, object]:
    body = (ROOT / relative).read_bytes()
    return {"path": relative, "sha256": hashlib.sha256(body).hexdigest(), "bytes": len(body)}


def main() -> int:
    hardening_stream = io.StringIO()
    hardening_suite = unittest.defaultTestLoader.discover(str(ROOT / "tests"), pattern="test_migration_hardening.py")
    hardening_tests = unittest.TextTestRunner(stream=hardening_stream, verbosity=2).run(hardening_suite)
    full_stream = io.StringIO()
    full_suite = unittest.defaultTestLoader.discover(str(ROOT / "tests"))
    full_tests = unittest.TextTestRunner(stream=full_stream, verbosity=1).run(full_suite)

    temp_root = ROOT / "tests/.tmp"
    temp_root.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(dir=temp_root) as directory:
        root = Path(directory)
        v1, predecessor = root / "v1.sqlite3", root / "v1.backup.sqlite3"
        legacy(v1)
        migration = migrate_v1_to_v2(v1, predecessor)
        store = Store(root / "load.sqlite3")
        store.initialize()
        base = EventInput(stream_id="load:0", actor_id="actor:load", event_type="note.recorded", category="EVIDENCE", foundation_version="foundation:1", goal_version="goal:2", privacy_class="privacy:owner", audience="audience:owner", purpose="purpose:load", occurred_at="2026-10-10T00:00:00Z", payload={"index": 0})
        started = time.perf_counter()
        for index in range(100):
            store.append(replace(base, stream_id=f"load:{index}", payload={"index": index}))
        elapsed = time.perf_counter() - started
        load_state = store.verify(read_only=True)
        predecessor_exists = predecessor.is_file()
        predecessor_bytes = predecessor.stat().st_size if predecessor_exists else None
    failed = json.loads(FAILED.read_text(encoding="utf-8"))
    checks = {
        "hardening_tests_pass": hardening_tests.wasSuccessful(),
        "hardening_test_count": hardening_tests.testsRun == MIGRATION_TESTS,
        "full_suite_pass": full_tests.wasSuccessful(),
        "full_suite_test_count": full_tests.testsRun == FULL_SUITE_TESTS,
        "deadlock_baseline_preserved": failed.get("status") == "PRESERVED_FAILED_BASELINE" and "hung" in failed.get("observed", ""),
        "migration_verified": migration["verified"] is True and migration["event_count"] == 1,
        "predecessor_preserved": predecessor_exists and migration["backup_bytes"] == predecessor_bytes,
        "bounded_load_valid": load_state["valid"] and load_state["event_count"] == 100,
    }
    result = {
        "schema": "hirc.m08-s002-validation/1",
        "stone": "M08-S002",
        "status": "PASS" if all(checks.values()) else "FAIL",
        "checks": checks,
        "files": [identity(path) for path in FILES],
        "hardening_test_output": hardening_stream.getvalue().splitlines(),
        "full_suite_output": full_stream.getvalue().splitlines(),
        "migration_control": migration,
        "load_control": {"events": 100, "elapsed_seconds": elapsed, "head_hash": load_state["head_hash"]},
        "surviving_limits": [
            "Only exact v1-to-v2 migration is supported; no future or unknown schema is inferred.",
            "Seeded malformed identifiers and a 100-event local load are finite tests, not broad fuzzing or a throughput guarantee.",
            "Power-loss injection, long soak, cross-machine restore, encrypted storage and independent security review remain open."
        ],
        "nonclaim": "M08-S002 exact predecessor migration and bounded local hardening evidence only."
    }
    OUTPUT.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps(result, indent=2))
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())

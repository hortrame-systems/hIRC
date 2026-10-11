#!/usr/bin/env python3
"""Reproduce M08-S001 verified atomic backup and restore checks."""

from __future__ import annotations

import ast
import hashlib
import io
import json
import sys
import tempfile
import unittest
from pathlib import Path

from validation_config import FULL_SUITE_TESTS, RECOVERY_TESTS


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from hirc.recovery import backup_store, restore_store  # noqa: E402
from hirc.store import EventInput, Store  # noqa: E402


OUTPUT = ROOT / "implementation/m08-s001-validation.json"
FAILED = ROOT / "implementation/m08-s001-recovery-validation-v1-failed.json"
FILES = (
    "implementation/M08_RELEASE_HARDENING_PLAN.md",
    "implementation/README.md",
    "src/hirc/recovery.py",
    "src/hirc/store.py",
    "src/hirc/cli.py",
    "tests/test_recovery.py",
    "implementation/m08-s001-recovery-validation-v1-failed.json",
)
FORBIDDEN_IMPORTS = {"socket", "http", "urllib", "requests", "aiohttp", "subprocess"}


def identity(relative: str) -> dict[str, object]:
    body = (ROOT / relative).read_bytes()
    return {"path": relative, "sha256": hashlib.sha256(body).hexdigest(), "bytes": len(body)}


def imported_roots(path: Path) -> set[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    values: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            values.update(alias.name.split(".", 1)[0] for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            values.add(node.module.split(".", 1)[0])
    return values


def main() -> int:
    recovery_stream = io.StringIO()
    recovery_suite = unittest.defaultTestLoader.discover(str(ROOT / "tests"), pattern="test_recovery.py")
    recovery_tests = unittest.TextTestRunner(stream=recovery_stream, verbosity=2).run(recovery_suite)
    full_stream = io.StringIO()
    full_suite = unittest.defaultTestLoader.discover(str(ROOT / "tests"))
    full_tests = unittest.TextTestRunner(stream=full_stream, verbosity=1).run(full_suite)

    temp_root = ROOT / "tests/.tmp"
    temp_root.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(dir=temp_root) as directory:
        store = Store(Path(directory) / "m08-s001.sqlite3")
        store.initialize()
        store.append(EventInput(stream_id="work:backup", actor_id="actor:validator", event_type="work.created", category="EVIDENCE", foundation_version="foundation:1", goal_version="goal:2", privacy_class="privacy:owner", audience="audience:owner", purpose="purpose:m08-backup", occurred_at="2026-10-10T00:00:00Z", payload={"work_id": "work:backup", "title": "Backup", "owner": "actor:validator", "next_action": "Restore"}))
        backup_path = Path(directory) / "backup.sqlite3"
        restored_path = Path(directory) / "restored.sqlite3"
        backup = backup_store(store.path, backup_path)
        restored = restore_store(backup_path, restored_path)
        restored_state = Store(restored_path).verify(read_only=True)

    failed = json.loads(FAILED.read_text(encoding="utf-8"))
    imports = imported_roots(ROOT / "src/hirc/recovery.py") & FORBIDDEN_IMPORTS
    checks = {
        "recovery_tests_pass": recovery_tests.wasSuccessful(),
        "recovery_test_count": recovery_tests.testsRun == RECOVERY_TESTS,
        "full_suite_pass": full_tests.wasSuccessful(),
        "full_suite_test_count": full_tests.testsRun == FULL_SUITE_TESTS,
        "failed_baseline_preserved": failed.get("status") == "PRESERVED_FAILED_BASELINE" and bool(failed.get("second_observed_failure")),
        "network_process_imports_absent": not imports,
        "backup_restore_heads_match": backup["head_hash"] == restored["head_hash"] == restored_state["head_hash"],
        "restored_store_valid": restored_state["valid"],
        "unencrypted_hold_explicit": backup["encrypted"] is False and backup["sensitive_data_release_allowed"] is False,
    }
    result = {
        "schema": "hirc.m08-s001-validation/1",
        "stone": "M08-S001",
        "status": "PASS" if all(checks.values()) else "FAIL",
        "checks": checks,
        "files": [identity(path) for path in FILES],
        "recovery_test_output": recovery_stream.getvalue().splitlines(),
        "full_suite_output": full_stream.getvalue().splitlines(),
        "backup_control": backup,
        "restore_control": restored,
        "forbidden_imports": sorted(imports),
        "surviving_limits": [
            "Backups preserve plaintext SQLite data; sensitive-data release remains blocked pending supported encryption and key custody.",
            "Finite Windows-local checks do not establish durability across every filesystem, power-loss point or storage-controller behavior.",
            "Schema migration, fuzz/load/soak, clean package install, cross-machine recovery and empirical UI/security review remain open."
        ],
        "nonclaim": "M08-S001 verified local backup/restore evidence only; not production disaster-recovery assurance."
    }
    OUTPUT.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps(result, indent=2))
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())

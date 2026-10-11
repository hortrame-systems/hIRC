#!/usr/bin/env python3
"""Reproduce the M08-S009 atomic create-if-absent publication repair."""

from __future__ import annotations

import hashlib
import io
import json
import sys
import unittest
from pathlib import Path

from validation_config import (
    EXPECTED_RELEASE_FAILURES,
    FULL_SUITE_TESTS,
    MIGRATION_TESTS,
    RECOVERY_TESTS,
    WITNESS_TESTS,
)


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
OUTPUT = ROOT / "implementation/m08-s009-validation.json"
FILES = (
    "implementation/M08_RELEASE_HARDENING_PLAN.md",
    "implementation/m08-s009-validation-v1-failed.json",
    "implementation/validate_m08_s009.py",
    "implementation/validation_config.py",
    "src/hirc/atomic.py",
    "src/hirc/migration.py",
    "src/hirc/recovery.py",
    "src/hirc/witness.py",
    "tests/test_migration_hardening.py",
    "tests/test_recovery.py",
    "tests/test_witness.py",
)


def identity(path: str) -> dict:
    body = (ROOT / path).read_bytes()
    return {"path": path, "sha256": hashlib.sha256(body).hexdigest(), "bytes": len(body)}


def run(pattern: str) -> tuple[unittest.TestResult, list[str]]:
    stream = io.StringIO()
    suite = unittest.defaultTestLoader.discover(str(ROOT / "tests"), pattern=pattern)
    result = unittest.TextTestRunner(stream=stream, verbosity=2).run(suite)
    return result, stream.getvalue().splitlines()


def main() -> int:
    recovery, recovery_output = run("test_recovery.py")
    migration, migration_output = run("test_migration_hardening.py")
    witness, witness_output = run("test_witness.py")
    full_stream = io.StringIO()
    full_suite = unittest.defaultTestLoader.discover(str(ROOT / "tests"))
    full = unittest.TextTestRunner(stream=full_stream, verbosity=1).run(full_suite)
    baseline = json.loads((ROOT / "implementation/m08-s009-validation-v1-failed.json").read_text(encoding="utf-8"))
    checks = {
        "failed_baseline_preserved": baseline.get("status") == "FAIL" and baseline.get("finding", {}).get("id") == "M08-S009-F001",
        "recovery_tests_pass": recovery.wasSuccessful(),
        "recovery_test_count": recovery.testsRun == RECOVERY_TESTS,
        "migration_tests_pass": migration.wasSuccessful(),
        "migration_test_count": migration.testsRun == MIGRATION_TESTS,
        "witness_tests_pass": witness.wasSuccessful(),
        "witness_test_count": witness.testsRun == WITNESS_TESTS,
        "backup_race_regression_present": any("test_concurrent_target_creation_is_never_overwritten" in line for line in recovery_output),
        "migration_race_regression_present": any("test_concurrent_backup_target_creation_is_never_overwritten" in line for line in migration_output),
        "witness_race_regression_present": any("test_concurrent_witness_creation_is_never_overwritten" in line for line in witness_output),
        "full_suite_pass": full.wasSuccessful(),
        "full_suite_test_count": full.testsRun == FULL_SUITE_TESTS,
        "expected_release_failures_preserved": len(full.expectedFailures) == EXPECTED_RELEASE_FAILURES,
    }
    result = {
        "schema": "hirc.m08-s009-validation/1",
        "stone": "M08-S009",
        "status": "PASS_ATOMIC_CREATE_IF_ABSENT_SCOPE" if all(checks.values()) else "FAIL",
        "checks": checks,
        "files": [identity(path) for path in FILES],
        "recovery_test_output": recovery_output,
        "migration_test_output": migration_output,
        "witness_test_output": witness_output,
        "full_suite_output": full_stream.getvalue().splitlines(),
        "repair": {
            "finding_id": "M08-S009-F001",
            "same_directory_required": True,
            "windows_atomic_no_replace_rename": True,
            "posix_atomic_no_replace_hard_link": True,
            "concurrent_destination_preserved": True,
            "migration_source_unchanged_when_backup_name_lost": True,
        },
        "surviving_limits": [
            "The Windows implementation is exercised here; the POSIX hard-link branch still needs a native POSIX run.",
            "A same-user writer can mutate a published file afterward; protected witness/key custody and OS permissions remain separate controls.",
            "This does not establish physical power-loss or directory-entry durability across every filesystem.",
        ],
        "nonclaim": "M08-S009 local atomic no-overwrite repair only; not cross-platform filesystem or release assurance.",
    }
    OUTPUT.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps(result, indent=2))
    return 0 if result["status"].startswith("PASS_") else 1


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Reproduce the M08-S011 read-only verification boundary repair."""

from __future__ import annotations

import hashlib
import io
import json
import sys
import unittest
from pathlib import Path

from validation_config import EXPECTED_RELEASE_FAILURES, FULL_SUITE_TESTS, STORE_TESTS


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
OUTPUT = ROOT / "implementation/m08-s011-validation.json"
FILES = (
    "implementation/M08_RELEASE_HARDENING_PLAN.md",
    "implementation/m08-s011-validation-v1-failed.json",
    "implementation/m08-s011-validation-v2-failed.json",
    "implementation/validate_m08_s011.py",
    "implementation/validation_config.py",
    "src/hirc/store.py",
    "tests/test_store.py",
)


def identity(path: str) -> dict:
    body = (ROOT / path).read_bytes()
    return {"path": path, "sha256": hashlib.sha256(body).hexdigest(), "bytes": len(body)}


def main() -> int:
    store_stream = io.StringIO()
    store_suite = unittest.defaultTestLoader.discover(str(ROOT / "tests"), pattern="test_store.py")
    store = unittest.TextTestRunner(stream=store_stream, verbosity=2).run(store_suite)
    full_stream = io.StringIO()
    full_suite = unittest.defaultTestLoader.discover(str(ROOT / "tests"))
    full = unittest.TextTestRunner(stream=full_stream, verbosity=1).run(full_suite)
    baseline = json.loads((ROOT / "implementation/m08-s011-validation-v1-failed.json").read_text(encoding="utf-8"))
    baseline_v2 = json.loads((ROOT / "implementation/m08-s011-validation-v2-failed.json").read_text(encoding="utf-8"))
    store_output = store_stream.getvalue().splitlines()
    checks = {
        "failed_baseline_preserved": baseline.get("status") == "FAIL" and baseline.get("finding", {}).get("id") == "M08-S011-F001",
        "projection_baseline_preserved": baseline_v2.get("status") == "FAIL" and baseline_v2.get("finding", {}).get("id") == "M08-S011-F002",
        "store_tests_pass": store.wasSuccessful(),
        "store_test_count": store.testsRun == STORE_TESTS,
        "read_only_regression_present": any("test_verify_and_status_use_read_only_connections" in line for line in store_output),
        "full_suite_pass": full.wasSuccessful(),
        "full_suite_test_count": full.testsRun == FULL_SUITE_TESTS,
        "expected_release_failures_preserved": len(full.expectedFailures) == EXPECTED_RELEASE_FAILURES,
    }
    result = {
        "schema": "hirc.m08-s011-validation/1",
        "stone": "M08-S011",
        "status": "PASS_READ_ONLY_VERIFICATION_SCOPE" if all(checks.values()) else "FAIL",
        "checks": checks,
        "files": [identity(path) for path in FILES],
        "store_test_output": store_output,
        "full_suite_output": full_stream.getvalue().splitlines(),
        "repair": {
            "finding_id": "M08-S011-F001",
            "verify_read_only_default": True,
            "status_read_only": True,
            "iter_events_read_only": True,
            "verified_snapshot_read_only": True,
            "append_and_migration_explicitly_writable": True,
        },
        "surviving_limits": [
            "SQLite read-only mode does not protect against another privileged process mutating the file concurrently; verified snapshots and external witnesses remain required.",
            "Filesystem and SQLite may still read WAL/journal state; this result only establishes the connection mode used by hIRC.",
            "Live storage remains plaintext and independent penetration review remains open.",
        ],
        "nonclaim": "M08-S011 local read-only verification connection repair only; not complete frozen-log or release assurance.",
    }
    OUTPUT.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps(result, indent=2))
    return 0 if result["status"].startswith("PASS_") else 1


if __name__ == "__main__":
    raise SystemExit(main())

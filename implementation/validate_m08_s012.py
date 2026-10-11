#!/usr/bin/env python3
"""Reproduce the M08-S012 canonical JSON ambiguity repair."""

from __future__ import annotations

import hashlib
import io
import json
import sys
import unittest
from pathlib import Path

from validation_config import (
    ADAPTER_TESTS,
    EXPECTED_RELEASE_FAILURES,
    FULL_SUITE_TESTS,
    MIGRATION_TESTS,
    STORE_TESTS,
)


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
OUTPUT = ROOT / "implementation/m08-s012-validation.json"
FILES = (
    "implementation/M08_RELEASE_HARDENING_PLAN.md",
    "implementation/m08-s012-validation-v1-failed.json",
    "implementation/validate_m08_s012.py",
    "implementation/validation_config.py",
    "src/hirc/canonical.py",
    "src/hirc/cli.py",
    "src/hirc/store.py",
    "src/hirc/migration.py",
    "tests/test_store.py",
    "tests/test_adapter.py",
    "tests/test_migration_hardening.py",
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
    store, store_output = run("test_store.py")
    adapter, adapter_output = run("test_adapter.py")
    migration, migration_output = run("test_migration_hardening.py")
    full_stream = io.StringIO()
    full_suite = unittest.defaultTestLoader.discover(str(ROOT / "tests"))
    full = unittest.TextTestRunner(stream=full_stream, verbosity=1).run(full_suite)
    baseline = json.loads((ROOT / "implementation/m08-s012-validation-v1-failed.json").read_text(encoding="utf-8"))
    checks = {
        "failed_baseline_preserved": baseline.get("status") == "FAIL" and baseline.get("finding", {}).get("id") == "M08-S012-F001",
        "store_tests_pass": store.wasSuccessful() and store.testsRun == STORE_TESTS,
        "adapter_tests_pass": adapter.wasSuccessful() and adapter.testsRun == ADAPTER_TESTS,
        "migration_tests_pass": migration.wasSuccessful() and migration.testsRun == MIGRATION_TESTS,
        "stored_payload_regression_present": any("test_verifier_rejects_noncanonical_duplicate_key_payload" in line for line in store_output),
        "file_ingress_regression_present": any("test_cli_rejects_duplicate_json_keys" in line for line in adapter_output),
        "legacy_migration_regression_present": any("test_duplicate_key_legacy_payload_refuses_without_schema_change" in line for line in migration_output),
        "full_suite_pass": full.wasSuccessful(),
        "full_suite_test_count": full.testsRun == FULL_SUITE_TESTS,
        "expected_release_failures_preserved": len(full.expectedFailures) == EXPECTED_RELEASE_FAILURES,
    }
    result = {
        "schema": "hirc.m08-s012-validation/1",
        "stone": "M08-S012",
        "status": "PASS_CANONICAL_JSON_AMBIGUITY_REPAIR_SCOPE" if all(checks.values()) else "FAIL",
        "checks": checks,
        "files": [identity(path) for path in FILES],
        "store_test_output": store_output,
        "adapter_test_output": adapter_output,
        "migration_test_output": migration_output,
        "full_suite_output": full_stream.getvalue().splitlines(),
        "repair": {
            "finding_id": "M08-S012-F001",
            "duplicate_keys_rejected_at_ingress": True,
            "stored_payload_exact_canonical_bytes_required": True,
            "legacy_migration_requires_canonical_payload": True,
            "same_head_raw_payload_rewrite_rejected": True,
        },
        "surviving_limits": [
            "Canonical raw payload validation does not defeat a privileged full-chain rewrite without a protected external witness.",
            "Other serialization formats and future remote adapters require their own ambiguity controls.",
            "Live storage remains plaintext and independent penetration review remains open.",
        ],
        "nonclaim": "M08-S012 local canonical-JSON ambiguity repair only; not complete tamper-proof or release assurance.",
    }
    OUTPUT.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps(result, indent=2))
    return 0 if result["status"].startswith("PASS_") else 1


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Reproduce the M08-S010 bounded UTF-8 JSON file ingress repair."""

from __future__ import annotations

import hashlib
import io
import json
import sys
import unittest
from pathlib import Path

from validation_config import (
    ADAPTER_TESTS,
    DECISION_TESTS,
    EXPECTED_RELEASE_FAILURES,
    FULL_SUITE_TESTS,
    WITNESS_TESTS,
)


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
OUTPUT = ROOT / "implementation/m08-s010-validation.json"
FILES = (
    "implementation/M08_RELEASE_HARDENING_PLAN.md",
    "implementation/m08-s010-validation-v1-failed.json",
    "implementation/validate_m08_s010.py",
    "implementation/validation_config.py",
    "src/hirc/canonical.py",
    "src/hirc/cli.py",
    "src/hirc/witness.py",
    "tests/test_adapter.py",
    "tests/test_decision_preview.py",
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
    adapter, adapter_output = run("test_adapter.py")
    decision, decision_output = run("test_decision_preview.py")
    witness, witness_output = run("test_witness.py")
    full_stream = io.StringIO()
    full_suite = unittest.defaultTestLoader.discover(str(ROOT / "tests"))
    full = unittest.TextTestRunner(stream=full_stream, verbosity=1).run(full_suite)
    baseline = json.loads((ROOT / "implementation/m08-s010-validation-v1-failed.json").read_text(encoding="utf-8"))
    checks = {
        "failed_baseline_preserved": baseline.get("status") == "FAIL" and baseline.get("finding", {}).get("id") == "M08-S010-F001",
        "adapter_tests_pass": adapter.wasSuccessful() and adapter.testsRun == ADAPTER_TESTS,
        "decision_tests_pass": decision.wasSuccessful() and decision.testsRun == DECISION_TESTS,
        "witness_tests_pass": witness.wasSuccessful() and witness.testsRun == WITNESS_TESTS,
        "oversized_ingress_regression_present": any("test_cli_rejects_oversized_json_file_before_parsing" in line for line in adapter_output),
        "invalid_utf8_regression_present": any("test_cli_invalid_utf8_file_fails_closed" in line for line in decision_output),
        "bounded_witness_regression_present": any("test_oversized_witness_file_is_rejected_before_parsing" in line for line in witness_output),
        "full_suite_pass": full.wasSuccessful(),
        "full_suite_test_count": full.testsRun == FULL_SUITE_TESTS,
        "expected_release_failures_preserved": len(full.expectedFailures) == EXPECTED_RELEASE_FAILURES,
    }
    result = {
        "schema": "hirc.m08-s010-validation/1",
        "stone": "M08-S010",
        "status": "PASS_BOUNDED_JSON_FILE_INGRESS_SCOPE" if all(checks.values()) else "FAIL",
        "checks": checks,
        "files": [identity(path) for path in FILES],
        "adapter_test_output": adapter_output,
        "decision_test_output": decision_output,
        "witness_test_output": witness_output,
        "full_suite_output": full_stream.getvalue().splitlines(),
        "repair": {
            "finding_id": "M08-S010-F001",
            "predecode_byte_limit": True,
            "strict_utf8": True,
            "bounded_depth_and_canonical_size": True,
            "cli_errors_fail_closed_to_held": True,
        },
        "surviving_limits": [
            "SQLite row materialization and encrypted-backup streaming have separate resource profiles not closed by this file-ingress repair.",
            "Local filesystem availability and quota exhaustion remain operating-environment concerns.",
            "No remote JSON input or network path is enabled.",
        ],
        "nonclaim": "M08-S010 bounded local JSON file ingress repair only; not general denial-of-service or release assurance.",
    }
    OUTPUT.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps(result, indent=2))
    return 0 if result["status"].startswith("PASS_") else 1


if __name__ == "__main__":
    raise SystemExit(main())

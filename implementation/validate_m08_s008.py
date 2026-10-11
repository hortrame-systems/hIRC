#!/usr/bin/env python3
"""Reproduce the M08-S008 materialized outbox integrity repair checks."""

from __future__ import annotations

import hashlib
import io
import json
import sys
import unittest
from pathlib import Path

from validation_config import EXPECTED_RELEASE_FAILURES, FULL_SUITE_TESTS, OUTBOX_TESTS


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
OUTPUT = ROOT / "implementation/m08-s008-validation.json"
FILES = (
    "implementation/M08_RELEASE_HARDENING_PLAN.md",
    "implementation/m08-s008-validation-v1-failed.json",
    "implementation/validate_m08_s008.py",
    "src/hirc/store.py",
    "tests/test_outbox.py",
)


def identity(path: str) -> dict:
    body = (ROOT / path).read_bytes()
    return {"path": path, "sha256": hashlib.sha256(body).hexdigest(), "bytes": len(body)}


def main() -> int:
    outbox_stream = io.StringIO()
    outbox_suite = unittest.defaultTestLoader.discover(str(ROOT / "tests"), pattern="test_outbox.py")
    outbox = unittest.TextTestRunner(stream=outbox_stream, verbosity=2).run(outbox_suite)

    full_stream = io.StringIO()
    full_suite = unittest.defaultTestLoader.discover(str(ROOT / "tests"))
    full = unittest.TextTestRunner(stream=full_stream, verbosity=1).run(full_suite)

    baseline = json.loads((ROOT / "implementation/m08-s008-validation-v1-failed.json").read_text(encoding="utf-8"))
    checks = {
        "failed_baseline_preserved": baseline.get("status") == "FAIL" and baseline.get("finding", {}).get("id") == "M08-S008-F001",
        "outbox_suite_pass": outbox.wasSuccessful(),
        "outbox_test_count": outbox.testsRun == OUTBOX_TESTS,
        "full_suite_pass": full.wasSuccessful(),
        "full_suite_test_count": full.testsRun == FULL_SUITE_TESTS,
        "three_expected_release_failures": len(full.expectedFailures) == EXPECTED_RELEASE_FAILURES,
        "stage_rebinding_regression_present": "test_privileged_stage_rebinding_is_detected_after_trigger_restoration" in outbox_stream.getvalue(),
        "schema_weakening_regression_present": "test_privileged_outbox_schema_weakening_is_detected" in outbox_stream.getvalue(),
    }
    result = {
        "schema": "hirc.m08-s008-validation/1",
        "stone": "M08-S008",
        "status": "PASS_LOCAL_INTEGRITY_REPAIR_SCOPE" if all(checks.values()) else "FAIL",
        "checks": checks,
        "files": [identity(path) for path in FILES],
        "outbox_test_output": outbox_stream.getvalue().splitlines(),
        "full_suite_output": full_stream.getvalue().splitlines(),
        "repair": {
            "finding_id": "M08-S008-F001",
            "stage_payload_binding": True,
            "stage_boundary_binding": True,
            "exact_schema_object_set": True,
            "event_chain_head_alone_sufficient": False,
        },
        "surviving_limits": [
            "A same-user privileged writer can still rewrite the event chain and requires the separately protected witness to make rollback detectable.",
            "The local SQLite store remains plaintext and sensitive-data release remains blocked.",
            "This repair is not an independent penetration review or cross-machine recovery result.",
        ],
        "nonclaim": "M08-S008 local materialized-outbox integrity repair only; not sensitive-data, production or public release acceptance.",
    }
    OUTPUT.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps(result, indent=2))
    return 0 if result["status"].startswith("PASS_") else 1


if __name__ == "__main__":
    raise SystemExit(main())

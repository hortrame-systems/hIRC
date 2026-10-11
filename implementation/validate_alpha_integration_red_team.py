#!/usr/bin/env python3
"""Reproduce the first cross-component alpha red-team batch."""

from __future__ import annotations

import hashlib
import io
import json
import sys
import unittest
from pathlib import Path

from validation_config import FULL_SUITE_TESTS


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "implementation/alpha-integration-red-team-validation-v1.json"
FAILED_V1 = ROOT / "implementation/m06-s001-red-team-validation-v1-failed.json"
FAILED_V2 = ROOT / "implementation/alpha-integration-red-team-validation-v2-failed.json"
sys.path.insert(0, str(ROOT / "src"))


FILES = (
    "src/hirc/store.py",
    "src/hirc/projection.py",
    "tests/test_integration.py",
    "implementation/RED_TEAM_INTEGRATION_TEST_PLAN.md",
    "implementation/m06-s001-red-team-validation-v1-failed.json",
    "implementation/alpha-integration-red-team-validation-v2-failed.json",
)


def identity(relative: str) -> dict[str, object]:
    body = (ROOT / relative).read_bytes()
    return {"path": relative, "sha256": hashlib.sha256(body).hexdigest(), "bytes": len(body)}


def main() -> int:
    integration_stream = io.StringIO()
    integration_suite = unittest.defaultTestLoader.discover(
        str(ROOT / "tests"), pattern="test_integration.py"
    )
    integration_tests = unittest.TextTestRunner(
        stream=integration_stream, verbosity=2
    ).run(integration_suite)
    full_stream = io.StringIO()
    full_suite = unittest.defaultTestLoader.discover(str(ROOT / "tests"))
    full_tests = unittest.TextTestRunner(stream=full_stream, verbosity=2).run(full_suite)
    failed_v1 = json.loads(FAILED_V1.read_text(encoding="utf-8"))
    failed_v2 = json.loads(FAILED_V2.read_text(encoding="utf-8"))
    repaired_v1 = {
        "test_tampered_chain_rejects_next_append",
        "test_missing_disabled_capability_rejects_next_append",
        "test_briefing_inherits_privacy_audience_and_purpose",
        "test_projection_rejects_silent_information_boundary_change",
    }
    repaired_v2 = {
        "test_correction_cannot_widen_target_boundary",
        "test_held_dependency_blocks_transitive_descendants",
        "test_invalid_allowed_sibling_fails_projection",
        "test_missing_append_only_trigger_rejects_next_append",
        "test_projection_does_not_trust_separate_verify_then_read",
        "test_reinitialize_refuses_to_repair_corrupt_capability_state",
    }
    failed_v1_tests = {f"test_{item['test']}" for item in failed_v1["failed"]}
    failed_v2_tests = {f"test_{item['test']}" for item in failed_v2["failed"]}
    repaired_tests = repaired_v1 | repaired_v2
    checks = {
        "first_failed_baseline_preserved": failed_v1.get("status") == "PRESERVED_FAILED_BASELINE",
        "four_first_failures_bound": failed_v1_tests == repaired_v1,
        "second_failed_baseline_preserved": failed_v2.get("status") == "PRESERVED_FAILED_BASELINE",
        "six_second_failures_bound": failed_v2_tests == repaired_v2,
        "integration_tests_pass": integration_tests.wasSuccessful(),
        "integration_test_count": integration_tests.testsRun == 18,
        "full_suite_pass": full_tests.wasSuccessful(),
        "full_suite_test_count": full_tests.testsRun == FULL_SUITE_TESTS,
    }
    result = {
        "schema": "hirc.alpha-integration-red-team-validation/1",
        "status": "PASS" if all(checks.values()) else "FAIL",
        "checks": checks,
        "files": [identity(path) for path in FILES],
        "integration_test_output": integration_stream.getvalue().splitlines(),
        "full_suite_output": full_stream.getvalue().splitlines(),
        "repaired_findings": sorted(repaired_tests),
        "surviving_limits": [
            "No writable UI, provider, outbox, secret, encryption, installed-package, external-effect or Bridge component exists yet; M06-S001 adds only a static read-only snapshot.",
            "The full suite is run from the source tree; plain discovery in an uninstalled checkout cannot import hirc until PYTHONPATH is supplied or the package is installed.",
            "Finite concurrency tests do not establish universal race freedom or crash safety.",
            "No fuzzing, load/soak, cross-machine recovery, accessibility or independent penetration review has run."
        ],
        "nonclaim": "Two local cross-component alpha attack batches only; not full security assurance or M06 UI acceptance."
    }
    OUTPUT.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps(result, indent=2))
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())

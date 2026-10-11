#!/usr/bin/env python3
"""Reproduce M07-S003 atomic local no-dispatch outbox checks."""

from __future__ import annotations

import hashlib
import io
import json
import sys
import tempfile
import unittest
from pathlib import Path

from validation_config import FULL_SUITE_TESTS, OUTBOX_TESTS


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from hirc.adapter import AcceptanceOnlyAdapter, DeterministicEchoAdapter, build_adapter_request, run_local_adapter  # noqa: E402
from hirc.outbox import record_adapter_run  # noqa: E402
from hirc.store import Store  # noqa: E402


OUTPUT = ROOT / "implementation/m07-s003-validation.json"
FILES = (
    "implementation/M07_FORMATION_ADAPTER_PLAN.md",
    "implementation/README.md",
    "src/hirc/store.py",
    "src/hirc/outbox.py",
    "src/hirc/adapter.py",
    "src/hirc/cli.py",
    "tests/test_outbox.py",
)


def identity(relative: str) -> dict[str, object]:
    body = (ROOT / relative).read_bytes()
    return {"path": relative, "sha256": hashlib.sha256(body).hexdigest(), "bytes": len(body)}


def request(text: str) -> dict:
    return build_adapter_request({
        "actor_id": "actor:validator", "task_id": "task:hirc", "admission_ref": "admission:recorded",
        "foundation_version": "foundation:1", "goal_version": "goal:2", "privacy_class": "privacy:owner",
        "audience": "audience:owner", "purpose": "purpose:m07-outbox-validation", "requested_at": "time:20261010T000000Z",
        "capability": "capability:local-transform", "payload": {"text": text},
    })


def main() -> int:
    outbox_stream = io.StringIO()
    outbox_suite = unittest.defaultTestLoader.discover(str(ROOT / "tests"), pattern="test_outbox.py")
    outbox_tests = unittest.TextTestRunner(stream=outbox_stream, verbosity=2).run(outbox_suite)
    full_stream = io.StringIO()
    full_suite = unittest.defaultTestLoader.discover(str(ROOT / "tests"))
    full_tests = unittest.TextTestRunner(stream=full_stream, verbosity=1).run(full_suite)

    temp_root = ROOT / "tests/.tmp"
    temp_root.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(dir=temp_root) as directory:
        store = Store(Path(directory) / "m07-s003.sqlite3")
        store.initialize()
        observed = record_adapter_run(
            store,
            run_local_adapter(DeterministicEchoAdapter(), request("observed")),
            idempotency_key="idempotency:observed",
            authority_ref="authority:local",
            occurred_at="2026-10-10T00:00:00Z",
        )
        uncertain = record_adapter_run(
            store,
            run_local_adapter(AcceptanceOnlyAdapter(), request("uncertain")),
            idempotency_key="idempotency:uncertain",
            authority_ref="authority:local",
            occurred_at="2026-10-10T00:00:01Z",
        )
        verification = store.verify()
    by_key = {item["idempotency_key"]: item for item in uncertain["items"]}
    checks = {
        "outbox_tests_pass": outbox_tests.wasSuccessful(),
        "outbox_test_count": outbox_tests.testsRun == OUTBOX_TESTS,
        "full_suite_pass": full_tests.wasSuccessful(),
        "full_suite_test_count": full_tests.testsRun == FULL_SUITE_TESTS,
        "store_valid": verification["valid"],
        "two_items_six_events": len(uncertain["items"]) == 2 and verification["event_count"] == 6,
        "observed_state_separate": by_key["idempotency:observed"]["reported_state"] == "PROVIDER_ACCEPTED" and by_key["idempotency:observed"]["observed_state"] == "OBSERVED",
        "unknown_not_promoted": by_key["idempotency:uncertain"]["reported_state"] == "PROVIDER_ACCEPTED" and by_key["idempotency:uncertain"]["observed_state"] == "UNKNOWN",
        "external_dispatch_disabled": uncertain["external_dispatch_enabled"] is False,
        "first_view_is_prefix": len(observed["items"]) == 1 and observed["items"][0]["observed_state"] == "OBSERVED",
    }
    result = {
        "schema": "hirc.m07-s003-validation/1",
        "stone": "M07-S003",
        "status": "PASS" if all(checks.values()) else "FAIL",
        "checks": checks,
        "files": [identity(path) for path in FILES],
        "outbox_test_output": outbox_stream.getvalue().splitlines(),
        "full_suite_output": full_stream.getvalue().splitlines(),
        "control_view": uncertain,
        "surviving_limits": [
            "Exactly-once behavior is established only for this local SQLite transaction and deterministic duplicate fixture, not distributed systems or providers.",
            "Provider acceptance and observed output are fake local evidence; no network dispatch or production observation occurs.",
            "Schema migration, crash injection below SQLite's guarantees, backup/restore and cross-machine recovery remain M08 work."
        ],
        "nonclaim": "M07-S003 atomic local fake-provider outbox evidence only; external dispatch remains disabled."
    }
    OUTPUT.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps(result, indent=2))
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())

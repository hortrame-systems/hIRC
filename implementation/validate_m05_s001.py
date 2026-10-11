#!/usr/bin/env python3
"""Reproduce the M05-S001 work and return-briefing acceptance checks."""

from __future__ import annotations

import hashlib
import io
import json
import sys
import tempfile
import unittest
from pathlib import Path

from validation_config import FULL_SUITE_TESTS


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
OUTPUT = ROOT / "implementation/m05-s001-validation.json"
sys.path.insert(0, str(SRC))

from hirc.projection import build_briefing  # noqa: E402
from hirc.store import EventInput, Store  # noqa: E402


FILES = (
    "src/hirc/projection.py",
    "src/hirc/cli.py",
    "src/hirc/store.py",
    "tests/test_projection.py",
    "implementation/README.md",
)
BASE = {
    "actor_id": "actor:validator",
    "category": "EVIDENCE",
    "foundation_version": "foundation:1",
    "goal_version": "goal:2",
    "privacy_class": "privacy:owner",
    "audience": "audience:owner",
    "purpose": "purpose:work-recovery",
    "occurred_at": "2026-10-10T00:00:00Z",
}


def identity(relative: str) -> dict[str, object]:
    body = (ROOT / relative).read_bytes()
    return {"path": relative, "sha256": hashlib.sha256(body).hexdigest(), "bytes": len(body)}


def append(store: Store, event_type: str, payload: dict, stream: str) -> None:
    store.append(EventInput(stream_id=stream, event_type=event_type, payload=payload, **BASE))


def main() -> int:
    output = io.StringIO()
    suite = unittest.defaultTestLoader.discover(str(ROOT / "tests"), pattern="test_projection.py")
    tests = unittest.TextTestRunner(stream=output, verbosity=2).run(suite)

    temp_root = ROOT / "tests/.tmp"
    temp_root.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(dir=temp_root) as directory:
        store = Store(Path(directory) / "m05.sqlite3")
        store.initialize()
        append(store, "work.created", {"work_id": "work:blocked", "title": "Blocked", "owner": "actor:validator", "next_action": "Await evidence"}, "work:blocked")
        append(store, "work.created", {"work_id": "work:ready", "title": "Ready sibling", "owner": "actor:validator", "next_action": "Continue"}, "work:ready")
        append(store, "commitment.declared", {"commitment_id": "commitment:one", "work_id": "work:ready", "owner": "actor:validator", "description": "Complete sibling"}, "work:ready")
        append(store, "hold.placed", {"hold_id": "hold:blocked", "work_id": "work:blocked", "reason": "missing review", "reopen_when": "review arrives", "allowed_sibling_work": "work:ready"}, "work:blocked")
        append(store, "observation.recorded", {"work_id": "work:ready", "claim": "provider operation", "reported_state": "PROVIDER_ACCEPTED", "observed_state": "UNKNOWN"}, "work:ready")
        briefing = build_briefing(store)

    work = {item["work_id"]: item for item in briefing["work"]}
    checks = {
        "unit_tests": tests.wasSuccessful(),
        "unit_test_count": tests.testsRun == 5,
        "briefing_schema": briefing["schema"] == "hirc.return-briefing/1",
        "blocked_work_held": work["work:blocked"]["status"] == "HELD",
        "sibling_still_ready": work["work:ready"]["status"] == "OPEN",
        "sibling_path_exposed": briefing["holds"][0]["allowed_sibling_work"] == "work:ready",
        "commitment_present": briefing["commitments"][0]["status"] == "OPEN",
        "reported_not_observed": work["work:ready"]["observations"][0]["reported_state"] == "PROVIDER_ACCEPTED"
        and work["work:ready"]["observations"][0]["observed_state"] == "UNKNOWN",
        "source_chain_bound": briefing["event_count"] == 5 and briefing["store_head"] != "0" * 64,
    }
    result = {
        "schema": "hirc.m05-s001-validation/1",
        "stone": "M05-S001",
        "status": "PASS" if all(checks.values()) else "FAIL",
        "checks": checks,
        "files": [identity(path) for path in FILES],
        "unit_test_output": output.getvalue().splitlines(),
        "briefing_control": briefing,
        "nonclaim": "Deterministic local work projection and return-briefing evidence only; it does not validate scheduling, agent execution, authority, external observation, UI behavior or production recovery assurance.",
    }
    OUTPUT.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps(result, indent=2))
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())

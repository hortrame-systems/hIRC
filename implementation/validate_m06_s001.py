#!/usr/bin/env python3
"""Reproduce M06-S001 read-only local UI snapshot acceptance checks."""

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
sys.path.insert(0, str(ROOT / "src"))

from hirc.projection import build_briefing  # noqa: E402
from hirc.store import EventInput, Store  # noqa: E402
from hirc.ui import write_snapshot  # noqa: E402


OUTPUT = ROOT / "implementation/m06-s001-validation.json"
REFERENCE = ROOT / "implementation/m06-s001-reference.html"
FILES = (
    "implementation/M06_LOCAL_UI_PLAN.md",
    "implementation/README.md",
    "src/hirc/ui.py",
    "src/hirc/cli.py",
    "tests/test_ui.py",
    "implementation/m06-s001-browser-check-hold.md",
)
BASE = {
    "actor_id": "actor:lucent",
    "category": "EVIDENCE",
    "foundation_version": "foundation:1",
    "goal_version": "goal:2",
    "privacy_class": "privacy:owner",
    "audience": "audience:owner",
    "purpose": "purpose:m06-validation",
    "occurred_at": "2026-10-10T00:00:00Z",
}


def identity(relative: str) -> dict[str, object]:
    body = (ROOT / relative).read_bytes()
    return {"path": relative, "sha256": hashlib.sha256(body).hexdigest(), "bytes": len(body)}


def append(store: Store, event_type: str, payload: dict, stream: str) -> None:
    store.append(EventInput(stream_id=stream, event_type=event_type, payload=payload, **BASE))


def main() -> int:
    ui_stream = io.StringIO()
    ui_suite = unittest.defaultTestLoader.discover(str(ROOT / "tests"), pattern="test_ui.py")
    ui_tests = unittest.TextTestRunner(stream=ui_stream, verbosity=2).run(ui_suite)
    full_stream = io.StringIO()
    full_suite = unittest.defaultTestLoader.discover(str(ROOT / "tests"))
    full_tests = unittest.TextTestRunner(stream=full_stream, verbosity=1).run(full_suite)

    temp_root = ROOT / "tests/.tmp"
    temp_root.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(dir=temp_root) as directory:
        store = Store(Path(directory) / "m06.sqlite3")
        store.initialize()
        append(store, "work.created", {"work_id": "work:build", "title": "Build local UI", "owner": "actor:lucent", "next_action": "Inspect the read-only snapshot"}, "work:build")
        append(store, "work.created", {"work_id": "work:review", "title": "Independent review", "owner": "actor:oriel", "next_action": "Await current readiness"}, "work:review")
        append(store, "work.created", {"work_id": "work:release", "title": "Release", "owner": "actor:lucent", "next_action": "Wait for review"}, "work:release")
        append(store, "dependency.added", {"work_id": "work:release", "depends_on": "work:review"}, "work:release")
        append(store, "hold.placed", {"hold_id": "hold:review", "work_id": "work:review", "reason": "reviewer readiness", "reopen_when": "current exact-frame review arrives", "allowed_sibling_work": "work:build"}, "work:review")
        append(store, "commitment.declared", {"commitment_id": "commitment:ui", "work_id": "work:build", "owner": "actor:lucent", "description": "Keep the surface local and read-only"}, "work:build")
        briefing = build_briefing(store)
        snapshot = write_snapshot(briefing, REFERENCE)

    html = REFERENCE.read_text(encoding="utf-8")
    by_id = {item["work_id"]: item for item in briefing["work"]}
    checks = {
        "ui_tests_pass": ui_tests.wasSuccessful(),
        "ui_test_count": ui_tests.testsRun == 5,
        "full_suite_pass": full_tests.wasSuccessful(),
        "full_suite_test_count": full_tests.testsRun == FULL_SUITE_TESTS,
        "reference_is_read_only": snapshot["read_only"] is True,
        "reference_head_matches": snapshot["source_head"] == briefing["store_head"],
        "open_work_runnable": by_id["work:build"]["status"] == "OPEN",
        "direct_hold_visible": by_id["work:review"]["status"] == "HELD",
        "dependent_block_visible": by_id["work:release"]["status"] == "BLOCKED",
        "navigation_controls_present": all(f'id="{item}"' in html for item in ("back", "forward", "resume", "search")),
        "restrictive_csp_present": "default-src &#x27;none&#x27;" in html and "script-src &#x27;sha256-" in html,
        "no_remote_resource": "http://" not in html and "https://" not in html,
        "dangerous_dom_sinks_absent": "innerHTML" not in html and "eval(" not in html,
    }
    result = {
        "schema": "hirc.m06-s001-validation/1",
        "stone": "M06-S001",
        "status": "PASS" if all(checks.values()) else "FAIL",
        "checks": checks,
        "files": [identity(path) for path in FILES] + [identity("implementation/m06-s001-reference.html")],
        "ui_test_output": ui_stream.getvalue().splitlines(),
        "full_suite_output": full_stream.getvalue().splitlines(),
        "reference": snapshot,
        "surviving_limits": [
            "Static source and unit checks do not establish browser-engine, screen-reader, zoom/reflow, forced-colors, pointer-target or human-usability behavior.",
            "The snapshot is read-only. Interruption preview is validated separately in M06-S002; actual interruption persistence plus refusal, correction and trusted-preview state transitions remain outside this stone.",
            "No listener, provider, network, external effect or Bridge path is implemented."
        ],
        "nonclaim": "M06-S001 local read-only snapshot only; not complete UI acceptance or release assurance."
    }
    OUTPUT.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps(result, indent=2))
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())

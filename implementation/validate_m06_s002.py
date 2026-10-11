#!/usr/bin/env python3
"""Reproduce M06-S002 deterministic no-effect interruption preview checks."""

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
from hirc.ui import INTERRUPT_MODES, SCRIPT, interrupt_preview, write_snapshot  # noqa: E402


OUTPUT = ROOT / "implementation/m06-s002-validation.json"
REFERENCE = ROOT / "implementation/m06-s002-reference.html"
FILES = (
    "implementation/M06_LOCAL_UI_PLAN.md",
    "implementation/README.md",
    "src/hirc/ui.py",
    "tests/test_interrupt_ui.py",
    "implementation/m06-s001-browser-check-hold.md",
)
BASE = {
    "actor_id": "actor:lucent",
    "category": "EVIDENCE",
    "foundation_version": "foundation:1",
    "goal_version": "goal:2",
    "privacy_class": "privacy:owner",
    "audience": "audience:owner",
    "purpose": "purpose:m06-interrupt-validation",
    "occurred_at": "2026-10-10T00:00:00Z",
}


def identity(relative: str) -> dict[str, object]:
    body = (ROOT / relative).read_bytes()
    return {"path": relative, "sha256": hashlib.sha256(body).hexdigest(), "bytes": len(body)}


def main() -> int:
    interrupt_stream = io.StringIO()
    interrupt_suite = unittest.defaultTestLoader.discover(str(ROOT / "tests"), pattern="test_interrupt_ui.py")
    interrupt_tests = unittest.TextTestRunner(stream=interrupt_stream, verbosity=2).run(interrupt_suite)
    full_stream = io.StringIO()
    full_suite = unittest.defaultTestLoader.discover(str(ROOT / "tests"))
    full_tests = unittest.TextTestRunner(stream=full_stream, verbosity=1).run(full_suite)

    previews = {
        mode: interrupt_preview(mode, "Current work", "New task", "Pause now; resume after review" if mode == "custom" else "")
        for mode in INTERRUPT_MODES
    }
    temp_root = ROOT / "tests/.tmp"
    temp_root.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(dir=temp_root) as directory:
        store = Store(Path(directory) / "m06-s002.sqlite3")
        store.initialize()
        store.append(EventInput(stream_id="work:current", event_type="work.created", payload={"work_id": "work:current", "title": "Current work", "owner": "actor:lucent", "next_action": "Continue"}, **BASE))
        briefing = build_briefing(store)
        snapshot = write_snapshot(briefing, REFERENCE)

    html = REFERENCE.read_text(encoding="utf-8")
    forbidden_runtime_edges = ("fetch(", "XMLHttpRequest", "WebSocket", "localStorage", "sessionStorage", "indexedDB", "sendBeacon")
    checks = {
        "interrupt_tests_pass": interrupt_tests.wasSuccessful(),
        "interrupt_test_count": interrupt_tests.testsRun == 4,
        "full_suite_pass": full_tests.wasSuccessful(),
        "full_suite_test_count": full_tests.testsRun == FULL_SUITE_TESTS,
        "exact_four_modes": list(INTERRUPT_MODES) == ["cut", "high", "low", "custom"],
        "all_previews_no_effect": all(
            result[field] is False
            for result in previews.values()
            for field in ("persisted", "scheduled", "authorized", "effect_performed")
        ),
        "cut_stops_current": previews["cut"]["order"][-1] == "stop the interrupted task",
        "high_returns_to_prior": previews["high"]["order"][-1] == "resume the exact prior task",
        "low_keeps_current": previews["low"]["order"][0] == "continue current work",
        "custom_is_explicit": previews["custom"]["custom"] == "Pause now; resume after review",
        "surface_contains_four_values": all(f'value="{mode}"' in html for mode in INTERRUPT_MODES),
        "surface_has_no_form_submission": "<form" not in html and "formaction" not in html,
        "runtime_persistence_and_network_edges_absent": not any(edge in SCRIPT for edge in forbidden_runtime_edges),
        "reference_head_matches": snapshot["source_head"] == briefing["store_head"],
    }
    result = {
        "schema": "hirc.m06-s002-validation/1",
        "stone": "M06-S002",
        "status": "PASS" if all(checks.values()) else "FAIL",
        "checks": checks,
        "files": [identity(path) for path in FILES] + [identity("implementation/m06-s002-reference.html")],
        "interrupt_test_output": interrupt_stream.getvalue().splitlines(),
        "full_suite_output": full_stream.getvalue().splitlines(),
        "previews": previews,
        "reference": snapshot,
        "surviving_limits": [
            "The choices are deterministic previews; no queue, checkpoint, scheduler or event persistence is implemented by this stone.",
            "Rendered browser/keyboard/screen-reader interaction remains held by the existing local-file browser-policy boundary.",
            "No authority, network, external effect or Bridge path is enabled."
        ],
        "nonclaim": "M06-S002 no-effect interruption preview only; not task scheduling or interruption execution."
    }
    OUTPUT.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps(result, indent=2))
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())

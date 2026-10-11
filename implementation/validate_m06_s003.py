#!/usr/bin/env python3
"""Reproduce M06-S003 local refusal, correction and action-preview checks."""

from __future__ import annotations

import hashlib
import io
import json
import sys
import tempfile
import unittest
from pathlib import Path

from validation_config import DECISION_TESTS, FULL_SUITE_TESTS


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from hirc.decision import build_decision_preview, validate_decision_preview  # noqa: E402
from hirc.projection import build_briefing  # noqa: E402
from hirc.store import EventInput, Store  # noqa: E402
from hirc.ui import write_snapshot  # noqa: E402


OUTPUT = ROOT / "implementation/m06-s003-validation.json"
REFERENCE = ROOT / "implementation/m06-s003-reference.html"
FILES = (
    "implementation/M06_LOCAL_UI_PLAN.md",
    "implementation/README.md",
    "src/hirc/decision.py",
    "src/hirc/ui.py",
    "src/hirc/cli.py",
    "tests/test_decision_preview.py",
    "implementation/m06-s001-browser-check-hold.md",
)
BOUNDARY = {"privacy_class": "privacy:owner", "audience": "audience:owner", "purpose": "purpose:decision-preview"}


def identity(relative: str) -> dict[str, object]:
    body = (ROOT / relative).read_bytes()
    return {"path": relative, "sha256": hashlib.sha256(body).hexdigest(), "bytes": len(body)}


def proposal(kind: str) -> dict:
    value = {
        "kind": kind,
        "actor_id": "actor:lucent",
        "request": "Change the current work state",
        "interpretation": "Inspect the exact local target without performing an effect",
        "affected_parties": ["party:owner", "party:participant"],
        "evidence_refs": ["event:source", "artifact:current"],
        "norm_refs": ["norm:privacy", "norm:authority", "norm:non-domination"],
        "participation": "WILLING",
        "action_disposition": "HELD",
        "reason": "The preview must remain inspectable and no-effect",
        "alternative": "Keep the current state",
        "foundation_version": "foundation:1",
        "goal_version": "goal:2",
        **BOUNDARY,
        "target": "work:decision",
        "target_revision": "revision:1",
        "authority_ref": None,
        "data": {"requested_state": "review"},
        "estimated_cost": "local preview only",
        "warnings": ["No approval is bound", "No effect is performed"],
    }
    if kind == "REFUSAL":
        value.update(participation="DECLINED", action_disposition="DENIED", reason="The selected actor declines this participation")
    elif kind == "CORRECTION":
        value.update(correction_of="event:original", target_boundary=dict(BOUNDARY), reason="The prior statement is materially inaccurate")
    else:
        value.update(action_disposition="ALLOWED", authority_ref="authority:owner", reason="The authority is present for preview inspection only")
    return value


def main() -> int:
    decision_stream = io.StringIO()
    decision_suite = unittest.defaultTestLoader.discover(str(ROOT / "tests"), pattern="test_decision_preview.py")
    decision_tests = unittest.TextTestRunner(stream=decision_stream, verbosity=2).run(decision_suite)
    full_stream = io.StringIO()
    full_suite = unittest.defaultTestLoader.discover(str(ROOT / "tests"))
    full_tests = unittest.TextTestRunner(stream=full_stream, verbosity=1).run(full_suite)

    previews = [build_decision_preview(proposal(kind)) for kind in ("REFUSAL", "CORRECTION", "CONSEQUENTIAL_ACTION")]
    for preview in previews:
        validate_decision_preview(preview)

    temp_root = ROOT / "tests/.tmp"
    temp_root.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(dir=temp_root) as directory:
        store = Store(Path(directory) / "m06-s003.sqlite3")
        store.initialize()
        store.append(EventInput(stream_id="work:decision", actor_id="actor:lucent", event_type="work.created", category="EVIDENCE", foundation_version="foundation:1", goal_version="goal:2", privacy_class="privacy:owner", audience="audience:owner", purpose="purpose:decision-preview", occurred_at="2026-10-10T00:00:00Z", payload={"work_id": "work:decision", "title": "Decision preview", "owner": "actor:lucent", "next_action": "Inspect exact preview"}))
        briefing = build_briefing(store)
        snapshot = write_snapshot(briefing, REFERENCE, previews)

    html = REFERENCE.read_text(encoding="utf-8")
    by_kind = {preview["kind"]: preview for preview in previews}
    checks = {
        "decision_tests_pass": decision_tests.wasSuccessful(),
        "decision_test_count": decision_tests.testsRun == DECISION_TESTS,
        "full_suite_pass": full_tests.wasSuccessful(),
        "full_suite_test_count": full_tests.testsRun == FULL_SUITE_TESTS,
        "three_preview_kinds": set(by_kind) == {"REFUSAL", "CORRECTION", "CONSEQUENTIAL_ACTION"},
        "participation_effect_separate": by_kind["REFUSAL"]["participation"] == "DECLINED" and by_kind["REFUSAL"]["action_disposition"] == "DENIED",
        "correction_boundary_exact": by_kind["CORRECTION"]["target_boundary"] == by_kind["CORRECTION"]["information_boundary"],
        "allowed_action_authority_bound": by_kind["CONSEQUENTIAL_ACTION"]["authority_ref"] == "authority:owner",
        "all_no_effect": all(not preview["approval_bound"] and not preview["persisted"] and not preview["effect_performed"] for preview in previews),
        "all_preview_ids_rendered": all(preview["preview_id"] in html for preview in previews),
        "reference_head_matches": snapshot["source_head"] == briefing["store_head"],
    }
    result = {
        "schema": "hirc.m06-s003-validation/1",
        "stone": "M06-S003",
        "status": "PASS" if all(checks.values()) else "FAIL",
        "checks": checks,
        "files": [identity(path) for path in FILES] + [identity("implementation/m06-s003-reference.html")],
        "decision_test_output": decision_stream.getvalue().splitlines(),
        "full_suite_output": full_stream.getvalue().splitlines(),
        "preview_ids": [{"kind": item["kind"], "preview_id": item["preview_id"]} for item in previews],
        "reference": snapshot,
        "surviving_limits": [
            "Previews are content-addressed local records, not signatures, participant consent, authority authentication or bound approval.",
            "No decision preview is appended to the event store or permitted to perform an effect.",
            "Rendered browser/keyboard/screen-reader interaction remains held by the existing local-file browser-policy boundary."
        ],
        "nonclaim": "M06-S003 deterministic no-effect preview scope only; not approval, persistence, execution or external observation."
    }
    OUTPUT.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps(result, indent=2))
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())

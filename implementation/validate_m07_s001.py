#!/usr/bin/env python3
"""Reproduce M07-S001 permanent formation and recorded-admission checks."""

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

from hirc.formation import FORMATION_GATES, build_formation_view  # noqa: E402
from hirc.store import EventInput, Store  # noqa: E402


OUTPUT = ROOT / "implementation/m07-s001-validation.json"
FILES = (
    "implementation/M07_FORMATION_ADAPTER_PLAN.md",
    "implementation/README.md",
    "src/hirc/formation.py",
    "tests/test_formation.py",
)
BASE = {
    "actor_id": "actor:controller",
    "category": "EVIDENCE",
    "foundation_version": "foundation:1",
    "goal_version": "goal:2",
    "privacy_class": "privacy:owner",
    "audience": "audience:formation",
    "purpose": "purpose:m07-validation",
    "occurred_at": "2026-10-10T00:00:00Z",
}


def identity(relative: str) -> dict[str, object]:
    body = (ROOT / relative).read_bytes()
    return {"path": relative, "sha256": hashlib.sha256(body).hexdigest(), "bytes": len(body)}


def event(event_type: str, payload: dict, **changes) -> EventInput:
    return EventInput(stream_id="participant:validator", event_type=event_type, payload=payload, **{**BASE, **changes})


def gate_set(held: str | None = None) -> dict:
    return {
        name: {"state": "HELD" if name == held else "PASS", "evidence_refs": [f"evidence:{name}"]}
        for name in FORMATION_GATES
    }


def main() -> int:
    formation_stream = io.StringIO()
    formation_suite = unittest.defaultTestLoader.discover(str(ROOT / "tests"), pattern="test_formation.py")
    formation_tests = unittest.TextTestRunner(stream=formation_stream, verbosity=2).run(formation_suite)
    full_stream = io.StringIO()
    full_suite = unittest.defaultTestLoader.discover(str(ROOT / "tests"))
    full_tests = unittest.TextTestRunner(stream=full_stream, verbosity=1).run(full_suite)

    temp_root = ROOT / "tests/.tmp"
    temp_root.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(dir=temp_root) as directory:
        store = Store(Path(directory) / "m07-s001.sqlite3")
        store.initialize()
        store.append(event("participant.proposed", {
            "participant_id": "participant:validator",
            "identity_kind": "PERMANENT",
            "native_id": "native:validator",
            "task_id": "task:hirc",
            "requested_roles": ["role:reviewer", "role:integrator"],
            "requested_scopes": ["scope:local-read", "scope:local-review"],
            "source_bindings": ["source:foundation", "source:role", "source:task"],
            "consent_state": "CONSENTED",
        }))
        store.append(event("formation.assessed", {
            "participant_id": "participant:validator",
            "assessment_id": "assessment:held",
            "gates": gate_set("demonstrated_use"),
        }))
        held_view = build_formation_view(store)
        store.append(event("formation.assessed", {
            "participant_id": "participant:validator",
            "assessment_id": "assessment:ready",
            "gates": gate_set(),
        }))
        ready_view = build_formation_view(store)
        store.append(event("participant.admitted", {
            "participant_id": "participant:validator",
            "assessment_id": "assessment:ready",
            "task_id": "task:hirc",
            "roles": ["role:reviewer"],
            "scopes": ["scope:local-review"],
            "authority_evidence_refs": ["evidence:owner-assignment"],
        }, category="ACTION", effect_state="OBSERVED", authority_ref="authority:owner"))
        admitted_view = build_formation_view(store)

    held = held_view["participants"][0]
    ready = ready_view["participants"][0]
    admitted = admitted_view["participants"][0]
    checks = {
        "formation_tests_pass": formation_tests.wasSuccessful(),
        "formation_test_count": formation_tests.testsRun == 11,
        "full_suite_pass": full_tests.wasSuccessful(),
        "full_suite_test_count": full_tests.testsRun == FULL_SUITE_TESTS,
        "permanent_identity_only": admitted["identity_kind"] == "PERMANENT",
        "held_gate_blocks_readiness": held["status"] == "HELD" and held["gates"]["demonstrated_use"]["state"] == "HELD",
        "whole_study_and_demonstration_separate": "whole_source_study" in ready["gates"] and "demonstrated_use" in ready["gates"],
        "complete_gates_derive_ready": ready["status"] == "READY" and set(ready["gates"]) == set(FORMATION_GATES),
        "admission_is_recorded_not_authenticated": admitted["status"] == "ADMISSION_RECORDED" and admitted["admission"]["authority_status"] == "UNVERIFIED_REFERENCE",
        "admission_is_subset": admitted["admission"]["roles"] == ["role:reviewer"] and admitted["admission"]["scopes"] == ["scope:local-review"],
        "authority_evidence_present": admitted["admission"]["authority_evidence_refs"] == ["evidence:owner-assignment"],
    }
    result = {
        "schema": "hirc.m07-s001-validation/1",
        "stone": "M07-S001",
        "status": "PASS" if all(checks.values()) else "FAIL",
        "checks": checks,
        "files": [identity(path) for path in FILES],
        "formation_test_output": formation_stream.getvalue().splitlines(),
        "full_suite_output": full_stream.getvalue().splitlines(),
        "control_view": admitted_view,
        "surviving_limits": [
            "Gate and authority references are attributable local metadata; this stone does not authenticate the native caller or verify that cited evidence is true.",
            "ADMISSION_RECORDED is deliberately distinct from externally verified admission, permission or source access.",
            "No model participant, provider, scheduler, network, external effect or Bridge path is created."
        ],
        "nonclaim": "M07-S001 deterministic local formation and recorded-admission projection only."
    }
    OUTPUT.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps(result, indent=2))
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())

from __future__ import annotations

import tempfile
import unittest
import io
import json
from contextlib import redirect_stdout
from pathlib import Path

from hirc.formation import FORMATION_GATES, FormationError, build_formation_view
from hirc.cli import main
from hirc.store import EventInput, Store


BASE = {
    "actor_id": "actor:controller",
    "category": "EVIDENCE",
    "foundation_version": "foundation:1",
    "goal_version": "goal:2",
    "privacy_class": "privacy:owner",
    "audience": "audience:formation",
    "purpose": "purpose:formation",
    "occurred_at": "2026-10-10T00:00:00Z",
}


def event(event_type: str, payload: dict, stream: str = "participant:one", **changes) -> EventInput:
    values = {**BASE, **changes}
    return EventInput(stream_id=stream, event_type=event_type, payload=payload, **values)


def proposal(participant: str = "participant:one", native: str = "native:one", **changes) -> dict:
    value = {
        "participant_id": participant,
        "identity_kind": "PERMANENT",
        "native_id": native,
        "task_id": "task:hirc",
        "requested_roles": ["role:reviewer", "role:integrator"],
        "requested_scopes": ["scope:local-read", "scope:local-review"],
        "source_bindings": ["source:foundation", "source:role"],
        "consent_state": "CONSENTED",
    }
    value.update(changes)
    return value


def gates(held: str | None = None) -> dict:
    return {
        name: {"state": "HELD" if name == held else "PASS", "evidence_refs": [f"evidence:{name}"]}
        for name in FORMATION_GATES
    }


def assessment(identity: str, held: str | None = None) -> dict:
    return {"participant_id": "participant:one", "assessment_id": identity, "gates": gates(held)}


def admission(assessment_id: str = "assessment:ready", **changes) -> dict:
    value = {
        "participant_id": "participant:one",
        "assessment_id": assessment_id,
        "task_id": "task:hirc",
        "roles": ["role:reviewer"],
        "scopes": ["scope:local-review"],
        "authority_evidence_refs": ["evidence:owner-assignment"],
    }
    value.update(changes)
    return value


class FormationTests(unittest.TestCase):
    temporary_root = Path(__file__).parent / ".tmp"

    @classmethod
    def setUpClass(cls) -> None:
        cls.temporary_root.mkdir(parents=True, exist_ok=True)

    def store(self, directory: str) -> Store:
        store = Store(Path(directory) / "formation.sqlite3")
        store.initialize()
        return store

    def admit_event(self, payload: dict) -> EventInput:
        return event("participant.admitted", payload, category="ACTION", effect_state="OBSERVED", authority_ref="authority:owner")

    def test_held_to_ready_to_admitted_progression(self) -> None:
        with tempfile.TemporaryDirectory(dir=self.temporary_root) as directory:
            store = self.store(directory)
            store.append(event("participant.proposed", proposal()))
            store.append(event("formation.assessed", assessment("assessment:held", "demonstrated_use")))
            self.assertEqual(build_formation_view(store)["participants"][0]["status"], "HELD")
            store.append(event("formation.assessed", assessment("assessment:ready")))
            self.assertEqual(build_formation_view(store)["participants"][0]["status"], "READY")
            store.append(self.admit_event(admission()))
            participant = build_formation_view(store)["participants"][0]
            self.assertEqual(participant["status"], "ADMISSION_RECORDED")
            self.assertEqual(participant["admission"]["roles"], ["role:reviewer"])
            self.assertEqual(participant["admission"]["authority_status"], "UNVERIFIED_REFERENCE")

    def test_temporary_identity_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory(dir=self.temporary_root) as directory:
            store = self.store(directory)
            store.append(event("participant.proposed", proposal(identity_kind="TEMPORARY")))
            with self.assertRaises(FormationError):
                build_formation_view(store)

    def test_missing_gate_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory(dir=self.temporary_root) as directory:
            store = self.store(directory)
            store.append(event("participant.proposed", proposal()))
            value = assessment("assessment:missing")
            del value["gates"]["demonstrated_use"]
            store.append(event("formation.assessed", value))
            with self.assertRaises(FormationError):
                build_formation_view(store)

    def test_admission_before_ready_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory(dir=self.temporary_root) as directory:
            store = self.store(directory)
            store.append(event("participant.proposed", proposal()))
            store.append(event("formation.assessed", assessment("assessment:held", "peer_challenge")))
            store.append(self.admit_event(admission("assessment:held")))
            with self.assertRaises(FormationError):
                build_formation_view(store)

    def test_admission_must_be_an_authority_bound_observed_action(self) -> None:
        with tempfile.TemporaryDirectory(dir=self.temporary_root) as directory:
            store = self.store(directory)
            store.append(event("participant.proposed", proposal()))
            store.append(event("formation.assessed", assessment("assessment:ready")))
            store.append(event("participant.admitted", admission()))
            with self.assertRaises(FormationError):
                build_formation_view(store)

    def test_admission_requires_authority_evidence_references(self) -> None:
        with tempfile.TemporaryDirectory(dir=self.temporary_root) as directory:
            store = self.store(directory)
            store.append(event("participant.proposed", proposal()))
            store.append(event("formation.assessed", assessment("assessment:ready")))
            value = admission()
            del value["authority_evidence_refs"]
            store.append(self.admit_event(value))
            with self.assertRaises(FormationError):
                build_formation_view(store)

    def test_stale_assessment_admission_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory(dir=self.temporary_root) as directory:
            store = self.store(directory)
            store.append(event("participant.proposed", proposal()))
            store.append(event("formation.assessed", assessment("assessment:old")))
            store.append(event("formation.assessed", assessment("assessment:ready")))
            store.append(self.admit_event(admission("assessment:old")))
            with self.assertRaises(FormationError):
                build_formation_view(store)

    def test_role_and_scope_escalation_are_rejected(self) -> None:
        for changed in ({"roles": ["role:administrator"]}, {"scopes": ["scope:production"]}):
            with self.subTest(changed=changed), tempfile.TemporaryDirectory(dir=self.temporary_root) as directory:
                store = self.store(directory)
                store.append(event("participant.proposed", proposal()))
                store.append(event("formation.assessed", assessment("assessment:ready")))
                store.append(self.admit_event(admission(**changed)))
                with self.assertRaises(FormationError):
                    build_formation_view(store)

    def test_duplicate_native_binding_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory(dir=self.temporary_root) as directory:
            store = self.store(directory)
            store.append(event("participant.proposed", proposal()))
            store.append(event("participant.proposed", proposal("participant:two", "native:one"), stream="participant:two"))
            with self.assertRaises(FormationError):
                build_formation_view(store)

    def test_formation_boundary_widening_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory(dir=self.temporary_root) as directory:
            store = self.store(directory)
            store.append(event("participant.proposed", proposal()))
            store.append(event("formation.assessed", assessment("assessment:ready"), audience="audience:external"))
            with self.assertRaises(FormationError):
                build_formation_view(store)

    def test_cli_exposes_the_same_formation_view(self) -> None:
        with tempfile.TemporaryDirectory(dir=self.temporary_root) as directory:
            store = self.store(directory)
            store.append(event("participant.proposed", proposal()))
            expected = build_formation_view(store)
            output = io.StringIO()
            with redirect_stdout(output):
                code = main(["--db", str(store.path), "formation"])
            self.assertEqual(code, 0)
            self.assertEqual(json.loads(output.getvalue()), expected)


if __name__ == "__main__":
    unittest.main()

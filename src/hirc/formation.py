"""Deterministic permanent-participant formation and admission projection."""

from __future__ import annotations

import json
from typing import Any

from .store import IDENTIFIER, IntegrityError, Store


FORMATION_GATES = (
    "source_currency",
    "whole_source_study",
    "role_training",
    "task_training",
    "demonstrated_use",
    "peer_challenge",
    "participant_consent",
    "native_identity_binding",
    "privacy_and_access_scope",
    "fitting_capacity",
)
GATE_STATES = frozenset({"PASS", "HELD"})


class FormationError(IntegrityError):
    """A verified chain contains an incoherent formation history."""


def _required(payload: dict[str, Any], *keys: str) -> None:
    missing = [key for key in keys if key not in payload]
    if missing:
        raise FormationError("formation payload missing: " + ", ".join(missing))


def _identifier(name: str, value: Any) -> str:
    if not isinstance(value, str) or not IDENTIFIER.fullmatch(value):
        raise FormationError(f"{name} must be a bounded identifier")
    return value


def _identifiers(name: str, value: Any) -> list[str]:
    if not isinstance(value, list) or not value:
        raise FormationError(f"{name} must be a nonempty identifier list")
    normalized = sorted({_identifier(name, item) for item in value})
    if not normalized:
        raise FormationError(f"{name} must be a nonempty identifier list")
    return normalized


def _assert_boundary(row: dict[str, Any], participant: dict[str, Any]) -> None:
    observed = (row["privacy_class"], row["audience"], row["purpose"])
    expected = (
        participant["information_boundary"]["privacy_class"],
        participant["information_boundary"]["audience"],
        participant["information_boundary"]["purpose"],
    )
    if observed != expected:
        raise FormationError("participant information boundary changed during formation")


def _gates(value: Any) -> dict[str, dict[str, Any]]:
    if not isinstance(value, dict) or set(value) != set(FORMATION_GATES):
        raise FormationError("formation assessment must contain the exact required gate set")
    normalized: dict[str, dict[str, Any]] = {}
    for name in FORMATION_GATES:
        gate = value[name]
        if not isinstance(gate, dict) or set(gate) != {"state", "evidence_refs"}:
            raise FormationError(f"formation gate has invalid shape: {name}")
        if gate["state"] not in GATE_STATES:
            raise FormationError(f"formation gate has invalid state: {name}")
        normalized[name] = {
            "state": gate["state"],
            "evidence_refs": _identifiers(f"{name}.evidence_refs", gate["evidence_refs"]),
        }
    return normalized


def build_formation_view(store: Store) -> dict[str, Any]:
    try:
        verification, rows = store.verified_snapshot()
    except IntegrityError as error:
        raise FormationError("cannot project formation from an invalid event chain") from error
    participants: dict[str, dict[str, Any]] = {}
    native_bindings: dict[str, str] = {}
    source_events: list[str] = []

    for row in rows:
        event_type = row["event_type"]
        if event_type not in {"participant.proposed", "formation.assessed", "participant.admitted"}:
            continue
        payload = json.loads(row["payload_json"])
        event_id = row["event_id"]
        source_events.append(event_id)
        if event_type == "participant.proposed":
            _required(
                payload,
                "participant_id",
                "identity_kind",
                "native_id",
                "task_id",
                "requested_roles",
                "requested_scopes",
                "source_bindings",
                "consent_state",
            )
            participant_id = _identifier("participant_id", payload["participant_id"])
            native_id = _identifier("native_id", payload["native_id"])
            if participant_id in participants:
                raise FormationError(f"duplicate participant proposal: {participant_id}")
            if native_id in native_bindings:
                raise FormationError(f"native identity already bound: {native_id}")
            if payload["identity_kind"] != "PERMANENT":
                raise FormationError("temporary or unknown participant identities are forbidden")
            if payload["consent_state"] != "CONSENTED":
                raise FormationError("participant proposal requires explicit consent")
            participants[participant_id] = {
                "participant_id": participant_id,
                "identity_kind": "PERMANENT",
                "native_id": native_id,
                "task_id": _identifier("task_id", payload["task_id"]),
                "requested_roles": _identifiers("requested_roles", payload["requested_roles"]),
                "requested_scopes": _identifiers("requested_scopes", payload["requested_scopes"]),
                "source_bindings": _identifiers("source_bindings", payload["source_bindings"]),
                "consent_state": "CONSENTED",
                "status": "FORMING",
                "latest_assessment_id": None,
                "gates": None,
                "admission": None,
                "information_boundary": {
                    "privacy_class": row["privacy_class"],
                    "audience": row["audience"],
                    "purpose": row["purpose"],
                },
                "source_events": {"proposed": event_id, "assessment": None, "admitted": None},
            }
            native_bindings[native_id] = participant_id
            continue

        _required(payload, "participant_id")
        participant_id = _identifier("participant_id", payload["participant_id"])
        if participant_id not in participants:
            raise FormationError(f"formation event references missing participant: {participant_id}")
        participant = participants[participant_id]
        _assert_boundary(row, participant)
        if event_type == "formation.assessed":
            _required(payload, "assessment_id", "gates")
            if participant["status"] == "ADMISSION_RECORDED":
                raise FormationError("participant with recorded admission cannot be reassessed in M07-S001")
            gates = _gates(payload["gates"])
            participant["latest_assessment_id"] = _identifier("assessment_id", payload["assessment_id"])
            participant["gates"] = gates
            participant["status"] = "READY" if all(item["state"] == "PASS" for item in gates.values()) else "HELD"
            participant["source_events"]["assessment"] = event_id
            continue

        _required(payload, "assessment_id", "task_id", "roles", "scopes", "authority_evidence_refs")
        if row["category"] != "ACTION" or row["effect_state"] != "OBSERVED" or not row["authority_ref"]:
            raise FormationError("admission must be an authority-bound observed action")
        if participant["status"] != "READY":
            raise FormationError("participant admission requires current READY formation")
        if payload["assessment_id"] != participant["latest_assessment_id"]:
            raise FormationError("participant admission references a stale assessment")
        if _identifier("task_id", payload["task_id"]) != participant["task_id"]:
            raise FormationError("participant admission changed the task")
        roles = _identifiers("roles", payload["roles"])
        scopes = _identifiers("scopes", payload["scopes"])
        if not set(roles) <= set(participant["requested_roles"]):
            raise FormationError("participant admission escalates requested roles")
        if not set(scopes) <= set(participant["requested_scopes"]):
            raise FormationError("participant admission escalates requested scopes")
        participant["status"] = "ADMISSION_RECORDED"
        participant["admission"] = {
            "roles": roles,
            "scopes": scopes,
            "authority_ref": row["authority_ref"],
            "authority_evidence_refs": _identifiers(
                "authority_evidence_refs", payload["authority_evidence_refs"]
            ),
            "authority_status": "UNVERIFIED_REFERENCE",
            "effect_state": row["effect_state"],
        }
        participant["source_events"]["admitted"] = event_id

    return {
        "schema": "hirc.formation-view/1",
        "store_head": verification["head_hash"],
        "event_count": verification["event_count"],
        "formation_event_count": len(source_events),
        "participants": [participants[key] for key in sorted(participants)],
        "source_events": source_events,
        "nonclaim": "A deterministic local formation projection and recorded admission are not native authentication, comprehension, qualification by themselves, source access or verified authority.",
    }

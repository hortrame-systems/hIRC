"""Deterministic work/recovery projections derived from verified events."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import Any

from .store import IntegrityError, Store


WORK_STATUSES = frozenset({"OPEN", "ACTIVE", "HELD", "COMPLETE", "CANCELLED"})
COMMITMENT_STATUSES = frozenset({"OPEN", "SATISFIED", "RELEASED", "HELD"})
OBSERVED_STATES = frozenset({"UNKNOWN", "REPORTED", "REQUESTED", "SENT", "PROVIDER_ACCEPTED", "OBSERVED", "FAILED"})


class ProjectionError(IntegrityError):
    """An otherwise intact event chain cannot form a coherent work projection."""


@dataclass(slots=True)
class WorkView:
    work_id: str
    title: str
    owner: str
    status: str
    next_action: str
    created_event: str
    status_event: str
    privacy_class: str
    audience: str
    purpose: str
    dependencies: set[str] = field(default_factory=set)
    active_holds: set[str] = field(default_factory=set)
    observations: list[dict[str, Any]] = field(default_factory=list)


@dataclass(slots=True)
class CommitmentView:
    commitment_id: str
    work_id: str
    owner: str
    description: str
    status: str
    source_event: str
    status_event: str
    privacy_class: str
    audience: str
    purpose: str


def _required(payload: dict[str, Any], *keys: str) -> None:
    missing = [key for key in keys if not isinstance(payload.get(key), str) or not payload[key].strip()]
    if missing:
        raise ProjectionError(f"event payload missing required text: {', '.join(missing)}")


def _assert_boundary(row, item, label: str) -> None:
    observed = (row["privacy_class"], row["audience"], row["purpose"])
    expected = (item.privacy_class, item.audience, item.purpose)
    if observed != expected:
        raise ProjectionError(f"information boundary changed for {label}")


def _cycle(work: dict[str, WorkView]) -> list[str] | None:
    visiting: list[str] = []
    complete: set[str] = set()

    def walk(identity: str) -> list[str] | None:
        if identity in visiting:
            start = visiting.index(identity)
            return visiting[start:] + [identity]
        if identity in complete:
            return None
        visiting.append(identity)
        for dependency in sorted(work[identity].dependencies):
            found = walk(dependency)
            if found:
                return found
        visiting.pop()
        complete.add(identity)
        return None

    for identity in sorted(work):
        found = walk(identity)
        if found:
            return found
    return None


def build_briefing(store: Store) -> dict[str, Any]:
    try:
        verification, event_rows = store.verified_snapshot()
    except IntegrityError as error:
        raise ProjectionError("cannot project an invalid event chain") from error

    work: dict[str, WorkView] = {}
    commitments: dict[str, CommitmentView] = {}
    holds: dict[str, dict[str, Any]] = {}
    corrections: list[dict[str, Any]] = []
    ignored: list[dict[str, str]] = []

    for row in event_rows:
        payload = json.loads(row["payload_json"])
        event_type = row["event_type"]
        event_id = row["event_id"]

        if event_type == "work.created":
            _required(payload, "work_id", "title", "owner", "next_action")
            identity = payload["work_id"]
            if identity in work:
                raise ProjectionError(f"duplicate work item: {identity}")
            work[identity] = WorkView(
                work_id=identity,
                title=payload["title"],
                owner=payload["owner"],
                status="OPEN",
                next_action=payload["next_action"],
                created_event=event_id,
                status_event=event_id,
                privacy_class=row["privacy_class"],
                audience=row["audience"],
                purpose=row["purpose"],
            )
        elif event_type == "work.status":
            _required(payload, "work_id", "status", "next_action")
            identity = payload["work_id"]
            if identity not in work:
                raise ProjectionError(f"status references missing work item: {identity}")
            _assert_boundary(row, work[identity], identity)
            if payload["status"] not in WORK_STATUSES:
                raise ProjectionError(f"invalid work status: {payload['status']}")
            work[identity].status = payload["status"]
            work[identity].next_action = payload["next_action"]
            work[identity].status_event = event_id
        elif event_type == "commitment.declared":
            _required(payload, "commitment_id", "work_id", "owner", "description")
            identity = payload["commitment_id"]
            if payload["work_id"] not in work:
                raise ProjectionError(f"commitment references missing work item: {payload['work_id']}")
            _assert_boundary(row, work[payload["work_id"]], payload["work_id"])
            if identity in commitments:
                raise ProjectionError(f"duplicate commitment: {identity}")
            commitments[identity] = CommitmentView(
                commitment_id=identity,
                work_id=payload["work_id"],
                owner=payload["owner"],
                description=payload["description"],
                status="OPEN",
                source_event=event_id,
                status_event=event_id,
                privacy_class=row["privacy_class"],
                audience=row["audience"],
                purpose=row["purpose"],
            )
        elif event_type == "commitment.status":
            _required(payload, "commitment_id", "status")
            identity = payload["commitment_id"]
            if identity not in commitments:
                raise ProjectionError(f"status references missing commitment: {identity}")
            _assert_boundary(row, commitments[identity], identity)
            if payload["status"] not in COMMITMENT_STATUSES:
                raise ProjectionError(f"invalid commitment status: {payload['status']}")
            commitments[identity].status = payload["status"]
            commitments[identity].status_event = event_id
        elif event_type == "dependency.added":
            _required(payload, "work_id", "depends_on")
            identity, dependency = payload["work_id"], payload["depends_on"]
            if identity not in work or dependency not in work:
                raise ProjectionError("dependency references missing work item")
            _assert_boundary(row, work[identity], identity)
            _assert_boundary(row, work[dependency], dependency)
            if identity == dependency:
                raise ProjectionError("work item cannot depend on itself")
            work[identity].dependencies.add(dependency)
        elif event_type == "hold.placed":
            _required(payload, "hold_id", "work_id", "reason", "reopen_when", "allowed_sibling_work")
            identity = payload["hold_id"]
            if payload["work_id"] not in work:
                raise ProjectionError(f"hold references missing work item: {payload['work_id']}")
            _assert_boundary(row, work[payload["work_id"]], payload["work_id"])
            if identity in holds and holds[identity]["state"] == "ACTIVE":
                raise ProjectionError(f"hold already active: {identity}")
            holds[identity] = {
                "hold_id": identity,
                "work_id": payload["work_id"],
                "reason": payload["reason"],
                "reopen_when": payload["reopen_when"],
                "allowed_sibling_work": payload["allowed_sibling_work"],
                "state": "ACTIVE",
                "source_event": event_id,
                "cleared_event": None,
            }
            work[payload["work_id"]].active_holds.add(identity)
        elif event_type == "hold.cleared":
            _required(payload, "hold_id", "resolution")
            identity = payload["hold_id"]
            if identity not in holds or holds[identity]["state"] != "ACTIVE":
                raise ProjectionError(f"clear references inactive hold: {identity}")
            _assert_boundary(row, work[holds[identity]["work_id"]], holds[identity]["work_id"])
            holds[identity]["state"] = "CLEARED"
            holds[identity]["resolution"] = payload["resolution"]
            holds[identity]["cleared_event"] = event_id
            work[holds[identity]["work_id"]].active_holds.remove(identity)
        elif event_type == "observation.recorded":
            _required(payload, "work_id", "claim", "reported_state", "observed_state")
            identity = payload["work_id"]
            if identity not in work:
                raise ProjectionError(f"observation references missing work item: {identity}")
            _assert_boundary(row, work[identity], identity)
            if payload["reported_state"] not in OBSERVED_STATES or payload["observed_state"] not in OBSERVED_STATES:
                raise ProjectionError("invalid reported or observed state")
            work[identity].observations.append(
                {
                    "claim": payload["claim"],
                    "reported_state": payload["reported_state"],
                    "observed_state": payload["observed_state"],
                    "source_event": event_id,
                }
            )
        elif row["category"] == "CORRECTION":
            corrections.append(
                {
                    "event_id": event_id,
                    "correction_of": row["correction_of"],
                    "payload": payload,
                    "information_boundary": {
                        "privacy_class": row["privacy_class"],
                        "audience": row["audience"],
                        "purpose": row["purpose"],
                    },
                }
            )
        else:
            ignored.append({"event_id": event_id, "event_type": event_type})

    cycle = _cycle(work)
    if cycle:
        raise ProjectionError("dependency cycle: " + " -> ".join(cycle))

    blocking_memo: dict[str, set[str]] = {}

    def dependency_blockers(identity: str) -> set[str]:
        if identity in blocking_memo:
            return blocking_memo[identity]
        blocked: set[str] = set()
        for dependency in work[identity].dependencies:
            if work[dependency].active_holds:
                blocked.add(dependency)
            blocked.update(dependency_blockers(dependency))
        blocking_memo[identity] = blocked
        return blocked

    for hold in holds.values():
        sibling = hold["allowed_sibling_work"]
        if sibling not in work:
            raise ProjectionError(f"hold names missing sibling work: {sibling}")
        if sibling == hold["work_id"]:
            raise ProjectionError("held work cannot be its own allowed sibling")
        if work[sibling].active_holds or dependency_blockers(sibling):
            raise ProjectionError(f"allowed sibling is not independently runnable: {sibling}")
        if work[sibling].status not in {"OPEN", "ACTIVE"}:
            raise ProjectionError(f"allowed sibling is not currently runnable: {sibling}")

    work_rows = []
    for identity in sorted(work):
        item = work[identity]
        blocked_by = sorted(dependency_blockers(identity))
        status = "HELD" if item.active_holds else "BLOCKED" if blocked_by else item.status
        work_rows.append(
            {
                "work_id": item.work_id,
                "title": item.title,
                "owner": item.owner,
                "status": status,
                "declared_status": item.status,
                "next_action": item.next_action,
                "dependencies": sorted(item.dependencies),
                "active_holds": sorted(item.active_holds),
                "blocked_by": blocked_by,
                "observations": item.observations,
                "information_boundary": {
                    "privacy_class": item.privacy_class,
                    "audience": item.audience,
                    "purpose": item.purpose,
                },
                "source_events": {"created": item.created_event, "status": item.status_event},
            }
        )
    return {
        "schema": "hirc.return-briefing/1",
        "store_head": verification["head_hash"],
        "event_count": verification["event_count"],
        "work": work_rows,
        "commitments": [
            {
                "commitment_id": item.commitment_id,
                "work_id": item.work_id,
                "owner": item.owner,
                "description": item.description,
                "status": item.status,
                "information_boundary": {
                    "privacy_class": item.privacy_class,
                    "audience": item.audience,
                    "purpose": item.purpose,
                },
                "source_events": {"declared": item.source_event, "status": item.status_event},
            }
            for item in sorted(commitments.values(), key=lambda value: value.commitment_id)
        ],
        "holds": [holds[key] for key in sorted(holds)],
        "corrections": corrections,
        "unprojected_events": ignored,
    }

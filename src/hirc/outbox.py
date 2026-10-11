"""Atomic local outbox journal for fake-adapter results; dispatch stays disabled."""

from __future__ import annotations

import json
from typing import Any

from .adapter import validate_adapter_run
from .canonical import canonical_json, sha256_text
from .store import EventInput, IntegrityError, Store


class OutboxError(IntegrityError):
    """The local outbox history is missing, contradictory or effectful."""


def _outbox_identity(request_id: str, idempotency_key: str) -> str:
    signature = sha256_text(canonical_json({"request_id": request_id, "idempotency_key": idempotency_key}))
    return f"outbox:{signature}"


def _event(
    request: dict[str, Any],
    event_type: str,
    payload: dict[str, Any],
    occurred_at: str,
    authority_ref: str,
    *,
    category: str = "ACTION",
    effect_state: str,
) -> EventInput:
    boundary = request["information_boundary"]
    return EventInput(
        stream_id=f"outbox-stream:{request['request_sha256']}",
        actor_id=request["actor_id"],
        event_type=event_type,
        category=category,
        foundation_version=request["foundation_version"],
        goal_version=request["goal_version"],
        privacy_class=boundary["privacy_class"],
        audience=boundary["audience"],
        purpose=boundary["purpose"],
        occurred_at=occurred_at,
        payload=payload,
        effect_state=effect_state,
        authority_ref=authority_ref if category == "ACTION" else None,
    )


def record_adapter_run(
    store: Store,
    run: dict[str, Any],
    *,
    idempotency_key: str,
    authority_ref: str,
    occurred_at: str,
) -> dict[str, Any]:
    try:
        validate_adapter_run(run)
    except IntegrityError as error:
        raise OutboxError("outbox requires a valid local no-effect adapter run") from error
    request = run.get("request")
    outbox_id = _outbox_identity(request["request_id"], idempotency_key)
    base = {
        "outbox_id": outbox_id,
        "request_id": request["request_id"],
        "external_dispatch_enabled": False,
    }
    enqueue = _event(
        request,
        "outbox.enqueued",
        {**base, "idempotency_key": idempotency_key},
        occurred_at,
        authority_ref,
        effect_state="REQUESTED",
    )
    store.enqueue_outbox(
        enqueue,
        outbox_id=outbox_id,
        request_id=request["request_id"],
        idempotency_key=idempotency_key,
    )
    acceptance = run.get("acceptance")
    if not isinstance(acceptance, dict):
        raise OutboxError("adapter run is missing provider acceptance")
    accepted = _event(
        request,
        "outbox.provider-accepted",
        {**base, "acceptance_id": acceptance.get("acceptance_id")},
        occurred_at,
        authority_ref,
        effect_state="PROVIDER_ACCEPTED",
    )
    store.append_outbox_stage(accepted, outbox_id=outbox_id, stage="PROVIDER_ACCEPTED")
    observation = run.get("observation")
    if observation is None:
        unknown = _event(
            request,
            "outbox.observation-unknown",
            {**base, "reason": run.get("observation_error") or "observation unavailable"},
            occurred_at,
            authority_ref,
            category="EVIDENCE",
            effect_state="NONE",
        )
        store.append_outbox_stage(unknown, outbox_id=outbox_id, stage="UNKNOWN")
    else:
        observed = _event(
            request,
            "outbox.observed",
            {**base, "observation_id": observation.get("observation_id")},
            occurred_at,
            authority_ref,
            effect_state="OBSERVED",
        )
        store.append_outbox_stage(observed, outbox_id=outbox_id, stage="OBSERVED")
    return build_outbox_view(store)


def build_outbox_view(store: Store) -> dict[str, Any]:
    try:
        verification, rows = store.verified_snapshot()
    except IntegrityError as error:
        raise OutboxError("cannot project outbox from invalid store") from error
    items: dict[str, dict[str, Any]] = {}
    for row in rows:
        event_type = row["event_type"]
        if not event_type.startswith("outbox."):
            continue
        payload = json.loads(row["payload_json"])
        if payload.get("external_dispatch_enabled") is not False:
            raise OutboxError("outbox event enables external dispatch")
        identity = payload.get("outbox_id")
        if event_type == "outbox.enqueued":
            if identity in items:
                raise OutboxError(f"duplicate outbox item: {identity}")
            items[identity] = {
                "outbox_id": identity,
                "request_id": payload.get("request_id"),
                "idempotency_key": payload.get("idempotency_key"),
                "reported_state": "REQUESTED",
                "observed_state": "UNKNOWN",
                "external_dispatch_enabled": False,
                "source_events": {"enqueued": row["event_id"], "accepted": None, "terminal": None},
                "information_boundary": {
                    "privacy_class": row["privacy_class"],
                    "audience": row["audience"],
                    "purpose": row["purpose"],
                },
            }
            continue
        if identity not in items:
            raise OutboxError(f"outbox transition references missing item: {identity}")
        item = items[identity]
        boundary = (row["privacy_class"], row["audience"], row["purpose"])
        expected = tuple(item["information_boundary"][key] for key in ("privacy_class", "audience", "purpose"))
        if boundary != expected or payload.get("request_id") != item["request_id"]:
            raise OutboxError("outbox transition changed request or information boundary")
        if event_type == "outbox.provider-accepted":
            if item["reported_state"] != "REQUESTED":
                raise OutboxError("duplicate or out-of-order provider acceptance")
            item["reported_state"] = "PROVIDER_ACCEPTED"
            item["source_events"]["accepted"] = row["event_id"]
        elif event_type == "outbox.observed":
            if item["reported_state"] != "PROVIDER_ACCEPTED" or item["source_events"]["terminal"]:
                raise OutboxError("observed result lacks one provider acceptance")
            item["observed_state"] = "OBSERVED"
            item["source_events"]["terminal"] = row["event_id"]
        elif event_type == "outbox.observation-unknown":
            if item["reported_state"] != "PROVIDER_ACCEPTED" or item["source_events"]["terminal"]:
                raise OutboxError("unknown observation lacks one provider acceptance")
            item["observed_state"] = "UNKNOWN"
            item["observation_error"] = payload.get("reason")
            item["source_events"]["terminal"] = row["event_id"]
        else:
            raise OutboxError(f"unknown outbox transition: {event_type}")
    return {
        "schema": "hirc.outbox-view/1",
        "store_head": verification["head_hash"],
        "event_count": verification["event_count"],
        "items": [items[key] for key in sorted(items)],
        "external_dispatch_enabled": False,
        "nonclaim": "The local outbox records fake-adapter states only; it does not dispatch a network or external effect.",
    }

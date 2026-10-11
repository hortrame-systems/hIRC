"""Keyed external head witness for detecting local store rollback/truncation."""

from __future__ import annotations

import hashlib
import hmac
import json
import os
import tempfile
from pathlib import Path
from typing import Any

from .atomic import AtomicPublishError, publish_new
from .canonical import canonical_json, load_bounded_json_file
from .store import IntegrityError, Store


class WitnessError(IntegrityError):
    """The external head witness is invalid, mismatched or cannot be preserved."""


def _key(value: bytes) -> bytes:
    if not isinstance(value, bytes) or len(value) < 32:
        raise WitnessError("witness key must contain at least 32 bytes")
    return value


def _unsigned(store_path: Path, state: dict[str, Any]) -> dict[str, Any]:
    return {
        "schema": "hirc.head-witness/1",
        "store_name": store_path.name,
        "schema_version": state.get("schema_version", "hirc.local-store/2"),
        "event_count": state["event_count"],
        "head_hash": state["head_hash"],
        "disabled_capabilities_sha256": hashlib.sha256(
            canonical_json(state["disabled_capabilities"]).encode("utf-8")
        ).hexdigest(),
        "algorithm": "HMAC-SHA-256",
        "key_id": "caller-supplied-not-stored",
    }


def create_head_witness(store: Store, output: str | Path, key: bytes) -> dict[str, Any]:
    secret = _key(key)
    destination = Path(output)
    if destination.exists():
        raise WitnessError("head-witness target already exists")
    state = store.status()
    if not state["valid"]:
        raise WitnessError("cannot witness an invalid store")
    unsigned = _unsigned(store.path, state)
    signature = hmac.new(secret, canonical_json(unsigned).encode("utf-8"), hashlib.sha256).hexdigest()
    witness = {**unsigned, "hmac_sha256": signature}
    body = (json.dumps(witness, indent=2, sort_keys=True) + "\n").encode("utf-8")
    destination.parent.mkdir(parents=True, exist_ok=True)
    handle, temporary_name = tempfile.mkstemp(prefix=f".{destination.name}.", suffix=".tmp", dir=destination.parent)
    os.close(handle)
    temporary = Path(temporary_name)
    try:
        temporary.write_bytes(body)
        with temporary.open("r+b") as stream:
            stream.flush(); os.fsync(stream.fileno())
        try:
            publish_new(temporary, destination)
        except AtomicPublishError as error:
            raise WitnessError("head-witness target appeared during publication") from error
    except BaseException:
        try: temporary.unlink()
        except FileNotFoundError: pass
        raise
    return {"path": str(destination.resolve()), "sha256": hashlib.sha256(body).hexdigest(), "bytes": len(body), "event_count": witness["event_count"], "head_hash": witness["head_hash"], "key_stored": False}


def verify_head_witness(store: Store, witness_path: str | Path, key: bytes) -> dict[str, Any]:
    secret = _key(key)
    path = Path(witness_path)
    try:
        witness = load_bounded_json_file(path, max_bytes=65_536, max_depth=16)
    except (OSError, ValueError, json.JSONDecodeError) as error:
        raise WitnessError("head witness is unreadable") from error
    if not isinstance(witness, dict) or "hmac_sha256" not in witness:
        raise WitnessError("head witness shape invalid")
    unsigned = {name: value for name, value in witness.items() if name != "hmac_sha256"}
    expected = hmac.new(secret, canonical_json(unsigned).encode("utf-8"), hashlib.sha256).hexdigest()
    if not hmac.compare_digest(str(witness["hmac_sha256"]), expected):
        raise WitnessError("head witness authentication failed")
    state = store.status()
    if not state["valid"]:
        raise WitnessError("current store is invalid")
    current = _unsigned(store.path, state)
    if current != unsigned:
        raise WitnessError("current store head does not match the external witness")
    return {"schema": "hirc.head-witness-verification/1", "valid": True, "event_count": state["event_count"], "head_hash": state["head_hash"], "key_stored": False, "independent_public_signature": False}

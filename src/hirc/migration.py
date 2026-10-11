"""Explicit verified migration from the pre-outbox v1 local store to v2."""

from __future__ import annotations

import hashlib
import json
import os
import sqlite3
import tempfile
from contextlib import closing
from pathlib import Path
from typing import Any

from .atomic import AtomicPublishError, publish_new
from .canonical import canonical_json, sha256_text, strict_json_loads
from .store import (
    DISABLED_CAPABILITIES,
    EventInput,
    SCHEMA_VERSION,
    ZERO_HASH,
    IntegrityError,
    Store,
    _event_document,
    validate_event,
)


LEGACY_SCHEMA_VERSION = "hirc.local-store/1"
LEGACY_TRIGGER_SQL = {
    "events_no_update": "CREATE TRIGGER events_no_update BEFORE UPDATE ON events BEGIN SELECT RAISE(ABORT, 'hirc events are append-only'); END",
    "events_no_delete": "CREATE TRIGGER events_no_delete BEFORE DELETE ON events BEGIN SELECT RAISE(ABORT, 'hirc events are append-only'); END",
    "capability_no_update": "CREATE TRIGGER capability_no_update BEFORE UPDATE ON capability_state BEGIN SELECT RAISE(ABORT, 'capabilities are immutable in M04-S001'); END",
    "capability_no_delete": "CREATE TRIGGER capability_no_delete BEFORE DELETE ON capability_state BEGIN SELECT RAISE(ABORT, 'capabilities are immutable in M04-S001'); END",
}


class MigrationError(IntegrityError):
    """The predecessor store cannot be migrated without losing its evidence."""


def _normalize_sql(value: str | None) -> str:
    return " ".join((value or "").split())


def _verify_v1(connection: sqlite3.Connection) -> dict[str, Any]:
    connection.row_factory = sqlite3.Row
    if connection.execute("PRAGMA integrity_check").fetchone()[0] != "ok":
        raise MigrationError("legacy SQLite integrity check failed")
    metadata = dict(connection.execute("SELECT key,value FROM meta"))
    if metadata.get("schema_version") != LEGACY_SCHEMA_VERSION:
        raise MigrationError("source is not the exact supported v1 schema")
    if dict(connection.execute("SELECT capability,state FROM capability_state")) != DISABLED_CAPABILITIES:
        raise MigrationError("legacy disabled capability set mismatch")
    triggers = {
        row["name"]: _normalize_sql(row["sql"])
        for row in connection.execute("SELECT name,sql FROM sqlite_master WHERE type='trigger'")
    }
    expected = {name: _normalize_sql(sql) for name, sql in LEGACY_TRIGGER_SQL.items()}
    if triggers != expected:
        raise MigrationError("legacy append-only trigger set mismatch")
    if connection.execute(
        "SELECT count(*) FROM sqlite_master WHERE name IN ('outbox_items','outbox_stages')"
    ).fetchone()[0]:
        raise MigrationError("legacy source already contains unowned outbox tables")
    rows = connection.execute("SELECT * FROM events ORDER BY sequence").fetchall()
    expected_sequence = 1
    expected_prev = ZERO_HASH
    for row in rows:
        if row["sequence"] != expected_sequence or row["prev_hash"] != expected_prev:
            raise MigrationError("legacy event sequence or previous hash mismatch")
        try:
            payload = strict_json_loads(row["payload_json"])
        except (json.JSONDecodeError, ValueError) as error:
            raise MigrationError("legacy event payload is invalid JSON") from error
        if row["payload_json"] != canonical_json(payload):
            raise MigrationError("legacy event payload is not canonical JSON")
        event = EventInput(
            stream_id=row["stream_id"], actor_id=row["actor_id"], event_type=row["event_type"],
            category=row["category"], foundation_version=row["foundation_version"], goal_version=row["goal_version"],
            privacy_class=row["privacy_class"], audience=row["audience"], purpose=row["purpose"],
            occurred_at=row["occurred_at"], payload=payload, effect_state=row["effect_state"],
            authority_ref=row["authority_ref"], correction_of=row["correction_of"],
        )
        try:
            validate_event(event)
        except IntegrityError as error:
            raise MigrationError("legacy event validation failed") from error
        expected_hash = sha256_text(canonical_json(_event_document(row["sequence"], row["prev_hash"], event)))
        if row["event_hash"] != expected_hash or row["event_id"] != f"event:{expected_hash}":
            raise MigrationError("legacy event hash or identity mismatch")
        expected_prev = expected_hash
        expected_sequence += 1
    return {"event_count": len(rows), "head_hash": expected_prev}


def migrate_v1_to_v2(source: str | Path, backup: str | Path) -> dict[str, Any]:
    source_path = Path(source)
    backup_path = Path(backup)
    if not source_path.is_file():
        raise MigrationError("migration source is missing")
    if backup_path.exists():
        raise MigrationError("migration backup target already exists")
    backup_path.parent.mkdir(parents=True, exist_ok=True)
    handle, temporary_name = tempfile.mkstemp(prefix=f".{backup_path.name}.", suffix=".tmp", dir=backup_path.parent)
    os.close(handle)
    temporary = Path(temporary_name)
    try:
        with closing(sqlite3.connect(source_path)) as source_connection, closing(
            sqlite3.connect(temporary)
        ) as backup_connection:
            source_connection.backup(backup_connection)
            backup_connection.commit()
        with closing(sqlite3.connect(temporary)) as backup_check:
            before = _verify_v1(backup_check)
        with temporary.open("r+b") as stream:
            stream.flush()
            os.fsync(stream.fileno())
        backup_body = temporary.read_bytes()
        try:
            publish_new(temporary, backup_path)
        except AtomicPublishError as error:
            raise MigrationError("migration backup target appeared during publication") from error
    except BaseException:
        try:
            temporary.unlink()
        except FileNotFoundError:
            pass
        raise
    with closing(sqlite3.connect(source_path)) as connection:
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA foreign_keys=ON")
        connection.execute("BEGIN IMMEDIATE")
        current = _verify_v1(connection)
        if current != before:
            connection.rollback()
            raise MigrationError("source changed after backup; migration refused and backup preserved")
        connection.execute("UPDATE meta SET value=? WHERE key='schema_version'", (SCHEMA_VERSION,))
        connection.execute("CREATE TABLE outbox_items (idempotency_key TEXT PRIMARY KEY, outbox_id TEXT NOT NULL UNIQUE, request_id TEXT NOT NULL, enqueue_event_id TEXT NOT NULL UNIQUE REFERENCES events(event_id)) WITHOUT ROWID")
        connection.execute("CREATE TABLE outbox_stages (outbox_id TEXT NOT NULL REFERENCES outbox_items(outbox_id), stage TEXT NOT NULL CHECK (stage IN ('ENQUEUED', 'PROVIDER_ACCEPTED', 'OBSERVED', 'UNKNOWN')), event_id TEXT NOT NULL UNIQUE REFERENCES events(event_id), PRIMARY KEY(outbox_id, stage)) WITHOUT ROWID")
        connection.execute("CREATE TRIGGER outbox_items_no_update BEFORE UPDATE ON outbox_items BEGIN SELECT RAISE(ABORT, 'hirc outbox items are append-only'); END")
        connection.execute("CREATE TRIGGER outbox_items_no_delete BEFORE DELETE ON outbox_items BEGIN SELECT RAISE(ABORT, 'hirc outbox items are append-only'); END")
        connection.execute("CREATE TRIGGER outbox_stages_no_update BEFORE UPDATE ON outbox_stages BEGIN SELECT RAISE(ABORT, 'hirc outbox stages are append-only'); END")
        connection.execute("CREATE TRIGGER outbox_stages_no_delete BEFORE DELETE ON outbox_stages BEGIN SELECT RAISE(ABORT, 'hirc outbox stages are append-only'); END")
        connection.commit()
    after = Store(source_path).verify(read_only=True)
    if not after["valid"] or after["event_count"] != before["event_count"] or after["head_hash"] != before["head_hash"]:
        raise MigrationError("migrated store failed v2 verification; preserved backup is available")
    return {
        "schema": "hirc.store-migration/1",
        "from": LEGACY_SCHEMA_VERSION,
        "to": SCHEMA_VERSION,
        "source": str(source_path.resolve()),
        "backup": str(backup_path.resolve()),
        "backup_sha256": hashlib.sha256(backup_body).hexdigest(),
        "backup_bytes": len(backup_body),
        "event_count": after["event_count"],
        "head_hash": after["head_hash"],
        "outbox_items": 0,
        "verified": True,
    }

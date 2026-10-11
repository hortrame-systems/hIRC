"""Dependency-free local append-only hIRC event store."""

from __future__ import annotations

import json
import re
import sqlite3
from contextlib import closing
from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Iterable

from .canonical import bounded_canonical_json, canonical_json, sha256_text, strict_json_loads


SCHEMA_VERSION = "hirc.local-store/2"
ZERO_HASH = "0" * 64
CATEGORIES = frozenset({"EVIDENCE", "INFERENCE", "NORM", "AUTHORITY", "ACTION", "CORRECTION"})
EFFECT_STATES = frozenset({"NONE", "REQUESTED", "SENT", "PROVIDER_ACCEPTED", "OBSERVED", "DECLINED"})
IDENTIFIER = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:/-]{0,255}$")
STRICT_UTC = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?Z$")

DISABLED_CAPABILITIES = {
    "bridge": "DISABLED",
    "network_listeners": "DISABLED",
    "external_effects": "DISABLED",
    "temporary_agents": "DISABLED",
    "debate_scheduler": "DISABLED",
    "competition_runtime": "DISABLED",
    "bayesian_authority_effect": "DISABLED",
    "foundation_self_activation": "DISABLED",
    "arbitrary_extensions": "DISABLED",
}

REQUIRED_TRIGGER_SQL = {
    "events_no_update": "CREATE TRIGGER events_no_update BEFORE UPDATE ON events BEGIN SELECT RAISE(ABORT, 'hirc events are append-only'); END",
    "events_no_delete": "CREATE TRIGGER events_no_delete BEFORE DELETE ON events BEGIN SELECT RAISE(ABORT, 'hirc events are append-only'); END",
    "capability_no_update": "CREATE TRIGGER capability_no_update BEFORE UPDATE ON capability_state BEGIN SELECT RAISE(ABORT, 'capabilities are immutable in M04-S001'); END",
    "capability_no_delete": "CREATE TRIGGER capability_no_delete BEFORE DELETE ON capability_state BEGIN SELECT RAISE(ABORT, 'capabilities are immutable in M04-S001'); END",
    "outbox_items_no_update": "CREATE TRIGGER outbox_items_no_update BEFORE UPDATE ON outbox_items BEGIN SELECT RAISE(ABORT, 'hirc outbox items are append-only'); END",
    "outbox_items_no_delete": "CREATE TRIGGER outbox_items_no_delete BEFORE DELETE ON outbox_items BEGIN SELECT RAISE(ABORT, 'hirc outbox items are append-only'); END",
    "outbox_stages_no_update": "CREATE TRIGGER outbox_stages_no_update BEFORE UPDATE ON outbox_stages BEGIN SELECT RAISE(ABORT, 'hirc outbox stages are append-only'); END",
    "outbox_stages_no_delete": "CREATE TRIGGER outbox_stages_no_delete BEFORE DELETE ON outbox_stages BEGIN SELECT RAISE(ABORT, 'hirc outbox stages are append-only'); END",
}

REQUIRED_SCHEMA_SQL = {
    "meta": "CREATE TABLE meta ( key TEXT PRIMARY KEY, value TEXT NOT NULL ) WITHOUT ROWID",
    "capability_state": "CREATE TABLE capability_state ( capability TEXT PRIMARY KEY, state TEXT NOT NULL CHECK (state = 'DISABLED') ) WITHOUT ROWID",
    "events": "CREATE TABLE events ( sequence INTEGER PRIMARY KEY, event_id TEXT NOT NULL UNIQUE, event_hash TEXT NOT NULL UNIQUE CHECK (length(event_hash) = 64), prev_hash TEXT NOT NULL CHECK (length(prev_hash) = 64), stream_id TEXT NOT NULL, actor_id TEXT NOT NULL, event_type TEXT NOT NULL, category TEXT NOT NULL, foundation_version TEXT NOT NULL, goal_version TEXT NOT NULL, privacy_class TEXT NOT NULL, audience TEXT NOT NULL, purpose TEXT NOT NULL, occurred_at TEXT NOT NULL, effect_state TEXT NOT NULL, authority_ref TEXT, correction_of TEXT, payload_json TEXT NOT NULL )",
    "outbox_items": "CREATE TABLE outbox_items ( idempotency_key TEXT PRIMARY KEY, outbox_id TEXT NOT NULL UNIQUE, request_id TEXT NOT NULL, enqueue_event_id TEXT NOT NULL UNIQUE REFERENCES events(event_id) ) WITHOUT ROWID",
    "outbox_stages": "CREATE TABLE outbox_stages ( outbox_id TEXT NOT NULL REFERENCES outbox_items(outbox_id), stage TEXT NOT NULL CHECK (stage IN ('ENQUEUED', 'PROVIDER_ACCEPTED', 'OBSERVED', 'UNKNOWN')), event_id TEXT NOT NULL UNIQUE REFERENCES events(event_id), PRIMARY KEY(outbox_id, stage) ) WITHOUT ROWID",
    "events_stream_sequence": "CREATE INDEX events_stream_sequence ON events(stream_id, sequence)",
}


class IntegrityError(RuntimeError):
    """The store or proposed event violates a deterministic integrity rule."""


@dataclass(frozen=True, slots=True)
class EventInput:
    stream_id: str
    actor_id: str
    event_type: str
    category: str
    foundation_version: str
    goal_version: str
    privacy_class: str
    audience: str
    purpose: str
    occurred_at: str
    payload: dict[str, Any]
    effect_state: str = "NONE"
    authority_ref: str | None = None
    correction_of: str | None = None


@dataclass(frozen=True, slots=True)
class AppendResult:
    sequence: int
    event_id: str
    event_hash: str
    prev_hash: str


def _require_identifier(name: str, value: str) -> None:
    if not isinstance(value, str) or not IDENTIFIER.fullmatch(value):
        raise IntegrityError(f"{name} must be a bounded identifier")


def _validate_timestamp(value: str) -> None:
    if not isinstance(value, str) or not STRICT_UTC.fullmatch(value):
        raise IntegrityError("occurred_at must be a strict UTC timestamp ending in Z")
    try:
        datetime.fromisoformat(value.removesuffix("Z") + "+00:00")
    except ValueError as error:
        raise IntegrityError("occurred_at is not a valid calendar timestamp") from error


def validate_event(event: EventInput) -> None:
    for name in (
        "stream_id",
        "actor_id",
        "event_type",
        "foundation_version",
        "goal_version",
        "privacy_class",
        "audience",
        "purpose",
    ):
        _require_identifier(name, getattr(event, name))
    if event.category not in CATEGORIES:
        raise IntegrityError(f"category must be one of {sorted(CATEGORIES)}")
    if event.effect_state not in EFFECT_STATES:
        raise IntegrityError(f"effect_state must be one of {sorted(EFFECT_STATES)}")
    if event.authority_ref is not None:
        _require_identifier("authority_ref", event.authority_ref)
    if event.correction_of is not None:
        _require_identifier("correction_of", event.correction_of)
    if event.category == "CORRECTION" and event.correction_of is None:
        raise IntegrityError("a CORRECTION event must identify correction_of")
    if event.category != "CORRECTION" and event.correction_of is not None:
        raise IntegrityError("correction_of is reserved for CORRECTION events")
    if event.effect_state != "NONE" and event.category != "ACTION":
        raise IntegrityError("effect_state is only valid for ACTION events")
    if event.effect_state not in {"NONE", "DECLINED"} and event.authority_ref is None:
        raise IntegrityError("effectful ACTION events require authority_ref")
    if not isinstance(event.payload, dict):
        raise IntegrityError("payload must be a JSON object")
    try:
        bounded_canonical_json(event.payload)
    except (TypeError, ValueError, RecursionError) as error:
        raise IntegrityError("payload is not canonical JSON data") from error
    _validate_timestamp(event.occurred_at)


def _event_document(sequence: int, prev_hash: str, event: EventInput) -> dict[str, Any]:
    document = asdict(event)
    document["sequence"] = sequence
    document["prev_hash"] = prev_hash
    return document


def _event_from_row(row: sqlite3.Row) -> EventInput:
    return EventInput(
        stream_id=row["stream_id"],
        actor_id=row["actor_id"],
        event_type=row["event_type"],
        category=row["category"],
        foundation_version=row["foundation_version"],
        goal_version=row["goal_version"],
        privacy_class=row["privacy_class"],
        audience=row["audience"],
        purpose=row["purpose"],
        occurred_at=row["occurred_at"],
        payload=strict_json_loads(row["payload_json"]),
        effect_state=row["effect_state"],
        authority_ref=row["authority_ref"],
        correction_of=row["correction_of"],
    )


def _normalized_sql(value: str | None) -> str:
    return " ".join((value or "").split())


def _normalized_schema_sql(value: str | None) -> str:
    """Discard formatting whitespace while preserving quoted SQL literals exactly."""
    result: list[str] = []
    quoted = False
    index = 0
    source = value or ""
    while index < len(source):
        character = source[index]
        if character == "'":
            result.append(character)
            if quoted and index + 1 < len(source) and source[index + 1] == "'":
                result.append("'")
                index += 2
                continue
            quoted = not quoted
        elif not quoted and character.isspace():
            index += 1
            continue
        else:
            result.append(character)
        index += 1
    return "".join(result)


class Store:
    def __init__(self, path: str | Path):
        self.path = Path(path)

    def _connect(self, *, read_only: bool = False) -> sqlite3.Connection:
        if read_only:
            locator = self.path.resolve().as_uri() + "?mode=ro"
            connection = sqlite3.connect(locator, uri=True)
        else:
            connection = sqlite3.connect(self.path)
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA foreign_keys = ON")
        if not read_only:
            connection.execute("PRAGMA synchronous = FULL")
        return connection

    def _verify_connection(
        self, connection: sqlite3.Connection
    ) -> tuple[list[str], list[sqlite3.Row], dict[str, str], str]:
        errors: list[str] = []
        integrity = connection.execute("PRAGMA integrity_check").fetchone()[0]
        if integrity != "ok":
            errors.append(f"sqlite integrity: {integrity}")
        metadata = dict(connection.execute("SELECT key, value FROM meta"))
        if metadata.get("schema_version") != SCHEMA_VERSION:
            errors.append("schema version mismatch")
        capabilities = dict(connection.execute("SELECT capability, state FROM capability_state"))
        if capabilities != DISABLED_CAPABILITIES:
            errors.append("disabled capability set mismatch")
        triggers = {
            row["name"]: _normalized_sql(row["sql"])
            for row in connection.execute(
                "SELECT name, sql FROM sqlite_master WHERE type='trigger'"
            )
        }
        expected_triggers = {
            name: _normalized_sql(sql) for name, sql in REQUIRED_TRIGGER_SQL.items()
        }
        if triggers != expected_triggers:
            errors.append("append-only trigger set mismatch")
        schema_objects = {
            row["name"]: _normalized_schema_sql(row["sql"])
            for row in connection.execute(
                "SELECT name, sql FROM sqlite_master "
                "WHERE type IN ('table', 'index') AND name NOT LIKE 'sqlite_%'"
            )
        }
        expected_schema = {
            name: _normalized_schema_sql(sql) for name, sql in REQUIRED_SCHEMA_SQL.items()
        }
        if schema_objects != expected_schema:
            errors.append("store schema object set mismatch")
        rows = connection.execute("SELECT * FROM events ORDER BY sequence").fetchall()

        expected_prev = ZERO_HASH
        expected_sequence = 1
        for row in rows:
            if row["sequence"] != expected_sequence:
                errors.append(f"sequence gap at {expected_sequence}")
            if row["prev_hash"] != expected_prev:
                errors.append(f"previous hash mismatch at {row['sequence']}")
            try:
                payload = strict_json_loads(row["payload_json"])
            except (json.JSONDecodeError, ValueError):
                errors.append(f"invalid payload JSON at {row['sequence']}")
                payload = {}
            try:
                canonical_payload = bounded_canonical_json(payload)
            except (TypeError, ValueError, RecursionError):
                canonical_payload = ""
            if row["payload_json"] != canonical_payload:
                errors.append(f"payload JSON is not canonical at {row['sequence']}")
            event = EventInput(
                stream_id=row["stream_id"],
                actor_id=row["actor_id"],
                event_type=row["event_type"],
                category=row["category"],
                foundation_version=row["foundation_version"],
                goal_version=row["goal_version"],
                privacy_class=row["privacy_class"],
                audience=row["audience"],
                purpose=row["purpose"],
                occurred_at=row["occurred_at"],
                payload=payload,
                effect_state=row["effect_state"],
                authority_ref=row["authority_ref"],
                correction_of=row["correction_of"],
            )
            try:
                validate_event(event)
            except IntegrityError as error:
                errors.append(f"invalid event at {row['sequence']}: {error}")
            expected_hash = sha256_text(
                canonical_json(_event_document(row["sequence"], row["prev_hash"], event))
            )
            if row["event_hash"] != expected_hash:
                errors.append(f"event hash mismatch at {row['sequence']}")
            if row["event_id"] != f"event:{row['event_hash']}":
                errors.append(f"event id mismatch at {row['sequence']}")
            expected_prev = row["event_hash"]
            expected_sequence += 1
        event_rows = {row["event_id"]: row for row in rows}
        for row in rows:
            if row["correction_of"] is None:
                continue
            target = event_rows.get(row["correction_of"])
            if target is None or target["sequence"] >= row["sequence"]:
                errors.append(f"correction target missing or nonprior at {row['sequence']}")
            elif any(
                row[name] != target[name]
                for name in ("privacy_class", "audience", "purpose")
            ):
                errors.append(f"correction boundary mismatch at {row['sequence']}")
        outbox_items = connection.execute(
            "SELECT idempotency_key, outbox_id, request_id, enqueue_event_id FROM outbox_items"
        ).fetchall()
        outbox_stages = connection.execute(
            "SELECT outbox_id, stage, event_id FROM outbox_stages"
        ).fetchall()
        items_by_id = {row["outbox_id"]: row for row in outbox_items}
        stages_by_item: dict[str, dict[str, sqlite3.Row]] = {}
        expected_stage_types = {
            "ENQUEUED": "outbox.enqueued",
            "PROVIDER_ACCEPTED": "outbox.provider-accepted",
            "OBSERVED": "outbox.observed",
            "UNKNOWN": "outbox.observation-unknown",
        }
        for stage in outbox_stages:
            stages_by_item.setdefault(stage["outbox_id"], {})[stage["stage"]] = stage
            event_row = event_rows.get(stage["event_id"])
            item_row = items_by_id.get(stage["outbox_id"])
            if item_row is None:
                errors.append(f"outbox stage references missing item: {stage['outbox_id']}")
            if event_row is None:
                errors.append(f"outbox stage references missing event: {stage['event_id']}")
            elif event_row["event_type"] != expected_stage_types.get(stage["stage"]):
                errors.append(f"outbox stage event type mismatch: {stage['outbox_id']}:{stage['stage']}")
            else:
                try:
                    stage_payload = json.loads(event_row["payload_json"])
                except json.JSONDecodeError:
                    stage_payload = {}
                if (
                    stage_payload.get("outbox_id") != stage["outbox_id"]
                    or stage_payload.get("external_dispatch_enabled") is not False
                    or item_row is not None
                    and stage_payload.get("request_id") != item_row["request_id"]
                ):
                    errors.append(f"outbox stage payload mismatch: {stage['outbox_id']}:{stage['stage']}")
                if item_row is not None:
                    enqueue_row = event_rows.get(item_row["enqueue_event_id"])
                    if enqueue_row is not None and any(
                        event_row[name] != enqueue_row[name]
                        for name in (
                            "stream_id",
                            "actor_id",
                            "foundation_version",
                            "goal_version",
                            "privacy_class",
                            "audience",
                            "purpose",
                        )
                    ):
                        errors.append(f"outbox stage boundary mismatch: {stage['outbox_id']}:{stage['stage']}")
        for item in outbox_items:
            stages = stages_by_item.get(item["outbox_id"], {})
            enqueue = stages.get("ENQUEUED")
            if enqueue is None or enqueue["event_id"] != item["enqueue_event_id"]:
                errors.append(f"outbox enqueue stage mismatch: {item['outbox_id']}")
            event_row = event_rows.get(item["enqueue_event_id"])
            if event_row is None:
                errors.append(f"outbox item references missing enqueue event: {item['outbox_id']}")
                continue
            try:
                payload = json.loads(event_row["payload_json"])
            except json.JSONDecodeError:
                continue
            if (
                payload.get("outbox_id") != item["outbox_id"]
                or payload.get("request_id") != item["request_id"]
                or payload.get("idempotency_key") != item["idempotency_key"]
                or payload.get("external_dispatch_enabled") is not False
            ):
                errors.append(f"outbox item payload mismatch: {item['outbox_id']}")
            if "OBSERVED" in stages and "UNKNOWN" in stages:
                errors.append(f"outbox has contradictory terminal observation states: {item['outbox_id']}")
        return errors, rows, capabilities, expected_prev

    def initialize(self, *, sensitive: bool = False) -> None:
        if sensitive:
            raise IntegrityError(
                "sensitive mode requires an admitted encrypted live-store backend; plaintext fallback is forbidden"
            )
        if self.path.is_file() and self.path.stat().st_size:
            try:
                existing = self.verify()
            except sqlite3.Error as error:
                raise IntegrityError("existing store schema is unreadable") from error
            if not existing["valid"]:
                raise IntegrityError(
                    "existing store integrity failure: " + "; ".join(existing["errors"])
                )
            return
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with closing(self._connect()) as connection, connection:
            connection.executescript(
                """
                PRAGMA journal_mode = WAL;
                CREATE TABLE IF NOT EXISTS meta (
                    key TEXT PRIMARY KEY,
                    value TEXT NOT NULL
                ) WITHOUT ROWID;
                CREATE TABLE IF NOT EXISTS capability_state (
                    capability TEXT PRIMARY KEY,
                    state TEXT NOT NULL CHECK (state = 'DISABLED')
                ) WITHOUT ROWID;
                CREATE TABLE IF NOT EXISTS events (
                    sequence INTEGER PRIMARY KEY,
                    event_id TEXT NOT NULL UNIQUE,
                    event_hash TEXT NOT NULL UNIQUE CHECK (length(event_hash) = 64),
                    prev_hash TEXT NOT NULL CHECK (length(prev_hash) = 64),
                    stream_id TEXT NOT NULL,
                    actor_id TEXT NOT NULL,
                    event_type TEXT NOT NULL,
                    category TEXT NOT NULL,
                    foundation_version TEXT NOT NULL,
                    goal_version TEXT NOT NULL,
                    privacy_class TEXT NOT NULL,
                    audience TEXT NOT NULL,
                    purpose TEXT NOT NULL,
                    occurred_at TEXT NOT NULL,
                    effect_state TEXT NOT NULL,
                    authority_ref TEXT,
                    correction_of TEXT,
                    payload_json TEXT NOT NULL
                );
                CREATE INDEX IF NOT EXISTS events_stream_sequence
                    ON events(stream_id, sequence);
                CREATE TABLE IF NOT EXISTS outbox_items (
                    idempotency_key TEXT PRIMARY KEY,
                    outbox_id TEXT NOT NULL UNIQUE,
                    request_id TEXT NOT NULL,
                    enqueue_event_id TEXT NOT NULL UNIQUE REFERENCES events(event_id)
                ) WITHOUT ROWID;
                CREATE TABLE IF NOT EXISTS outbox_stages (
                    outbox_id TEXT NOT NULL REFERENCES outbox_items(outbox_id),
                    stage TEXT NOT NULL CHECK (stage IN ('ENQUEUED', 'PROVIDER_ACCEPTED', 'OBSERVED', 'UNKNOWN')),
                    event_id TEXT NOT NULL UNIQUE REFERENCES events(event_id),
                    PRIMARY KEY(outbox_id, stage)
                ) WITHOUT ROWID;
                CREATE TRIGGER IF NOT EXISTS events_no_update
                    BEFORE UPDATE ON events
                    BEGIN SELECT RAISE(ABORT, 'hirc events are append-only'); END;
                CREATE TRIGGER IF NOT EXISTS events_no_delete
                    BEFORE DELETE ON events
                    BEGIN SELECT RAISE(ABORT, 'hirc events are append-only'); END;
                CREATE TRIGGER IF NOT EXISTS capability_no_update
                    BEFORE UPDATE ON capability_state
                    BEGIN SELECT RAISE(ABORT, 'capabilities are immutable in M04-S001'); END;
                CREATE TRIGGER IF NOT EXISTS capability_no_delete
                    BEFORE DELETE ON capability_state
                    BEGIN SELECT RAISE(ABORT, 'capabilities are immutable in M04-S001'); END;
                CREATE TRIGGER IF NOT EXISTS outbox_items_no_update
                    BEFORE UPDATE ON outbox_items
                    BEGIN SELECT RAISE(ABORT, 'hirc outbox items are append-only'); END;
                CREATE TRIGGER IF NOT EXISTS outbox_items_no_delete
                    BEFORE DELETE ON outbox_items
                    BEGIN SELECT RAISE(ABORT, 'hirc outbox items are append-only'); END;
                CREATE TRIGGER IF NOT EXISTS outbox_stages_no_update
                    BEFORE UPDATE ON outbox_stages
                    BEGIN SELECT RAISE(ABORT, 'hirc outbox stages are append-only'); END;
                CREATE TRIGGER IF NOT EXISTS outbox_stages_no_delete
                    BEFORE DELETE ON outbox_stages
                    BEGIN SELECT RAISE(ABORT, 'hirc outbox stages are append-only'); END;
                """
            )
            connection.execute(
                "INSERT OR IGNORE INTO meta(key, value) VALUES('schema_version', ?)",
                (SCHEMA_VERSION,),
            )
            for capability, state in sorted(DISABLED_CAPABILITIES.items()):
                connection.execute(
                    "INSERT OR IGNORE INTO capability_state(capability, state) VALUES(?, ?)",
                    (capability, state),
                )
        verification = self.verify()
        if not verification["valid"]:
            raise IntegrityError("initialized store did not pass verification")

    def append(self, event: EventInput) -> AppendResult:
        with closing(self._connect()) as connection, connection:
            connection.execute("BEGIN IMMEDIATE")
            self._require_valid_connection(connection)
            result = self._append_on_connection(connection, event)
        return result

    def _require_valid_connection(self, connection: sqlite3.Connection) -> None:
        existing_errors, _, _, _ = self._verify_connection(connection)
        if existing_errors:
            raise IntegrityError("existing store integrity failure: " + "; ".join(existing_errors))
        metadata = connection.execute("SELECT value FROM meta WHERE key='schema_version'").fetchone()
        if metadata is None or metadata["value"] != SCHEMA_VERSION:
            raise IntegrityError("store is missing the selected schema version")

    def _append_on_connection(self, connection: sqlite3.Connection, event: EventInput) -> AppendResult:
        validate_event(event)
        payload_json = bounded_canonical_json(event.payload)
        tail = connection.execute(
            "SELECT sequence, event_hash FROM events ORDER BY sequence DESC LIMIT 1"
        ).fetchone()
        if event.correction_of is not None:
            target = connection.execute(
                "SELECT privacy_class, audience, purpose FROM events WHERE event_id=?",
                (event.correction_of,),
            ).fetchone()
            if target is None:
                raise IntegrityError("correction_of does not identify an existing event")
            target_boundary = (target["privacy_class"], target["audience"], target["purpose"])
            correction_boundary = (event.privacy_class, event.audience, event.purpose)
            if correction_boundary != target_boundary:
                raise IntegrityError("correction must preserve the target information boundary")
        sequence = 1 if tail is None else int(tail["sequence"]) + 1
        prev_hash = ZERO_HASH if tail is None else str(tail["event_hash"])
        document = _event_document(sequence, prev_hash, event)
        event_hash = sha256_text(canonical_json(document))
        event_id = f"event:{event_hash}"
        connection.execute(
            """
            INSERT INTO events(
                sequence, event_id, event_hash, prev_hash, stream_id,
                actor_id, event_type, category, foundation_version,
                goal_version, privacy_class, audience, purpose, occurred_at,
                effect_state, authority_ref, correction_of, payload_json
            ) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                sequence,
                event_id,
                event_hash,
                prev_hash,
                event.stream_id,
                event.actor_id,
                event.event_type,
                event.category,
                event.foundation_version,
                event.goal_version,
                event.privacy_class,
                event.audience,
                event.purpose,
                event.occurred_at,
                event.effect_state,
                event.authority_ref,
                event.correction_of,
                payload_json,
            ),
        )
        return AppendResult(sequence, event_id, event_hash, prev_hash)

    @staticmethod
    def _result_from_row(row: sqlite3.Row) -> AppendResult:
        return AppendResult(row["sequence"], row["event_id"], row["event_hash"], row["prev_hash"])

    def enqueue_outbox(
        self,
        event: EventInput,
        *,
        outbox_id: str,
        request_id: str,
        idempotency_key: str,
    ) -> AppendResult:
        for name, value in (("outbox_id", outbox_id), ("request_id", request_id), ("idempotency_key", idempotency_key)):
            _require_identifier(name, value)
        expected_payload = {
            "outbox_id": outbox_id,
            "request_id": request_id,
            "idempotency_key": idempotency_key,
            "external_dispatch_enabled": False,
        }
        if (
            event.event_type != "outbox.enqueued"
            or event.category != "ACTION"
            or event.effect_state != "REQUESTED"
            or event.payload != expected_payload
        ):
            raise IntegrityError("outbox enqueue event does not match the atomic contract")
        with closing(self._connect()) as connection, connection:
            connection.execute("BEGIN IMMEDIATE")
            self._require_valid_connection(connection)
            existing = connection.execute(
                """
                SELECT e.* FROM outbox_items i
                JOIN events e ON e.event_id=i.enqueue_event_id
                WHERE i.idempotency_key=?
                """,
                (idempotency_key,),
            ).fetchone()
            if existing is not None:
                item = connection.execute(
                    "SELECT outbox_id, request_id FROM outbox_items WHERE idempotency_key=?",
                    (idempotency_key,),
                ).fetchone()
                if item["outbox_id"] != outbox_id or item["request_id"] != request_id or _event_from_row(existing) != event:
                    raise IntegrityError("idempotency key collision with different outbox request")
                return self._result_from_row(existing)
            if connection.execute("SELECT 1 FROM outbox_items WHERE outbox_id=?", (outbox_id,)).fetchone():
                raise IntegrityError("outbox_id already belongs to another idempotency key")
            result = self._append_on_connection(connection, event)
            connection.execute(
                "INSERT INTO outbox_items(idempotency_key,outbox_id,request_id,enqueue_event_id) VALUES(?,?,?,?)",
                (idempotency_key, outbox_id, request_id, result.event_id),
            )
            connection.execute(
                "INSERT INTO outbox_stages(outbox_id,stage,event_id) VALUES(?,?,?)",
                (outbox_id, "ENQUEUED", result.event_id),
            )
        return result

    def append_outbox_stage(self, event: EventInput, *, outbox_id: str, stage: str) -> AppendResult:
        _require_identifier("outbox_id", outbox_id)
        expected = {
            "PROVIDER_ACCEPTED": ("outbox.provider-accepted", "ACTION", "PROVIDER_ACCEPTED"),
            "OBSERVED": ("outbox.observed", "ACTION", "OBSERVED"),
            "UNKNOWN": ("outbox.observation-unknown", "EVIDENCE", "NONE"),
        }
        if stage not in expected or (event.event_type, event.category, event.effect_state) != expected[stage]:
            raise IntegrityError("outbox stage event does not match the declared stage")
        if event.payload.get("outbox_id") != outbox_id or event.payload.get("external_dispatch_enabled") is not False:
            raise IntegrityError("outbox stage payload mismatch")
        with closing(self._connect()) as connection, connection:
            connection.execute("BEGIN IMMEDIATE")
            self._require_valid_connection(connection)
            item = connection.execute(
                "SELECT request_id, enqueue_event_id FROM outbox_items WHERE outbox_id=?",
                (outbox_id,),
            ).fetchone()
            if item is None:
                raise IntegrityError("outbox stage references missing item")
            enqueue = connection.execute(
                "SELECT stream_id, actor_id, foundation_version, goal_version, privacy_class, audience, purpose "
                "FROM events WHERE event_id=?",
                (item["enqueue_event_id"],),
            ).fetchone()
            if event.payload.get("request_id") != item["request_id"]:
                raise IntegrityError("outbox stage request_id mismatch")
            if enqueue is None or any(
                getattr(event, name) != enqueue[name]
                for name in (
                    "stream_id", "actor_id", "foundation_version", "goal_version",
                    "privacy_class", "audience", "purpose",
                )
            ):
                raise IntegrityError("outbox stage information boundary mismatch")
            existing = connection.execute(
                """
                SELECT e.* FROM outbox_stages s JOIN events e ON e.event_id=s.event_id
                WHERE s.outbox_id=? AND s.stage=?
                """,
                (outbox_id, stage),
            ).fetchone()
            if existing is not None:
                if _event_from_row(existing) != event:
                    raise IntegrityError("outbox stage already exists with different evidence")
                return self._result_from_row(existing)
            stages = {
                row["stage"]
                for row in connection.execute("SELECT stage FROM outbox_stages WHERE outbox_id=?", (outbox_id,))
            }
            if "ENQUEUED" not in stages or stage in {"OBSERVED", "UNKNOWN"} and "PROVIDER_ACCEPTED" not in stages:
                raise IntegrityError("outbox stage prerequisite missing")
            if stage in {"OBSERVED", "UNKNOWN"} and ({"OBSERVED", "UNKNOWN"} & stages):
                raise IntegrityError("outbox terminal observation state already recorded")
            result = self._append_on_connection(connection, event)
            connection.execute(
                "INSERT INTO outbox_stages(outbox_id,stage,event_id) VALUES(?,?,?)",
                (outbox_id, stage, result.event_id),
            )
        return result

    def iter_events(self) -> Iterable[sqlite3.Row]:
        with closing(self._connect(read_only=True)) as connection, connection:
            rows = connection.execute("SELECT * FROM events ORDER BY sequence").fetchall()
        return rows

    def verified_snapshot(self) -> tuple[dict[str, Any], list[dict[str, Any]]]:
        """Return verification and its exact event rows from one read transaction."""
        if not self.path.is_file():
            raise IntegrityError("store missing")
        with closing(self._connect(read_only=True)) as connection:
            connection.execute("BEGIN")
            errors, rows, capabilities, expected_prev = self._verify_connection(connection)
            result = {
                "valid": not errors,
                "event_count": len(rows),
                "head_hash": expected_prev,
                "disabled_capabilities": capabilities,
                "errors": errors,
            }
            materialized = [dict(row) for row in rows]
            connection.rollback()
        if errors:
            raise IntegrityError("store integrity failure: " + "; ".join(errors))
        return result, materialized

    def verify(self, *, read_only: bool = True) -> dict[str, Any]:
        if not self.path.is_file():
            return {"valid": False, "event_count": 0, "head_hash": ZERO_HASH, "errors": ["store missing"]}
        with closing(self._connect(read_only=read_only)) as connection, connection:
            errors, rows, capabilities, expected_prev = self._verify_connection(connection)
        return {
            "valid": not errors,
            "event_count": len(rows),
            "head_hash": expected_prev,
            "disabled_capabilities": capabilities,
            "errors": errors,
        }

    def status(self) -> dict[str, Any]:
        result = self.verify()
        result["path"] = str(self.path.resolve())
        result["schema_version"] = SCHEMA_VERSION
        result["encrypted_at_rest"] = False
        result["sensitive_data_release_allowed"] = False
        return result

"""Command-line surface for the M04-S001 local integrity core."""

from __future__ import annotations

import argparse
import json
import sqlite3
import sys
from datetime import datetime, timezone
from pathlib import Path

from .canonical import canonical_json, load_bounded_json_file, strict_json_loads
from .adapter import AcceptanceOnlyAdapter, DeterministicEchoAdapter, build_adapter_request, run_local_adapter
from .decision import build_decision_preview, write_decision_preview
from .formation import build_formation_view
from .outbox import build_outbox_view, record_adapter_run
from .recovery import backup_store, restore_store
from .migration import migrate_v1_to_v2
from .witness import create_head_witness, verify_head_witness
from .projection import ProjectionError, build_briefing
from .store import EventInput, IntegrityError, Store
from .ui import write_snapshot


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="hirc")
    parser.add_argument("--db", default=".hirc/hirc.sqlite3", help="local SQLite store")
    commands = parser.add_subparsers(dest="command", required=True)
    init = commands.add_parser("init", help="initialize a local disabled-by-default store")
    init.add_argument("--sensitive", action="store_true", help="require an admitted encrypted live-store backend")
    commands.add_parser("status", help="show local integrity and capability state")
    commands.add_parser("verify", help="verify the complete append-only chain")
    commands.add_parser("briefing", help="derive the current work and recovery briefing")
    commands.add_parser("formation", help="derive permanent-participant formation state")
    commands.add_parser("outbox", help="derive the local no-dispatch outbox state")
    snapshot = commands.add_parser("ui-snapshot", help="write a read-only local HTML briefing")
    snapshot.add_argument("--output", default=".hirc/briefing.html")
    snapshot.add_argument("--decision", action="append", default=[], help="local decision-preview JSON file")
    decision = commands.add_parser("decision-preview", help="build a canonical local no-effect decision preview")
    decision.add_argument("--input", required=True, help="local proposal JSON file")
    decision.add_argument("--output", help="optional local preview JSON file")
    adapter = commands.add_parser("adapter-run", help="run the deterministic local fake adapter")
    adapter.add_argument("--input", required=True, help="local adapter-request proposal JSON file")
    adapter.add_argument("--acceptance-only", action="store_true", help="simulate acceptance without an observation")
    outbox_record = commands.add_parser("outbox-record", help="record a local fake-adapter run atomically")
    outbox_record.add_argument("--input", required=True, help="local adapter-request proposal JSON file")
    outbox_record.add_argument("--idempotency-key", required=True)
    outbox_record.add_argument("--authority-ref", required=True)
    outbox_record.add_argument("--occurred-at", required=True)
    outbox_record.add_argument("--acceptance-only", action="store_true")
    backup = commands.add_parser("backup", help="write a verified atomic local backup")
    backup.add_argument("--output", required=True)
    restore = commands.add_parser("restore", help="restore a verified backup to a new local store")
    restore.add_argument("--input", required=True)
    restore.add_argument("--output", required=True)
    migrate = commands.add_parser("migrate-v1", help="migrate an exact verified v1 store to v2")
    migrate.add_argument("--backup", required=True, help="new immutable predecessor backup path")
    witness_create = commands.add_parser("witness-create", help="write a keyed external store-head witness")
    witness_create.add_argument("--output", required=True)
    witness_create.add_argument("--key-stdin", action="store_true", required=True)
    witness_verify = commands.add_parser("witness-verify", help="verify the store against a keyed external witness")
    witness_verify.add_argument("--input", required=True)
    witness_verify.add_argument("--key-stdin", action="store_true", required=True)
    record = commands.add_parser("record", help="append one canonical local event")
    record.add_argument("--stream", required=True)
    record.add_argument("--actor", required=True)
    record.add_argument("--type", required=True, dest="event_type")
    record.add_argument("--category", required=True)
    record.add_argument("--foundation", required=True)
    record.add_argument("--goal", required=True)
    record.add_argument("--privacy", required=True)
    record.add_argument("--audience", required=True)
    record.add_argument("--purpose", required=True)
    record.add_argument("--occurred-at")
    record.add_argument("--effect-state", default="NONE")
    record.add_argument("--authority-ref")
    record.add_argument("--correction-of")
    record.add_argument("--payload-json", required=True)
    return parser


def _print(value: object) -> None:
    print(json.dumps(value, indent=2, ensure_ascii=False, sort_keys=True))


def main(argv: list[str] | None = None) -> int:
    arguments = _parser().parse_args(argv)
    store = Store(Path(arguments.db))
    try:
        if arguments.command in {"witness-create", "witness-verify"}:
            key = sys.stdin.buffer.readline().rstrip(b"\r\n")
            if arguments.command == "witness-create":
                _print(create_head_witness(store, arguments.output, key))
            else:
                _print(verify_head_witness(store, arguments.input, key))
            return 0
        if arguments.command == "restore":
            _print(restore_store(arguments.input, arguments.output))
            return 0
        if arguments.command == "migrate-v1":
            _print(migrate_v1_to_v2(store.path, arguments.backup))
            return 0
        if arguments.command == "decision-preview":
            proposal = load_bounded_json_file(arguments.input)
            result = build_decision_preview(proposal)
            if arguments.output:
                write_decision_preview(result, arguments.output)
            _print(result)
            return 0
        if arguments.command == "adapter-run":
            proposal = load_bounded_json_file(arguments.input)
            request = build_adapter_request(proposal)
            adapter = AcceptanceOnlyAdapter() if arguments.acceptance_only else DeterministicEchoAdapter()
            _print(run_local_adapter(adapter, request))
            return 0
        if arguments.command == "outbox-record":
            proposal = load_bounded_json_file(arguments.input)
            request = build_adapter_request(proposal)
            adapter = AcceptanceOnlyAdapter() if arguments.acceptance_only else DeterministicEchoAdapter()
            run = run_local_adapter(adapter, request)
            _print(record_adapter_run(store, run, idempotency_key=arguments.idempotency_key, authority_ref=arguments.authority_ref, occurred_at=arguments.occurred_at))
            return 0
        if arguments.command == "backup":
            _print(backup_store(store.path, arguments.output))
            return 0
        if arguments.command == "init":
            store.initialize(sensitive=arguments.sensitive)
            _print(store.status())
            return 0
        if arguments.command in {"status", "verify"}:
            result = store.status() if arguments.command == "status" else store.verify()
            _print(result)
            return 0 if result["valid"] else 2
        if arguments.command == "briefing":
            _print(build_briefing(store))
            return 0
        if arguments.command == "formation":
            _print(build_formation_view(store))
            return 0
        if arguments.command == "outbox":
            _print(build_outbox_view(store))
            return 0
        if arguments.command == "ui-snapshot":
            previews = [load_bounded_json_file(path) for path in arguments.decision]
            _print(write_snapshot(build_briefing(store), arguments.output, previews))
            return 0
        payload = strict_json_loads(arguments.payload_json)
        if not isinstance(payload, dict):
            raise IntegrityError("payload-json must decode to an object")
        occurred_at = arguments.occurred_at or datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
        result = store.append(
            EventInput(
                stream_id=arguments.stream,
                actor_id=arguments.actor,
                event_type=arguments.event_type,
                category=arguments.category,
                foundation_version=arguments.foundation,
                goal_version=arguments.goal,
                privacy_class=arguments.privacy,
                audience=arguments.audience,
                purpose=arguments.purpose,
                occurred_at=occurred_at,
                payload=payload,
                effect_state=arguments.effect_state,
                authority_ref=arguments.authority_ref,
                correction_of=arguments.correction_of,
            )
        )
        _print({**result.__dict__} if hasattr(result, "__dict__") else {
            "sequence": result.sequence,
            "event_id": result.event_id,
            "event_hash": result.event_hash,
            "prev_hash": result.prev_hash,
        })
        return 0
    except (IntegrityError, ProjectionError, ValueError, json.JSONDecodeError, sqlite3.Error, OSError) as error:
        print(canonical_json({"error": str(error), "state": "HELD"}), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())

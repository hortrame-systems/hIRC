from __future__ import annotations

import json
import io
import random
import sqlite3
import tempfile
import unittest
from dataclasses import asdict, replace
from pathlib import Path
from contextlib import closing, redirect_stdout
from unittest.mock import patch

import hirc.atomic as atomic
from hirc.canonical import canonical_json, sha256_text
from hirc.migration import MigrationError, migrate_v1_to_v2
from hirc.store import DISABLED_CAPABILITIES, EventInput, IntegrityError, Store, ZERO_HASH, _event_document, validate_event
from hirc.cli import main


LEGACY_SQL = """
CREATE TABLE meta(key TEXT PRIMARY KEY,value TEXT NOT NULL) WITHOUT ROWID;
CREATE TABLE capability_state(capability TEXT PRIMARY KEY,state TEXT NOT NULL CHECK(state='DISABLED')) WITHOUT ROWID;
CREATE TABLE events(sequence INTEGER PRIMARY KEY,event_id TEXT NOT NULL UNIQUE,event_hash TEXT NOT NULL UNIQUE CHECK(length(event_hash)=64),prev_hash TEXT NOT NULL CHECK(length(prev_hash)=64),stream_id TEXT NOT NULL,actor_id TEXT NOT NULL,event_type TEXT NOT NULL,category TEXT NOT NULL,foundation_version TEXT NOT NULL,goal_version TEXT NOT NULL,privacy_class TEXT NOT NULL,audience TEXT NOT NULL,purpose TEXT NOT NULL,occurred_at TEXT NOT NULL,effect_state TEXT NOT NULL,authority_ref TEXT,correction_of TEXT,payload_json TEXT NOT NULL);
CREATE INDEX events_stream_sequence ON events(stream_id,sequence);
CREATE TRIGGER events_no_update BEFORE UPDATE ON events BEGIN SELECT RAISE(ABORT, 'hirc events are append-only'); END;
CREATE TRIGGER events_no_delete BEFORE DELETE ON events BEGIN SELECT RAISE(ABORT, 'hirc events are append-only'); END;
CREATE TRIGGER capability_no_update BEFORE UPDATE ON capability_state BEGIN SELECT RAISE(ABORT, 'capabilities are immutable in M04-S001'); END;
CREATE TRIGGER capability_no_delete BEFORE DELETE ON capability_state BEGIN SELECT RAISE(ABORT, 'capabilities are immutable in M04-S001'); END;
"""


def sample_event() -> EventInput:
    return EventInput(stream_id="work:legacy", actor_id="actor:legacy", event_type="note.recorded", category="EVIDENCE", foundation_version="foundation:1", goal_version="goal:1", privacy_class="privacy:owner", audience="audience:owner", purpose="purpose:migration", occurred_at="2026-10-10T00:00:00Z", payload={"note": "legacy"})


def legacy(path: Path, with_event: bool = True) -> None:
    connection = sqlite3.connect(path)
    connection.executescript(LEGACY_SQL)
    connection.execute("INSERT INTO meta VALUES('schema_version','hirc.local-store/1')")
    connection.executemany("INSERT INTO capability_state VALUES(?,?)", sorted(DISABLED_CAPABILITIES.items()))
    if with_event:
        event = sample_event()
        document = _event_document(1, ZERO_HASH, event)
        event_hash = sha256_text(canonical_json(document))
        connection.execute("INSERT INTO events VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", (1, f"event:{event_hash}", event_hash, ZERO_HASH, event.stream_id, event.actor_id, event.event_type, event.category, event.foundation_version, event.goal_version, event.privacy_class, event.audience, event.purpose, event.occurred_at, event.effect_state, event.authority_ref, event.correction_of, canonical_json(event.payload)))
    connection.commit()
    connection.close()


class MigrationHardeningTests(unittest.TestCase):
    temporary_root = Path(__file__).parent / ".tmp"

    @classmethod
    def setUpClass(cls) -> None:
        cls.temporary_root.mkdir(parents=True, exist_ok=True)

    def test_valid_v1_event_chain_migrates_with_backup(self) -> None:
        with tempfile.TemporaryDirectory(dir=self.temporary_root) as directory:
            source, backup = Path(directory) / "v1.sqlite3", Path(directory) / "v1.backup.sqlite3"
            legacy(source)
            result = migrate_v1_to_v2(source, backup)
            self.assertTrue(result["verified"])
            self.assertTrue(backup.is_file())
            self.assertEqual(Store(source).verify()["event_count"], 1)

    def test_empty_v1_migrates(self) -> None:
        with tempfile.TemporaryDirectory(dir=self.temporary_root) as directory:
            source, backup = Path(directory) / "v1.sqlite3", Path(directory) / "backup.sqlite3"
            legacy(source, with_event=False)
            self.assertEqual(migrate_v1_to_v2(source, backup)["event_count"], 0)

    def test_corrupt_chain_refuses_without_schema_change(self) -> None:
        with tempfile.TemporaryDirectory(dir=self.temporary_root) as directory:
            source, backup = Path(directory) / "v1.sqlite3", Path(directory) / "backup.sqlite3"
            legacy(source)
            connection = sqlite3.connect(source)
            connection.execute("DROP TRIGGER events_no_update")
            connection.execute("UPDATE events SET purpose='purpose:tampered'")
            connection.execute("CREATE TRIGGER events_no_update BEFORE UPDATE ON events BEGIN SELECT RAISE(ABORT, 'hirc events are append-only'); END")
            connection.commit(); connection.close()
            with self.assertRaises(MigrationError): migrate_v1_to_v2(source, backup)
            self.assertFalse(backup.exists())
            connection = sqlite3.connect(source)
            self.assertEqual(connection.execute("SELECT value FROM meta WHERE key='schema_version'").fetchone()[0], "hirc.local-store/1")
            connection.close()

    def test_duplicate_key_legacy_payload_refuses_without_schema_change(self) -> None:
        with tempfile.TemporaryDirectory(dir=self.temporary_root) as directory:
            source, backup = Path(directory) / "v1.sqlite3", Path(directory) / "backup.sqlite3"
            legacy(source)
            with closing(sqlite3.connect(source)) as connection, connection:
                connection.execute("DROP TRIGGER events_no_update")
                connection.execute(
                    "UPDATE events SET payload_json=? WHERE sequence=1",
                    ('{"note":"forged","note":"legacy"}',),
                )
                connection.execute(
                    "CREATE TRIGGER events_no_update BEFORE UPDATE ON events "
                    "BEGIN SELECT RAISE(ABORT, 'hirc events are append-only'); END"
                )
            with self.assertRaises(MigrationError):
                migrate_v1_to_v2(source, backup)
            self.assertFalse(backup.exists())
            with closing(sqlite3.connect(source)) as connection:
                self.assertEqual(
                    connection.execute("SELECT value FROM meta WHERE key='schema_version'").fetchone()[0],
                    "hirc.local-store/1",
                )

    def test_missing_legacy_trigger_refuses(self) -> None:
        with tempfile.TemporaryDirectory(dir=self.temporary_root) as directory:
            source, backup = Path(directory) / "v1.sqlite3", Path(directory) / "backup.sqlite3"
            legacy(source)
            connection = sqlite3.connect(source); connection.execute("DROP TRIGGER events_no_delete"); connection.commit(); connection.close()
            with self.assertRaises(MigrationError): migrate_v1_to_v2(source, backup)

    def test_existing_backup_target_refuses(self) -> None:
        with tempfile.TemporaryDirectory(dir=self.temporary_root) as directory:
            source, backup = Path(directory) / "v1.sqlite3", Path(directory) / "backup.sqlite3"
            legacy(source); backup.write_bytes(b"keep")
            with self.assertRaises(MigrationError): migrate_v1_to_v2(source, backup)
            self.assertEqual(backup.read_bytes(), b"keep")

    def test_concurrent_backup_target_creation_is_never_overwritten(self) -> None:
        with tempfile.TemporaryDirectory(dir=self.temporary_root) as directory:
            source, backup = Path(directory) / "v1.sqlite3", Path(directory) / "backup.sqlite3"
            legacy(source)
            original_publish = atomic._publish_new_name
            def create_racer_then_publish(temporary: Path, destination: Path) -> None:
                Path(destination).write_bytes(b"concurrent-writer")
                original_publish(temporary, destination)
            with patch("hirc.atomic._publish_new_name", side_effect=create_racer_then_publish):
                with self.assertRaises(MigrationError): migrate_v1_to_v2(source, backup)
            self.assertEqual(backup.read_bytes(), b"concurrent-writer")
            with closing(sqlite3.connect(source)) as connection:
                self.assertEqual(
                    connection.execute("SELECT value FROM meta WHERE key='schema_version'").fetchone()[0],
                    "hirc.local-store/1",
                )

    def test_v2_source_is_not_silently_remigrated(self) -> None:
        with tempfile.TemporaryDirectory(dir=self.temporary_root) as directory:
            source, backup = Path(directory) / "v2.sqlite3", Path(directory) / "backup.sqlite3"
            Store(source).initialize()
            with self.assertRaises(MigrationError): migrate_v1_to_v2(source, backup)

    def test_seeded_invalid_identifiers_fail_without_store_damage(self) -> None:
        rng = random.Random(20261010)
        base = sample_event()
        for _ in range(100):
            invalid = " " + "".join(chr(rng.randint(1, 31)) for _ in range(3))
            with self.assertRaises(IntegrityError): validate_event(replace(base, actor_id=invalid))

    def test_bounded_hundred_event_load_verifies(self) -> None:
        with tempfile.TemporaryDirectory(dir=self.temporary_root) as directory:
            store = Store(Path(directory) / "load.sqlite3"); store.initialize()
            base = sample_event()
            for index in range(100):
                store.append(replace(base, stream_id=f"load:{index}", payload={"index": index}))
            result = store.verify()
            self.assertTrue(result["valid"])
            self.assertEqual(result["event_count"], 100)

    def test_cli_migrates_exact_v1(self) -> None:
        with tempfile.TemporaryDirectory(dir=self.temporary_root) as directory:
            source, backup = Path(directory) / "v1.sqlite3", Path(directory) / "backup.sqlite3"
            legacy(source)
            output = io.StringIO()
            with redirect_stdout(output):
                code = main(["--db", str(source), "migrate-v1", "--backup", str(backup)])
            self.assertEqual(code, 0)
            self.assertTrue(json.loads(output.getvalue())["verified"])
            self.assertTrue(Store(source).verify()["valid"])


if __name__ == "__main__": unittest.main()

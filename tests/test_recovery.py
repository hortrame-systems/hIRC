from __future__ import annotations

import io
import json
import sqlite3
import tempfile
import unittest
from contextlib import closing, redirect_stdout
from pathlib import Path
from unittest.mock import patch

import hirc.atomic as atomic
from hirc.adapter import DeterministicEchoAdapter, build_adapter_request, run_local_adapter
from hirc.cli import main
from hirc.outbox import build_outbox_view, record_adapter_run
from hirc.projection import build_briefing
from hirc.recovery import RecoveryError, backup_store, restore_store
from hirc.store import EventInput, Store


BASE = {
    "actor_id": "actor:owner", "category": "EVIDENCE", "foundation_version": "foundation:1",
    "goal_version": "goal:2", "privacy_class": "privacy:owner", "audience": "audience:owner",
    "purpose": "purpose:recovery", "occurred_at": "2026-10-10T00:00:00Z",
}


class RecoveryTests(unittest.TestCase):
    temporary_root = Path(__file__).parent / ".tmp"

    @classmethod
    def setUpClass(cls) -> None:
        cls.temporary_root.mkdir(parents=True, exist_ok=True)

    def populated(self, directory: str) -> Store:
        store = Store(Path(directory) / "source.sqlite3")
        store.initialize()
        store.append(EventInput(stream_id="work:recovery", event_type="work.created", payload={"work_id": "work:recovery", "title": "Recover", "owner": "actor:owner", "next_action": "Back up"}, **BASE))
        request = build_adapter_request({
            "actor_id": "actor:owner", "task_id": "task:hirc", "admission_ref": "admission:recorded",
            "foundation_version": "foundation:1", "goal_version": "goal:2", "privacy_class": "privacy:owner",
            "audience": "audience:owner", "purpose": "purpose:recovery", "requested_at": "time:20261010T000000Z",
            "capability": "capability:local-transform", "payload": {"text": "recover"},
        })
        record_adapter_run(store, run_local_adapter(DeterministicEchoAdapter(), request), idempotency_key="idempotency:recovery", authority_ref="authority:local", occurred_at="2026-10-10T00:00:01Z")
        return store

    def test_backup_and_restore_preserve_all_views(self) -> None:
        with tempfile.TemporaryDirectory(dir=self.temporary_root) as directory:
            store = self.populated(directory)
            backup = Path(directory) / "backup.sqlite3"
            restored = Path(directory) / "restored.sqlite3"
            backup_result = backup_store(store.path, backup)
            restore_result = restore_store(backup, restored)
            self.assertEqual(build_briefing(store), build_briefing(Store(restored)))
            self.assertEqual(build_outbox_view(store), build_outbox_view(Store(restored)))
            self.assertEqual(backup_result["head_hash"], restore_result["head_hash"])
            self.assertFalse(backup_result["encrypted"])
            self.assertFalse(backup_result["sensitive_data_release_allowed"])

    def test_corrupt_source_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory(dir=self.temporary_root) as directory:
            store = self.populated(directory)
            with closing(sqlite3.connect(store.path)) as connection, connection:
                connection.execute("DROP TRIGGER events_no_update")
                connection.execute("UPDATE events SET purpose='purpose:tampered' WHERE sequence=1")
            target = Path(directory) / "backup.sqlite3"
            with self.assertRaises(RecoveryError):
                backup_store(store.path, target)
            self.assertFalse(target.exists())

    def test_existing_target_is_never_overwritten(self) -> None:
        with tempfile.TemporaryDirectory(dir=self.temporary_root) as directory:
            store = self.populated(directory)
            target = Path(directory) / "occupied.sqlite3"
            target.write_bytes(b"keep")
            with self.assertRaises(RecoveryError):
                backup_store(store.path, target)
            self.assertEqual(target.read_bytes(), b"keep")

    def test_concurrent_target_creation_is_never_overwritten(self) -> None:
        with tempfile.TemporaryDirectory(dir=self.temporary_root) as directory:
            store = self.populated(directory)
            target = Path(directory) / "raced.sqlite3"
            original_publish = atomic._publish_new_name

            def create_racer_then_publish(source: Path, destination: Path) -> None:
                Path(destination).write_bytes(b"concurrent-writer")
                original_publish(source, destination)

            with patch("hirc.atomic._publish_new_name", side_effect=create_racer_then_publish):
                with self.assertRaises(RecoveryError):
                    backup_store(store.path, target)
            self.assertEqual(target.read_bytes(), b"concurrent-writer")

    def test_truncated_backup_does_not_create_restore_target(self) -> None:
        with tempfile.TemporaryDirectory(dir=self.temporary_root) as directory:
            store = self.populated(directory)
            backup = Path(directory) / "backup.sqlite3"
            backup_store(store.path, backup)
            body = backup.read_bytes()
            backup.write_bytes(body[: max(1, len(body) // 3)])
            target = Path(directory) / "restore.sqlite3"
            with self.assertRaises(RecoveryError):
                restore_store(backup, target)
            self.assertFalse(target.exists())

    def test_reopened_backup_matches_source_head(self) -> None:
        with tempfile.TemporaryDirectory(dir=self.temporary_root) as directory:
            store = self.populated(directory)
            backup = Path(directory) / "backup.sqlite3"
            result = backup_store(store.path, backup)
            self.assertEqual(Store(backup).verify()["head_hash"], result["head_hash"])

    def test_cli_backup_and_restore(self) -> None:
        with tempfile.TemporaryDirectory(dir=self.temporary_root) as directory:
            store = self.populated(directory)
            backup = Path(directory) / "cli-backup.sqlite3"
            restored = Path(directory) / "cli-restored.sqlite3"
            output = io.StringIO()
            with redirect_stdout(output):
                backup_code = main(["--db", str(store.path), "backup", "--output", str(backup)])
            self.assertEqual(backup_code, 0)
            with redirect_stdout(io.StringIO()):
                restore_code = main(["restore", "--input", str(backup), "--output", str(restored)])
            self.assertEqual(restore_code, 0)
            self.assertTrue(Store(restored).verify()["valid"])


if __name__ == "__main__":
    unittest.main()

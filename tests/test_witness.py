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
from hirc.cli import main
from hirc.store import EventInput, Store
from hirc.witness import WitnessError, create_head_witness, verify_head_witness


KEY = b"k" * 32
BASE = dict(actor_id="actor:owner", category="EVIDENCE", foundation_version="foundation:1", goal_version="goal:1", privacy_class="privacy:owner", audience="audience:owner", purpose="purpose:witness", occurred_at="2026-10-10T00:00:00Z")


class WitnessTests(unittest.TestCase):
    temporary_root = Path(__file__).parent / ".tmp"

    @classmethod
    def setUpClass(cls) -> None: cls.temporary_root.mkdir(parents=True, exist_ok=True)

    def store(self, directory: str) -> Store:
        store = Store(Path(directory) / "witness.sqlite3"); store.initialize()
        store.append(EventInput(stream_id="note:one", event_type="note.recorded", payload={"index": 1}, **BASE))
        store.append(EventInput(stream_id="note:two", event_type="note.recorded", payload={"index": 2}, **BASE))
        return store

    def test_create_and_verify(self) -> None:
        with tempfile.TemporaryDirectory(dir=self.temporary_root) as directory:
            store=self.store(directory); path=Path(directory)/"head.json"
            result=create_head_witness(store,path,KEY)
            self.assertEqual(result["event_count"],2)
            self.assertTrue(verify_head_witness(store,path,KEY)["valid"])

    def test_privileged_tail_truncation_is_detected(self) -> None:
        with tempfile.TemporaryDirectory(dir=self.temporary_root) as directory:
            store=self.store(directory); path=Path(directory)/"head.json"; create_head_witness(store,path,KEY)
            with closing(sqlite3.connect(store.path)) as connection, connection:
                connection.execute("DROP TRIGGER events_no_delete"); connection.execute("DELETE FROM events WHERE sequence=2"); connection.execute("CREATE TRIGGER events_no_delete BEFORE DELETE ON events BEGIN SELECT RAISE(ABORT, 'hirc events are append-only'); END")
            self.assertTrue(store.verify()["valid"])
            with self.assertRaises(WitnessError): verify_head_witness(store,path,KEY)

    def test_wrong_key_and_changed_witness_are_rejected(self) -> None:
        with tempfile.TemporaryDirectory(dir=self.temporary_root) as directory:
            store=self.store(directory); path=Path(directory)/"head.json"; create_head_witness(store,path,KEY)
            with self.assertRaises(WitnessError): verify_head_witness(store,path,b"z"*32)
            value=json.loads(path.read_text()); value["event_count"]=99; path.write_text(json.dumps(value),encoding="utf-8")
            with self.assertRaises(WitnessError): verify_head_witness(store,path,KEY)

    def test_existing_witness_is_not_overwritten(self) -> None:
        with tempfile.TemporaryDirectory(dir=self.temporary_root) as directory:
            store=self.store(directory); path=Path(directory)/"head.json"; path.write_bytes(b"keep")
            with self.assertRaises(WitnessError): create_head_witness(store,path,KEY)
            self.assertEqual(path.read_bytes(),b"keep")

    def test_concurrent_witness_creation_is_never_overwritten(self) -> None:
        with tempfile.TemporaryDirectory(dir=self.temporary_root) as directory:
            store=self.store(directory); path=Path(directory)/"head.json"
            original_publish=atomic._publish_new_name
            def create_racer_then_publish(source: Path, destination: Path) -> None:
                Path(destination).write_bytes(b"concurrent-writer")
                original_publish(source,destination)
            with patch("hirc.atomic._publish_new_name",side_effect=create_racer_then_publish):
                with self.assertRaises(WitnessError): create_head_witness(store,path,KEY)
            self.assertEqual(path.read_bytes(),b"concurrent-writer")

    def test_short_key_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory(dir=self.temporary_root) as directory:
            store=self.store(directory)
            with self.assertRaises(WitnessError): create_head_witness(store,Path(directory)/"head.json",b"short")

    def test_oversized_witness_file_is_rejected_before_parsing(self) -> None:
        with tempfile.TemporaryDirectory(dir=self.temporary_root) as directory:
            store=self.store(directory); path=Path(directory)/"head.json"
            path.write_bytes(b" " * 65_537)
            with self.assertRaisesRegex(WitnessError,"unreadable"):
                verify_head_witness(store,path,KEY)

    def test_cli_reads_key_from_stdin_not_arguments(self) -> None:
        with tempfile.TemporaryDirectory(dir=self.temporary_root) as directory:
            store=self.store(directory); path=Path(directory)/"head.json"
            stdin=io.TextIOWrapper(io.BytesIO(KEY+b"\n"),encoding="utf-8")
            output=io.StringIO()
            with patch("sys.stdin",stdin), redirect_stdout(output):
                code=main(["--db",str(store.path),"witness-create","--output",str(path),"--key-stdin"])
            self.assertEqual(code,0)
            stdin=io.TextIOWrapper(io.BytesIO(KEY+b"\n"),encoding="utf-8")
            with patch("sys.stdin",stdin), redirect_stdout(io.StringIO()):
                code=main(["--db",str(store.path),"witness-verify","--input",str(path),"--key-stdin"])
            self.assertEqual(code,0)


if __name__=="__main__": unittest.main()

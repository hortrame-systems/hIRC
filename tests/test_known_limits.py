from __future__ import annotations

import json
import sqlite3
import tempfile
import unittest
import zipfile
from contextlib import closing
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
import sys
sys.path.insert(0, str(ROOT / "implementation"))

from build_pyz import build  # noqa: E402
from hirc.store import EventInput, Store  # noqa: E402


class KnownReleaseLimits(unittest.TestCase):
    """Expected failures keep unresolved release claims executable and visible."""

    temporary_root = Path(__file__).parent / ".tmp"

    @classmethod
    def setUpClass(cls) -> None:
        cls.temporary_root.mkdir(parents=True, exist_ok=True)

    @unittest.expectedFailure
    def test_store_alone_detects_privileged_tail_truncation(self) -> None:
        with tempfile.TemporaryDirectory(dir=self.temporary_root) as directory:
            store = Store(Path(directory) / "tail.sqlite3")
            store.initialize()
            base = dict(actor_id="actor:owner", category="EVIDENCE", foundation_version="foundation:1", goal_version="goal:1", privacy_class="privacy:owner", audience="audience:owner", purpose="purpose:limit", occurred_at="2026-10-10T00:00:00Z")
            store.append(EventInput(stream_id="note:one", event_type="note.recorded", payload={"index": 1}, **base))
            store.append(EventInput(stream_id="note:two", event_type="note.recorded", payload={"index": 2}, **base))
            with closing(sqlite3.connect(store.path)) as connection, connection:
                connection.execute("DROP TRIGGER events_no_delete")
                connection.execute("DELETE FROM events WHERE sequence=2")
                connection.execute("CREATE TRIGGER events_no_delete BEFORE DELETE ON events BEGIN SELECT RAISE(ABORT, 'hirc events are append-only'); END")
            self.assertFalse(store.verify()["valid"], "requires a protected external/signed head witness")

    @unittest.expectedFailure
    def test_store_is_encrypted_at_rest(self) -> None:
        with tempfile.TemporaryDirectory(dir=self.temporary_root) as directory:
            store = Store(Path(directory) / "plaintext.sqlite3")
            store.initialize()
            self.assertNotEqual(store.path.read_bytes()[:16], b"SQLite format 3\x00")

    @unittest.expectedFailure
    def test_release_manifest_has_an_independently_verifiable_signature(self) -> None:
        with tempfile.TemporaryDirectory(dir=self.temporary_root) as directory:
            package = Path(directory) / "hirc.pyz"
            build(package)
            with zipfile.ZipFile(package) as archive:
                manifest = json.loads(archive.read("hirc-package-manifest.json"))
            self.assertIn("signature", manifest)


if __name__ == "__main__":
    unittest.main()

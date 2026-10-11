from __future__ import annotations

import sqlite3
import tempfile
import unittest
from contextlib import closing
from dataclasses import replace
from pathlib import Path
from unittest.mock import patch

from hirc.canonical import canonical_json, sha256_text
from hirc.store import (
    DISABLED_CAPABILITIES,
    EventInput,
    IntegrityError,
    Store,
    _event_document,
    validate_event,
)


def evidence(payload: dict | None = None) -> EventInput:
    return EventInput(
        stream_id="work:alpha",
        actor_id="actor:local-human",
        event_type="work.created",
        category="EVIDENCE",
        foundation_version="foundation:1",
        goal_version="goal:2",
        privacy_class="privacy:owner",
        audience="audience:owner",
        purpose="purpose:work-recovery",
        occurred_at="2026-10-10T00:00:00Z",
        payload=payload or {"title": "First work item"},
    )


class StoreTests(unittest.TestCase):
    temporary_root = Path(__file__).parent / ".tmp"

    @classmethod
    def setUpClass(cls) -> None:
        cls.temporary_root.mkdir(parents=True, exist_ok=True)

    def temporary_directory(self) -> tempfile.TemporaryDirectory[str]:
        return tempfile.TemporaryDirectory(dir=self.temporary_root)

    def make_store(self, directory: str, name: str = "hirc.sqlite3") -> Store:
        store = Store(Path(directory) / name)
        store.initialize()
        return store

    def test_initial_state_disables_every_high_risk_capability(self) -> None:
        with self.temporary_directory() as directory:
            result = self.make_store(directory).verify()
            self.assertTrue(result["valid"])
            self.assertEqual(result["disabled_capabilities"], DISABLED_CAPABILITIES)
            self.assertEqual(result["event_count"], 0)

    def test_plaintext_status_is_explicit_and_sensitive_mode_fails_closed(self) -> None:
        with self.temporary_directory() as directory:
            target = Path(directory) / "sensitive.sqlite3"
            with self.assertRaises(IntegrityError):
                Store(target).initialize(sensitive=True)
            self.assertFalse(target.exists())
            normal = self.make_store(directory, "normal.sqlite3").status()
            self.assertIs(normal["encrypted_at_rest"], False)
            self.assertIs(normal["sensitive_data_release_allowed"], False)

    def test_same_inputs_produce_same_first_event_identity(self) -> None:
        with self.temporary_directory() as directory:
            first = self.make_store(directory, "first.sqlite3").append(evidence())
            second = self.make_store(directory, "second.sqlite3").append(evidence())
            self.assertEqual(first.event_id, second.event_id)
            self.assertEqual(first.event_hash, second.event_hash)

    def test_effectful_action_requires_authority(self) -> None:
        with self.temporary_directory() as directory:
            store = self.make_store(directory)
            invalid = replace(evidence(), category="ACTION", effect_state="REQUESTED")
            with self.assertRaises(IntegrityError):
                store.append(invalid)

    def test_correction_requires_and_preserves_target(self) -> None:
        with self.temporary_directory() as directory:
            store = self.make_store(directory)
            original = store.append(evidence())
            correction = EventInput(
                stream_id="work:alpha",
                actor_id="actor:local-human",
                event_type="work.corrected",
                category="CORRECTION",
                foundation_version="foundation:1",
                goal_version="goal:2",
                privacy_class="privacy:owner",
                audience="audience:owner",
                purpose="purpose:work-recovery",
                occurred_at="2026-10-10T00:01:00Z",
                payload={"title": "Corrected title"},
                correction_of=original.event_id,
            )
            store.append(correction)
            rows = list(store.iter_events())
            self.assertEqual(len(rows), 2)
            self.assertEqual(rows[1]["correction_of"], original.event_id)
            self.assertTrue(store.verify()["valid"])

    def test_correction_cannot_target_missing_event(self) -> None:
        with self.temporary_directory() as directory:
            store = self.make_store(directory)
            correction = EventInput(
                stream_id="work:alpha",
                actor_id="actor:local-human",
                event_type="work.corrected",
                category="CORRECTION",
                foundation_version="foundation:1",
                goal_version="goal:2",
                privacy_class="privacy:owner",
                audience="audience:owner",
                purpose="purpose:work-recovery",
                occurred_at="2026-10-10T00:01:00Z",
                payload={"title": "Unbound correction"},
                correction_of="event:" + "f" * 64,
            )
            with self.assertRaises(IntegrityError):
                store.append(correction)

    def test_correction_cannot_change_target_information_boundary(self) -> None:
        with self.temporary_directory() as directory:
            store = self.make_store(directory)
            original = store.append(evidence())
            correction = replace(
                evidence({"title": "Cross-boundary correction"}),
                event_type="work.corrected",
                category="CORRECTION",
                audience="audience:public",
                occurred_at="2026-10-10T00:01:00Z",
                correction_of=original.event_id,
            )
            with self.assertRaises(IntegrityError):
                store.append(correction)
            self.assertEqual(store.verify()["event_count"], 1)

    def test_verifier_rejects_self_rehashed_impossible_correction_history(self) -> None:
        for variant in ("missing-target", "cross-boundary"):
            with self.subTest(variant=variant), self.temporary_directory() as directory:
                store = self.make_store(directory)
                original = store.append(evidence())
                correction = replace(
                    evidence({"title": "Correction"}),
                    event_type="work.corrected",
                    category="CORRECTION",
                    occurred_at="2026-10-10T00:01:00Z",
                    correction_of=original.event_id,
                )
                stored = store.append(correction)
                impossible = replace(
                    correction,
                    correction_of="event:" + "f" * 64 if variant == "missing-target" else original.event_id,
                    audience="audience:public" if variant == "cross-boundary" else correction.audience,
                )
                forged_hash = sha256_text(canonical_json(_event_document(stored.sequence, stored.prev_hash, impossible)))
                with closing(sqlite3.connect(store.path)) as connection, connection:
                    connection.execute("DROP TRIGGER events_no_update")
                    connection.execute(
                        "UPDATE events SET event_id=?, event_hash=?, audience=?, correction_of=? WHERE sequence=?",
                        (
                            f"event:{forged_hash}",
                            forged_hash,
                            impossible.audience,
                            impossible.correction_of,
                            stored.sequence,
                        ),
                    )
                    connection.execute(
                        "CREATE TRIGGER events_no_update BEFORE UPDATE ON events "
                        "BEGIN SELECT RAISE(ABORT, 'hirc events are append-only'); END"
                    )
                result = store.verify()
                self.assertFalse(result["valid"])
                expected = (
                    "correction target missing or nonprior"
                    if variant == "missing-target"
                    else "correction boundary mismatch"
                )
                self.assertTrue(any(expected in item for item in result["errors"]))

    def test_ordinary_update_and_delete_are_denied(self) -> None:
        with self.temporary_directory() as directory:
            store = self.make_store(directory)
            store.append(evidence())
            with closing(sqlite3.connect(store.path)) as connection:
                with self.assertRaises(sqlite3.IntegrityError):
                    connection.execute("UPDATE events SET purpose='purpose:other' WHERE sequence=1")
                connection.rollback()
                with self.assertRaises(sqlite3.IntegrityError):
                    connection.execute("DELETE FROM events WHERE sequence=1")

    def test_verifier_detects_privileged_tampering(self) -> None:
        with self.temporary_directory() as directory:
            store = self.make_store(directory)
            store.append(evidence())
            with closing(sqlite3.connect(store.path)) as connection, connection:
                connection.execute("DROP TRIGGER events_no_update")
                connection.execute("UPDATE events SET purpose='purpose:tampered' WHERE sequence=1")
            result = store.verify()
            self.assertFalse(result["valid"])
            self.assertIn("event hash mismatch at 1", result["errors"])

    def test_verifier_rejects_noncanonical_duplicate_key_payload(self) -> None:
        with self.temporary_directory() as directory:
            store = self.make_store(directory)
            before = store.append(evidence({"title": "First"}))
            with closing(sqlite3.connect(store.path)) as connection, connection:
                connection.execute("DROP TRIGGER events_no_update")
                connection.execute(
                    "UPDATE events SET payload_json=? WHERE sequence=1",
                    ('{"title":"forged","title":"First"}',),
                )
                connection.execute(
                    "CREATE TRIGGER events_no_update BEFORE UPDATE ON events "
                    "BEGIN SELECT RAISE(ABORT, 'hirc events are append-only'); END"
                )
            result = store.verify()
            self.assertEqual(result["head_hash"], before.event_hash)
            self.assertFalse(result["valid"])
            self.assertIn("payload JSON is not canonical at 1", result["errors"])

    def test_verify_and_status_use_read_only_connections(self) -> None:
        with self.temporary_directory() as directory:
            store = self.make_store(directory)
            observed: list[bool] = []
            original = store._connect
            def tracked(*, read_only: bool = False):
                observed.append(read_only)
                return original(read_only=read_only)
            with patch.object(store, "_connect", side_effect=tracked):
                self.assertTrue(store.verify()["valid"])
                self.assertTrue(store.status()["valid"])
                self.assertEqual(list(store.iter_events()), [])
                self.assertEqual(store.verified_snapshot()[0]["event_count"], 0)
            self.assertEqual(observed, [True, True, True, True])

    def test_payload_depth_size_and_utf8_limits_fail_closed(self) -> None:
        deep: dict = {}
        cursor = deep
        for _ in range(70):
            cursor["nested"] = {}
            cursor = cursor["nested"]
        cases = [deep, {"text": "x" * 1_100_000}, {"text": "\ud800"}]
        for payload in cases:
            with self.subTest(kind=len(str(type(payload)))):
                with self.assertRaises(IntegrityError):
                    validate_event(evidence(payload))


if __name__ == "__main__":
    unittest.main()

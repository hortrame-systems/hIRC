from __future__ import annotations

import json
import sqlite3
import tempfile
import threading
import unittest
from contextlib import closing
from pathlib import Path

from hirc.projection import ProjectionError, build_briefing
from hirc.store import EventInput, IntegrityError, Store


BASE = {
    "actor_id": "actor:red-team",
    "category": "EVIDENCE",
    "foundation_version": "foundation:1",
    "goal_version": "goal:2",
    "privacy_class": "privacy:owner",
    "audience": "audience:owner",
    "purpose": "purpose:red-team",
    "occurred_at": "2026-10-10T00:00:00Z",
}


def event(event_type: str, payload: dict, stream: str = "work:red-team", **changes) -> EventInput:
    values = {**BASE, **changes}
    return EventInput(stream_id=stream, event_type=event_type, payload=payload, **values)


class IntegrationRedTeamTests(unittest.TestCase):
    temporary_root = Path(__file__).parent / ".tmp"

    @classmethod
    def setUpClass(cls) -> None:
        cls.temporary_root.mkdir(parents=True, exist_ok=True)

    def store(self, directory: str) -> Store:
        store = Store(Path(directory) / "integration.sqlite3")
        store.initialize()
        return store

    def create_work(self, store: Store, identity: str = "work:red-team", title: str = "Red team") -> None:
        store.append(event("work.created", {"work_id": identity, "title": title, "owner": "actor:red-team", "next_action": "Attack"}, identity))

    def test_tampered_chain_rejects_next_append(self) -> None:
        with tempfile.TemporaryDirectory(dir=self.temporary_root) as directory:
            store = self.store(directory)
            self.create_work(store)
            with closing(sqlite3.connect(store.path)) as connection, connection:
                connection.execute("DROP TRIGGER events_no_update")
                connection.execute("UPDATE events SET purpose='purpose:tampered' WHERE sequence=1")
            with self.assertRaises(IntegrityError):
                store.append(event("work.status", {"work_id": "work:red-team", "status": "ACTIVE", "next_action": "Continue"}))

    def test_missing_disabled_capability_rejects_next_append(self) -> None:
        with tempfile.TemporaryDirectory(dir=self.temporary_root) as directory:
            store = self.store(directory)
            with closing(sqlite3.connect(store.path)) as connection, connection:
                connection.execute("DROP TRIGGER capability_no_delete")
                connection.execute("DELETE FROM capability_state WHERE capability='bridge'")
            with self.assertRaises(IntegrityError):
                self.create_work(store)

    def test_uncommitted_destructive_transaction_rolls_back(self) -> None:
        with tempfile.TemporaryDirectory(dir=self.temporary_root) as directory:
            store = self.store(directory)
            self.create_work(store)
            connection = sqlite3.connect(store.path)
            connection.execute("BEGIN IMMEDIATE")
            connection.execute("DROP TRIGGER events_no_update")
            connection.execute("UPDATE events SET purpose='purpose:uncommitted' WHERE sequence=1")
            connection.rollback()
            connection.close()
            self.assertTrue(store.verify()["valid"])
            store.append(event("work.status", {"work_id": "work:red-team", "status": "ACTIVE", "next_action": "Recovered"}))
            self.assertTrue(store.verify()["valid"])

    def test_concurrent_writers_form_one_contiguous_chain(self) -> None:
        with tempfile.TemporaryDirectory(dir=self.temporary_root) as directory:
            store = self.store(directory)
            barrier = threading.Barrier(6)
            failures: list[Exception] = []

            def writer(index: int) -> None:
                try:
                    barrier.wait()
                    store.append(event("note.recorded", {"index": index}, f"stream:{index}"))
                except Exception as error:  # recorded and asserted below
                    failures.append(error)

            threads = [threading.Thread(target=writer, args=(index,)) for index in range(6)]
            for thread in threads:
                thread.start()
            for thread in threads:
                thread.join()
            self.assertEqual(failures, [])
            rows = list(store.iter_events())
            self.assertEqual([row["sequence"] for row in rows], list(range(1, 7)))
            self.assertTrue(store.verify()["valid"])

    def test_briefing_inherits_privacy_audience_and_purpose(self) -> None:
        with tempfile.TemporaryDirectory(dir=self.temporary_root) as directory:
            store = self.store(directory)
            self.create_work(store)
            work = build_briefing(store)["work"][0]
            self.assertEqual(
                work["information_boundary"],
                {"privacy_class": "privacy:owner", "audience": "audience:owner", "purpose": "purpose:red-team"},
            )

    def test_projection_rejects_silent_information_boundary_change(self) -> None:
        with tempfile.TemporaryDirectory(dir=self.temporary_root) as directory:
            store = self.store(directory)
            self.create_work(store)
            store.append(
                event(
                    "work.status",
                    {"work_id": "work:red-team", "status": "ACTIVE", "next_action": "Widened"},
                    audience="audience:external",
                )
            )
            with self.assertRaises(ProjectionError):
                build_briefing(store)

    def test_command_shaped_content_remains_inert_data(self) -> None:
        with tempfile.TemporaryDirectory(dir=self.temporary_root) as directory:
            store = self.store(directory)
            shaped = "<script>alert(1)</script>; DROP TABLE events; file:///secret"
            self.create_work(store, title=shaped)
            result = build_briefing(store)
            self.assertEqual(result["work"][0]["title"], shaped)
            self.assertTrue(store.verify()["valid"])
            with closing(sqlite3.connect(store.path)) as connection:
                count = connection.execute("SELECT count(*) FROM events").fetchone()[0]
            self.assertEqual(count, 1)

    def test_reopen_reproduces_head_and_briefing(self) -> None:
        with tempfile.TemporaryDirectory(dir=self.temporary_root) as directory:
            store = self.store(directory)
            self.create_work(store)
            first = build_briefing(store)
            reopened = Store(store.path)
            second = build_briefing(reopened)
            self.assertEqual(first, second)

    def test_projection_does_not_trust_separate_verify_then_read(self) -> None:
        class VerifyThenTamperStore(Store):
            def verify(self):
                result = super().verify()
                with closing(sqlite3.connect(self.path)) as connection, connection:
                    connection.execute("DROP TRIGGER events_no_update")
                    connection.execute(
                        "UPDATE events SET payload_json=? WHERE sequence=1",
                        (json.dumps({"work_id": "work:red-team", "title": "tampered", "owner": "actor:red-team", "next_action": "Attack"}),),
                    )
                return result

        with tempfile.TemporaryDirectory(dir=self.temporary_root) as directory:
            normal = self.store(directory)
            self.create_work(normal, title="verified")
            racing = VerifyThenTamperStore(normal.path)
            briefing = build_briefing(racing)
            self.assertEqual(briefing["work"][0]["title"], "verified")
            self.assertTrue(Store(normal.path).verify()["valid"])

    def test_reinitialize_refuses_to_repair_corrupt_capability_state(self) -> None:
        with tempfile.TemporaryDirectory(dir=self.temporary_root) as directory:
            store = self.store(directory)
            with closing(sqlite3.connect(store.path)) as connection, connection:
                connection.execute("DROP TRIGGER capability_no_delete")
                connection.execute("DELETE FROM capability_state WHERE capability='bridge'")
            with self.assertRaises(IntegrityError):
                store.initialize()
            self.assertFalse(store.verify()["valid"])

    def test_missing_append_only_trigger_rejects_next_append(self) -> None:
        with tempfile.TemporaryDirectory(dir=self.temporary_root) as directory:
            store = self.store(directory)
            with closing(sqlite3.connect(store.path)) as connection, connection:
                connection.execute("DROP TRIGGER events_no_update")
            with self.assertRaises(IntegrityError):
                self.create_work(store)

    def test_held_dependency_blocks_transitive_descendants(self) -> None:
        with tempfile.TemporaryDirectory(dir=self.temporary_root) as directory:
            store = self.store(directory)
            for identity in ("work:root", "work:child", "work:grandchild", "work:sibling"):
                self.create_work(store, identity=identity, title=identity)
            store.append(event("dependency.added", {"work_id": "work:child", "depends_on": "work:root"}))
            store.append(event("dependency.added", {"work_id": "work:grandchild", "depends_on": "work:child"}))
            store.append(event("hold.placed", {"hold_id": "hold:root", "work_id": "work:root", "reason": "review", "reopen_when": "review arrives", "allowed_sibling_work": "work:sibling"}))
            by_id = {item["work_id"]: item for item in build_briefing(store)["work"]}
            self.assertEqual(by_id["work:root"]["status"], "HELD")
            self.assertEqual(by_id["work:child"]["status"], "BLOCKED")
            self.assertEqual(by_id["work:grandchild"]["status"], "BLOCKED")
            self.assertEqual(by_id["work:child"]["blocked_by"], ["work:root"])
            self.assertEqual(by_id["work:grandchild"]["blocked_by"], ["work:root"])
            self.assertEqual(by_id["work:sibling"]["status"], "OPEN")

    def test_invalid_allowed_sibling_fails_projection(self) -> None:
        with tempfile.TemporaryDirectory(dir=self.temporary_root) as directory:
            store = self.store(directory)
            self.create_work(store)
            store.append(event("hold.placed", {"hold_id": "hold:red", "work_id": "work:red-team", "reason": "review", "reopen_when": "review arrives", "allowed_sibling_work": "work:missing"}))
            with self.assertRaises(ProjectionError):
                build_briefing(store)
            self.assertTrue(store.verify()["valid"])

    def test_correction_cannot_widen_target_boundary(self) -> None:
        with tempfile.TemporaryDirectory(dir=self.temporary_root) as directory:
            store = self.store(directory)
            original = store.append(event("note.recorded", {"claim": "private"}))
            widened = event(
                "note.corrected",
                {"claim": "public"},
                category="CORRECTION",
                correction_of=original.event_id,
                audience="audience:external",
            )
            with self.assertRaises(IntegrityError):
                store.append(widened)
            self.assertEqual(store.verify()["event_count"], 1)

    def test_projection_failure_preserves_chain(self) -> None:
        with tempfile.TemporaryDirectory(dir=self.temporary_root) as directory:
            store = self.store(directory)
            store.append(event("work.status", {"work_id": "work:missing", "status": "ACTIVE", "next_action": "None"}))
            before = store.verify()
            with self.assertRaises(ProjectionError):
                build_briefing(store)
            after = store.verify()
            self.assertEqual(before, after)
            self.assertTrue(after["valid"])

    def test_effect_states_remain_distinct_without_promotion(self) -> None:
        with tempfile.TemporaryDirectory(dir=self.temporary_root) as directory:
            store = self.store(directory)
            states = ("REQUESTED", "SENT", "PROVIDER_ACCEPTED", "OBSERVED")
            for state in states:
                store.append(event("effect.state-recorded", {"state": state}, category="ACTION", effect_state=state, authority_ref="authority:fixture"))
            self.assertEqual([row["effect_state"] for row in store.iter_events()], list(states))
            briefing = build_briefing(store)
            self.assertEqual(len(briefing["unprojected_events"]), len(states))

    def test_duplicate_work_identity_fails_without_chain_damage(self) -> None:
        with tempfile.TemporaryDirectory(dir=self.temporary_root) as directory:
            store = self.store(directory)
            self.create_work(store)
            self.create_work(store, title="duplicate")
            with self.assertRaises(ProjectionError):
                build_briefing(store)
            self.assertTrue(store.verify()["valid"])

    def test_double_clear_fails_without_chain_damage(self) -> None:
        with tempfile.TemporaryDirectory(dir=self.temporary_root) as directory:
            store = self.store(directory)
            self.create_work(store)
            self.create_work(store, identity="work:sibling", title="Sibling")
            store.append(event("hold.placed", {"hold_id": "hold:red", "work_id": "work:red-team", "reason": "review", "reopen_when": "review arrives", "allowed_sibling_work": "work:sibling"}))
            store.append(event("hold.cleared", {"hold_id": "hold:red", "resolution": "done"}))
            store.append(event("hold.cleared", {"hold_id": "hold:red", "resolution": "again"}))
            with self.assertRaises(ProjectionError):
                build_briefing(store)
            self.assertTrue(store.verify()["valid"])


if __name__ == "__main__":
    unittest.main()

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from hirc.projection import ProjectionError, build_briefing
from hirc.store import EventInput, Store


BASE = {
    "actor_id": "actor:owner",
    "category": "EVIDENCE",
    "foundation_version": "foundation:1",
    "goal_version": "goal:2",
    "privacy_class": "privacy:owner",
    "audience": "audience:owner",
    "purpose": "purpose:work-recovery",
    "occurred_at": "2026-10-10T00:00:00Z",
}


def event(event_type: str, payload: dict, stream: str = "work:alpha") -> EventInput:
    return EventInput(stream_id=stream, event_type=event_type, payload=payload, **BASE)


class ProjectionTests(unittest.TestCase):
    temporary_root = Path(__file__).parent / ".tmp"

    @classmethod
    def setUpClass(cls) -> None:
        cls.temporary_root.mkdir(parents=True, exist_ok=True)

    def store(self, directory: str) -> Store:
        store = Store(Path(directory) / "projection.sqlite3")
        store.initialize()
        return store

    def create(self, store: Store, work_id: str, title: str) -> None:
        store.append(event("work.created", {"work_id": work_id, "title": title, "owner": "actor:owner", "next_action": "Start"}, work_id))

    def test_briefing_preserves_work_commitment_and_source_events(self) -> None:
        with tempfile.TemporaryDirectory(dir=self.temporary_root) as directory:
            store = self.store(directory)
            self.create(store, "work:alpha", "Alpha")
            store.append(event("commitment.declared", {"commitment_id": "commitment:one", "work_id": "work:alpha", "owner": "actor:owner", "description": "Deliver alpha"}))
            store.append(event("work.status", {"work_id": "work:alpha", "status": "ACTIVE", "next_action": "Implement"}))
            result = build_briefing(store)
            self.assertEqual(result["work"][0]["status"], "ACTIVE")
            self.assertEqual(result["commitments"][0]["status"], "OPEN")
            self.assertTrue(result["work"][0]["source_events"]["created"].startswith("event:"))

    def test_hold_blocks_only_its_work_and_exposes_sibling_path(self) -> None:
        with tempfile.TemporaryDirectory(dir=self.temporary_root) as directory:
            store = self.store(directory)
            self.create(store, "work:alpha", "Alpha")
            self.create(store, "work:beta", "Beta")
            store.append(event("hold.placed", {"hold_id": "hold:alpha", "work_id": "work:alpha", "reason": "review", "reopen_when": "review complete", "allowed_sibling_work": "work:beta"}))
            result = build_briefing(store)
            by_id = {item["work_id"]: item for item in result["work"]}
            self.assertEqual(by_id["work:alpha"]["status"], "HELD")
            self.assertEqual(by_id["work:beta"]["status"], "OPEN")
            self.assertEqual(result["holds"][0]["allowed_sibling_work"], "work:beta")

    def test_reported_and_observed_states_remain_distinct(self) -> None:
        with tempfile.TemporaryDirectory(dir=self.temporary_root) as directory:
            store = self.store(directory)
            self.create(store, "work:alpha", "Alpha")
            store.append(event("observation.recorded", {"work_id": "work:alpha", "claim": "remote push", "reported_state": "PROVIDER_ACCEPTED", "observed_state": "UNKNOWN"}))
            observation = build_briefing(store)["work"][0]["observations"][0]
            self.assertEqual(observation["reported_state"], "PROVIDER_ACCEPTED")
            self.assertEqual(observation["observed_state"], "UNKNOWN")

    def test_missing_reference_fails_projection(self) -> None:
        with tempfile.TemporaryDirectory(dir=self.temporary_root) as directory:
            store = self.store(directory)
            store.append(event("work.status", {"work_id": "work:missing", "status": "ACTIVE", "next_action": "None"}))
            with self.assertRaises(ProjectionError):
                build_briefing(store)

    def test_dependency_cycle_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory(dir=self.temporary_root) as directory:
            store = self.store(directory)
            self.create(store, "work:alpha", "Alpha")
            self.create(store, "work:beta", "Beta")
            store.append(event("dependency.added", {"work_id": "work:alpha", "depends_on": "work:beta"}))
            store.append(event("dependency.added", {"work_id": "work:beta", "depends_on": "work:alpha"}))
            with self.assertRaises(ProjectionError):
                build_briefing(store)


if __name__ == "__main__":
    unittest.main()

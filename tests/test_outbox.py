from __future__ import annotations

import sqlite3
import io
import json
import tempfile
import threading
import unittest
from contextlib import closing
from contextlib import redirect_stdout
from pathlib import Path

from hirc.adapter import AcceptanceOnlyAdapter, DeterministicEchoAdapter, build_adapter_request, run_local_adapter
from hirc.outbox import OutboxError, build_outbox_view, record_adapter_run
from hirc.store import EventInput, IntegrityError, Store
from hirc.cli import main


def request(text: str = "hello") -> dict:
    return build_adapter_request({
        "actor_id": "actor:local",
        "task_id": "task:hirc",
        "admission_ref": "admission:recorded",
        "foundation_version": "foundation:1",
        "goal_version": "goal:2",
        "privacy_class": "privacy:owner",
        "audience": "audience:owner",
        "purpose": "purpose:outbox",
        "requested_at": "time:20261010T000000Z",
        "capability": "capability:local-transform",
        "payload": {"text": text},
    })


class OutboxTests(unittest.TestCase):
    temporary_root = Path(__file__).parent / ".tmp"

    @classmethod
    def setUpClass(cls) -> None:
        cls.temporary_root.mkdir(parents=True, exist_ok=True)

    def store(self, directory: str) -> Store:
        store = Store(Path(directory) / "outbox.sqlite3")
        store.initialize()
        return store

    def record(self, store: Store, run: dict, key: str = "idempotency:test") -> dict:
        return record_adapter_run(store, run, idempotency_key=key, authority_ref="authority:local", occurred_at="2026-10-10T00:00:00Z")

    def test_observed_run_records_three_separate_states(self) -> None:
        with tempfile.TemporaryDirectory(dir=self.temporary_root) as directory:
            store = self.store(directory)
            view = self.record(store, run_local_adapter(DeterministicEchoAdapter(), request()))
            item = view["items"][0]
            self.assertEqual(item["reported_state"], "PROVIDER_ACCEPTED")
            self.assertEqual(item["observed_state"], "OBSERVED")
            self.assertEqual(store.verify()["event_count"], 3)

    def test_acceptance_only_stays_unknown(self) -> None:
        with tempfile.TemporaryDirectory(dir=self.temporary_root) as directory:
            store = self.store(directory)
            item = self.record(store, run_local_adapter(AcceptanceOnlyAdapter(), request()))["items"][0]
            self.assertEqual(item["reported_state"], "PROVIDER_ACCEPTED")
            self.assertEqual(item["observed_state"], "UNKNOWN")
            self.assertTrue(item["observation_error"])

    def test_same_idempotent_run_does_not_append_twice(self) -> None:
        with tempfile.TemporaryDirectory(dir=self.temporary_root) as directory:
            store = self.store(directory)
            run = run_local_adapter(DeterministicEchoAdapter(), request())
            first = self.record(store, run)
            second = self.record(store, run)
            self.assertEqual(first, second)
            self.assertEqual(store.verify()["event_count"], 3)

    def test_same_idempotency_key_for_different_request_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory(dir=self.temporary_root) as directory:
            store = self.store(directory)
            self.record(store, run_local_adapter(DeterministicEchoAdapter(), request("one")))
            with self.assertRaises(IntegrityError):
                self.record(store, run_local_adapter(DeterministicEchoAdapter(), request("two")))

    def test_concurrent_duplicate_record_is_exactly_once_locally(self) -> None:
        with tempfile.TemporaryDirectory(dir=self.temporary_root) as directory:
            store = self.store(directory)
            run = run_local_adapter(DeterministicEchoAdapter(), request())
            barrier = threading.Barrier(5)
            errors: list[Exception] = []
            def worker() -> None:
                try:
                    barrier.wait()
                    self.record(store, run)
                except Exception as error:
                    errors.append(error)
            threads = [threading.Thread(target=worker) for _ in range(5)]
            for thread in threads: thread.start()
            for thread in threads: thread.join()
            self.assertEqual(errors, [])
            self.assertEqual(store.verify()["event_count"], 3)
            self.assertEqual(len(build_outbox_view(store)["items"]), 1)

    def test_transition_before_enqueue_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory(dir=self.temporary_root) as directory:
            store = self.store(directory)
            bad = EventInput(stream_id="outbox-stream:missing", actor_id="actor:local", event_type="outbox.observed", category="ACTION", foundation_version="foundation:1", goal_version="goal:2", privacy_class="privacy:owner", audience="audience:owner", purpose="purpose:outbox", occurred_at="2026-10-10T00:00:00Z", payload={"outbox_id": "outbox:missing", "request_id": "adapter-request:missing", "external_dispatch_enabled": False}, effect_state="OBSERVED", authority_ref="authority:local")
            with self.assertRaises(IntegrityError):
                store.append_outbox_stage(bad, outbox_id="outbox:missing", stage="OBSERVED")

    def test_stage_request_or_information_boundary_mismatch_never_commits(self) -> None:
        for variant in ("request", "boundary"):
            with self.subTest(variant=variant), tempfile.TemporaryDirectory(dir=self.temporary_root) as directory:
                store = self.store(directory)
                run = run_local_adapter(DeterministicEchoAdapter(), request())
                item = self.record(store, run)["items"][0]
                before = store.verify()
                bad = EventInput(
                    stream_id=f"outbox-stream:{run['request']['request_sha256']}",
                    actor_id="actor:local",
                    event_type="outbox.provider-accepted",
                    category="ACTION",
                    foundation_version="foundation:1",
                    goal_version="goal:2",
                    privacy_class="privacy:owner",
                    audience="audience:public" if variant == "boundary" else "audience:owner",
                    purpose="purpose:outbox",
                    occurred_at="2026-10-10T00:00:00Z",
                    payload={
                        "outbox_id": item["outbox_id"],
                        "request_id": "adapter-request:other" if variant == "request" else item["request_id"],
                        "acceptance_id": "acceptance:replay",
                        "external_dispatch_enabled": False,
                    },
                    effect_state="PROVIDER_ACCEPTED",
                    authority_ref="authority:local",
                )
                with self.assertRaises(IntegrityError):
                    store.append_outbox_stage(bad, outbox_id=item["outbox_id"], stage="PROVIDER_ACCEPTED")
                after = store.verify()
                self.assertTrue(after["valid"])
                self.assertEqual(after["event_count"], before["event_count"])
                self.assertEqual(after["head_hash"], before["head_hash"])

    def test_privileged_outbox_table_tampering_is_detected(self) -> None:
        with tempfile.TemporaryDirectory(dir=self.temporary_root) as directory:
            store = self.store(directory)
            self.record(store, run_local_adapter(DeterministicEchoAdapter(), request()))
            with closing(sqlite3.connect(store.path)) as connection, connection:
                connection.execute("DROP TRIGGER outbox_items_no_update")
                connection.execute("UPDATE outbox_items SET request_id='adapter-request:tampered'")
            result = store.verify()
            self.assertFalse(result["valid"])
            self.assertTrue(any("outbox item payload mismatch" in item for item in result["errors"]))

    def test_privileged_stage_rebinding_is_detected_after_trigger_restoration(self) -> None:
        with tempfile.TemporaryDirectory(dir=self.temporary_root) as directory:
            store = self.store(directory)
            self.record(store, run_local_adapter(DeterministicEchoAdapter(), request("one")), "idempotency:one")
            self.record(store, run_local_adapter(DeterministicEchoAdapter(), request("two")), "idempotency:two")
            before = store.verify()
            with closing(sqlite3.connect(store.path)) as connection, connection:
                rows = connection.execute(
                    "SELECT outbox_id,event_id FROM outbox_stages WHERE stage='OBSERVED' ORDER BY outbox_id"
                ).fetchall()
                self.assertEqual(len(rows), 2)
                connection.execute("DROP TRIGGER outbox_stages_no_delete")
                connection.execute("DELETE FROM outbox_stages WHERE stage='OBSERVED'")
                connection.executemany(
                    "INSERT INTO outbox_stages(outbox_id,stage,event_id) VALUES(?,'OBSERVED',?)",
                    [(rows[0][0], rows[1][1]), (rows[1][0], rows[0][1])],
                )
                connection.execute(
                    "CREATE TRIGGER outbox_stages_no_delete BEFORE DELETE ON outbox_stages "
                    "BEGIN SELECT RAISE(ABORT, 'hirc outbox stages are append-only'); END"
                )
            result = store.verify()
            self.assertEqual(result["event_count"], before["event_count"])
            self.assertEqual(result["head_hash"], before["head_hash"])
            self.assertFalse(result["valid"])
            self.assertTrue(any("outbox stage payload mismatch" in item for item in result["errors"]))

    def test_privileged_outbox_schema_weakening_is_detected(self) -> None:
        with tempfile.TemporaryDirectory(dir=self.temporary_root) as directory:
            store = self.store(directory)
            self.record(store, run_local_adapter(DeterministicEchoAdapter(), request()))
            with closing(sqlite3.connect(store.path)) as connection:
                rows = connection.execute(
                    "SELECT outbox_id,stage,event_id FROM outbox_stages ORDER BY outbox_id,stage"
                ).fetchall()
                connection.execute("PRAGMA foreign_keys=OFF")
                connection.execute("DROP TABLE outbox_stages")
                connection.execute(
                    "CREATE TABLE outbox_stages (outbox_id TEXT NOT NULL, stage TEXT NOT NULL, event_id TEXT NOT NULL)"
                )
                connection.executemany(
                    "INSERT INTO outbox_stages(outbox_id,stage,event_id) VALUES(?,?,?)", rows
                )
                connection.execute(
                    "CREATE TRIGGER outbox_stages_no_update BEFORE UPDATE ON outbox_stages "
                    "BEGIN SELECT RAISE(ABORT, 'hirc outbox stages are append-only'); END"
                )
                connection.execute(
                    "CREATE TRIGGER outbox_stages_no_delete BEFORE DELETE ON outbox_stages "
                    "BEGIN SELECT RAISE(ABORT, 'hirc outbox stages are append-only'); END"
                )
                connection.commit()
            result = store.verify()
            self.assertFalse(result["valid"])
            self.assertIn("store schema object set mismatch", result["errors"])

    def test_external_dispatch_flag_is_rejected_by_projection(self) -> None:
        with tempfile.TemporaryDirectory(dir=self.temporary_root) as directory:
            store = self.store(directory)
            self.record(store, run_local_adapter(DeterministicEchoAdapter(), request()))
            with closing(sqlite3.connect(store.path)) as connection, connection:
                connection.execute("DROP TRIGGER events_no_update")
                connection.execute("UPDATE events SET payload_json=replace(payload_json, 'false', 'true') WHERE event_type='outbox.enqueued'")
            with self.assertRaises(OutboxError):
                build_outbox_view(store)

    def test_reopen_reproduces_outbox_view(self) -> None:
        with tempfile.TemporaryDirectory(dir=self.temporary_root) as directory:
            store = self.store(directory)
            self.record(store, run_local_adapter(DeterministicEchoAdapter(), request()))
            self.assertEqual(build_outbox_view(store), build_outbox_view(Store(store.path)))

    def test_cli_records_and_reads_the_same_outbox(self) -> None:
        with tempfile.TemporaryDirectory(dir=self.temporary_root) as directory:
            root = Path(directory)
            store = self.store(directory)
            source = root / "adapter.json"
            source.write_text(json.dumps({
                "actor_id": "actor:local", "task_id": "task:hirc", "admission_ref": "admission:recorded",
                "foundation_version": "foundation:1", "goal_version": "goal:2", "privacy_class": "privacy:owner",
                "audience": "audience:owner", "purpose": "purpose:outbox", "requested_at": "time:20261010T000000Z",
                "capability": "capability:local-transform", "payload": {"text": "cli"}
            }), encoding="utf-8")
            output = io.StringIO()
            with redirect_stdout(output):
                code = main(["--db", str(store.path), "outbox-record", "--input", str(source), "--idempotency-key", "idempotency:cli", "--authority-ref", "authority:local", "--occurred-at", "2026-10-10T00:00:00Z"])
            self.assertEqual(code, 0)
            recorded = json.loads(output.getvalue())
            output = io.StringIO()
            with redirect_stdout(output):
                code = main(["--db", str(store.path), "outbox"])
            self.assertEqual(code, 0)
            self.assertEqual(json.loads(output.getvalue()), recorded)


if __name__ == "__main__":
    unittest.main()

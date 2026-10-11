#!/usr/bin/env python3
"""Reproduce M08-S004 keyed external head-witness checks."""

from __future__ import annotations

import hashlib
import io
import json
import sqlite3
import sys
import tempfile
import unittest
from contextlib import closing
from pathlib import Path

from validation_config import EXPECTED_RELEASE_FAILURES, FULL_SUITE_TESTS, WITNESS_TESTS


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from hirc.store import EventInput, Store  # noqa: E402
from hirc.witness import WitnessError, create_head_witness, verify_head_witness  # noqa: E402


OUTPUT = ROOT / "implementation/m08-s004-validation.json"
FILES = (
    "implementation/M08_RELEASE_HARDENING_PLAN.md",
    "implementation/README.md",
    "src/hirc/witness.py",
    "src/hirc/cli.py",
    "tests/test_witness.py",
    "tests/test_known_limits.py",
)
KEY = b"validation-key-material-32-bytes!"


def identity(relative: str) -> dict[str, object]:
    body = (ROOT / relative).read_bytes()
    return {"path": relative, "sha256": hashlib.sha256(body).hexdigest(), "bytes": len(body)}


def main() -> int:
    witness_stream = io.StringIO()
    witness_suite = unittest.defaultTestLoader.discover(str(ROOT / "tests"), pattern="test_witness.py")
    witness_tests = unittest.TextTestRunner(stream=witness_stream, verbosity=2).run(witness_suite)
    full_stream = io.StringIO()
    full_suite = unittest.defaultTestLoader.discover(str(ROOT / "tests"))
    full_tests = unittest.TextTestRunner(stream=full_stream, verbosity=1).run(full_suite)

    temp_root = ROOT / "tests/.tmp"; temp_root.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(dir=temp_root) as directory:
        store=Store(Path(directory)/"witness.sqlite3"); store.initialize()
        base=dict(actor_id="actor:validator",category="EVIDENCE",foundation_version="foundation:1",goal_version="goal:1",privacy_class="privacy:owner",audience="audience:owner",purpose="purpose:witness-validation",occurred_at="2026-10-10T00:00:00Z")
        store.append(EventInput(stream_id="note:one",event_type="note.recorded",payload={"index":1},**base))
        store.append(EventInput(stream_id="note:two",event_type="note.recorded",payload={"index":2},**base))
        path=Path(directory)/"head.json"; created=create_head_witness(store,path,KEY); verified=verify_head_witness(store,path,KEY)
        with closing(sqlite3.connect(store.path)) as connection, connection:
            connection.execute("DROP TRIGGER events_no_delete"); connection.execute("DELETE FROM events WHERE sequence=2"); connection.execute("CREATE TRIGGER events_no_delete BEFORE DELETE ON events BEGIN SELECT RAISE(ABORT, 'hirc events are append-only'); END")
        chain_alone_valid=store.verify()["valid"]
        try: verify_head_witness(store,path,KEY)
        except WitnessError: truncation_detected=True
        else: truncation_detected=False
    checks={
        "witness_tests_pass":witness_tests.wasSuccessful(),
        "witness_test_count":witness_tests.testsRun==WITNESS_TESTS,
        "full_suite_pass":full_tests.wasSuccessful(),
        "full_suite_test_count":full_tests.testsRun==FULL_SUITE_TESTS,
        "three_expected_release_failures":len(full_tests.expectedFailures)==EXPECTED_RELEASE_FAILURES,
        "witness_created_and_verified":created["event_count"]==2 and verified["valid"],
        "tail_chain_locally_self_consistent":chain_alone_valid,
        "external_witness_detects_truncation":truncation_detected,
        "key_not_stored":created["key_stored"] is False and verified["key_stored"] is False,
        "public_signature_not_claimed":verified["independent_public_signature"] is False,
    }
    result={
        "schema":"hirc.m08-s004-validation/1","stone":"M08-S004","status":"PASS_TOOLING_SCOPE_KEY_CUSTODY_INTEGRATION_HELD" if all(checks.values()) else "FAIL",
        "checks":checks,"files":[identity(path) for path in FILES],"witness_test_output":witness_stream.getvalue().splitlines(),"full_suite_output":full_stream.getvalue().splitlines(),
        "control":{"created":created,"verified":verified,"tail_chain_valid_without_witness":chain_alone_valid,"truncation_detected_with_witness":truncation_detected},
        "surviving_limits":["No witness key is generated, stored, escrowed or distributed; operational key custody remains open.","HMAC is symmetric and does not provide an independently verifiable public signature.","Witness creation is not automatically required for every store mutation or backup; release integration remains open."],
        "nonclaim":"M08-S004 keyed local witness tooling only; not deployed anti-rollback assurance or public release signing."
    }
    OUTPUT.write_text(json.dumps(result,indent=2)+"\n",encoding="utf-8",newline="\n"); print(json.dumps(result,indent=2)); return 0 if result["status"].startswith("PASS_") else 1


if __name__=="__main__": raise SystemExit(main())

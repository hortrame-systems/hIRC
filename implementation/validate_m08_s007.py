#!/usr/bin/env python3
"""Bounded local soak plus abrupt child-process transaction rollback probe."""

from __future__ import annotations

import hashlib, json, subprocess, sys, tempfile, time
from dataclasses import replace
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
OUTPUT = ROOT / "implementation/m08-s007-validation.json"

from hirc.recovery import backup_store, restore_store
from hirc.store import EventInput, Store


def identity(path: str) -> dict:
    body = (ROOT / path).read_bytes()
    return {"path": path, "sha256": hashlib.sha256(body).hexdigest(), "bytes": len(body)}


def main() -> int:
    temp_root = ROOT / "tests/.tmp"
    temp_root.mkdir(parents=True, exist_ok=True)
    checkpoints = []
    with tempfile.TemporaryDirectory(dir=temp_root) as directory:
        root = Path(directory)
        store = Store(root / "soak.sqlite3")
        store.initialize()
        base = EventInput(stream_id="soak:0", actor_id="actor:soak", event_type="note.recorded", category="EVIDENCE", foundation_version="foundation:1", goal_version="goal:1", privacy_class="privacy:owner", audience="audience:owner", purpose="purpose:soak", occurred_at="2026-10-10T00:00:00Z", payload={"index": 0})
        started = time.perf_counter()
        for index in range(500):
            store.append(replace(base, stream_id=f"soak:{index}", payload={"index": index, "value": "x" * (index % 257)}))
            if index + 1 in {100, 250, 500}:
                state = Store(store.path).verify(read_only=True)
                checkpoints.append({"events": index + 1, "valid": state["valid"], "head_hash": state["head_hash"]})
        append_elapsed = time.perf_counter() - started
        before = store.verify(read_only=True)
        crash_code = "import os,sqlite3,sys;c=sqlite3.connect(sys.argv[1]);c.execute('BEGIN IMMEDIATE');c.execute('DROP TRIGGER events_no_update');c.execute(\"UPDATE events SET purpose='purpose:uncommitted-crash' WHERE sequence=1\");os._exit(91)"
        crashed = subprocess.run([sys.executable, "-B", "-c", crash_code, str(store.path)], cwd=ROOT, timeout=30)
        after = Store(store.path).verify(read_only=True)
        backup = root / "soak.backup.sqlite3"
        restored = root / "soak.restored.sqlite3"
        backup_result = backup_store(store.path, backup)
        restore_result = restore_store(backup, restored)
        restored_state = Store(restored).verify(read_only=True)
    checks = {
        "five_hundred_events_valid": before["valid"] and before["event_count"] == 500,
        "all_reopen_checkpoints_valid": all(item["valid"] for item in checkpoints),
        "child_exited_abruptly": crashed.returncode == 91,
        "uncommitted_transaction_rolled_back": after == before,
        "backup_restore_head_matches": backup_result["head_hash"] == restore_result["head_hash"] == restored_state["head_hash"],
        "restored_count_matches": restored_state["event_count"] == 500,
    }
    result = {
        "schema": "hirc.m08-s007-validation/1",
        "stone": "M08-S007",
        "status": "PASS_BOUNDED_LOCAL_SOAK_CRASH_SCOPE" if all(checks.values()) else "FAIL",
        "checks": checks,
        "files": [identity("implementation/M08_RELEASE_HARDENING_PLAN.md"), identity("implementation/validate_m08_s007.py")],
        "metrics": {"events": 500, "append_and_checkpoint_seconds": append_elapsed, "checkpoints": checkpoints},
        "surviving_limits": [
            "Abrupt process exit is not physical power loss or storage-controller failure.",
            "Five hundred events and one local run are not a long-duration production soak or throughput guarantee.",
            "Cross-machine, encrypted live-store and independent security review remain open."
        ],
        "nonclaim": "M08-S007 bounded Windows-local soak and rollback evidence only."
    }
    OUTPUT.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps(result, indent=2))
    return 0 if result["status"].startswith("PASS_") else 1


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Record S015 PASS after the public content and receipt commits were observed."""

from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REGISTER = ROOT / "review/milestone-03-stone-register.json"
RECEIPT = ROOT / "review/public/m03-s015-public-push-receipt-v1.json"
CLOSURE = ROOT / "review/public/m03-s015-final-closure-v1.json"
EXPECTED_HEAD = "cc4af0dbd6c02cedf49ed1ea1e3da30732e0a4cf"


def ref(path: Path) -> dict[str, object]:
    body = path.read_bytes()
    return {"path": path.relative_to(ROOT).as_posix(), "sha256": hashlib.sha256(body).hexdigest(), "bytes": len(body)}


def main() -> None:
    head = subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT, check=True, capture_output=True, text=True).stdout.strip()
    receipt = json.loads(RECEIPT.read_text(encoding="utf-8"))
    closure = json.loads(CLOSURE.read_text(encoding="utf-8"))
    if head != EXPECTED_HEAD or receipt.get("status") != "CONTENT_COMMIT_REMOTE_VERIFIED" or closure.get("status") != "PASS" or closure.get("receipt_commit") != head or not closure.get("remote_observation", {}).get("matched_receipt_commit"):
        raise SystemExit("public content/receipt prerequisite mismatch")
    value = json.loads(REGISTER.read_text(encoding="utf-8"))
    by_id = {item["id"]: item for item in value["stones"]}
    if by_id["M03-S014"]["status"] != "PASS" or by_id["M03-S015"]["status"] not in {"READY", "PASS"}:
        raise SystemExit("S015 prerequisite/state mismatch")
    by_id["M03-S015"]["status"] = "PASS"
    by_id["M03-S015"]["result"] = {
        "content_commit": closure["content_commit"],
        "receipt_commit": closure["receipt_commit"],
        "receipt": ref(RECEIPT),
        "closure": ref(CLOSURE),
        "remote_verified": True,
    }
    value["status"] = "MILESTONE_03_PASS"
    value["execution_state"] = {
        "state": "COMPLETE",
        "ready_stones": [],
        "runnable_stones": [],
        "scoped_holds": [],
        "rule": value["execution_state"]["rule"],
    }
    REGISTER.write_bytes((json.dumps(value, indent=2, ensure_ascii=False) + "\n").encode("utf-8"))
    print(json.dumps({"status": value["status"], "S015": "PASS", "content_commit": closure["content_commit"], "receipt_commit": closure["receipt_commit"]}))


if __name__ == "__main__":
    main()

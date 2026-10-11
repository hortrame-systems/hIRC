#!/usr/bin/env python3
"""Advance M03-S014 to PASS from the exact integrated review closure."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REGISTER = ROOT / "review/milestone-03-stone-register.json"
CLOSURE = ROOT / "review/m03-s014-integrated-review-closure-v1.json"
VALIDATION = ROOT / "review/fixtures/m03-s014-integrated-review-closure-validation-v1.json"


def ref(path: Path) -> dict[str, object]:
    body = path.read_bytes()
    return {"path": path.relative_to(ROOT).as_posix(), "sha256": hashlib.sha256(body).hexdigest(), "bytes": len(body)}


def main() -> None:
    closure = json.loads(CLOSURE.read_text(encoding="utf-8"))
    validation = json.loads(VALIDATION.read_text(encoding="utf-8"))
    if closure.get("stone_decision") != "PASS" or validation.get("status") != "PASS":
        raise SystemExit("S014 closure is not validated PASS")
    value = json.loads(REGISTER.read_text(encoding="utf-8"))
    by_id = {item["id"]: item for item in value["stones"]}
    if by_id["M03-S013"]["status"] != "PASS" or by_id["M03-S014"]["status"] not in {"READY", "PASS"}:
        raise SystemExit("S014 prerequisite/state mismatch")
    by_id["M03-S014"]["status"] = "PASS"
    by_id["M03-S014"]["result"] = {
        "closure": ref(CLOSURE),
        "validation": ref(VALIDATION),
        "accepted_scope": "Integrated peer challenge and exact finding reconciliation only; release residuals preserved.",
    }
    by_id["M03-S015"]["status"] = "READY"
    value["status"] = "STONE_014_PASS_S015_READY"
    value["execution_state"] = {
        "state": "RUNNABLE",
        "ready_stones": ["M03-S015"],
        "runnable_stones": ["M03-S015"],
        "scoped_holds": [],
        "rule": value["execution_state"]["rule"],
    }
    REGISTER.write_bytes((json.dumps(value, indent=2, ensure_ascii=False) + "\n").encode("utf-8"))
    print(json.dumps({"status": value["status"], "S014": "PASS", "S015": "READY"}))


if __name__ == "__main__":
    main()

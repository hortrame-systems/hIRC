#!/usr/bin/env python3
"""Validate the exact COTANGENT outcome-blind orientation assignment."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ENV_ROOT = ROOT.parent
SOURCE = ROOT / "review" / "m03-s014-security-blind-orientation-assignment-v1.json"
READINESS = ENV_ROOT / "runtime" / "agents" / "COTANGENT" / "checkpoints" / "5096e7cdb27447018f94e12eab1c9d39.json"


def identity(path: Path, display: str) -> dict:
    body = path.read_bytes(); return {"path": display, "sha256": hashlib.sha256(body).hexdigest(), "bytes": len(body)}


def main() -> int:
    parser = argparse.ArgumentParser(); parser.add_argument("--output"); args = parser.parse_args()
    assignment = json.loads(SOURCE.read_text(encoding="utf-8")); outer = json.loads(READINESS.read_text(encoding="utf-8")); readiness = json.loads(outer["text"])
    checks = []
    orientation = ROOT / assignment["orientation"]["path"]
    validation_path = ROOT / assignment["orientation_validation"]["path"]
    validation = json.loads(validation_path.read_text(encoding="utf-8"))
    checks.append({"name": "orientation-frame", "pass": assignment["orientation"] == identity(orientation, assignment["orientation"]["path"]) and assignment["orientation_validation"] == identity(validation_path, assignment["orientation_validation"]["path"]) and validation.get("status") == "PASS" and validation.get("checks", [])[2].get("observed") == [], "observed": assignment["orientation"]})
    checks.append({"name": "own-readiness", "pass": outer.get("actor") == "COTANGENT" and assignment["readiness"] == identity(READINESS, assignment["readiness"]["path"]) and readiness.get("state") == "READY_FOR_HIRC_BLIND_ORIENTATION" and readiness.get("education", {}).get("pending") == 0 and readiness.get("education", {}).get("source_holds") == [], "observed": assignment["readiness"]})
    capacity = assignment["capacity"]; floor = (capacity["capacity"] * capacity["hirc_retirement_floor_percent"] + 99) // 100
    checks.append({"name": "fresh-bounded-capacity", "pass": capacity["runway_state"] == "CLEAR" and capacity["bounded_owned_chunk_fits"] is True and capacity["remaining"] > floor + capacity["orientation_tokens"] + capacity["handoff_tokens"], "observed": {"floor": floor, **capacity}})
    checks.append({"name": "consent-and-exposure", "pass": assignment["consent"] == "EXACT_SECURITY_BLIND_ORIENTATION_ACCEPTED" and readiness.get("consent", "").startswith("I consent to the bounded blind-orientation") and len(assignment["known_exposure_limits"]) >= 4, "observed": assignment["known_exposure_limits"]})
    body = assignment["body_access"]
    checks.append({"name": "orientation-only-boundary", "pass": body == {"orientation": True, "stage_a": False, "stage_b": False, "linked_targets": False, "read_only": True} and all(assignment["prohibited"].values()), "observed": {"body_access": body, "prohibited": assignment["prohibited"]}})
    result = {"schema": "hirc.m03-s014-security-blind-orientation-assignment-validation/1", "status": "PASS" if all(item["pass"] for item in checks) else "FAIL", "assignment": identity(SOURCE, "review/m03-s014-security-blind-orientation-assignment-v1.json"), "checks": checks, "nonclaim": "Deterministic orientation gate validation only; not Stage A/B access, performed review or S014 acceptance."}
    rendered=json.dumps(result,indent=2)+"\n"
    if args.output:(ROOT/args.output).write_text(rendered,encoding="utf-8",newline="\n")
    print(rendered,end="");return 0 if result["status"]=="PASS" else 1


if __name__=="__main__":raise SystemExit(main())

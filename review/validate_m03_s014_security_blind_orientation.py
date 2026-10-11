#!/usr/bin/env python3
"""Validate that the security Stage A orientation preserves outcome blindness."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PACKET_PATH = "review/m03-s014-specialist-review-packets-v1.json"
ORIENTATION_PATH = "implementation/orientation/hirc-security-stage-a-blind-orientation-20261010-v1.md"
EXPECTED_PACKET_SHA = "b2b141c5caf9c6282442f6bad47f3bf38d3da6013d0125e0b71e012c9d2691f5"


def identity(path: str) -> dict:
    body = (ROOT / path).read_bytes()
    return {"path": path, "sha256": hashlib.sha256(body).hexdigest(), "bytes": len(body)}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output")
    args = parser.parse_args()

    packet_id = identity(PACKET_PATH)
    packet = json.loads((ROOT / PACKET_PATH).read_text(encoding="utf-8"))
    text = (ROOT / ORIENTATION_PATH).read_text(encoding="utf-8")
    lane = next(item for item in packet["lanes"] if item["lane"] == "security_privacy_dataflow")

    checks = []
    checks.append({"name": "frozen-packet", "pass": packet_id["sha256"] == EXPECTED_PACKET_SHA, "observed": packet_id})
    stage_a_errors = []
    for item in lane["stage_a_independent_inputs"]:
        row = f"| `{item['path']}` | `{item['sha256']}` | {item['bytes']:,} |"
        if text.count(row) != 1:
            stage_a_errors.append(item["path"])
    checks.append({"name": "exact-stage-a-rows", "pass": not stage_a_errors, "observed": {"count": len(lane["stage_a_independent_inputs"]), "errors": stage_a_errors}})

    disclosed_paths = [item["path"] for item in lane["stage_b_disclosed_evidence"]]
    leaked = [path for path in disclosed_paths if path in text]
    checks.append({"name": "no-stage-b-paths", "pass": not leaked, "observed": leaked})

    outcome_markers = [
        "135 source-tree tests",
        "expected release failures",
        "PASS_WITH_DECLARED",
        "controller preliminary finding",
        "security repair",
        "current-description-20261010",
        "LOCAL-DEVELOPER-PACKAGE-CHECKPOINT",
    ]
    present_markers = [marker for marker in outcome_markers if marker in text]
    checks.append({"name": "no-outcome-markers", "pass": not present_markers, "observed": present_markers})

    missing_questions = [question for question in lane["questions"] if text.count(question) != 1]
    missing_return = [item for item in lane["required_return"] if text.count(item) != 1]
    checks.append({"name": "questions-and-return", "pass": not missing_questions and not missing_return, "observed": {"missing_questions": missing_questions, "missing_return": missing_return}})

    controls = [
        "grants no body access by itself",
        "separate exact assignment",
        "before freezing the Stage A report",
        "disclose the exposure and stop",
        "not qualification, assignment, body access",
    ]
    missing_controls = [item for item in controls if item not in text]
    checks.append({"name": "gate-language", "pass": not missing_controls, "observed": missing_controls})

    result = {
        "schema": "hirc.m03-s014-security-blind-orientation-validation/1",
        "status": "PASS" if all(item["pass"] for item in checks) else "FAIL",
        "orientation": identity(ORIENTATION_PATH),
        "checks": checks,
        "nonclaim": "Deterministic outcome-blind preparation check only; not reviewer qualification, assignment, body access, independence proof or S014 acceptance.",
    }
    rendered = json.dumps(result, indent=2) + "\n"
    if args.output:
        (ROOT / args.output).write_text(rendered, encoding="utf-8", newline="\n")
    print(rendered, end="")
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Validate the completed Stage A assignment after its reviewed sources advance."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ENV_ROOT = ROOT.parent
ASSIGNMENT = ROOT / "review" / "m03-s014-metric-stage-a-assignment-v1.json"
ORIGINAL_VALIDATION = ROOT / "review" / "fixtures" / "m03-s014-metric-stage-a-assignment-validation-v1.json"
REPORT_VALIDATION = ROOT / "review" / "fixtures" / "m03-s014-metric-stage-a-report-validation-v1.json"
EXPECTED_ASSIGNMENT_SHA = "cc82e2059b2314ac835ea6989ae48efcb9c30db499b8141a0fbb58404ebb0d5e"
EXPECTED_VALIDATION_SHA = "31546dd82effc636a7a66f85ebfe3724c3dbf6af59ba7d5ac3246b247d944699"
EXPECTED_DRIFT = ["drafts/hirc_requirements_v1_1-draft.json", "review/revision-map-addendum-bayesian-trust-v1.json"]


def digest(path: Path) -> str: return hashlib.sha256(path.read_bytes()).hexdigest()
def identity(path: Path, base: Path = ROOT) -> dict: return {"path": path.relative_to(base).as_posix(), "sha256": digest(path), "bytes": path.stat().st_size}


def main() -> int:
    parser = argparse.ArgumentParser(); parser.add_argument("--output"); args = parser.parse_args()
    assignment = json.loads(ASSIGNMENT.read_text(encoding="utf-8"))
    original = json.loads(ORIGINAL_VALIDATION.read_text(encoding="utf-8"))
    drift = []
    missing = []
    for expected in assignment["lane"]["stage_a"]["inputs"]:
        path = ROOT / expected["path"]
        if not path.is_file(): missing.append(expected["path"])
        elif digest(path) != expected["sha256"] or path.stat().st_size != expected["bytes"]: drift.append(expected["path"])
    evidence_ok = True
    for expected in assignment["lane"]["evidence"]:
        path = ENV_ROOT / expected["path"]
        evidence_ok = evidence_ok and path.is_file() and digest(path) == expected["sha256"] and path.stat().st_size == expected["bytes"]
    checks = {
        "assignment_frozen": digest(ASSIGNMENT) == EXPECTED_ASSIGNMENT_SHA,
        "original_pass_receipt_preserved": digest(ORIGINAL_VALIDATION) == EXPECTED_VALIDATION_SHA and original.get("status") == "PASS",
        "only_declared_repair_sources_advanced": sorted(set(drift)) == EXPECTED_DRIFT,
        "no_historical_source_missing": not missing,
        "own_gate_evidence_preserved": evidence_ok,
        "stage_a_report_frozen_and_valid": json.loads(REPORT_VALIDATION.read_text(encoding="utf-8")).get("status") == "PASS",
    }
    result = {"schema": "hirc.m03-s014-metric-stage-a-assignment-history-validation/1", "status": "PASS" if all(checks.values()) else "FAIL", "assignment": identity(ASSIGNMENT), "original_validation": identity(ORIGINAL_VALIDATION), "current_source_drift": sorted(set(drift)), "missing_sources": sorted(set(missing)), "checks": checks, "nonclaim": "Historical assignment preservation after completed review; not a current admission, repair recheck or S014 acceptance."}
    rendered = json.dumps(result, indent=2) + "\n"
    if args.output: (ROOT / args.output).write_text(rendered, encoding="utf-8", newline="\n")
    print(rendered, end="")
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__": raise SystemExit(main())

#!/usr/bin/env python3
"""Validate the frozen specialist packet after its reviewed targets legitimately advance."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PACKET_PATH = ROOT / "review" / "m03-s014-specialist-review-packets-v1.json"
VIEW_PATH = ROOT / "review" / "m03-s014-specialist-review-packets-v1.md"
ORIENTATION_COPY = ROOT / "implementation" / "orientation" / "hirc-specialist-review-packets-20261010-v4.json"
ORIGINAL_VALIDATION = ROOT / "review" / "fixtures" / "m03-s014-specialist-review-packets-validation-v1.json"
EXPECTED_PACKET_SHA = "b2b141c5caf9c6282442f6bad47f3bf38d3da6013d0125e0b71e012c9d2691f5"
EXPECTED_VALIDATION_SHA = "bda29c17ad5c83fe95ac38e0b23b12fd9c882f1b73420fd609a39687ebbce350"
EXPECTED_ADVANCED_PATHS = [
    "drafts/hirc_requirements_v1_1-draft.json",
    "review/revision-map-addendum-bayesian-trust-v1.json",
]


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def identity(path: Path) -> dict:
    return {"path": path.relative_to(ROOT).as_posix(), "sha256": digest(path), "bytes": path.stat().st_size}


def main() -> int:
    parser = argparse.ArgumentParser(); parser.add_argument("--output"); args = parser.parse_args()
    packet = json.loads(PACKET_PATH.read_text(encoding="utf-8"))
    original_validation = json.loads(ORIGINAL_VALIDATION.read_text(encoding="utf-8"))
    source_rows = [item for lane in packet["lanes"] for stage in ("stage_a_independent_inputs", "stage_b_disclosed_evidence") for item in lane[stage]]
    drift = []
    missing = []
    for expected in source_rows:
        path = ROOT / expected["path"]
        if not path.is_file():
            missing.append(expected["path"]); continue
        if digest(path) != expected["sha256"] or path.stat().st_size != expected["bytes"]:
            drift.append(expected["path"])
    checks = {
        "packet_identity_frozen": digest(PACKET_PATH) == EXPECTED_PACKET_SHA,
        "orientation_copy_same_bytes": ORIENTATION_COPY.read_bytes() == PACKET_PATH.read_bytes(),
        "original_pass_receipt_preserved": digest(ORIGINAL_VALIDATION) == EXPECTED_VALIDATION_SHA and original_validation.get("status") == "PASS",
        "readable_view_retained": VIEW_PATH.is_file() and "security_privacy_dataflow" in VIEW_PATH.read_text(encoding="utf-8") and "metric_evaluator" in VIEW_PATH.read_text(encoding="utf-8"),
        "no_missing_historical_sources": not missing,
        "only_declared_post_review_source_advanced": sorted(set(drift)) == EXPECTED_ADVANCED_PATHS,
        "stage_a_report_validation_pass": json.loads((ROOT / "review/fixtures/m03-s014-metric-stage-a-report-validation-v1.json").read_text(encoding="utf-8")).get("status") == "PASS",
        "stage_b_report_validation_pass": json.loads((ROOT / "review/fixtures/m03-s014-metric-stage-b-report-validation-v1.json").read_text(encoding="utf-8")).get("status") == "PASS",
    }
    result = {
        "schema": "hirc.m03-s014-specialist-packet-history-validation/1",
        "status": "PASS" if all(checks.values()) else "FAIL",
        "packet": identity(PACKET_PATH),
        "original_validation": identity(ORIGINAL_VALIDATION),
        "current_source_drift": sorted(set(drift)),
        "missing_sources": sorted(set(missing)),
        "checks": checks,
        "nonclaim": "Historical packet preservation and expected post-review drift check only; not a current packet rebuild, security review, repair recheck or S014 acceptance.",
    }
    rendered = json.dumps(result, indent=2) + "\n"
    if args.output: (ROOT / args.output).write_text(rendered, encoding="utf-8", newline="\n")
    print(rendered, end="")
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__": raise SystemExit(main())

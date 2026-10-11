#!/usr/bin/env python3
"""Validate exact staged M03-S014 specialist review packets."""

from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "review"))
from build_m03_s014_specialist_packets import packet, render  # noqa: E402


SOURCE = ROOT / "review/m03-s014-specialist-review-packets-v1.json"
VIEW = ROOT / "review/m03-s014-specialist-review-packets-v1.md"
OUTPUT = ROOT / "review/fixtures/m03-s014-specialist-review-packets-validation-v1.json"


def main() -> int:
    actual = json.loads(SOURCE.read_text(encoding="utf-8"))
    expected = packet()
    errors: list[str] = []
    if actual != expected:
        errors.append("packet-drift")
    if VIEW.read_text(encoding="utf-8") != render(actual):
        errors.append("readable-view-drift")
    lanes = {lane.get("lane"): lane for lane in actual.get("lanes", [])}
    if set(lanes) != {"security_privacy_dataflow", "metric_evaluator"}:
        errors.append("lane-set")
    for name, lane in lanes.items():
        stage_a = [item.get("path") for item in lane.get("stage_a_independent_inputs", [])]
        stage_b = [item.get("path") for item in lane.get("stage_b_disclosed_evidence", [])]
        if not stage_a or not stage_b or len(stage_a) != len(set(stage_a)) or len(stage_b) != len(set(stage_b)):
            errors.append(f"stage-membership:{name}")
        if set(stage_a) & set(stage_b):
            errors.append(f"stage-overlap:{name}")
        if lane.get("assignment_state") != "UNASSIGNED_QUALIFIED_REVIEWER_REQUIRED" or lane.get("body_access_granted") is not False:
            errors.append(f"assignment-boundary:{name}")
        if len(lane.get("questions", [])) < 7 or len(lane.get("required_return", [])) < 6:
            errors.append(f"coverage:{name}")
    security = lanes.get("security_privacy_dataflow", {})
    security_a = {item.get("path") for item in security.get("stage_a_independent_inputs", [])}
    if not {"src/hirc/store.py", "src/hirc/canonical.py", "src/hirc/witness.py", "dist/hirc-local-0.1.0.dev0-manifest.json"} <= security_a:
        errors.append("security-core")
    if any("validation" in path or "failed" in path or path.startswith("tests/") for path in security_a):
        errors.append("security-stage-a-prior-findings")
    metric = lanes.get("metric_evaluator", {})
    metric_a = {item.get("path") for item in metric.get("stage_a_independent_inputs", [])}
    if not {"review/cultural-environment-quality-measures-v1.json", "review/contracts/hirc-bayesian-reliance.candidate.schema.v2.json", "drafts/hirc_requirements_v1_1-draft.json"} <= metric_a:
        errors.append("metric-core")
    cumulative = json.loads((ROOT / "implementation/executable-cumulative-validation.json").read_text(encoding="utf-8"))
    if cumulative.get("status") != "PASS_WITH_DECLARED_RELEASE_HOLDS" or cumulative.get("validator_count") != 21 or cumulative.get("full_suite_tests") != 135 or cumulative.get("expected_release_failures") != 3:
        errors.append("executable-frame")
    gate = actual.get("eligibility_gate", {})
    if gate.get("body_access_before_gate") is not False or gate.get("automatic_qualification") is not False or len(gate.get("all_required", [])) < 7:
        errors.append("eligibility-gate")
    result = {
        "schema": "hirc.m03-s014-specialist-review-packets-validation/1",
        "status": "PASS" if not errors else "FAIL",
        "errors": errors,
        "lane_counts": {
            name: {
                "stage_a": len(lane.get("stage_a_independent_inputs", [])),
                "stage_b": len(lane.get("stage_b_disclosed_evidence", [])),
                "questions": len(lane.get("questions", [])),
            }
            for name, lane in lanes.items()
        },
        "nonclaim": "Exact staged packet validation only; not reviewer readiness, performed review, S014 acceptance or release.",
    }
    OUTPUT.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps(result, indent=2))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())

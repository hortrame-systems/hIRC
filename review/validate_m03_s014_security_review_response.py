#!/usr/bin/env python3
"""Validate the security response's exact pins, finding coverage and open gates."""

from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "review/m03-s014-security-review-response-v1.json"
OUTPUT = ROOT / "review/fixtures/m03-s014-security-review-response-validation-v1.json"
EXPECTED_FINDINGS = {"SA-COT-F1", "SA-COT-F2", "SA-COT-F3"}


def errors(value: dict) -> list[str]:
    found: list[str] = []
    if value.get("status") != "CONTROLLER_REPAIR_COMPLETE_DISCLOSED_PEER_RECHECK_REQUIRED":
        found.append("status")
    if value.get("s014_state") != "OPEN" or value.get("s015_state") != "HELD":
        found.append("premature-gate")
    findings = value.get("findings", [])
    if {item.get("id") for item in findings} != EXPECTED_FINDINGS:
        found.append("finding-coverage")
    for item in findings:
        if item.get("controller_disposition") != "REPAIRED_PENDING_DISCLOSED_PEER_RECHECK":
            found.append(f"disposition:{item.get('id')}")
    for field in ("validation", "validator", "preserved_failure"):
        item = value.get(field, {})
        path = ROOT / item.get("path", "")
        if not path.is_file():
            found.append(f"missing:{field}")
        else:
            body = path.read_bytes()
            if hashlib.sha256(body).hexdigest() != item.get("sha256") or len(body) != item.get("bytes"):
                found.append(f"drift:{field}")
    for finding in findings:
        for target in finding.get("targets", []):
            path_text = target.get("path", "")
            path = ROOT / path_text
            if not path.is_file():
                found.append(f"missing-target:{path_text}")
                continue
            body = path.read_bytes()
            if hashlib.sha256(body).hexdigest() != target.get("sha256") or len(body) != target.get("bytes"):
                found.append(f"target-drift:{path_text}")
    if not value.get("residuals") or "not independent security acceptance" not in value.get("nonclaim", ""):
        found.append("residual-or-nonclaim")
    return found


def main() -> int:
    value = json.loads(SOURCE.read_text(encoding="utf-8"))
    positive = errors(value)
    mutations = []
    cases = []
    changed = copy.deepcopy(value); changed["s014_state"] = "PASS"; cases.append(("premature_s014", changed, "premature-gate"))
    changed = copy.deepcopy(value); changed["findings"] = changed["findings"][:-1]; cases.append(("missing_finding", changed, "finding-coverage"))
    changed = copy.deepcopy(value); changed["findings"][0]["controller_disposition"] = "CLOSED"; cases.append(("self_closed", changed, "disposition:SA-COT-F1"))
    changed = copy.deepcopy(value); changed["findings"][0]["targets"][0]["sha256"] = "0" * 64; cases.append(("target_drift", changed, "target-drift:src/hirc/store.py"))
    changed = copy.deepcopy(value); changed["residuals"] = []; cases.append(("erased_residuals", changed, "residual-or-nonclaim"))
    for name, changed, expected in cases:
        observed = errors(changed)
        mutations.append({"name": name, "expected": expected, "errors": observed, "rejected": expected in observed})
    passed = not positive and all(item["rejected"] for item in mutations)
    result = {
        "schema": "hirc.m03-s014-security-review-response-validation/1",
        "status": "PASS" if passed else "FAIL",
        "source": "review/m03-s014-security-review-response-v1.json",
        "positive": {"accepted": not positive, "errors": positive},
        "adverse": mutations,
        "nonclaim": "Structural and exact-revision response validation only; disclosed peer recheck and all external/runtime gates remain open.",
    }
    OUTPUT.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({"status": result["status"], "positive_errors": positive, "adverse": len(mutations)}))
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Validate the SA-COF-F1 controller delta response."""

from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "review/m03-s014-security-review-response-v2.json"
OUTPUT = ROOT / "review/fixtures/m03-s014-security-review-response-v2-validation-v1.json"


def validate(value: dict) -> list[str]:
    errors: list[str] = []
    if value.get("status") != "NEW_LOW_AVAILABILITY_FINDING_REPAIRED_DELTA_RECHECK_REQUIRED" or value.get("s014_state") != "OPEN":
        errors.append("gate")
    if set(value.get("preserved_original_dispositions", {})) != {"SA-COT-F1", "SA-COT-F2", "SA-COT-F3"}:
        errors.append("original-coverage")
    finding = value.get("finding", {})
    if finding.get("id") != "SA-COF-F1" or finding.get("controller_disposition") != "REPAIRED_PENDING_EXACT_DELTA_RECHECK":
        errors.append("finding")
    for item in [value.get("prior_response", {}), value.get("recheck_validation", {}), *finding.get("targets", []), value.get("validation", {}).get("cumulative", {})]:
        path = ROOT / item.get("path", "")
        if not path.is_file():
            errors.append(f"missing:{item.get('path')}")
        else:
            body = path.read_bytes()
            if hashlib.sha256(body).hexdigest() != item.get("sha256") or len(body) != item.get("bytes"):
                errors.append(f"drift:{item.get('path')}")
    if value.get("validation", {}).get("validator_count") != 21 or "140 tests PASS" not in value.get("validation", {}).get("full_suite", ""):
        errors.append("validation")
    if len(value.get("residuals", [])) != 2 or "not reviewer closure" not in value.get("nonclaim", ""):
        errors.append("residuals-or-nonclaim")
    return errors


def main() -> int:
    value = json.loads(SOURCE.read_text(encoding="utf-8"))
    positive = validate(value)
    cases = []
    changed = copy.deepcopy(value); changed["s014_state"] = "PASS"; cases.append(("premature_s014", changed, "gate"))
    changed = copy.deepcopy(value); changed["preserved_original_dispositions"].pop("SA-COT-F3"); cases.append(("lost_original", changed, "original-coverage"))
    changed = copy.deepcopy(value); changed["finding"]["controller_disposition"] = "CLOSED"; cases.append(("self_closed", changed, "finding"))
    changed = copy.deepcopy(value); changed["finding"]["targets"][0]["sha256"] = "0" * 64; cases.append(("target_drift", changed, "drift:src/hirc/adapter.py"))
    changed = copy.deepcopy(value); changed["residuals"] = []; cases.append(("erased_residuals", changed, "residuals-or-nonclaim"))
    adverse = []
    for name, changed, expected in cases:
        observed = validate(changed)
        adverse.append({"name": name, "expected": expected, "errors": observed, "rejected": expected in observed})
    passed = not positive and all(item["rejected"] for item in adverse)
    result = {
        "schema": "hirc.m03-s014-security-review-response-v2-validation/1",
        "status": "PASS" if passed else "FAIL",
        "source": "review/m03-s014-security-review-response-v2.json",
        "positive": {"accepted": not positive, "errors": positive},
        "adverse": adverse,
        "nonclaim": "Exact delta-response structure and pins only; COFACTOR recheck, whole security/privacy acceptance and S014 remain open.",
    }
    OUTPUT.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({"status": result["status"], "positive_errors": positive, "adverse": len(adverse)}))
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())

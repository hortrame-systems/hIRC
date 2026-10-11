#!/usr/bin/env python3
"""Validate COFACTOR's exact SA-COF-F1 delta assignment."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "review/m03-s014-security-delta-recheck-assignment-cofactor-v1.json"
OUTPUT = ROOT / "review/fixtures/m03-s014-security-delta-recheck-assignment-cofactor-validation-v1.json"


def validate(value: dict, preflight_path: Path) -> list[str]:
    errors: list[str] = []
    if value.get("state") != "ADMITTED_READ_ONLY_FINDINGS_EXPOSED_DELTA_RECHECK" or value.get("reviewer") != "COFACTOR" or value.get("finding") != "SA-COF-F1":
        errors.append("assignment")
    preflight = value.get("preflight", {})
    body = preflight_path.read_bytes()
    if preflight.get("sha256") != hashlib.sha256(body).hexdigest() or preflight.get("bytes") != len(body) or preflight.get("consent") != "EXACT_SA_COF_F1_DELTA_RECHECK_ACCEPTED" or preflight.get("capacity", {}).get("fit") is not True:
        errors.append("preflight")
    if len(value.get("sources", [])) != 6:
        errors.append("source-set")
    for item in value.get("sources", []):
        path = ROOT / item.get("path", "")
        if not path.is_file():
            errors.append(f"missing:{item.get('path')}")
        else:
            observed = path.read_bytes()
            if hashlib.sha256(observed).hexdigest() != item.get("sha256") or len(observed) != item.get("bytes"):
                errors.append(f"drift:{item.get('path')}")
    if any(flag is not True for flag in value.get("prohibited", {}).values()):
        errors.append("prohibited-scope")
    if len(value.get("required_output", [])) != 6:
        errors.append("required-output")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--preflight", required=True)
    args = parser.parse_args()
    preflight = Path(args.preflight).resolve()
    value = json.loads(SOURCE.read_text(encoding="utf-8"))
    positive = validate(value, preflight)
    cases = []
    changed = copy.deepcopy(value); changed["finding"] = "SA-COT-F3"; cases.append(("scope_expansion", changed, "assignment"))
    changed = copy.deepcopy(value); changed["preflight"]["consent"] = "NONE"; cases.append(("no_consent", changed, "preflight"))
    changed = copy.deepcopy(value); changed["sources"] = changed["sources"][:-1]; cases.append(("missing_source", changed, "source-set"))
    changed = copy.deepcopy(value); changed["sources"][3]["sha256"] = "0" * 64; cases.append(("adapter_drift", changed, "drift:src/hirc/adapter.py"))
    changed = copy.deepcopy(value); changed["prohibited"]["hirc_write"] = False; cases.append(("write_grant", changed, "prohibited-scope"))
    adverse = []
    for name, changed, expected in cases:
        observed = validate(changed, preflight)
        adverse.append({"name": name, "expected": expected, "errors": observed, "rejected": expected in observed})
    passed = not positive and all(item["rejected"] for item in adverse)
    result = {"schema": "hirc.m03-s014-security-delta-recheck-assignment-cofactor-validation/1", "status": "PASS" if passed else "FAIL", "source": "review/m03-s014-security-delta-recheck-assignment-cofactor-v1.json", "positive": {"accepted": not positive, "errors": positive}, "adverse": adverse, "nonclaim": "Exact delta assignment validation only; not report completion, whole security/privacy acceptance or S014 closure."}
    OUTPUT.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({"status": result["status"], "positive_errors": positive, "adverse": len(adverse)}))
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())

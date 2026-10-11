#!/usr/bin/env python3
"""Validate integrated S014 review coverage, exact pins and scoped residuals."""

from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "review/m03-s014-integrated-review-closure-v1.json"
OUTPUT = ROOT / "review/fixtures/m03-s014-integrated-review-closure-validation-v1.json"
EXPECTED_BRANCHES = {"product_accessibility_requirements_anti_domination", "metric_evaluator", "security_privacy_dataflow"}
EXPECTED_SECURITY_FINDINGS = {"SA-COT-F1", "SA-COT-F2", "SA-COT-F3", "SA-COF-F1"}


def validate(value: dict) -> list[str]:
    errors: list[str] = []
    if value.get("status") != "PASS_AT_DECLARED_M03_REVIEW_SCOPE_RELEASE_HOLDS_PRESERVED" or value.get("stone_decision") != "PASS":
        errors.append("decision")
    branches = {item.get("name"): item for item in value.get("branches", [])}
    if set(branches) != EXPECTED_BRANCHES or any(not item.get("status", "").startswith("PASS_") for item in branches.values()):
        errors.append("branch-coverage")
    security = branches.get("security_privacy_dataflow", {})
    if set(security.get("closed_findings", [])) != EXPECTED_SECURITY_FINDINGS:
        errors.append("security-findings")
    if len(value.get("evidence", [])) != 9:
        errors.append("evidence-set")
    for item in value.get("evidence", []):
        path = ROOT / item.get("path", "")
        if not path.is_file():
            errors.append(f"missing:{item.get('path')}")
        else:
            body = path.read_bytes()
            if hashlib.sha256(body).hexdigest() != item.get("sha256") or len(body) != item.get("bytes"):
                errors.append(f"drift:{item.get('path')}")
    integrity = value.get("review_integrity", {})
    if "declared aggregate outcome exposure" not in integrity.get("findings_unexposed_security_first_pass", "") or "findings-exposed" not in integrity.get("repair_rechecks", ""):
        errors.append("independence")
    if len(value.get("residual_holds", [])) != 4 or "not S015 completion" not in value.get("nonclaim", ""):
        errors.append("residuals-or-nonclaim")
    if value.get("next_eligible") != "M03-S015":
        errors.append("next")
    return errors


def main() -> int:
    value = json.loads(SOURCE.read_text(encoding="utf-8"))
    positive = validate(value)
    cases = []
    changed = copy.deepcopy(value); changed["stone_decision"] = "HELD"; cases.append(("wrong_decision", changed, "decision"))
    changed = copy.deepcopy(value); changed["branches"] = changed["branches"][:-1]; cases.append(("missing_branch", changed, "branch-coverage"))
    changed = copy.deepcopy(value); changed["branches"][2]["closed_findings"] = changed["branches"][2]["closed_findings"][:-1]; cases.append(("missing_security_finding", changed, "security-findings"))
    changed = copy.deepcopy(value); changed["evidence"][0]["sha256"] = "0" * 64; cases.append(("evidence_drift", changed, "drift:review/waymark-m03-s014-product-recheck-v1.md"))
    changed = copy.deepcopy(value); changed["residual_holds"] = []; cases.append(("erased_residuals", changed, "residuals-or-nonclaim"))
    adverse = []
    for name, changed, expected in cases:
        observed = validate(changed)
        adverse.append({"name": name, "expected": expected, "errors": observed, "rejected": expected in observed})
    passed = not positive and all(item["rejected"] for item in adverse)
    result = {"schema": "hirc.m03-s014-integrated-review-closure-validation/1", "status": "PASS" if passed else "FAIL", "source": "review/m03-s014-integrated-review-closure-v1.json", "positive": {"accepted": not positive, "errors": positive}, "adverse": adverse, "nonclaim": "S014 evidence/coverage validation only; no S015, release, publication, production or Bridge effect."}
    OUTPUT.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({"status": result["status"], "positive_errors": positive, "adverse": len(adverse)}))
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Build the integrated M03-S014 review closure at its declared milestone scope."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "review/m03-s014-integrated-review-closure-v1.json"


def ref(path: str) -> dict[str, object]:
    body = (ROOT / path).read_bytes()
    return {"path": path, "sha256": hashlib.sha256(body).hexdigest(), "bytes": len(body)}


def main() -> None:
    value = {
        "schema": "hirc.m03-s014-integrated-review-closure/1",
        "id": "HIRC-M03-S014-INTEGRATED-REVIEW-CLOSURE-001",
        "status": "PASS_AT_DECLARED_M03_REVIEW_SCOPE_RELEASE_HOLDS_PRESERVED",
        "stone_decision": "PASS",
        "declared_outcome": "Obtain independent permanent-peer product, security, privacy and anti-domination challenge and reconcile every consequence-bearing finding or justified NO_CHANGE.",
        "evidence": [
            ref("review/waymark-m03-s014-product-recheck-v1.md"),
            ref("review/fixtures/m03-s014-metric-final-recheck-validation-v1.json"),
            ref("review/fixtures/m03-s014-security-stage-a-report-validation-v1.json"),
            ref("review/m03-s014-security-review-response-v1.json"),
            ref("review/fixtures/m03-s014-security-repair-recheck-cofactor-report-validation-v1.json"),
            ref("review/m03-s014-security-review-response-v2.json"),
            ref("review/fixtures/m03-s014-security-delta-recheck-cofactor-report-validation-v1.json"),
            ref("implementation/executable-cumulative-validation.json"),
            ref("review/joint-consensus-matrix-draft-v11.json"),
        ],
        "branches": [
            {
                "name": "product_accessibility_requirements_anti_domination",
                "status": "PASS_AT_CORRECTED_DESIGN_FRAME",
                "reviewer": "WAYMARK",
                "result": "Three material contract/portability findings were repaired and independently rechecked; valid approvals and residual runtime/usability limits remain visible.",
            },
            {
                "name": "metric_evaluator",
                "status": "PASS_AT_SYNTHETIC_CANDIDATE_CONTRACT_SCOPE",
                "reviewer": "COFACTOR",
                "result": "All metric findings close through resolver-backed v3.2, 2 positive and 27 adverse cases, matrix v11 and an immutable reviewer-correction record.",
            },
            {
                "name": "security_privacy_dataflow",
                "status": "PASS_AT_STATIC_LOCAL_SOURCE_INTEGRITY_SCOPE",
                "reviewers": ["COTANGENT", "COFACTOR"],
                "result": "COTANGENT's 17-source first pass produced SA-COT-F1/F2/F3. Controller repairs received a findings-exposed exact COFACTOR recheck, which closed the original three and found SA-COF-F1. The delta repair and final recheck close SA-COF-F1. Broader security/privacy assurance remains withheld.",
                "closed_findings": ["SA-COT-F1", "SA-COT-F2", "SA-COT-F3", "SA-COF-F1"],
            },
        ],
        "review_integrity": {
            "findings_unexposed_security_first_pass": "COTANGENT content-blind with declared aggregate outcome exposure; not statistically independent or outcome-unexposed.",
            "repair_rechecks": "COFACTOR explicitly findings-exposed, common-mode and limited to source-integrity invariants; no security/privacy specialist title or whole-lane authority inferred.",
            "plain_approval": "The declared S014 task is independent challenge and finding reconciliation. Those conditions now pass; withholding S014 despite closure would confuse release assurance with the stone's actual scope.",
        },
        "residual_holds": [
            "No empirical usability/accessibility or affected-party privacy outcome evidence.",
            "No deployed external witness custody, encrypted live store, physical durability, real multiuser audience enforcement or arbitrary adapter isolation assurance.",
            "No Bridge/network/penetration/cryptographic/production/publication/release assurance.",
            "The three declared expected release failures remain external truncation witnessing, encrypted-at-rest storage and independently verifiable package signing.",
        ],
        "scope_judgment": "These residuals govern later implementation and release gates. They do not negate that the required S014 peer challenge occurred and every material finding received an exact evidence-backed disposition.",
        "next_eligible": "M03-S015",
        "nonclaim": "S014 review closure only; not S015 completion, release readiness, Bridge activation, production, publication or absence of unknown vulnerabilities.",
    }
    OUTPUT.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(ref("review/m03-s014-integrated-review-closure-v1.json")))


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Validate the exact corrected security packet and its remaining review boundary."""

from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "review/m03-s014-security-repair-closure-v1.json"
OUTPUT = ROOT / "review/fixtures/m03-s014-security-repair-closure-validation-v1.json"
REQUIRED_PEER_STONES = {"M03-S014-SEC-R003", "M03-S014-SEC-R004", "M03-S014-SEC-R005"}
REQUIRED_RESIDUALS = {
    "external_authority_and_resolver_truth",
    "actual_consent_encryption_deletion_and_runtime_enforcement",
    "qualified_whole_packet_security_privacy_dataflow_review",
    "s014_acceptance_and_s015_release",
}
REQUIRED_TARGETS = {
    "review/contracts/hirc-request-case.candidate.schema.v2.json",
    "review/contracts/hirc-bridge-gate.candidate.schema.json",
    "review/contracts/hirc-release-profile.candidate.schema.json",
    "review/contracts/hirc-transfer-case.candidate.schema.json",
    "review/fixtures/security-request-state-cases-v1.json",
    "review/fixtures/security-bridge-stage-cases-v1.json",
    "review/fixtures/security-release-profile-cases-v1.json",
    "review/fixtures/security-transfer-state-cases-v1.json",
    "review/fixtures/security-privacy-dataflow-cases-v1.json",
    "review/validate_security_request_states.ps1",
    "review/validate_security_bridge_stages.ps1",
    "review/validate_security_release_profile.ps1",
    "review/validate_security_transfer_states.ps1",
    "review/validate_security_privacy_dataflow.ps1",
    "review/fixtures/security-request-state-validation-v1.json",
    "review/fixtures/security-bridge-stage-validation-v1.json",
    "review/fixtures/security-release-profile-validation-v1.json",
    "review/fixtures/security-transfer-state-validation-v1.json",
    "review/fixtures/security-privacy-dataflow-validation-v1.json",
}


def digest(path: Path) -> tuple[str, int]:
    body = path.read_bytes()
    return hashlib.sha256(body).hexdigest(), len(body)


def validate(document: dict, check_files: bool = True) -> list[str]:
    errors: list[str] = []
    if document.get("status") != "READY_FOR_WHOLE_INDEPENDENT_SECURITY_REVIEW":
        errors.append("closure-status")
    if document.get("s014_state") != "OPEN" or document.get("s015_state") != "HELD":
        errors.append("milestone-boundary")
    if document.get("whole_security_review_state") != "PENDING":
        errors.append("whole-review-self-certified")

    targets = document.get("targets", [])
    paths = [item.get("path") for item in targets]
    if len(paths) != len(set(paths)):
        errors.append("duplicate-target")
    missing = sorted(REQUIRED_TARGETS - set(paths))
    for path in missing:
        errors.append(f"missing-target:{path}")
    if check_files:
        for item in targets:
            relative = item.get("path")
            if not isinstance(relative, str) or relative.startswith(("/", "\\")) or ".." in Path(relative).parts:
                errors.append("unsafe-target")
                continue
            path = ROOT / relative
            if not path.is_file():
                errors.append(f"unavailable-target:{relative}")
                continue
            actual_sha, actual_bytes = digest(path)
            if item.get("sha256") != actual_sha or item.get("bytes") != actual_bytes:
                errors.append(f"target-drift:{relative}")

    reviews = document.get("peer_reviews", [])
    review_stones = {item.get("stone") for item in reviews if item.get("accepted_local_scope") is True}
    if review_stones != REQUIRED_PEER_STONES:
        errors.append("peer-review-coverage")
    for item in reviews:
        if (
            item.get("disposition") not in {"PASS_LOCAL_SCOPE_WITH_RESIDUALS", "PASS_SPECIFICATION_SCOPE_WITH_RESIDUALS"}
            or not isinstance(item.get("evidence_sha256"), str)
            or len(item["evidence_sha256"]) != 64
            or not item.get("residuals_preserved")
        ):
            errors.append(f"peer-review-result:{item.get('stone')}")

    residual_ids = {item.get("id") for item in document.get("residuals", []) if item.get("state") == "OPEN"}
    if not REQUIRED_RESIDUALS <= residual_ids:
        errors.append("residual-coverage")

    for result_path in (
        "review/fixtures/security-request-state-validation-v1.json",
        "review/fixtures/security-bridge-stage-validation-v1.json",
        "review/fixtures/security-release-profile-validation-v1.json",
        "review/fixtures/security-transfer-state-validation-v1.json",
        "review/fixtures/security-privacy-dataflow-validation-v1.json",
    ):
        try:
            result = json.loads((ROOT / result_path).read_text(encoding="utf-8"))
            state = result.get("state", result.get("status"))
            if state != "PASS":
                errors.append(f"validation-not-pass:{result_path}")
        except (OSError, ValueError, TypeError):
            errors.append(f"validation-unavailable:{result_path}")
    return sorted(set(errors))


def main() -> int:
    source = json.loads(SOURCE.read_text(encoding="utf-8"))
    positive_errors = validate(source)
    mutations: list[tuple[str, dict, str]] = []
    changed = copy.deepcopy(source); changed["targets"][0]["sha256"] = "0" * 64
    mutations.append(("stale_target_hash", changed, f"target-drift:{source['targets'][0]['path']}"))
    changed = copy.deepcopy(source); changed["targets"] = [item for item in changed["targets"] if item["path"] != "review/contracts/hirc-bridge-gate.candidate.schema.json"]
    mutations.append(("missing_contract", changed, "missing-target:review/contracts/hirc-bridge-gate.candidate.schema.json"))
    changed = copy.deepcopy(source); changed["whole_security_review_state"] = "PASS"
    mutations.append(("self_certified_whole_review", changed, "whole-review-self-certified"))
    changed = copy.deepcopy(source); changed["peer_reviews"][0]["accepted_local_scope"] = False
    mutations.append(("missing_peer_scope", changed, "peer-review-coverage"))
    changed = copy.deepcopy(source); changed["residuals"] = []
    mutations.append(("erased_residuals", changed, "residual-coverage"))
    adverse = []
    for name, document, expected in mutations:
        errors = validate(document)
        adverse.append({"name": name, "expected_error": expected, "errors": errors, "rejected": expected in errors})
    status = "PASS" if not positive_errors and all(item["rejected"] for item in adverse) else "FAIL"
    result = {
        "schema": "hirc.m03-s014-security-repair-closure-validation/1",
        "status": status,
        "source": "review/m03-s014-security-repair-closure-v1.json",
        "positive": {"accepted": not positive_errors, "errors": positive_errors},
        "adverse": adverse,
        "all_adverse_rejected": all(item["rejected"] for item in adverse),
        "nonclaim": "Exact corrected-packet and local-review-boundary validation only; not runtime assurance, whole security review, S014 acceptance, S015 release or Bridge activation.",
    }
    OUTPUT.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps(result, indent=2))
    return 0 if status == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())

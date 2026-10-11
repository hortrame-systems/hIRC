#!/usr/bin/env python3
"""Validate the frozen security first-pass manifest and its negative boundaries."""

from __future__ import annotations

import copy
import hashlib
import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "review/m03-s014-security-first-pass-manifest-v1.json"
OUTPUT = ROOT / "review/fixtures/m03-s014-security-first-pass-manifest-validation-v1.json"


def blob(commit: str, path: str) -> bytes:
    return subprocess.run(
        ["git", "show", f"{commit}:{path}"],
        cwd=ROOT,
        check=True,
        capture_output=True,
    ).stdout


def validate(document: dict) -> list[str]:
    errors: list[str] = []
    commit = document.get("frozen_commit", "")
    allowlist = document.get("allowlist", [])
    paths = [item.get("path") for item in allowlist]
    if len(allowlist) != 8 or len(paths) != len(set(paths)):
        errors.append("allowlist-membership")
    excluded = set(document.get("excluded_paths", []))
    if excluded & set(paths):
        errors.append("excluded-path-admitted")
    for item in allowlist:
        try:
            raw = blob(commit, item["path"])
        except (subprocess.CalledProcessError, KeyError):
            errors.append(f"blob-missing:{item.get('path')}")
            continue
        if hashlib.sha256(raw).hexdigest() != item.get("sha256"):
            errors.append(f"blob-sha:{item['path']}")
        if len(raw) != item.get("bytes"):
            errors.append(f"blob-bytes:{item['path']}")
    criteria = document.get("fixed_criteria", [])
    if len(criteria) != 10:
        errors.append("fixed-criteria-count")
    required = " ".join(criteria).lower()
    for term in ("identity", "replay", "secret", "retention", "bridge", "positive controls", "residual risk"):
        if term not in required:
            errors.append(f"fixed-criteria:{term}")
    budget = document.get("declared_budget_tokens", {})
    if budget.get("total") != budget.get("reading_and_notes", 0) + budget.get("analysis_and_adverse_checks", 0) + budget.get("handoff", 0):
        errors.append("budget-sum")
    if document.get("reviewer_candidate", {}).get("disposition") != "PREPARATION_ONLY":
        errors.append("premature-review-admission")
    if "No allowlisted body" not in " ".join(document.get("stop_conditions", [])):
        errors.append("precondition-read-gate")
    return sorted(set(errors))


def main() -> int:
    source = json.loads(SOURCE.read_text(encoding="utf-8"))
    positive = validate(source)
    cases = []
    mutations = []

    changed = copy.deepcopy(source)
    changed["allowlist"][0]["sha256"] = "0" * 64
    mutations.append(("wrong_blob_hash", changed, "blob-sha:drafts/hirc_threat_model_v1_0-draft.md"))

    changed = copy.deepcopy(source)
    changed["allowlist"][0]["path"] = source["excluded_paths"][0]
    mutations.append(("product_finding_exposed", changed, "excluded-path-admitted"))

    changed = copy.deepcopy(source)
    changed["reviewer_candidate"]["disposition"] = "READY"
    mutations.append(("metadata_self_admits_reviewer", changed, "premature-review-admission"))

    changed = copy.deepcopy(source)
    changed["fixed_criteria"] = changed["fixed_criteria"][:-1]
    mutations.append(("criterion_removed", changed, "fixed-criteria-count"))

    changed = copy.deepcopy(source)
    changed["declared_budget_tokens"]["total"] = 1
    mutations.append(("budget_inconsistent", changed, "budget-sum"))

    for name, document, expected in mutations:
        errors = validate(document)
        cases.append({"name": name, "expected_error": expected, "errors": errors, "rejected": expected in errors})
    result = {
        "schema": "hirc.m03-s014-security-first-pass-manifest-validation/1",
        "status": "PASS" if not positive and all(item["rejected"] for item in cases) else "FAIL",
        "source": "review/m03-s014-security-first-pass-manifest-v1.json",
        "positive": {"accepted": not positive, "errors": positive},
        "adverse": cases,
        "all_adverse_rejected": all(item["rejected"] for item in cases),
        "nonclaim": "Git-blob, criteria and boundary validation only; not reviewer admission, semantic completeness, security proof or S014 acceptance."
    }
    rendered = json.dumps(result, indent=2) + "\n"
    OUTPUT.write_text(rendered, encoding="utf-8", newline="\n")
    print(rendered, end="")
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())

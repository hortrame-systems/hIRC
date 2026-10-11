#!/usr/bin/env python3
"""Validate the controller metric-review response and closed repair frame."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "review" / "m03-s014-metric-review-response-v1.json"


def identity(path: Path) -> dict:
    body = path.read_bytes()
    return {"path": path.relative_to(ROOT).as_posix(), "sha256": hashlib.sha256(body).hexdigest(), "bytes": len(body)}


def main() -> int:
    parser = argparse.ArgumentParser(); parser.add_argument("--output"); args = parser.parse_args()
    document = json.loads(SOURCE.read_text(encoding="utf-8"))
    checks = []
    source_errors = []
    for expected in document["sources"]:
        path = ROOT / expected["path"]
        observed = identity(path)
        if observed != expected: source_errors.append({"expected": expected, "observed": observed})
    checks.append({"name": "exact-source-frame", "pass": not source_errors, "observed": source_errors})
    finding_ids = {item["id"] for item in document["findings"]}
    checks.append({"name": "all-findings-disposed", "pass": finding_ids == {"MTR-A-F01", "MTR-A-F02", "MTR-A-F03", "MTR-A-F04", "MTR-A-F05", "MTR-A-F06", "MTR-B-F01"} and all(item["decision"] == "ACCEPTED_REPAIRED_RECHECK_REQUIRED" and item["tests"] for item in document["findings"]), "observed": sorted(finding_ids)})
    v3 = json.loads((ROOT / "review/fixtures/bayesian-reliance-v3-validation.json").read_text(encoding="utf-8"))
    reproduction = json.loads((ROOT / "review/fixtures/waymark-v2.1-reproduction-validation.json").read_text(encoding="utf-8"))
    matrix = json.loads((ROOT / "review/fixtures/m03-metric-matrix-repair-validation-v1.json").read_text(encoding="utf-8"))
    checks.append({"name": "repair-validations", "pass": v3.get("status") == "PASS" and v3.get("counts") == {"total": 19, "positive": 2, "adverse": 17} and reproduction.get("status") == "PASS" and matrix.get("status") == "PASS", "observed": {"v3": v3.get("status"), "reproduction": reproduction.get("status"), "matrix": matrix.get("status")}})
    requirements = json.loads((ROOT / "drafts/hirc_requirements_v1_1-draft.json").read_text(encoding="utf-8"))
    rows = {item["id"]: item for item in requirements["requirements"]}
    bound = all(rows[item_id].get("dependencies") == [document["id"]] and rows[item_id].get("acceptance_test_refs") for item_id in document["controls"]["requirements"]["ids"])
    checks.append({"name": "requirement-bindings", "pass": bound, "observed": document["controls"]["requirements"]["ids"]})
    checks.append({"name": "recheck-still-closed", "pass": document["state"] == "CONTROLLER_REPAIR_PASS_PEER_RECHECK_REQUIRED" and document["recheck"]["body_access_granted"] is False and len(document["open_residuals"]) >= 5 and "S014 closure" in document["nonclaim"], "observed": {"state": document["state"], "residuals": len(document["open_residuals"])}})
    result = {"schema": "hirc.m03-s014-metric-repair-response-validation/1", "status": "PASS" if all(item["pass"] for item in checks) else "FAIL", "response": identity(SOURCE), "checks": checks, "nonclaim": "Deterministic controller repair-frame validation only; not peer recheck, runtime/empirical validation or S014 acceptance."}
    rendered = json.dumps(result, indent=2) + "\n"
    if args.output: (ROOT / args.output).write_text(rendered, encoding="utf-8", newline="\n")
    print(rendered, end="")
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__": raise SystemExit(main())

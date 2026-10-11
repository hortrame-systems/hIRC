#!/usr/bin/env python3
"""Reproduce the historical WAYMARK v2.1 result from exact Git-bound inputs."""

from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TEMP_ROOT = ROOT.parent / "runtime" / "test-temp"
HISTORICAL_RESULT = ROOT / "review" / "fixtures" / "waymark-trust-contract-validation-v2.1.json"
FAILED_CURRENT_RERUN = ROOT / "review" / "fixtures" / "waymark-trust-contract-validation-v2.2-failed.json"
REPRODUCED_RESULT = ROOT / "review" / "fixtures" / "waymark-trust-contract-validation-v2.2-reproduced.json"
VALIDATION = ROOT / "review" / "fixtures" / "waymark-v2.1-reproduction-validation.json"
INPUTS = [
    "review/fixtures/validate_waymark_contract_cases_v2.1.ps1",
    "review/fixtures/waymark-trust-contract-cases-v1.json",
    "review/contracts/hirc-request-case.candidate.schema.json",
    "review/contracts/hirc-bayesian-reliance.candidate.schema.json",
    "review/contracts/hirc-cooperative-competition-charter.candidate.schema.json",
    "review/contracts/hirc-request-case.candidate.schema.v2.json",
    "review/contracts/hirc-bayesian-reliance.candidate.schema.v2.json",
    "review/contracts/hirc-cooperative-competition-charter.candidate.schema.v2.json",
]


def digest(body: bytes) -> str:
    return hashlib.sha256(body).hexdigest()


def identity(path: Path) -> dict:
    body = path.read_bytes()
    return {"path": str(path.relative_to(ROOT)).replace("\\", "/"), "sha256": digest(body), "bytes": len(body)}


def git_blob(path: str) -> bytes:
    return subprocess.run(["git", "cat-file", "blob", f"HEAD:{path}"], cwd=ROOT, capture_output=True, check=True).stdout


def comparable_cases(value: dict) -> list[dict]:
    fields = ("id", "base", "expected_semantic_valid", "structural_v2_valid", "adapted_input_sha256", "semantic_valid", "semantic_expectation_pass", "semantic_reasons")
    return [{key: row.get(key) for key in fields} for row in value["cases"]]


def main() -> int:
    TEMP_ROOT.mkdir(parents=True, exist_ok=True)
    expected_root = TEMP_ROOT.resolve()
    with tempfile.TemporaryDirectory(prefix="waymark-v21-", dir=TEMP_ROOT) as directory:
        sandbox = Path(directory).resolve()
        if not sandbox.is_relative_to(expected_root):
            raise RuntimeError("TEMP_SCOPE_ESCAPE")
        git_inputs = []
        for relative in INPUTS:
            body = git_blob(relative)
            target = sandbox / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(body)
            git_inputs.append({"path": relative, "sha256": digest(body), "bytes": len(body)})
        pwsh = shutil.which("pwsh")
        if not pwsh:
            raise RuntimeError("POWERSHELL_7_REQUIRED")
        harness = sandbox / "review" / "fixtures" / "validate_waymark_contract_cases_v2.1.ps1"
        run = subprocess.run([pwsh, "-NoProfile", "-File", str(harness)], cwd=sandbox, text=True, capture_output=True, check=False)
        if run.returncode != 0:
            raise RuntimeError("EXACT_HISTORICAL_REPLAY_FAILED:" + run.stderr.strip())
        reproduced = json.loads(run.stdout)

    historical = json.loads(HISTORICAL_RESULT.read_text(encoding="utf-8"))
    failed = json.loads(FAILED_CURRENT_RERUN.read_text(encoding="utf-8-sig"))
    REPRODUCED_RESULT.write_text(json.dumps(reproduced, indent=2) + "\n", encoding="utf-8", newline="\n")
    checks = {
        "historical_state_pass": historical.get("state") == "PASS",
        "reproduced_state_pass": reproduced.get("state") == "PASS",
        "exact_harness_hash": reproduced.get("adapter_harness", {}).get("sha256") == "000771021f331a019003da8172e2c6d2f072a826e1965d6ca2b7e4a43526509b",
        "stable_harness_path": reproduced.get("adapter_harness", {}).get("path") == "review/fixtures/validate_waymark_contract_cases_v2.1.ps1",
        "target_identities_match_historical": reproduced.get("validation_targets") == historical.get("validation_targets"),
        "fixture_identity_matches_historical": reproduced.get("fixture_sha256") == historical.get("fixture_sha256"),
        "adapted_inputs_and_outcomes_reproduced": comparable_cases(reproduced) == comparable_cases(historical),
        "current_drift_failure_preserved": failed.get("state") == "FAIL" and any(row.get("id") == "WST-C01" and row.get("expected_semantic_valid") and not row.get("structural_v2_valid") for row in failed.get("cases", [])),
    }
    result = {
        "schema": "hirc.waymark-v2.1-reproduction-validation/1",
        "status": "PASS" if all(checks.values()) else "FAIL",
        "git_source": "HEAD 1c525e3b464c58b6e037faaf6bb76626b32364e4",
        "inputs": git_inputs,
        "historical_result": identity(HISTORICAL_RESULT),
        "reproduced_result": identity(REPRODUCED_RESULT),
        "failed_current_rerun": identity(FAILED_CURRENT_RERUN),
        "checks": checks,
        "limits": "Exact historical Git-frame reproduction. It proves the stable harness regenerates the recorded serialized outcomes at those inputs; current working-tree drift and all runtime/statistical/privacy/authority claims remain separate.",
    }
    VALIDATION.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"status": result["status"], "checks": checks, "validation": identity(VALIDATION)}, indent=2))
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())

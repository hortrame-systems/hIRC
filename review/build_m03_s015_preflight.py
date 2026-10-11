#!/usr/bin/env python3
"""Build a deterministic M03-S015 closure preflight without performing Git effects."""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
JSON_OUTPUT = ROOT / "review/m03-s015-closure-preflight-v1.json"
MD_OUTPUT = ROOT / "review/m03-s015-closure-preflight-v1.md"
SECRET_PATTERNS = (
    re.compile(rb"sk-[A-Za-z0-9_-]{20,}"),
    re.compile(rb"AKIA[0-9A-Z]{16}"),
    re.compile(rb"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    re.compile(rb"ghp_[A-Za-z0-9]{30,}"),
    re.compile(rb"xox[baprs]-[A-Za-z0-9-]{20,}"),
)


def run(*args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(args, cwd=ROOT, text=True, capture_output=True, check=check)


def identity(path: str) -> dict[str, Any]:
    body = (ROOT / path).read_bytes()
    return {"path": path, "sha256": hashlib.sha256(body).hexdigest(), "bytes": len(body)}


def verify_ledger(ledger: dict[str, Any]) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    pathless: list[str] = []
    for artifact in ledger.get("artifacts", []):
        path = artifact.get("path")
        if not isinstance(path, str) or not path:
            pathless.append(str(artifact.get("id")))
            continue
        if not (ROOT / path).is_file():
            errors.append(f"missing:{artifact.get('id')}")
            continue
        observed = identity(path)
        if observed["sha256"] != artifact.get("sha256") or observed["bytes"] != artifact.get("bytes"):
            errors.append(f"identity:{artifact.get('id')}")
    return errors, pathless


def changed_files() -> list[str]:
    result = run("git", "ls-files", "--modified", "--others", "--exclude-standard")
    return sorted(line for line in result.stdout.splitlines() if line)


def secret_hits(files: list[str]) -> list[str]:
    hits: list[str] = []
    for path in files:
        source = ROOT / path
        if not source.is_file():
            continue
        body = source.read_bytes()
        if any(pattern.search(body) for pattern in SECRET_PATTERNS):
            hits.append(path)
    return hits


def build() -> dict[str, Any]:
    stones = json.loads((ROOT / "review/milestone-03-stone-register.json").read_text(encoding="utf-8"))
    stone_states = {item["id"]: item["status"] for item in stones["stones"]}
    packets = json.loads((ROOT / "review/m03-s014-specialist-review-packets-v1.json").read_text(encoding="utf-8"))
    lanes = {item["lane"]: item for item in packets["lanes"]}
    metric_assignment_path = ROOT / "review/m03-s014-metric-stage-a-assignment-v1.json"
    metric_assignment = json.loads(metric_assignment_path.read_text(encoding="utf-8")) if metric_assignment_path.is_file() else None
    metric_stage_b_assignment_path = ROOT / "review/m03-s014-metric-stage-b-assignment-v1.json"
    metric_stage_b_assignment = json.loads(metric_stage_b_assignment_path.read_text(encoding="utf-8")) if metric_stage_b_assignment_path.is_file() else None
    metric_stage_a_validation_path = ROOT / "review/fixtures/m03-s014-metric-stage-a-report-validation-v1.json"
    metric_stage_a_validation = json.loads(metric_stage_a_validation_path.read_text(encoding="utf-8")) if metric_stage_a_validation_path.is_file() else None
    metric_stage_b_validation_path = ROOT / "review/fixtures/m03-s014-metric-stage-b-report-validation-v1.json"
    metric_stage_b_validation = json.loads(metric_stage_b_validation_path.read_text(encoding="utf-8")) if metric_stage_b_validation_path.is_file() else None
    metric_repair_validation_path = ROOT / "review/fixtures/m03-s014-metric-repair-response-validation-v3.json"
    metric_repair_validation = json.loads(metric_repair_validation_path.read_text(encoding="utf-8")) if metric_repair_validation_path.is_file() else None
    metric_final_validation_path = ROOT / "review/fixtures/m03-s014-metric-final-recheck-validation-v1.json"
    metric_final_validation = json.loads(metric_final_validation_path.read_text(encoding="utf-8")) if metric_final_validation_path.is_file() else None
    security_assignment_path = ROOT / "review/m03-s014-security-stage-a-assignment-v1.json"
    security_assignment = json.loads(security_assignment_path.read_text(encoding="utf-8")) if security_assignment_path.is_file() else None
    security_stage_a_validation_path = ROOT / "review/fixtures/m03-s014-security-stage-a-report-validation-v1.json"
    security_stage_a_validation = json.loads(security_stage_a_validation_path.read_text(encoding="utf-8")) if security_stage_a_validation_path.is_file() else None
    security_recheck_assignment_validation_path = ROOT / "review/fixtures/m03-s014-security-repair-recheck-assignment-validation-v1.json"
    security_recheck_assignment_validation = json.loads(security_recheck_assignment_validation_path.read_text(encoding="utf-8")) if security_recheck_assignment_validation_path.is_file() else None
    security_recheck_validation_path = ROOT / "review/fixtures/m03-s014-integrated-review-closure-validation-v1.json"
    security_recheck_validation = json.loads(security_recheck_validation_path.read_text(encoding="utf-8")) if security_recheck_validation_path.is_file() else None
    publication_manifest_path = ROOT / "review/public/m03-s015-publication-manifest-v1.json"
    publication_manifest = json.loads(publication_manifest_path.read_text(encoding="utf-8")) if publication_manifest_path.is_file() else None
    publication_validation_path = ROOT / "review/public/m03-s015-publication-validation-v1.json"
    publication_validation = json.loads(publication_validation_path.read_text(encoding="utf-8")) if publication_validation_path.is_file() else None
    cumulative = json.loads((ROOT / "implementation/executable-cumulative-validation.json").read_text(encoding="utf-8"))
    ledger = json.loads((ROOT / "review/ledger.json").read_text(encoding="utf-8"))
    team = json.loads((ROOT / "review/hirc-team-stall-register-v1.json").read_text(encoding="utf-8"))
    holds = {item["id"]: item for item in team["holds"]}
    changed = changed_files()
    diff_check = run("git", "diff", "--check", check=False)
    head = run("git", "rev-parse", "HEAD").stdout.strip()
    remote_ref = run("git", "rev-parse", "origin/codex/hirc-master-plan-security", check=False)
    remote_head = remote_ref.stdout.strip() if remote_ref.returncode == 0 else None
    ledger_errors, pathless_ledger_artifacts = verify_ledger(ledger)
    secrets = secret_hits(changed)

    checks = {
        "s001_through_s013_pass": all(
            stone_states.get(name) == "PASS"
            for name in ["M03-S001", "M03-S001A", *[f"M03-S{index:03d}" for index in range(2, 14)]]
        ),
        "s014_pass": stone_states.get("M03-S014") == "PASS",
        "s015_not_prematurely_pass": stone_states.get("M03-S015") != "PASS",
        "security_review_assigned": bool(security_assignment and security_assignment.get("state") == "ADMITTED_READ_ONLY_STAGE_A_WITH_DECLARED_AGGREGATE_EXPOSURE"),
        "security_review_body_admitted": bool(security_assignment and security_assignment.get("stage_a", {}).get("body_access_granted") is True and security_assignment.get("stage_b", {}).get("body_access_granted") is False),
        "security_stage_a_report_frozen": bool(security_stage_a_validation and security_stage_a_validation.get("status") == "PASS"),
        "security_stage_b_assignment_valid": bool(security_recheck_assignment_validation and security_recheck_assignment_validation.get("status") == "PASS"),
        "security_stage_b_review_complete": bool(security_recheck_validation and security_recheck_validation.get("status") == "PASS"),
        "metric_review_assigned": bool(
            metric_stage_b_assignment
            and metric_stage_b_assignment.get("state") == "ADMITTED_READ_ONLY_STAGE_B"
            and metric_stage_b_assignment.get("lane", {}).get("name") == "metric_evaluator"
        ),
        "metric_review_body_admitted": bool(
            metric_stage_b_assignment
            and metric_stage_b_assignment.get("lane", {}).get("stage_b", {}).get("body_access_granted") is True
        ),
        "metric_stage_a_report_frozen": bool(metric_stage_a_validation and metric_stage_a_validation.get("status") == "PASS"),
        "metric_stage_b_review_complete": bool(metric_stage_b_validation and metric_stage_b_validation.get("status") == "PASS"),
        "metric_repair_frame_valid": bool(metric_repair_validation and metric_repair_validation.get("status") == "PASS"),
        "metric_repair_recheck_complete": bool(metric_final_validation and metric_final_validation.get("status") == "PASS"),
        "specialist_holds_closed": all(
            holds[name].get("state") not in {"HELD", "UNSTALLING", "AWAITING_EXTERNAL"}
            for name in ("HIRC-STALL-METRIC-REVIEWER-001", "HIRC-STALL-S014-SECURITY-PRIVACY-001")
        ),
        "executable_cumulative_pass": cumulative.get("status") == "PASS_WITH_DECLARED_RELEASE_HOLDS",
        "validator_count_21": cumulative.get("validator_count") == 21,
        "test_count_140": cumulative.get("full_suite_tests") == 140,
        "three_expected_release_failures": cumulative.get("expected_release_failures") == 3,
        "ledger_path_artifacts_exact": not ledger_errors,
        "ledger_pathless_metadata_declared": len(pathless_ledger_artifacts) == 5,
        "ledger_artifact_count_at_least_146": len(ledger.get("artifacts", [])) >= 146,
        "diff_check_clean": diff_check.returncode == 0,
        "changed_file_secret_scan_clean": not secrets,
        "publication_privacy_validation_pass": bool(publication_validation and publication_validation.get("status") == "PASS"),
        "publication_manifest_substantial": bool(publication_manifest and publication_manifest.get("file_count", 0) >= 100),
        "milestone_completion_report_present": (ROOT / "milestones/MILESTONE-03-COMPLETION.md").is_file(),
        "head_preserved": head == "1c525e3b464c58b6e037faaf6bb76626b32364e4",
        "remote_baseline_known": remote_head is not None,
    }
    blockers = [
        name
        for name in (
            "s014_pass",
            "security_review_assigned",
            "security_review_body_admitted",
            "security_stage_a_report_frozen",
            "security_stage_b_assignment_valid",
            "security_stage_b_review_complete",
            "metric_review_assigned",
            "metric_review_body_admitted",
            "metric_stage_a_report_frozen",
            "metric_stage_b_review_complete",
            "metric_repair_recheck_complete",
            "specialist_holds_closed",
        )
        if not checks[name]
    ]
    required_local = [name for name in checks if name not in blockers]
    local_failures = [name for name in required_local if not checks[name]]
    eligible = not blockers and not local_failures
    return {
        "schema": "hirc.m03-s015-closure-preflight/1",
        "id": "HIRC-M03-S015-CLOSURE-PREFLIGHT-001",
        "status": "READY_FOR_COMMIT_AND_AUTHORIZED_PUSH" if eligible else "HELD",
        "eligible_to_commit": eligible,
        "eligible_to_push": eligible,
        "checks": checks,
        "blockers": blockers,
        "local_failures": local_failures,
        "evidence": {
            "head": head,
            "remote_baseline": remote_head,
            "changed_file_count": len(changed),
            "secret_hit_paths": secrets,
            "ledger_errors": ledger_errors,
            "ledger_pathless_artifact_ids": pathless_ledger_artifacts,
            "packet": identity("review/m03-s014-specialist-review-packets-v1.json"),
            "security_assignment": identity("review/m03-s014-security-stage-a-assignment-v1.json") if security_assignment else None,
            "security_stage_a_validation": identity("review/fixtures/m03-s014-security-stage-a-report-validation-v1.json") if security_stage_a_validation else None,
            "security_recheck_assignment_validation": identity("review/fixtures/m03-s014-security-repair-recheck-assignment-validation-v1.json") if security_recheck_assignment_validation else None,
            "security_recheck_validation": identity("review/fixtures/m03-s014-integrated-review-closure-validation-v1.json") if security_recheck_validation else None,
            "metric_assignment": identity("review/m03-s014-metric-stage-a-assignment-v1.json") if metric_assignment else None,
            "metric_stage_a_validation": identity("review/fixtures/m03-s014-metric-stage-a-report-validation-v1.json") if metric_stage_a_validation else None,
            "metric_stage_b_assignment": identity("review/m03-s014-metric-stage-b-assignment-v1.json") if metric_stage_b_assignment else None,
            "metric_stage_b_validation": identity("review/fixtures/m03-s014-metric-stage-b-report-validation-v1.json") if metric_stage_b_validation else None,
            "metric_repair_validation": identity("review/fixtures/m03-s014-metric-repair-response-validation-v3.json") if metric_repair_validation else None,
            "metric_final_validation": identity("review/fixtures/m03-s014-metric-final-recheck-validation-v1.json") if metric_final_validation else None,
            "cumulative": identity("implementation/executable-cumulative-validation.json"),
            "package": identity("dist/hirc-local-0.1.0.dev0.pyz"),
            "team_register": identity("review/hirc-team-stall-register-v1.json"),
            "publication_manifest": identity("review/public/m03-s015-publication-manifest-v1.json") if publication_manifest else None,
            "publication_validation": identity("review/public/m03-s015-publication-validation-v1.json") if publication_validation else None,
            "milestone_report": identity("milestones/MILESTONE-03-COMPLETION.md") if (ROOT / "milestones/MILESTONE-03-COMPLETION.md").is_file() else None,
        },
        "next_action": "Stage only the exact public manifest plus its manifest and validation files, inspect the staged diff, commit the detailed Milestone 03 report, push through the authorized route and verify the remote ref before recording completion.",
        "nonclaim": "Read-only closure preflight. It performs no Git commit, push, release, publication, Bridge, production or reviewer admission effect.",
    }


def render(value: dict[str, Any]) -> str:
    lines = [
        "# Milestone 03 closure preflight — revision 1",
        "",
        f"**Status:** {value['status']}",
        f"**Eligible to commit:** {str(value['eligible_to_commit']).lower()}",
        f"**Eligible to push:** {str(value['eligible_to_push']).lower()}",
        "",
        value["nonclaim"],
        "",
        "## Checks",
        "",
        "| Check | Result |",
        "|---|---|",
    ]
    lines.extend(f"| `{name}` | {'PASS' if passed else 'HELD'} |" for name, passed in value["checks"].items())
    lines.extend(["", "## Active blockers", ""])
    lines.extend([f"- `{item}`" for item in value["blockers"]] or ["- None"])
    lines.extend(["", "## Local failures", ""])
    lines.extend([f"- `{item}`" for item in value["local_failures"]] or ["- None"])
    lines.extend(["", "## Next action", "", value["next_action"], ""])
    return "\n".join(lines)


def main() -> int:
    value = build()
    JSON_OUTPUT.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8", newline="\n")
    MD_OUTPUT.write_text(render(value), encoding="utf-8", newline="\n")
    print(json.dumps({"status": value["status"], "blockers": value["blockers"], "local_failures": value["local_failures"]}, indent=2))
    return 0 if not value["local_failures"] else 1


if __name__ == "__main__":
    raise SystemExit(main())

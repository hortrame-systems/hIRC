from __future__ import annotations

import copy
import hashlib
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PREDECESSOR = ROOT / "review" / "joint-consensus-matrix-draft-v7.json"
OUTPUT = ROOT / "review" / "joint-consensus-matrix-draft-v8.json"
RESULT = ROOT / "review" / "fixtures" / "m03-integrated-matrix-validation-v1.json"
EVIDENCE = [
    ("HIRC-M03-S003-WAYMARK-R01", ROOT / "review" / "waymark-m03-s003-independent-review-v1.md"),
    ("HIRC-M03-S003-LUCENT-R01", ROOT / "review" / "lucent-m03-s003-review-response-v1.md"),
    ("HIRC-M03-S003-WAYMARK-R01-RECHECK01", ROOT / "review" / "waymark-m03-s003-repair-recheck-v1.md"),
]
DTM_REQUIREMENTS = {f"U{number}" for number in range(186, 192)}
DTM_DECISIONS = {f"DTM-{number:03d}" for number in range(1, 6)}
CULTURAL_REQUIREMENTS = {f"U{number}" for number in range(192, 205)}
CULTURAL_DECISIONS = {f"CIE-{number:03d}" for number in range(1, 13)}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def evidence_rows() -> list[dict]:
    return [
        {"id": evidence_id, "path": path.relative_to(ROOT).as_posix(), "sha256": sha256(path), "bytes": path.stat().st_size}
        for evidence_id, path in EVIDENCE
    ]


def build(predecessor: dict) -> dict:
    output = copy.deepcopy(predecessor)
    output["id"] = "HIRC-JOINT-CONSENSUS-DRAFT-008"
    output["status"] = "DRAFT_M03_S003_ACCEPTED_CULTURAL_ROWS_S014_PENDING"
    output["review_evidence"] = evidence_rows()
    rationale = (
        "WAYMARK independently reviewed the frozen authored rows, LUCENT accepted and repaired the duplicate-ID finding, "
        "and WAYMARK independently rechecked the unchanged semantic output at the repaired integrator frame."
    )
    residual = (
        "Design/requirements review passed. Runtime enforcement, entropy/anti-resampling, privacy, liveness, accessibility, "
        "usability, recovery, provider and later integrated M03-S014 checks remain required."
    )
    for row in output["requirements"]:
        if row["id"] in DTM_REQUIREMENTS:
            row["waymark_position"] = "REVIEWED_NO_CHANGE_AFTER_VALIDATOR_REPAIR"
            row["joint_status"] = "BOUNDED_REVIEW_ACCEPTED_DESIGN_REQUIREMENTS_SCOPE"
            row["residual_dissent_or_hold"] = residual
            row["joint_rationale"] = rationale
    for row in output["decisions"]:
        if row["id"] in DTM_DECISIONS:
            row["waymark_position"] = "REVIEWED_NO_CHANGE_AFTER_VALIDATOR_REPAIR"
            row["joint_status"] = "BOUNDED_REVIEW_ACCEPTED_DESIGN_REQUIREMENTS_SCOPE"
            row["joint_rationale"] = rationale
            row["residual_dissent_or_hold"] = residual
    for hold in output["open_holds"]:
        if hold.get("id") == "HOLD-S003-EARLY-REVIEW":
            hold["status"] = "RESOLVED"
            hold["reason"] = "Bounded independent review found one duplicate-ID validator defect; repaired and independently rechecked PASS with semantic NO_CHANGE. Implementation residuals remain in the reviewed rows and M03-S014."
            hold["resolution_refs"] = [item[0] for item in EVIDENCE]
    output["nonclaim"] = (
        predecessor["nonclaim"]
        + " Draft 8 records bounded S003 review acceptance only; cultural rows remain pending M03-S014 and no implementation/runtime/whole-consensus claim follows."
    )
    return output


def validate(output: dict, predecessor: dict) -> list[str]:
    errors: list[str] = []
    expected_evidence = evidence_rows()
    if output.get("review_evidence") != expected_evidence:
        errors.append("review-evidence")
    for item in output.get("review_evidence", []):
        path = ROOT / item.get("path", "")
        if not path.is_file() or sha256(path) != item.get("sha256") or path.stat().st_size != item.get("bytes"):
            errors.append(f"review-evidence-hash:{item.get('id')}")

    predecessor_requirements = {row["id"]: row for row in predecessor["requirements"]}
    predecessor_decisions = {row["id"]: row for row in predecessor["decisions"]}
    output_requirements = {row["id"]: row for row in output.get("requirements", [])}
    output_decisions = {row["id"]: row for row in output.get("decisions", [])}
    if set(output_requirements) != set(predecessor_requirements):
        errors.append("requirement-identity-drift")
    if set(output_decisions) != set(predecessor_decisions):
        errors.append("decision-identity-drift")
    for row_id, row in output_requirements.items():
        if row_id not in DTM_REQUIREMENTS and row != predecessor_requirements[row_id]:
            errors.append(f"unreviewed-row-drift:{row_id}")
    for row_id, row in output_decisions.items():
        if row_id not in DTM_DECISIONS and row != predecessor_decisions[row_id]:
            errors.append(f"unreviewed-row-drift:{row_id}")
    for row_id in DTM_REQUIREMENTS:
        row = output_requirements.get(row_id, {})
        if row.get("joint_status") != "BOUNDED_REVIEW_ACCEPTED_DESIGN_REQUIREMENTS_SCOPE" or not row.get("joint_rationale"):
            errors.append(f"dtm-review-disposition:{row_id}")
    for row_id in DTM_DECISIONS:
        row = output_decisions.get(row_id, {})
        if row.get("joint_status") != "BOUNDED_REVIEW_ACCEPTED_DESIGN_REQUIREMENTS_SCOPE" or not row.get("joint_rationale"):
            errors.append(f"dtm-review-disposition:{row_id}")
    for row_id in CULTURAL_REQUIREMENTS:
        if output_requirements.get(row_id, {}).get("joint_status") != "PENDING_INDEPENDENT_PEER_REVIEW":
            errors.append(f"premature-cultural-consensus:{row_id}")
    for row_id in CULTURAL_DECISIONS:
        if output_decisions.get(row_id, {}).get("joint_status") != "PENDING_INDEPENDENT_PEER_REVIEW":
            errors.append(f"premature-cultural-consensus:{row_id}")
    hold = next((item for item in output.get("open_holds", []) if item.get("id") == "HOLD-S003-EARLY-REVIEW"), None)
    if not hold or hold.get("status") != "RESOLVED" or hold.get("resolution_refs") != [item[0] for item in EVIDENCE]:
        errors.append("s003-hold-not-resolved")
    if output.get("status") != "DRAFT_M03_S003_ACCEPTED_CULTURAL_ROWS_S014_PENDING":
        errors.append("matrix-status")
    return sorted(set(errors))


def adverse_tests(output: dict, predecessor: dict) -> list[dict]:
    cases: list[dict] = []

    def run(name: str, mutate, expected: str) -> None:
        candidate = copy.deepcopy(output)
        mutate(candidate)
        errors = validate(candidate, predecessor)
        cases.append({"name": name, "expected_error": expected, "errors": errors,
                      "rejected": any(expected in item for item in errors)})

    run("missing_recheck_evidence", lambda d: d["review_evidence"].pop(), "review-evidence")
    run("premature_cultural_consensus", lambda d: next(row for row in d["decisions"] if row["id"] == "CIE-001").update(joint_status="ACCEPTED"), "premature-cultural-consensus:CIE-001")
    run("unreviewed_predecessor_drift", lambda d: next(row for row in d["requirements"] if row["id"] == "U120").update(title="MUTATED"), "unreviewed-row-drift:U120")
    run("s003_hold_reopened", lambda d: next(row for row in d["open_holds"] if row["id"] == "HOLD-S003-EARLY-REVIEW").update(status="OPEN"), "s003-hold-not-resolved")
    run("review_hash_mismatch", lambda d: d["review_evidence"][0].update(sha256="0" * 64), "review-evidence-hash")
    return cases


def main() -> int:
    predecessor = json.loads(PREDECESSOR.read_text(encoding="utf-8"))
    output = build(predecessor)
    errors = validate(output, predecessor)
    adverse = adverse_tests(output, predecessor)
    OUTPUT.write_text(json.dumps(output, indent=2, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")
    result = {
        "schema": "hirc.m03-integrated-matrix-validation/1",
        "stone": "M03-S013",
        "predecessor": {"path": PREDECESSOR.relative_to(ROOT).as_posix(), "sha256": sha256(PREDECESSOR)},
        "output": {"path": OUTPUT.relative_to(ROOT).as_posix(), "sha256": sha256(OUTPUT), "requirements": len(output["requirements"]), "decisions": len(output["decisions"])},
        "review_evidence": evidence_rows(),
        "positive": {"accepted": not errors, "errors": errors},
        "adverse": adverse,
        "all_adverse_rejected": all(item["rejected"] for item in adverse),
        "claim": "Deterministic post-review matrix disposition and unrelated-row preservation only; not cultural peer review, implementation, runtime evidence or whole consensus.",
    }
    RESULT.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0 if not errors and result["all_adverse_rejected"] else 1


if __name__ == "__main__":
    sys.exit(main())

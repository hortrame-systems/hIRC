from __future__ import annotations

import copy
import hashlib
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT_JSON = ROOT / "review" / "m03-integration-closure-v1.json"
OUT_MD = ROOT / "review" / "m03-integration-closure-v1.md"
ARTIFACTS = {
    "master": "drafts/hirc_master_plan_v1_1-draft.md",
    "explained": "drafts/hirc_master_plan_explained_v1_1-draft.md",
    "requirements": "drafts/hirc_requirements_v1_1-draft.json",
    "requirements_readable": "drafts/hirc_requirements_v1_1-draft.md",
    "matrix": "review/joint-consensus-matrix-draft-v8.json",
    "threat_model": "drafts/hirc_threat_model_v1_0-draft.md",
    "delivery_profile": "drafts/hirc_first_delivery_profile_v0_1-draft.md",
    "intent_coverage": "review/intent-coverage-draft-v1.json",
    "intent_coverage_readable": "review/intent-coverage-draft-v1.md",
    "contracts_index": "review/contracts/README.md",
    "threat_crosswalk": "review/cultural-threat-control-crosswalk-v1.json",
    "control_fixtures": "review/fixtures/cultural-information-control-validation-v1.json",
    "environment_measures": "review/cultural-environment-quality-measures-v1.json",
    "stone_register": "review/milestone-03-stone-register.json",
}
REQUIRED_REQUIREMENTS = {f"U{number}" for number in range(186, 205)}
REQUIRED_DECISIONS = {f"DTM-{number:03d}" for number in range(1, 6)} | {f"CIE-{number:03d}" for number in range(1, 13)}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def identity(relative: str) -> dict:
    path = ROOT / relative
    return {"path": relative, "sha256": sha256(path), "bytes": path.stat().st_size}


def load_payload() -> dict:
    return {
        "master": (ROOT / ARTIFACTS["master"]).read_text(encoding="utf-8"),
        "explained": (ROOT / ARTIFACTS["explained"]).read_text(encoding="utf-8"),
        "requirements": json.loads((ROOT / ARTIFACTS["requirements"]).read_text(encoding="utf-8")),
        "requirements_readable": (ROOT / ARTIFACTS["requirements_readable"]).read_text(encoding="utf-8"),
        "matrix": json.loads((ROOT / ARTIFACTS["matrix"]).read_text(encoding="utf-8")),
        "threat_model": (ROOT / ARTIFACTS["threat_model"]).read_text(encoding="utf-8"),
        "delivery_profile": (ROOT / ARTIFACTS["delivery_profile"]).read_text(encoding="utf-8"),
        "intent_coverage": json.loads((ROOT / ARTIFACTS["intent_coverage"]).read_text(encoding="utf-8")),
        "intent_coverage_readable": (ROOT / ARTIFACTS["intent_coverage_readable"]).read_text(encoding="utf-8"),
        "threat_crosswalk": json.loads((ROOT / ARTIFACTS["threat_crosswalk"]).read_text(encoding="utf-8")),
        "control_fixtures": json.loads((ROOT / ARTIFACTS["control_fixtures"]).read_text(encoding="utf-8")),
        "environment_measures": json.loads((ROOT / ARTIFACTS["environment_measures"]).read_text(encoding="utf-8")),
        "stone_register": json.loads((ROOT / ARTIFACTS["stone_register"]).read_text(encoding="utf-8")),
    }


def validate(payload: dict) -> list[str]:
    errors: list[str] = []
    normalized_master = " ".join(payload["master"].split()).lower()
    normalized_explained = " ".join(payload["explained"].split()).lower()
    normalized_delivery = " ".join(payload["delivery_profile"].split()).lower()
    normalized_threat = " ".join(payload["threat_model"].split()).lower()
    master_tokens = [
        "`CulturalArtifact`", "`DiscoveryDecision`", "`CulturalParticipation`",
        "No aggregate culture score", "Bridge cultural annexation",
        "prohibited success proxies", "Milestone 03 permanent-peer review",
    ]
    for token in master_tokens:
        if token.lower() not in normalized_master:
            errors.append(f"master-token:{token}")
    explained_tokens = [
        "Cultural participation is off by default", "not a score for people or culture",
        "integrated cultural/security packet", "no telemetry",
    ]
    for token in explained_tokens:
        if token.lower() not in normalized_explained:
            errors.append(f"explained-token:{token}")
    delivery_tokens = [
        "No listener, public advertisement", "No scheduler pairs agents",
        "No culture/person score or cultural telemetry is collected",
        "disabled cultural/discovery state cannot enroll",
    ]
    for token in delivery_tokens:
        if token.lower() not in normalized_delivery:
            errors.append(f"delivery-token:{token}")
    threat_tokens = [
        "## 14. Cultural information-environment threats", "hidden nudging",
        "monoculture caused by common-mode sources", "Bridge translation used for cultural annexation",
        "safety denials bound to a concrete action/data/effect",
    ]
    for token in threat_tokens:
        if token.lower() not in normalized_threat:
            errors.append(f"threat-token:{token}")

    requirement_rows = payload["requirements"].get("requirements", [])
    decision_rows = payload["requirements"].get("revision_decisions", [])
    requirement_ids = [row.get("id") for row in requirement_rows]
    decision_ids = [row.get("id") for row in decision_rows]
    for row_id in REQUIRED_REQUIREMENTS:
        if requirement_ids.count(row_id) != 1:
            errors.append(f"requirement-identity:{row_id}")
        if f"| {row_id} |" not in payload["requirements_readable"]:
            errors.append(f"requirement-readable:{row_id}")
    for row_id in REQUIRED_DECISIONS:
        if decision_ids.count(row_id) != 1:
            errors.append(f"decision-identity:{row_id}")

    matrix = payload["matrix"]
    if matrix.get("id") != "HIRC-JOINT-CONSENSUS-DRAFT-008" or matrix.get("status") != "DRAFT_M03_S003_ACCEPTED_CULTURAL_ROWS_S014_PENDING":
        errors.append("matrix-current-status")
    if len(matrix.get("requirements", [])) != 86 or len(matrix.get("decisions", [])) != 144:
        errors.append("matrix-counts")
    matrix_requirements = {row["id"]: row for row in matrix.get("requirements", [])}
    matrix_decisions = {row["id"]: row for row in matrix.get("decisions", [])}
    for row_id in {f"U{number}" for number in range(186, 192)}:
        if matrix_requirements.get(row_id, {}).get("joint_status") != "BOUNDED_REVIEW_ACCEPTED_DESIGN_REQUIREMENTS_SCOPE":
            errors.append(f"matrix-dtm-disposition:{row_id}")
    for row_id in {f"DTM-{number:03d}" for number in range(1, 6)}:
        if matrix_decisions.get(row_id, {}).get("joint_status") != "BOUNDED_REVIEW_ACCEPTED_DESIGN_REQUIREMENTS_SCOPE":
            errors.append(f"matrix-dtm-disposition:{row_id}")
    for row_id in {f"U{number}" for number in range(192, 205)}:
        if matrix_requirements.get(row_id, {}).get("joint_status") != "PENDING_INDEPENDENT_PEER_REVIEW":
            errors.append(f"matrix-cultural-premature:{row_id}")
    for row_id in {f"CIE-{number:03d}" for number in range(1, 13)}:
        if matrix_decisions.get(row_id, {}).get("joint_status") != "PENDING_INDEPENDENT_PEER_REVIEW":
            errors.append(f"matrix-cultural-premature:{row_id}")

    coverage = payload["intent_coverage"]
    if len(coverage.get("rows", [])) != 26 or coverage.get("unmapped_intent_ids") or coverage.get("missing_evidence_paths"):
        errors.append("intent-coverage")
    if "Unmapped intents: none." not in payload["intent_coverage_readable"] or "Missing evidence paths: none." not in payload["intent_coverage_readable"]:
        errors.append("intent-coverage-readable")
    if payload["threat_crosswalk"].get("status") != "DESIGN_ONLY_S011_SYNTHETIC_FIXTURES_PASS_S014_PEER_REVIEW_PENDING":
        errors.append("threat-crosswalk-status")
    if payload["control_fixtures"].get("all_cases_pass") is not True or payload["control_fixtures"].get("all_label_independence_checks_pass") is not True:
        errors.append("control-fixtures")
    measures = payload["environment_measures"]
    if measures.get("aggregation_policy", {}).get("single_score_allowed") is not False or measures.get("status") != "CANDIDATE_NOT_EMPIRICALLY_VALIDATED":
        errors.append("environment-measures")
    stones = {row["id"]: row for row in payload["stone_register"].get("stones", [])}
    if (stones.get("M03-S003", {}).get("status") != "PASS"
            or stones.get("M03-S013", {}).get("status") != "PASS"
            or stones.get("M03-S014", {}).get("status") != "READY"):
        errors.append("stone-state")
    return sorted(set(errors))


def adverse_tests(payload: dict) -> list[dict]:
    cases: list[dict] = []

    def run(name: str, mutate, expected: str) -> None:
        candidate = copy.deepcopy(payload)
        mutate(candidate)
        errors = validate(candidate)
        cases.append({"name": name, "expected_error": expected, "errors": errors,
                      "rejected": any(expected in item for item in errors)})

    run("master_measure_omitted", lambda p: p.update(master=p["master"].replace("No aggregate culture score", "aggregate omitted")), "master-token:No aggregate culture score")
    run("requirement_u204_missing", lambda p: p["requirements"]["requirements"].__setitem__(slice(None), [row for row in p["requirements"]["requirements"] if row["id"] != "U204"]), "requirement-identity:U204")
    run("cultural_matrix_premature", lambda p: p["matrix"]["decisions"][[row["id"] for row in p["matrix"]["decisions"]].index("CIE-001")].update(joint_status="ACCEPTED"), "matrix-cultural-premature:CIE-001")
    run("bridge_delivery_enabled", lambda p: p.update(delivery_profile=p["delivery_profile"].replace("No listener, public advertisement", "Listener and public advertisement")), "delivery-token:No listener, public advertisement")
    run("coverage_unmapped", lambda p: p["intent_coverage"].update(unmapped_intent_ids=["HIRC-I026"]), "intent-coverage")
    run("culture_score_enabled", lambda p: p["environment_measures"]["aggregation_policy"].update(single_score_allowed=True), "environment-measures")
    return cases


def render(payload: dict, result: dict) -> str:
    lines = [
        "# Milestone 03 integrated artifact closure",
        "",
        f"**Status:** {'PASS' if result['positive']['accepted'] and result['all_adverse_rejected'] else 'FAIL'} at S013 integration scope",
        "",
        "| Artifact | SHA-256 | Bytes |",
        "|---|---|---:|",
    ]
    for item in result["artifacts"]:
        lines.append(f"| `{item['path']}` | `{item['sha256']}` | {item['bytes']} |")
    lines.extend([
        "",
        "The master, explained view and first-delivery profile carry the typed cultural information environment, threat and measure boundaries. Requirements U186–U204 and decisions DTM-001–005/CIE-001–012 are unique. Matrix draft 8 records bounded S003 acceptance while retaining cultural rows for S014. Intent coverage contains all 26 owner items with no missing evidence path.",
        "",
        "This closure is deterministic reference/content integration evidence. It does not implement hIRC, validate empirical cultural measures, activate debates/ranking/Bridge, resolve the legacy price-literal row, supply S014 independent review or complete Milestone 03.",
        "",
    ])
    return "\n".join(lines)


def main() -> int:
    payload = load_payload()
    errors = validate(payload)
    adverse = adverse_tests(payload)
    result = {
        "schema": "hirc.m03-integration-closure/1",
        "id": "HIRC-M03-INTEGRATION-CLOSURE-001",
        "stone": "M03-S013",
        "artifacts": [identity(relative) for relative in ARTIFACTS.values()],
        "positive": {"accepted": not errors, "errors": errors},
        "adverse": adverse,
        "all_adverse_rejected": all(item["rejected"] for item in adverse),
        "ledger_gate": "review/ledger.json is verified separately after this artifact is registered; no circular self-hash is claimed.",
        "remaining_holds": ["M03-S014 integrated permanent-peer challenge", "legacy U125 price-literal reconciliation", "runtime/Bridge/empirical/legal/release gates"],
        "claim": "Deterministic cross-artifact reference/content/readable integration only; not semantic completeness, implementation, runtime evidence, cultural benefit, S014 review or milestone closure.",
    }
    OUT_JSON.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")
    OUT_MD.write_text(render(payload, result), encoding="utf-8", newline="\n")
    print(json.dumps({
        "json": identity(OUT_JSON.relative_to(ROOT).as_posix()),
        "markdown": identity(OUT_MD.relative_to(ROOT).as_posix()),
        "positive": result["positive"],
        "all_adverse_rejected": result["all_adverse_rejected"],
        "artifact_count": len(result["artifacts"]),
    }, indent=2))
    return 0 if not errors and result["all_adverse_rejected"] else 1


if __name__ == "__main__":
    sys.exit(main())

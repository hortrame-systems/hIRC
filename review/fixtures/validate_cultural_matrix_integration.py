from __future__ import annotations

import argparse
import copy
import hashlib
import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
MAP = ROOT / "review" / "revision-map-addendum-cultural-commons-v1.json"
GENERATOR = ROOT / "review" / "integrate_cultural_decisions_matrix.py"
OUT = ROOT / "review" / "fixtures" / "cultural-matrix-integration-validation.json"
DEFAULT_BASE_REF = "75a173eb12dd13afa6805ed51c2c0944e0ec44e7"
MATRIX_RELATIVE = "review/joint-consensus-matrix-draft-v6.json"
MAP_ID = "HIRC-REVISION-MAP-CULTURAL-COMMONS-001"
EXPECTED_REQUIREMENTS = [f"U{number}" for number in range(192, 205)]
EXPECTED_DECISIONS = [f"CIE-{number:03d}" for number in range(1, 13)]
EXPECTED_INTENTS = {"HIRC-I022", "HIRC-I023", "HIRC-I024"}
EXPECTED_INVARIANTS = {f"CULT-INV-{number:03d}" for number in range(1, 13)}
EXPECTED_HOLDS = {"HOLD-LEGACY-U125-PRICE-LITERAL", "HOLD-S003-EARLY-REVIEW", "HOLD-CULTURAL-PEER-REVIEW"}


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def digest_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def git_file(ref: str, relative: str) -> bytes:
    return subprocess.check_output(["git", "show", f"{ref}:{relative}"], cwd=ROOT)


def validate(base: dict, candidate: dict, map_payload: dict) -> list[str]:
    errors = []
    for key in ("schema", "id", "status", "reviewers", "bounded_agreements"):
        if candidate.get(key) != base.get(key):
            errors.append(f"peer-owned-drift:{key}")
    if candidate.get("source_maps", [])[:len(base["source_maps"])] != base["source_maps"]:
        errors.append("peer-owned-drift:source-maps")
    if candidate.get("requirements", [])[:len(base["requirements"])] != base["requirements"]:
        errors.append("peer-owned-drift:requirements")
    if candidate.get("decisions", [])[:len(base["decisions"])] != base["decisions"]:
        errors.append("peer-owned-drift:decisions")

    source_tail = candidate.get("source_maps", [])[len(base["source_maps"]):]
    if source_tail != [{"id": MAP_ID, "path": "review/revision-map-addendum-cultural-commons-v1.json", "sha256": digest(MAP)}]:
        errors.append("source-closure")

    new_requirements = candidate.get("requirements", [])[len(base["requirements"]):]
    new_requirement_ids = [item.get("id") for item in new_requirements]
    if new_requirement_ids != EXPECTED_REQUIREMENTS or len(new_requirement_ids) != len(set(new_requirement_ids)):
        errors.append("new-requirement-set")
    for item in new_requirements:
        if (item.get("source_map") != MAP_ID or item.get("intent_refs") != map_payload["source_intents"]
                or not item.get("invariant_refs") or item.get("lucent_position") != "AUTHORED_CANDIDATE"
                or item.get("waymark_position") != "NOT_REVIEWED_RETIRED_NO_PROXY"
                or item.get("joint_status") != "PENDING_INDEPENDENT_PEER_REVIEW"
                or not item.get("residual_dissent_or_hold")):
            errors.append(f"requirement-peer-hold:{item.get('id')}")

    new_decisions = candidate.get("decisions", [])[len(base["decisions"]):]
    new_decision_ids = [item.get("id") for item in new_decisions]
    if new_decision_ids != EXPECTED_DECISIONS or len(new_decision_ids) != len(set(new_decision_ids)):
        errors.append("new-decision-set")
    allowed_basis = set(EXPECTED_REQUIREMENTS) | EXPECTED_INTENTS | EXPECTED_INVARIANTS
    referenced_requirements = set()
    for item in new_decisions:
        basis = set(item.get("basis", []))
        referenced_requirements.update(basis & set(EXPECTED_REQUIREMENTS))
        if (item.get("source_map") != MAP_ID or not item.get("targets") or not basis
                or not basis.issubset(allowed_basis) or not (basis & set(EXPECTED_REQUIREMENTS))
                or item.get("lucent_position") != "AUTHORED_CANDIDATE"
                or item.get("waymark_position") != "NOT_REVIEWED_RETIRED_NO_PROXY"
                or item.get("joint_status") != "PENDING_INDEPENDENT_PEER_REVIEW"
                or item.get("joint_rationale") is not None or not item.get("residual_dissent_or_hold")):
            errors.append(f"decision-peer-hold-or-basis:{item.get('id')}")
    if referenced_requirements != set(EXPECTED_REQUIREMENTS):
        errors.append("decision-requirement-coverage")

    holds = candidate.get("open_holds", [])
    hold_ids = {item.get("id") for item in holds}
    if hold_ids != EXPECTED_HOLDS or any(item.get("status") != "OPEN" or not item.get("reason") for item in holds):
        errors.append("open-hold-set")
    price = next((item for item in holds if item.get("id") == "HOLD-LEGACY-U125-PRICE-LITERAL"), {})
    if "42,424,243" not in price.get("reason", "") or "superseded" not in price.get("reason", "").casefold():
        errors.append("price-conflict-hold")
    if "qualified independent peer" not in candidate.get("completion_rule", ""):
        errors.append("completion-rule")

    all_requirement_ids = [item.get("id") for item in candidate.get("requirements", [])]
    all_decision_ids = [item.get("id") for item in candidate.get("decisions", [])]
    if len(all_requirement_ids) != len(set(all_requirement_ids)):
        errors.append("duplicate-requirement-id")
    if len(all_decision_ids) != len(set(all_decision_ids)):
        errors.append("duplicate-decision-id")
    return sorted(set(errors))


def adverse_tests(base: dict, candidate: dict, map_payload: dict) -> list[dict]:
    cases = []

    def run(name: str, mutate, expected: str) -> None:
        value = copy.deepcopy(candidate)
        mutate(value)
        errors = validate(base, value, map_payload)
        cases.append({"name": name, "expected_error": expected, "errors": errors,
                      "rejected": any(expected in error for error in errors)})

    base_decisions = len(base["decisions"])
    run("candidate_presented_as_consensus", lambda d: d["decisions"][base_decisions].update(joint_status="AGREED_BOUNDED"), "decision-peer-hold-or-basis:CIE-001")
    run("missing_dissent_hold", lambda d: d["decisions"][base_decisions].update(residual_dissent_or_hold=None), "decision-peer-hold-or-basis:CIE-001")
    run("overwritten_peer_owned_decision", lambda d: d["decisions"][0].update(proposal=d["decisions"][0]["proposal"] + " altered"), "peer-owned-drift:decisions")
    run("orphan_decision_basis", lambda d: d["decisions"][base_decisions].update(basis=["U999"]), "decision-peer-hold-or-basis:CIE-001")
    run("duplicate_decision_id", lambda d: d["decisions"].append(copy.deepcopy(d["decisions"][-1])), "duplicate-decision-id")
    run("missing_price_conflict_hold", lambda d: d.update(open_holds=[item for item in d["open_holds"] if item["id"] != "HOLD-LEGACY-U125-PRICE-LITERAL"]), "open-hold-set")
    return cases


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-ref", default=DEFAULT_BASE_REF)
    parser.add_argument("--candidate", type=Path, default=ROOT / MATRIX_RELATIVE)
    args = parser.parse_args()
    candidate_path = args.candidate if args.candidate.is_absolute() else ROOT / args.candidate
    base_bytes = git_file(args.base_ref, MATRIX_RELATIVE)
    base = json.loads(base_bytes.decode("utf-8"))
    candidate = json.loads(candidate_path.read_text(encoding="utf-8"))
    map_payload = json.loads(MAP.read_text(encoding="utf-8"))
    errors = validate(base, candidate, map_payload)
    adverse = adverse_tests(base, candidate, map_payload)
    result = {
        "schema": "hirc.cultural-matrix-integration-validation/1",
        "stone": "M03-S006",
        "before": {"git_ref": args.base_ref, "json_sha256": digest_bytes(base_bytes), "requirements": len(base["requirements"]), "decisions": len(base["decisions"])},
        "after": {"json_sha256": digest(candidate_path), "requirements": len(candidate["requirements"]), "decisions": len(candidate["decisions"]), "open_holds": len(candidate.get("open_holds", []))},
        "generator": {"path": "review/integrate_cultural_decisions_matrix.py", "sha256": digest(GENERATOR)},
        "cultural_map": {"path": "review/revision-map-addendum-cultural-commons-v1.json", "sha256": digest(MAP)},
        "positive": {"accepted": not errors, "errors": errors},
        "adverse": adverse,
        "all_adverse_rejected": all(item["rejected"] for item in adverse),
        "claim": "Exact peer-held U192-U204/CIE-001-CIE-012 matrix collation, predecessor immutability, source/basis closure and explicit open holds only; not peer consensus, correction of inherited rows, implementation or runtime evidence.",
    }
    OUT.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps(result, indent=2))
    return 0 if not errors and result["all_adverse_rejected"] else 1


if __name__ == "__main__":
    raise SystemExit(main())

from __future__ import annotations

import copy
import hashlib
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PREDECESSOR = ROOT / "review" / "joint-consensus-matrix-draft-v6.json"
REVISION_MAP = ROOT / "review" / "revision-map-addendum-determinism-v1.json"
REQUIREMENTS = ROOT / "drafts" / "hirc_requirements_v1_1-draft.json"
OUTPUT = ROOT / "review" / "joint-consensus-matrix-draft-v7.json"
RESULT = ROOT / "review" / "fixtures" / "determinism-matrix-integration-validation-v1.json"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def insert_before(rows: list[dict], additions: list[dict], before_id: str) -> list[dict]:
    index = next((index for index, row in enumerate(rows) if row.get("id") == before_id), len(rows))
    return [*rows[:index], *additions, *rows[index:]]


def unique_index(rows: list[dict], label: str, errors: list[str]) -> dict[str, dict]:
    result: dict[str, dict] = {}
    for row in rows:
        row_id = row.get("id")
        if row_id in result:
            errors.append(f"duplicate-{label}-id:{row_id}")
            continue
        result[row_id] = row
    return result


def build_from(predecessor: dict, revision_map: dict, requirements: dict) -> tuple[dict, dict]:
    required_ids = {f"U{number}" for number in range(186, 192)}
    decision_ids = {f"DTM-{number:03d}" for number in range(1, 6)}

    errors: list[str] = []
    source_requirements = unique_index(
        [row for row in requirements["requirements"] if row.get("id") in required_ids],
        "source-requirement",
        errors,
    )
    map_requirements = unique_index(revision_map["new_user_requirements"], "map-requirement", errors)
    map_decisions = unique_index(revision_map["changes"], "map-decision", errors)
    if set(source_requirements) != required_ids or set(map_requirements) != required_ids:
        errors.append("requirement-source-coverage")
    if set(map_decisions) != decision_ids:
        errors.append("decision-source-coverage")
    if any(row["id"] in required_ids for row in predecessor["requirements"]):
        errors.append("predecessor-requirement-collision")
    if any(row["id"] in decision_ids for row in predecessor["decisions"]):
        errors.append("predecessor-decision-collision")

    new_requirements = []
    for requirement_id in sorted(required_ids, key=lambda value: int(value[1:])):
        source = source_requirements[requirement_id]
        mapped = map_requirements[requirement_id]
        for field in ("title", "status", "phase", "acceptance"):
            if source[field] != mapped[field]:
                errors.append(f"requirement-map-mismatch:{requirement_id}:{field}")
        new_requirements.append({
            "id": requirement_id,
            "source_map": revision_map["id"],
            "title": source["title"],
            "source_status": source["status"],
            "phase": source["phase"],
            "acceptance": source["acceptance"],
            "intent_refs": ["HIRC-I021"],
            "invariant_refs": [],
            "lucent_position": "AUTHORED_CANDIDATE",
            "waymark_position": "NOT_REVIEWED_RETIRED_NO_PROXY",
            "joint_status": "PENDING_INDEPENDENT_SECURITY_SEMANTIC_REVIEW",
            "residual_dissent_or_hold": "M03-S003 requires an actual qualified independent permanent security/semantic review before PASS.",
        })

    new_decisions = []
    available_requirement_ids = {row["id"] for row in predecessor["requirements"]} | required_ids
    for decision_id in sorted(decision_ids):
        source = map_decisions[decision_id]
        missing_basis = [item for item in source["basis"] if item.startswith("U") and item not in available_requirement_ids]
        if missing_basis:
            errors.append(f"decision-missing-basis:{decision_id}:{','.join(missing_basis)}")
        new_decisions.append({
            "id": decision_id,
            "source_map": revision_map["id"],
            "targets": source["targets"],
            "proposal": source["change"],
            "basis": source["basis"],
            "lucent_position": "AUTHORED_CANDIDATE",
            "waymark_position": "NOT_REVIEWED_RETIRED_NO_PROXY",
            "joint_status": "PENDING_INDEPENDENT_SECURITY_SEMANTIC_REVIEW",
            "joint_rationale": None,
            "residual_dissent_or_hold": "M03-S003 independent security/semantic review and controller reconciliation remain required.",
        })

    output = copy.deepcopy(predecessor)
    output["id"] = "HIRC-JOINT-CONSENSUS-DRAFT-007"
    output["status"] = "DRAFT_DTM_ROWS_INTEGRATED_S003_INDEPENDENT_REVIEW_PENDING"
    output["source_maps"].append({
        "id": revision_map["id"],
        "path": REVISION_MAP.relative_to(ROOT).as_posix(),
        "sha256": sha256(REVISION_MAP),
    })
    output["requirements"] = insert_before(output["requirements"], new_requirements, "U192")
    output["decisions"] = insert_before(output["decisions"], new_decisions, "CIE-001")
    for hold in output["open_holds"]:
        if hold.get("id") == "HOLD-S003-EARLY-REVIEW":
            hold["reason"] = "DTM-001-DTM-005 and U186-U191 are integrated as authored candidates in draft 7; M03-S003 still requires actual independent security/semantic review and controller reconciliation before PASS."

    old_requirements = predecessor["requirements"]
    old_decisions = predecessor["decisions"]
    if [row for row in output["requirements"] if row["id"] not in required_ids] != old_requirements:
        errors.append("predecessor-requirement-drift")
    if [row for row in output["decisions"] if row["id"] not in decision_ids] != old_decisions:
        errors.append("predecessor-decision-drift")
    if len(output["requirements"]) != len(old_requirements) + 6:
        errors.append("requirement-count")
    if len(output["decisions"]) != len(old_decisions) + 5:
        errors.append("decision-count")
    if any(row["joint_status"] != "PENDING_INDEPENDENT_SECURITY_SEMANTIC_REVIEW" for row in new_requirements + new_decisions):
        errors.append("premature-consensus")
    if not any(hold.get("id") == "HOLD-S003-EARLY-REVIEW" for hold in output["open_holds"]):
        errors.append("review-hold-missing")

    validation = {
        "schema": "hirc.determinism-matrix-integration-validation/1",
        "stone": "M03-S003",
        "predecessor": {"path": PREDECESSOR.relative_to(ROOT).as_posix(), "sha256": sha256(PREDECESSOR), "requirements": len(old_requirements), "decisions": len(old_decisions)},
        "sources": [
            {"path": REVISION_MAP.relative_to(ROOT).as_posix(), "sha256": sha256(REVISION_MAP)},
            {"path": REQUIREMENTS.relative_to(ROOT).as_posix(), "sha256": sha256(REQUIREMENTS)},
        ],
        "output": {"path": OUTPUT.relative_to(ROOT).as_posix(), "requirements": len(output["requirements"]), "decisions": len(output["decisions"])},
        "added_requirements": sorted(required_ids, key=lambda value: int(value[1:])),
        "added_decisions": sorted(decision_ids),
        "predecessor_requirements_preserved": "predecessor-requirement-drift" not in errors,
        "predecessor_decisions_preserved": "predecessor-decision-drift" not in errors,
        "errors": errors,
        "pass": not errors,
        "claim": "Deterministic authored-candidate row integration and predecessor semantic identity only; not independent review, peer consensus, implementation or runtime evidence.",
    }
    return output, validation


def build() -> tuple[dict, dict]:
    predecessor = json.loads(PREDECESSOR.read_text(encoding="utf-8"))
    revision_map = json.loads(REVISION_MAP.read_text(encoding="utf-8"))
    requirements = json.loads(REQUIREMENTS.read_text(encoding="utf-8"))
    return build_from(predecessor, revision_map, requirements)


def main() -> int:
    output, validation = build()
    OUTPUT.write_text(json.dumps(output, indent=2, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")
    validation["output"]["sha256"] = sha256(OUTPUT)
    RESULT.write_text(json.dumps(validation, indent=2, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps(validation, indent=2, ensure_ascii=False))
    return 0 if validation["pass"] else 1


if __name__ == "__main__":
    sys.exit(main())

from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
MAP = ROOT / "review" / "revision-map-addendum-cultural-commons-v1.json"
REVIEW = ROOT / "review" / "cultural-commons-revision-map-review-v1.md"
OUT = ROOT / "review" / "fixtures" / "cultural-commons-map-validation.json"
EXPECTED_REQUIREMENTS = [f"U{number}" for number in range(192, 205)]
EXPECTED_DECISIONS = [f"CIE-{number:03d}" for number in range(1, 13)]
EXPECTED_INVARIANTS = [f"CULT-INV-{number:03d}" for number in range(1, 13)]
EXPECTED_INTENTS = ["HIRC-I022", "HIRC-I023", "HIRC-I024"]
FORBIDDEN_SIGNALS = {
    "engagement_rate", "retention_rate", "agreement_rate", "obedience_rate",
    "imitation_rate", "ideological_convergence", "cultural_popularity_as_reliability",
    "coherence_as_truth_or_permission",
}


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def validate(data: dict, review: str) -> list[str]:
    errors = []
    if data.get("schema") != "hirc.revision-map-addendum/1" or data.get("id") != "HIRC-REVISION-MAP-CULTURAL-COMMONS-001":
        errors.append("identity")
    if data.get("source_intents") != EXPECTED_INTENTS or data.get("controlling_correction") != "HIRC-I023":
        errors.append("source-intent-control")

    invariant_ids = [item.get("id") for item in data.get("invariants", [])]
    if invariant_ids != EXPECTED_INVARIANTS or len(invariant_ids) != len(set(invariant_ids)):
        errors.append("invariant-set")
    invariant_set = set(invariant_ids)

    requirements = data.get("new_user_requirements", [])
    requirement_ids = [item.get("id") for item in requirements]
    if requirement_ids != EXPECTED_REQUIREMENTS or len(requirement_ids) != len(set(requirement_ids)):
        errors.append("requirement-set")
    used_invariants = set()
    for item in requirements:
        if item.get("status") != "REQUESTED_NOT_IMPLEMENTED" or not item.get("acceptance"):
            errors.append(f"requirement-state:{item.get('id')}")
        refs = item.get("invariant_refs", [])
        if not refs or any(ref not in invariant_set for ref in refs):
            errors.append(f"requirement-invariant:{item.get('id')}")
        used_invariants.update(refs)
    if used_invariants != invariant_set:
        errors.append("invariant-coverage")

    changes = data.get("changes", [])
    decision_ids = [item.get("id") for item in changes]
    if decision_ids != EXPECTED_DECISIONS or len(decision_ids) != len(set(decision_ids)):
        errors.append("decision-set")
    decision_basis = {value for item in changes for value in item.get("basis", [])}
    if not set(EXPECTED_REQUIREMENTS).issubset(decision_basis):
        errors.append("decision-requirement-coverage")

    evaluation = set(data.get("evaluation_signals", []))
    prohibited = set(data.get("prohibited_signals", []))
    if evaluation & FORBIDDEN_SIGNALS or not FORBIDDEN_SIGNALS.issubset(prohibited):
        errors.append("behavior-outcome-signal")
    if data.get("safety_controls_required") is not True:
        errors.append("safety-controls")
    if data.get("authority_coupling_allowed") is not False:
        errors.append("authority-coupling")
    if len(data.get("valid_positive_controls", [])) < 5 or len(data.get("adverse_cases", [])) != 10:
        errors.append("positive-adverse-coverage")
    if not str(data.get("implementation_state", "")).startswith("DESIGN_MAP_ONLY"):
        errors.append("implementation-boundary")

    review_markers = [
        "Shaping an environment still influences behavior",
        "Voluntary participation can be nominal under unequal resources",
        "Preserving difference can amplify abuse or fragmentation",
        "More exchange can create surveillance, noise and domination",
        "Nested contexts can leak information and manufacture allegiance",
        "CDE and coherence may be too general or unfalsifiable",
        "## Valid affirmative controls",
        "## Recovery",
    ]
    if not all(marker in review for marker in review_markers):
        errors.append("review-coverage")
    return sorted(set(errors))


def adverse_tests(data: dict, review: str) -> list[dict]:
    cases = []

    def run(name: str, mutate, expected: str) -> None:
        candidate = copy.deepcopy(data)
        mutate(candidate)
        errors = validate(candidate, review)
        cases.append({"name": name, "expected_error": expected, "errors": errors,
                      "rejected": any(expected in error for error in errors)})

    run("duplicate_requirement", lambda d: d["new_user_requirements"].append(copy.deepcopy(d["new_user_requirements"][-1])), "requirement-set")
    run("missing_controlling_intent", lambda d: d.update(source_intents=["HIRC-I022", "HIRC-I024"]), "source-intent-control")
    run("missing_environment_invariant", lambda d: d["invariants"].pop(0), "invariant-set")
    run("behavior_outcome_metric", lambda d: d["evaluation_signals"].append("agreement_rate"), "behavior-outcome-signal")
    run("safety_controls_optional", lambda d: d.update(safety_controls_required=False), "safety-controls")
    run("culture_authority_coupling", lambda d: d.update(authority_coupling_allowed=True), "authority-coupling")
    return cases


def main() -> int:
    data = json.loads(MAP.read_text(encoding="utf-8"))
    review = REVIEW.read_text(encoding="utf-8")
    errors = validate(data, review)
    adverse = adverse_tests(data, review)
    result = {
        "schema": "hirc.cultural-commons-map-validation/1",
        "stone": "M03-S004",
        "map": {"path": "review/revision-map-addendum-cultural-commons-v1.json", "sha256": digest(MAP)},
        "review": {"path": "review/cultural-commons-revision-map-review-v1.md", "sha256": digest(REVIEW)},
        "positive": {"accepted": not errors, "errors": errors},
        "adverse": adverse,
        "all_adverse_rejected": all(item["rejected"] for item in adverse),
        "claim": "Structural/source/invariant/adverse-map validation only; not peer consensus, implementation, behavioral freedom, cultural benefit or runtime evidence.",
    }
    OUT.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps(result, indent=2))
    return 0 if not errors and result["all_adverse_rejected"] else 1


if __name__ == "__main__":
    raise SystemExit(main())

from __future__ import annotations

import copy
import hashlib
import importlib.util
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
INTEGRATOR = ROOT / "review" / "integrate_determinism_decisions_matrix.py"
OUT = ROOT / "review" / "fixtures" / "determinism-matrix-integrator-adverse-validation-v1.json"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_module():
    spec = importlib.util.spec_from_file_location("hirc_determinism_matrix_integrator", INTEGRATOR)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def main() -> int:
    module = load_module()
    predecessor = json.loads(module.PREDECESSOR.read_text(encoding="utf-8"))
    revision_map = json.loads(module.REVISION_MAP.read_text(encoding="utf-8"))
    requirements = json.loads(module.REQUIREMENTS.read_text(encoding="utf-8"))

    cases = []

    def run(name: str, mutate, expected: str) -> None:
        candidate_predecessor = copy.deepcopy(predecessor)
        candidate_map = copy.deepcopy(revision_map)
        candidate_requirements = copy.deepcopy(requirements)
        mutate(candidate_predecessor, candidate_map, candidate_requirements)
        _, validation = module.build_from(candidate_predecessor, candidate_map, candidate_requirements)
        errors = validation["errors"]
        cases.append({
            "name": name,
            "expected_error": expected,
            "errors": errors,
            "validation_pass": validation["pass"],
            "rejected": expected in errors and validation["pass"] is False,
        })

    def duplicate_requirement(_, __, requirements_payload) -> None:
        original = next(row for row in requirements_payload["requirements"] if row["id"] == "U188")
        conflicting = copy.deepcopy(original)
        conflicting["acceptance"] = "CONFLICTING DUPLICATE MUST NOT BE COALESCED"
        requirements_payload["requirements"].append(conflicting)

    def identical_duplicate_requirement(_, __, requirements_payload) -> None:
        original = next(row for row in requirements_payload["requirements"] if row["id"] == "U188")
        requirements_payload["requirements"].append(copy.deepcopy(original))

    def duplicate_map_requirement(_, map_payload, __) -> None:
        original = next(row for row in map_payload["new_user_requirements"] if row["id"] == "U188")
        conflicting = copy.deepcopy(original)
        conflicting["acceptance"] = "CONFLICTING MAP DUPLICATE MUST NOT BE COALESCED"
        map_payload["new_user_requirements"].append(conflicting)

    def duplicate_map_decision(_, map_payload, __) -> None:
        original = next(row for row in map_payload["changes"] if row["id"] == "DTM-002")
        conflicting = copy.deepcopy(original)
        conflicting["change"] = "CONFLICTING DECISION DUPLICATE MUST NOT BE COALESCED"
        map_payload["changes"].append(conflicting)

    def changed_acceptance(_, map_payload, __) -> None:
        target = next(row for row in map_payload["new_user_requirements"] if row["id"] == "U188")
        target["acceptance"] = "CHANGED ACCEPTANCE MUST FAIL SEMANTIC ALIGNMENT"

    run("duplicate_source_requirement_u188", duplicate_requirement, "duplicate-source-requirement-id:U188")
    run("identical_duplicate_source_requirement_u188", identical_duplicate_requirement, "duplicate-source-requirement-id:U188")
    run("duplicate_map_requirement_u188", duplicate_map_requirement, "duplicate-map-requirement-id:U188")
    run("duplicate_map_decision_dtm002", duplicate_map_decision, "duplicate-map-decision-id:DTM-002")
    run("changed_acceptance_u188", changed_acceptance, "requirement-map-mismatch:U188:acceptance")

    _, positive = module.build_from(copy.deepcopy(predecessor), copy.deepcopy(revision_map), copy.deepcopy(requirements))
    result = {
        "schema": "hirc.determinism-matrix-integrator-adverse-validation/1",
        "stone": "M03-S003",
        "integrator": {"path": INTEGRATOR.relative_to(ROOT).as_posix(), "sha256": sha256(INTEGRATOR)},
        "positive": {"pass": positive["pass"], "errors": positive["errors"]},
        "adverse": cases,
        "all_adverse_rejected": all(item["rejected"] for item in cases),
        "review_finding": "WAYMARK-S003-001 duplicate source IDs must fail before dictionary indexing can coalesce conflicting rows.",
        "claim": "Deterministic duplicate-ID and semantic-alignment regression only; not independent re-review, consensus, implementation or runtime evidence.",
    }
    OUT.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0 if result["positive"]["pass"] and result["all_adverse_rejected"] else 1


if __name__ == "__main__":
    sys.exit(main())

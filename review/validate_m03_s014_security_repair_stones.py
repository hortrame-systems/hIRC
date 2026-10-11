#!/usr/bin/env python3
"""Validate the controller security-repair dependency graph and hard gates."""

from __future__ import annotations

import copy
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "review/m03-s014-security-repair-stones-v1.json"
OUTPUT = ROOT / "review/fixtures/m03-s014-security-repair-stones-validation-v1.json"
ALLOWED = {"CAPTURED", "READY", "ACTIVE", "PASS", "HELD", "FAIL"}


def validate(document: dict) -> list[str]:
    errors: list[str] = []
    stones = document.get("stones", [])
    ids = [item.get("id") for item in stones]
    if len(stones) != 6 or len(ids) != len(set(ids)):
        errors.append("stone-identity")
    by_id = {item.get("id"): item for item in stones}
    for item in stones:
        identity = item.get("id")
        if item.get("status") not in ALLOWED:
            errors.append(f"status:{identity}")
        for field in ("outcome", "write_scope", "positive_controls", "adverse_cases", "stop_condition"):
            if not item.get(field):
                errors.append(f"field:{identity}:{field}")
        for dependency in item.get("prerequisites", []):
            if dependency not in by_id:
                errors.append(f"missing-prerequisite:{identity}:{dependency}")
            elif item.get("status") in {"READY", "ACTIVE", "PASS"} and by_id[dependency].get("status") != "PASS":
                errors.append(f"premature:{identity}:{dependency}")
    visiting: set[str] = set()
    visited: set[str] = set()

    def walk(identity: str) -> None:
        if identity in visiting:
            errors.append(f"cycle:{identity}")
            return
        if identity in visited or identity not in by_id:
            return
        visiting.add(identity)
        for dependency in by_id[identity].get("prerequisites", []):
            walk(dependency)
        visiting.remove(identity)
        visited.add(identity)

    for identity in ids:
        walk(identity)
    if document.get("execution_state", {}).get("project_blocked") and any(item.get("status") in {"READY", "ACTIVE"} for item in stones):
        errors.append("global-stall-with-ready-repair")
    if "cannot close M03-S014" not in document.get("independence", ""):
        errors.append("independence-limit")
    return sorted(set(errors))


def main() -> int:
    source = json.loads(SOURCE.read_text(encoding="utf-8"))
    positive = validate(source)
    cases = []
    mutations = []
    changed = copy.deepcopy(source); changed["stones"][4]["status"] = "HELD"; changed["stones"][5]["status"] = "READY"; mutations.append(("premature_ready", changed, "premature:M03-S014-SEC-R006:M03-S014-SEC-R005"))
    changed = copy.deepcopy(source); changed["stones"][0]["prerequisites"] = ["M03-S014-SEC-R006"]; mutations.append(("cycle", changed, "cycle:M03-S014-SEC-R001"))
    changed = copy.deepcopy(source); changed["stones"][0]["adverse_cases"] = []; mutations.append(("missing_adverse", changed, "field:M03-S014-SEC-R001:adverse_cases"))
    changed = copy.deepcopy(source); changed["execution_state"]["project_blocked"] = True; changed["stones"][5]["status"] = "ACTIVE"; mutations.append(("false_global_stall", changed, "global-stall-with-ready-repair"))
    changed = copy.deepcopy(source); changed["independence"] = "Independent review complete."; mutations.append(("self_certified_independence", changed, "independence-limit"))
    for name, document, expected in mutations:
        errors = validate(document)
        cases.append({"name": name, "expected_error": expected, "errors": errors, "rejected": expected in errors})
    result = {
        "schema": "hirc.m03-s014-security-repair-stones-validation/1",
        "status": "PASS" if not positive and all(item["rejected"] for item in cases) else "FAIL",
        "source": "review/m03-s014-security-repair-stones-v1.json",
        "positive": {"accepted": not positive, "errors": positive},
        "adverse": cases,
        "all_adverse_rejected": all(item["rejected"] for item in cases),
        "nonclaim": "Graph/field/gate validation only; not repair implementation, semantic correctness, independent review or S014 closure."
    }
    rendered = json.dumps(result, indent=2) + "\n"
    OUTPUT.write_text(rendered, encoding="utf-8", newline="\n")
    print(rendered, end="")
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())

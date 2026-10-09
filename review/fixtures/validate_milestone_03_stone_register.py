from __future__ import annotations

import copy
import hashlib
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
REGISTER = ROOT / "review" / "milestone-03-stone-register.json"
OUT_MD = ROOT / "review" / "milestone-03-stone-register.md"
OUT_RESULT = ROOT / "review" / "fixtures" / "milestone-03-stone-register-validation.json"
VALID_STATES = {
    "CAPTURED", "READY", "ACTIVE", "CHECKING", "PASS", "FAILED", "HELD",
    "NOT_VERIFIED", "SUPERSEDED",
}
REQUIRED_LISTS = {
    "bounded_scope", "positive_controls", "adverse_cases", "required_evidence",
    "next_eligible",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def validate(data: dict) -> list[str]:
    errors: list[str] = []
    if data.get("schema") != "hirc.stone-register/1":
        errors.append("schema")
    stones = data.get("stones")
    if not isinstance(stones, list) or not stones:
        return errors + ["stones"]

    ids = [stone.get("id") for stone in stones]
    if any(not isinstance(item, str) or not item for item in ids):
        errors.append("stone-id")
    if len(ids) != len(set(ids)):
        errors.append("duplicate-id")
    by_id = {stone.get("id"): stone for stone in stones if isinstance(stone.get("id"), str)}

    for stone in stones:
        stone_id = stone.get("id", "?")
        if not isinstance(stone.get("outcome"), str) or not stone["outcome"].strip():
            errors.append(f"{stone_id}:outcome")
        if stone.get("status") not in VALID_STATES:
            errors.append(f"{stone_id}:status")
        prerequisites = stone.get("prerequisites")
        if not isinstance(prerequisites, list):
            errors.append(f"{stone_id}:prerequisites")
            prerequisites = []
        for prerequisite in prerequisites:
            if prerequisite not in by_id:
                errors.append(f"{stone_id}:missing-prerequisite:{prerequisite}")
        for field in REQUIRED_LISTS:
            value = stone.get(field)
            if not isinstance(value, list) or (field != "next_eligible" and not value):
                errors.append(f"{stone_id}:{field}")
        for field in ("owner", "canonical_writer", "independent_review", "recovery", "stop_condition"):
            if not isinstance(stone.get(field), str) or not stone[field].strip():
                errors.append(f"{stone_id}:{field}")
        for candidate in stone.get("next_eligible", []):
            if candidate not in by_id:
                errors.append(f"{stone_id}:missing-next:{candidate}")

    visiting: set[str] = set()
    visited: set[str] = set()

    def visit(stone_id: str) -> None:
        if stone_id in visiting:
            errors.append(f"cycle:{stone_id}")
            return
        if stone_id in visited or stone_id not in by_id:
            return
        visiting.add(stone_id)
        for prerequisite in by_id[stone_id].get("prerequisites", []):
            visit(prerequisite)
        visiting.remove(stone_id)
        visited.add(stone_id)

    for stone_id in by_id:
        visit(stone_id)

    for stone in stones:
        if stone.get("status") in {"ACTIVE", "CHECKING", "PASS"}:
            for prerequisite in stone.get("prerequisites", []):
                if prerequisite in by_id and by_id[prerequisite].get("status") != "PASS":
                    errors.append(f"{stone['id']}:premature:{prerequisite}")

    terminals = [stone["id"] for stone in stones if not stone.get("next_eligible")]
    if terminals != ["M03-S015"]:
        errors.append("terminal")

    execution = data.get("execution_state")
    ready_ids = sorted(stone["id"] for stone in stones if stone.get("status") == "READY")
    if not isinstance(execution, dict):
        errors.append("execution-state")
    else:
        declared_ready = execution.get("ready_stones")
        if declared_ready != ready_ids:
            errors.append("execution-ready-mismatch")
        if not isinstance(execution.get("scoped_holds"), list):
            errors.append("scoped-holds")
        elif any(item not in by_id for item in execution["scoped_holds"]):
            errors.append("unknown-scoped-hold")
        else:
            runnable_ids = sorted(item for item in ready_ids if item not in execution["scoped_holds"])
            if execution.get("runnable_stones") != runnable_ids:
                errors.append("execution-runnable-mismatch")
            if runnable_ids and execution.get("state") != "RUNNABLE":
                errors.append("global-stall-with-runnable-work")
        if not isinstance(execution.get("rule"), str) or not execution["rule"].strip():
            errors.append("execution-rule")
    return sorted(set(errors))


def render(data: dict) -> str:
    lines = [
        "# Milestone 03 stone register",
        "",
        f"**Status:** {data['status']}",
        "",
        f"**Canonical source:** `review/milestone-03-stone-register.json`",
        "",
        "This is the readable projection of the canonical JSON register. PASS claims",
        "remain limited to each stone's declared evidence. Runtime and Bridge remain disabled.",
        "",
        "| Stone | State | Prerequisites | Outcome | Next |",
        "|---|---|---|---|---|",
    ]
    for stone in data["stones"]:
        prerequisites = ", ".join(stone["prerequisites"]) or "—"
        next_items = ", ".join(stone["next_eligible"]) or "—"
        outcome = stone["outcome"].replace("|", "\\|")
        lines.append(f"| {stone['id']} | {stone['status']} | {prerequisites} | {outcome} | {next_items} |")
    lines.extend([
        "",
        "## Gate",
        "",
        data["advance_rule"],
        "",
        "## Explicitly excluded effects",
        "",
    ])
    lines.extend(f"- {item}" for item in data["excluded_effects"])
    lines.append("")
    return "\n".join(lines)


def adverse_tests(data: dict) -> list[dict]:
    cases = []

    def run(name: str, mutate, expected: str) -> None:
        candidate = copy.deepcopy(data)
        mutate(candidate)
        errors = validate(candidate)
        cases.append({"name": name, "expected_error": expected, "errors": errors,
                      "rejected": any(expected in item for item in errors)})

    run("duplicate_id", lambda d: d["stones"][1].update(id="M03-S001"), "duplicate-id")
    run("missing_prerequisite", lambda d: d["stones"][1]["prerequisites"].append("M03-NOT-THERE"), "missing-prerequisite")
    run("cycle", lambda d: d["stones"][0]["prerequisites"].append("M03-S015"), "cycle")
    def make_dependent_stone_premature(d: dict) -> None:
        by_id = {stone["id"]: stone for stone in d["stones"]}
        for stone in d["stones"]:
            if stone["status"] == "CAPTURED" and any(by_id[item]["status"] != "PASS" for item in stone["prerequisites"]):
                stone["status"] = "ACTIVE"
                return
        raise RuntimeError("no captured dependent stone available for adverse mutation")

    run("premature_active", make_dependent_stone_premature, "premature")
    run("missing_adverse_cases", lambda d: d["stones"][3].update(adverse_cases=[]), "adverse_cases")
    run("missing_recovery", lambda d: d["stones"][4].update(recovery=""), "recovery")
    def make_global_stall(d: dict) -> None:
        if d["execution_state"].get("runnable_stones"):
            d["execution_state"]["state"] = "HELD"
            return
        by_id = {stone["id"]: stone for stone in d["stones"]}
        by_id["M03-S012"]["status"] = "READY"
        d["execution_state"].update(
            state="HELD",
            ready_stones=["M03-S003", "M03-S012"],
            runnable_stones=["M03-S012"],
        )

    run("global_stall_with_ready_work", make_global_stall, "global-stall-with-runnable-work")
    return cases


def main() -> int:
    data = json.loads(REGISTER.read_text(encoding="utf-8"))
    errors = validate(data)
    markdown = render(data)
    OUT_MD.write_text(markdown, encoding="utf-8", newline="\n")
    adverse = adverse_tests(data)
    result = {
        "schema": "hirc.stone-register-validation/1",
        "register": {"path": REGISTER.relative_to(ROOT).as_posix(), "sha256": sha256(REGISTER)},
        "validator": {"path": Path(__file__).resolve().relative_to(ROOT).as_posix(), "sha256": sha256(Path(__file__))},
        "positive": {"accepted": not errors, "errors": errors},
        "adverse": adverse,
        "all_adverse_rejected": all(item["rejected"] for item in adverse),
        "corrections": [
            "The premature-active adverse mutation became stale as targeted stones legitimately advanced. It now selects the first CAPTURED stone with an unmet prerequisite, preserving the invariant across register progress."
        ],
        "claim": "Deterministic graph/field/gate validation only; not semantic correctness, implementation, peer consensus or runtime evidence.",
    }
    OUT_RESULT.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0 if not errors and result["all_adverse_rejected"] else 1


if __name__ == "__main__":
    sys.exit(main())

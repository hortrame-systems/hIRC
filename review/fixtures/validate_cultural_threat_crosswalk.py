from __future__ import annotations

import copy
import hashlib
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "review" / "cultural-threat-control-crosswalk-v1.json"
OUT = ROOT / "review" / "fixtures" / "cultural-threat-control-crosswalk-validation-v1.json"

EXPECTED_THREATS = {
    "CULT-T01": "HIDDEN_NUDGING",
    "CULT-T02": "CULTURAL_MEMORY_POISONING",
    "CULT-T03": "MENTOR_AUTHORITY_INFLATION",
    "CULT-T04": "RANKING_CAPTURE_AND_FILTER_BUBBLE",
    "CULT-T05": "COMMON_MODE_MONOCULTURE",
    "CULT-T06": "CONFORMITY_CONDITIONED_PARTICIPATION",
    "CULT-T07": "SAFETY_GATE_AS_OBEDIENCE_CONTROL",
    "CULT-T08": "BRIDGE_CULTURAL_ANNEXATION",
}
EXPECTED_REQUIREMENTS = {f"U{number}" for number in range(192, 205)}
EXPECTED_DECISIONS = {f"CIE-{number:03d}" for number in range(1, 13)}
REQUIRED_THREAT_FIELDS = {
    "assets", "actors", "path", "consequence", "control_refs", "detection",
    "containment", "recovery", "residual_risk", "future_fixture_refs",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def nonempty_list(value) -> bool:
    return isinstance(value, list) and bool(value) and all(isinstance(item, str) and item.strip() for item in value)


def validate(data: dict) -> list[str]:
    errors: list[str] = []
    if data.get("schema") != "hirc.cultural-threat-control-crosswalk/1":
        errors.append("schema")
    coverage = data.get("coverage")
    if not isinstance(coverage, dict):
        return [*errors, "coverage"]
    if set(coverage.get("requirements", [])) != EXPECTED_REQUIREMENTS:
        errors.append("requirement-coverage")
    if set(coverage.get("candidate_decisions", [])) != EXPECTED_DECISIONS:
        errors.append("decision-coverage")
    contracts = coverage.get("contracts")
    if not nonempty_list(contracts):
        errors.append("contract-coverage")
    else:
        for contract in contracts:
            if not (ROOT / contract).is_file():
                errors.append(f"missing-contract:{contract}")

    threats = data.get("threats")
    if not isinstance(threats, list):
        return [*errors, "threats"]
    ids = [item.get("id") for item in threats if isinstance(item, dict)]
    if len(ids) != len(set(ids)):
        errors.append("duplicate-threat-id")
    actual = {item.get("id"): item.get("name") for item in threats if isinstance(item, dict)}
    if actual != EXPECTED_THREATS:
        errors.append("threat-coverage")
    for threat in threats:
        if not isinstance(threat, dict):
            errors.append("threat-object")
            continue
        threat_id = threat.get("id", "?")
        for field in REQUIRED_THREAT_FIELDS:
            value = threat.get(field)
            if field in {"path", "consequence", "residual_risk"}:
                if not isinstance(value, str) or not value.strip():
                    errors.append(f"{threat_id}:{field}")
            elif not nonempty_list(value):
                errors.append(f"{threat_id}:{field}")
        controls = threat.get("control_refs", [])
        if not any(item in EXPECTED_REQUIREMENTS for item in controls):
            errors.append(f"{threat_id}:requirement-control")
        if not any(item in EXPECTED_DECISIONS for item in controls):
            errors.append(f"{threat_id}:decision-control")
        if any(not item.startswith("M03-S011:CULT-A") for item in threat.get("future_fixture_refs", [])):
            errors.append(f"{threat_id}:future-fixture")

    positives = {item.get("id"): item for item in data.get("positive_controls", []) if isinstance(item, dict)}
    if set(positives) != {"CULT-PC01", "CULT-PC02"}:
        errors.append("positive-control-coverage")
    else:
        default = positives["CULT-PC01"].get("conditions", {})
        for field in ("visible", "versioned", "participant_selected", "reversible", "direct_source_available", "dissent_reachable", "standing_unchanged"):
            if default.get(field) is not True:
                errors.append(f"CULT-PC01:{field}")
        if default.get("authority_effect") != "NONE":
            errors.append("CULT-PC01:authority-effect")
        safety = positives["CULT-PC02"].get("conditions", {})
        for field in ("concrete_effect_binding", "least_scope", "reason_visible", "appeal_available", "standing_preserved", "prohibited_effect_remains_denied"):
            if safety.get(field) is not True:
                errors.append(f"CULT-PC02:{field}")
        if safety.get("cultural_condition") is not False:
            errors.append("CULT-PC02:cultural-condition")

    if data.get("authority_effect") != "NONE":
        errors.append("authority-effect")
    if data.get("reliability_effect") != "NONE":
        errors.append("reliability-effect")
    for field in ("activation_gate", "nonclaim"):
        if not isinstance(data.get(field), str) or not data[field].strip():
            errors.append(field)
    return sorted(set(errors))


def adverse_tests(data: dict) -> list[dict]:
    cases: list[dict] = []

    def run(name: str, mutate, expected: str) -> None:
        candidate = copy.deepcopy(data)
        mutate(candidate)
        errors = validate(candidate)
        cases.append({"name": name, "expected_error": expected, "errors": errors,
                      "rejected": any(expected in item for item in errors)})

    run("missing_detection", lambda d: d["threats"][0].update(detection=[]), "detection")
    run("missing_recovery", lambda d: d["threats"][1].update(recovery=[]), "recovery")
    run("cultural_authority_promotion", lambda d: d.update(authority_effect="ROLE_PROMOTION"), "authority-effect")
    run("hidden_contextual_default", lambda d: d["positive_controls"][0]["conditions"].update(visible=False), "CULT-PC01:visible")
    run("safety_denial_on_culture", lambda d: d["positive_controls"][1]["conditions"].update(cultural_condition=True), "CULT-PC02:cultural-condition")
    run("bridge_threat_omitted", lambda d: d["threats"].pop(), "threat-coverage")
    run("requirement_gap", lambda d: d["coverage"]["requirements"].remove("U204"), "requirement-coverage")
    return cases


def main() -> int:
    data = json.loads(SOURCE.read_text(encoding="utf-8"))
    errors = validate(data)
    adverse = adverse_tests(data)
    result = {
        "schema": "hirc.cultural-threat-control-crosswalk-validation/1",
        "stone": "M03-S010",
        "source": {"path": SOURCE.relative_to(ROOT).as_posix(), "sha256": sha256(SOURCE)},
        "validator": {"path": Path(__file__).resolve().relative_to(ROOT).as_posix(), "sha256": sha256(Path(__file__))},
        "positive": {"accepted": not errors, "errors": errors},
        "adverse": adverse,
        "all_adverse_rejected": all(item["rejected"] for item in adverse),
        "claim": "Deterministic field, identity, reference and positive-control validation only; not complete threat coverage, implementation, runtime enforcement, consent, privacy, accessibility, cultural benefit or peer review.",
    }
    OUT.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0 if not errors and result["all_adverse_rejected"] else 1


if __name__ == "__main__":
    sys.exit(main())

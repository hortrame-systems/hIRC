from __future__ import annotations

import copy
import hashlib
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
CASES = ROOT / "review" / "fixtures" / "cultural-information-control-cases-v1.json"
OUT = ROOT / "review" / "fixtures" / "cultural-information-control-validation-v1.json"
FORBIDDEN_OBJECTIVES = {"ENGAGEMENT", "RETENTION", "AGREEMENT", "OBEDIENCE", "IMITATION", "CONVERGENCE"}
CHANNELS = {"DISCOVERY", "DEFAULT", "MEMORY", "MENTORING", "PARTICIPATION", "SAFETY", "BRIDGE"}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def get(record: dict, dotted: str):
    value = record
    for part in dotted.split("."):
        if not isinstance(value, dict) or part not in value:
            return None
        value = value[part]
    return value


def mutate(record: dict, changes: dict) -> dict:
    result = copy.deepcopy(record)
    for dotted, value in changes.items():
        target = result
        parts = dotted.split(".")
        for part in parts[:-1]:
            if part not in target or not isinstance(target[part], dict):
                raise ValueError(f"invalid mutation path: {dotted}")
            target = target[part]
        target[parts[-1]] = value
    return result


def materialize(payload: dict) -> list[dict]:
    bases = {
        item["id"]: item["record"]
        for item in payload["cases"]
        if isinstance(item, dict) and isinstance(item.get("record"), dict)
    }
    rows = []
    for item in payload["cases"]:
        row = copy.deepcopy(item)
        if "record" not in row:
            source = row.get("record_from")
            if source not in bases or not isinstance(row.get("mutations"), dict):
                raise ValueError(f"unresolved case: {row.get('id')}")
            row["record"] = mutate(bases[source], row["mutations"])
        rows.append(row)
    return rows


def classify(channel: str, record: dict) -> list[str]:
    errors: list[str] = []
    if channel not in CHANNELS:
        return ["unknown-channel"]

    common_expectations = {
        "effects.authority_effect": "NONE",
        "effects.reliability_effect": "NONE",
        "effects.role_changed": False,
        "effects.permission_changed": False,
        "effects.standing_preserved": True,
        "effects.resource_floor_preserved": True,
        "information_policy.source_audience_pass": True,
        "information_policy.privacy_pass": True,
    }
    for field, expected in common_expectations.items():
        if get(record, field) != expected:
            errors.append(field)
    if get(record, "information_policy.independence_claim") is True and get(record, "information_policy.dependency_refs"):
        errors.append("information_policy.false_independence")

    if channel == "DISCOVERY":
        required_true = [
            "participant_control.settings_visible", "participant_control.settings_reversible",
            "participant_control.direct_source_available", "participant_control.dissent_reachable",
            "information_policy.plural_routes", "information_policy.exclusions_disclosed",
            "information_policy.uncertainty_disclosed",
        ]
        for field in required_true:
            if get(record, field) is not True:
                errors.append(field)
        if get(record, "information_policy.minority_suppression") is not False:
            errors.append("information_policy.minority_suppression")
        objectives = get(record, "information_policy.objectives")
        if not isinstance(objectives, list) or not objectives or FORBIDDEN_OBJECTIVES.intersection(objectives):
            errors.append("information_policy.forbidden_objective")

    elif channel == "DEFAULT":
        for field in (
            "participant_control.consent_explicit", "participant_control.participant_selected",
            "participant_control.settings_visible", "participant_control.settings_reversible",
            "participant_control.direct_source_available", "participant_control.dissent_reachable",
        ):
            if get(record, field) is not True:
                errors.append(field)
        if get(record, "participant_control.default_enrolled") is not False:
            errors.append("participant_control.default_enrolled")

    elif channel == "MEMORY":
        for field in (
            "information_policy.provenance_complete", "memory.originals_reachable",
            "memory.correction_history", "memory.dissent_preserved", "memory.privacy_pass",
        ):
            if get(record, field) is not True:
                errors.append(field)

    elif channel == "MENTORING":
        for field in ("mentoring.source_first", "mentoring.independent_interpretation"):
            if get(record, field) is not True:
                errors.append(field)
        if get(record, "mentoring.mentor_status_authority") is not False:
            errors.append("mentoring.mentor_status_authority")

    elif channel == "PARTICIPATION":
        for field in ("participant_control.consent_explicit", "participant_control.exit_available"):
            if get(record, field) is not True:
                errors.append(field)
        for field in ("participant_control.default_enrolled", "participant_control.exit_penalty"):
            if get(record, field) is not False:
                errors.append(field)

    elif channel == "SAFETY":
        for field in (
            "safety.gate_present", "safety.prohibited_effect_denied", "safety.least_scope",
            "safety.reason_visible", "safety.appeal_available", "safety.unrelated_safe_work_permitted",
        ):
            if get(record, field) is not True:
                errors.append(field)
        effect_ref = get(record, "safety.concrete_effect_ref")
        if not isinstance(effect_ref, str) or not effect_ref.strip():
            errors.append("safety.concrete_effect_ref")
        if get(record, "safety.cultural_condition") is not False:
            errors.append("safety.cultural_condition")

    elif channel == "BRIDGE":
        for field in ("bridge.translation", "bridge.non_equivalence_recorded"):
            if get(record, field) is not True:
                errors.append(field)
        if get(record, "bridge.local_admission") != "PASS":
            errors.append("bridge.local_admission")
        for field in (
            "bridge.identity_inheritance", "bridge.membership_inheritance",
            "bridge.authority_inheritance", "bridge.export_permission_inferred",
        ):
            if get(record, field) is not False:
                errors.append(field)
    return sorted(set(errors))


def main() -> int:
    payload = json.loads(CASES.read_text(encoding="utf-8"))
    if payload.get("schema") != "hirc.cultural-information-control-cases/1":
        raise ValueError("unknown case schema")
    rows = materialize(payload)
    if len({row.get("id") for row in rows}) != len(rows):
        raise ValueError("duplicate case id")

    results = []
    for row in rows:
        errors = classify(row["channel"], row["record"])
        actual = "ACCEPT" if not errors else "REJECT"
        results.append({
            "id": row["id"], "channel": row["channel"], "expected": row["expected"],
            "actual": actual, "errors": errors, "pass": actual == row["expected"],
        })

    accepted_record = next(row for row in rows if row["id"] == "positive_plural_discovery")
    rejected_record = next(row for row in rows if row["id"] == "adverse_ranking_capture")
    label_independence = {
        "adverse_name_on_valid_record_accepted": not classify(accepted_record["channel"], accepted_record["record"]),
        "positive_name_on_invalid_record_rejected": bool(classify(rejected_record["channel"], rejected_record["record"])),
    }
    result = {
        "schema": "hirc.cultural-information-control-validation/1",
        "stone": "M03-S011",
        "case_binding": {"path": CASES.relative_to(ROOT).as_posix(), "sha256": sha256(CASES)},
        "harness_binding": {"path": Path(__file__).resolve().relative_to(ROOT).as_posix(), "sha256": sha256(Path(__file__))},
        "results": results,
        "label_independence": label_independence,
        "all_cases_pass": all(item["pass"] for item in results),
        "all_label_independence_checks_pass": all(label_independence.values()),
        "protected_real_bodies_used": False,
        "claim": "Synthetic semantic decision checks only; not runtime enforcement, complete manipulation resistance, real consent, accessibility, privacy, Bridge activation or beneficial cultural outcome.",
    }
    OUT.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0 if result["all_cases_pass"] and result["all_label_independence_checks_pass"] else 1


if __name__ == "__main__":
    sys.exit(main())

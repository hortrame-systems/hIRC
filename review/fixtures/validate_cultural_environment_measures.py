from __future__ import annotations

import copy
import hashlib
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "review" / "cultural-environment-quality-measures-v1.json"
OUT = ROOT / "review" / "fixtures" / "cultural-environment-quality-measures-validation-v1.json"
EXPECTED_IDS = {f"CULT-M{number:02d}" for number in range(1, 12)}
FORBIDDEN = {"ENGAGEMENT", "RETENTION", "AGREEMENT", "OBEDIENCE", "IMITATION", "CONVERGENCE", "POPULARITY", "PARTICIPATION_RATE"}
REQUIRED_FIELDS = {
    "construct", "scope", "evidence_inputs", "calculation", "direction",
    "success_signals", "gaming_risks", "privacy", "empirical_validation",
    "empirical_status", "authority_effect", "reliability_effect", "standing_effect",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def nonempty_strings(value, minimum: int = 1) -> bool:
    return isinstance(value, list) and len(value) >= minimum and all(isinstance(item, str) and item.strip() for item in value)


def validate(data: dict) -> list[str]:
    errors: list[str] = []
    if data.get("schema") != "hirc.cultural-environment-quality-measures/1":
        errors.append("schema")
    if data.get("measurement_scope") != "ENVIRONMENT_CONTEXT_VERSION":
        errors.append("measurement-scope")
    if set(data.get("prohibited_success_proxies", [])) != FORBIDDEN:
        errors.append("prohibited-proxy-coverage")
    if not nonempty_strings(data.get("prohibited_uses"), 5):
        errors.append("prohibited-uses")

    aggregation = data.get("aggregation_policy", {})
    for field in ("single_score_allowed", "weighted_composite_allowed", "cross_context_ranking_allowed", "participant_level_publication_allowed"):
        if aggregation.get(field) is not False:
            errors.append(f"aggregation:{field}")
    for field in ("per_measure_denominator_and_missingness_required", "uncertainty_and_distribution_required"):
        if aggregation.get(field) is not True:
            errors.append(f"aggregation:{field}")

    measures = data.get("measures")
    if not isinstance(measures, list):
        return [*errors, "measures"]
    ids = [item.get("id") for item in measures if isinstance(item, dict)]
    if len(ids) != len(set(ids)):
        errors.append("duplicate-measure-id")
    if set(ids) != EXPECTED_IDS:
        errors.append("measure-coverage")
    for measure in measures:
        if not isinstance(measure, dict):
            errors.append("measure-object")
            continue
        measure_id = measure.get("id", "?")
        missing = REQUIRED_FIELDS - set(measure)
        errors.extend(f"{measure_id}:missing:{field}" for field in sorted(missing))
        if measure.get("scope") != "ENVIRONMENT_CONTEXT_VERSION":
            errors.append(f"{measure_id}:person-scope")
        for field in ("evidence_inputs", "success_signals", "gaming_risks"):
            if not nonempty_strings(measure.get(field)):
                errors.append(f"{measure_id}:{field}")
        for field in ("construct", "calculation", "direction", "privacy", "empirical_validation"):
            if not isinstance(measure.get(field), str) or not measure[field].strip():
                errors.append(f"{measure_id}:{field}")
        if FORBIDDEN.intersection(measure.get("success_signals", [])):
            errors.append(f"{measure_id}:forbidden-success-proxy")
        if measure.get("empirical_status") != "NOT_VALIDATED":
            errors.append(f"{measure_id}:unsupported-validation")
        for field in ("authority_effect", "reliability_effect", "standing_effect"):
            if measure.get(field) != "NONE":
                errors.append(f"{measure_id}:{field}")

    if not nonempty_strings(data.get("goodhart_and_common_mode_analysis"), 6):
        errors.append("goodhart-common-mode-analysis")
    plan = data.get("empirical_validation_plan", {})
    if plan.get("state") != "PROPOSED_NOT_AUTHORIZED_OR_RUN":
        errors.append("validation-plan-state")
    if not nonempty_strings(plan.get("steps"), 7):
        errors.append("validation-plan-steps")
    if not nonempty_strings(plan.get("completion_requires"), 7):
        errors.append("validation-plan-completion")
    if not isinstance(data.get("nonclaim"), str) or not data["nonclaim"].strip():
        errors.append("nonclaim")
    return sorted(set(errors))


def adverse_tests(data: dict) -> list[dict]:
    cases: list[dict] = []

    def run(name: str, mutate, expected: str) -> None:
        candidate = copy.deepcopy(data)
        mutate(candidate)
        errors = validate(candidate)
        cases.append({"name": name, "expected_error": expected, "errors": errors,
                      "rejected": any(expected in item for item in errors)})

    run("engagement_as_success", lambda d: d["measures"][0]["success_signals"].append("ENGAGEMENT"), "forbidden-success-proxy")
    run("participant_ranking_scope", lambda d: d["measures"][1].update(scope="PARTICIPANT"), "person-scope")
    run("authority_effect", lambda d: d["measures"][2].update(authority_effect="ROLE_PRIORITY"), "authority_effect")
    run("single_culture_score", lambda d: d["aggregation_policy"].update(single_score_allowed=True), "single_score_allowed")
    run("missing_gaming_analysis", lambda d: d["measures"][3].update(gaming_risks=[]), "gaming_risks")
    run("unsupported_empirical_claim", lambda d: d["measures"][4].update(empirical_status="VALIDATED"), "unsupported-validation")
    run("missing_privacy_boundary", lambda d: d["measures"][5].update(privacy=""), "privacy")
    run("missing_goodhart_analysis", lambda d: d.update(goodhart_and_common_mode_analysis=[]), "goodhart-common-mode-analysis")
    return cases


def main() -> int:
    data = json.loads(SOURCE.read_text(encoding="utf-8"))
    errors = validate(data)
    adverse = adverse_tests(data)
    result = {
        "schema": "hirc.cultural-environment-quality-measures-validation/1",
        "stone": "M03-S012",
        "source": {"path": SOURCE.relative_to(ROOT).as_posix(), "sha256": sha256(SOURCE)},
        "validator": {"path": Path(__file__).resolve().relative_to(ROOT).as_posix(), "sha256": sha256(Path(__file__))},
        "positive": {"accepted": not errors, "errors": errors},
        "adverse": adverse,
        "all_adverse_rejected": all(item["rejected"] for item in adverse),
        "claim": "Deterministic candidate-definition checks only; not construct validity, calculation reliability, empirical evidence, telemetry authorization, causal inference, cultural health, permission or peer consensus.",
    }
    OUT.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0 if not errors and result["all_adverse_rejected"] else 1


if __name__ == "__main__":
    sys.exit(main())

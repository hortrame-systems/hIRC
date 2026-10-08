from __future__ import annotations

import argparse
import copy
import hashlib
import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
GENERATOR = ROOT / "review" / "build_requirements_v1_1.py"
MAP = ROOT / "review" / "revision-map-addendum-cultural-commons-v1.json"
OUT = ROOT / "review" / "fixtures" / "cultural-requirements-validation.json"
DEFAULT_BASE_REF = "cb755a61d20ef6b4e5d5c0d24ec7abb4b919f113"
MAP_ID = "HIRC-REVISION-MAP-CULTURAL-COMMONS-001"
EXPECTED_INTENTS = ["HIRC-I022", "HIRC-I023", "HIRC-I024"]
EXPECTED_REQUIREMENTS = [f"U{number}" for number in range(192, 205)]
EXPECTED_DECISIONS = [f"CIE-{number:03d}" for number in range(1, 13)]
FORBIDDEN_MARKERS = {"selects participant beliefs", "agreement_rate", "conformity_score", "permission_from_culture"}


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def digest_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def git_file(ref: str, relative: str) -> bytes:
    return subprocess.check_output(["git", "show", f"{ref}:{relative}"], cwd=ROOT)


def escape(value: object) -> str:
    return str(value if value is not None else "").replace("|", "\\|").replace("\n", " ")


def readable_rows(markdown: str, valid_ids: set[str]) -> dict[str, str]:
    rows = {}
    for line in markdown.splitlines():
        if line.startswith("| "):
            identifier = line.split("|", 2)[1].strip()
            if identifier in valid_ids:
                rows[identifier] = line
    return rows


def validate(base: dict, candidate: dict, markdown: str, map_payload: dict) -> list[str]:
    errors = []
    old_requirements = base["requirements"]
    old_ids = [item["id"] for item in old_requirements]
    old_set = set(old_ids)
    candidate_ids = [item["id"] for item in candidate["requirements"]]
    candidate_by_id = {item["id"]: item for item in candidate["requirements"]}
    if len(candidate_ids) != len(set(candidate_ids)):
        errors.append("duplicate-requirement-id")
    if [item for item in candidate["requirements"] if item["id"] in old_set] != old_requirements:
        errors.append("unrelated-predecessor-drift")
    if [item for item in candidate_ids if item not in old_set] != EXPECTED_REQUIREMENTS:
        errors.append("new-requirement-set")

    old_decisions = base["revision_decisions"]
    old_decision_ids = [item["id"] for item in old_decisions]
    old_decision_set = set(old_decision_ids)
    candidate_decision_ids = [item["id"] for item in candidate["revision_decisions"]]
    if [item for item in candidate["revision_decisions"] if item["id"] in old_decision_set] != old_decisions:
        errors.append("unrelated-decision-drift")
    if [item for item in candidate_decision_ids if item not in old_decision_set] != EXPECTED_DECISIONS:
        errors.append("new-decision-set")

    map_rows = [item for item in candidate["source_maps"] if item["id"] == MAP_ID]
    if (map_payload.get("source_intents") != EXPECTED_INTENTS
            or map_payload.get("controlling_correction") != "HIRC-I023"
            or len(map_rows) != 1 or map_rows[0]["sha256"] != digest(MAP)):
        errors.append("source-closure")

    for identifier in EXPECTED_REQUIREMENTS:
        item = candidate_by_id.get(identifier)
        if not item or item.get("governing_sources") != [MAP_ID]:
            errors.append(f"source-closure:{identifier}")
            continue
        refs = item.get("rationale_refs", [])
        invariant_refs = item.get("invariant_refs", [])
        if refs[:3] != EXPECTED_INTENTS or not invariant_refs or refs[3:] != invariant_refs:
            errors.append(f"source-closure:{identifier}")
        combined = (item.get("title", "") + " " + item.get("acceptance", "")).casefold()
        if any(marker in combined for marker in FORBIDDEN_MARKERS):
            errors.append(f"behavior-control:{identifier}")

    privacy_requirements = {
        "U194": {"CULT-INV-005", "CULT-INV-009"},
        "U199": {"CULT-INV-005", "CULT-INV-009", "CULT-INV-010"},
    }
    for identifier, required in privacy_requirements.items():
        item = candidate_by_id.get(identifier, {})
        text = (item.get("title", "") + " " + item.get("acceptance", "")).casefold()
        if not required.issubset(set(item.get("invariant_refs", []))) or not ({"audience", "privacy"} & set(text.replace(",", " ").split())):
            errors.append(f"privacy-audience:{identifier}")

    counts = candidate.get("counts", {})
    if counts.get("requirements") != len(candidate["requirements"]) or counts.get("requirements") != 237:
        errors.append("requirement-count")
    if counts.get("revision_decisions") != len(candidate["revision_decisions"]) or counts.get("revision_decisions") != 144:
        errors.append("decision-count")

    rows = readable_rows(markdown, set(candidate_ids))
    if set(rows) != set(candidate_ids) or len(rows) != len(candidate_ids):
        errors.append("readable-parity")
    else:
        for item in candidate["requirements"]:
            line = rows[item["id"]]
            if escape(item["title"]) not in line or escape(item["acceptance"]) not in line or escape(item["status"]) not in line:
                errors.append(f"readable-parity:{item['id']}")
    return sorted(set(errors))


def adverse_tests(base: dict, candidate: dict, markdown: str, map_payload: dict) -> list[dict]:
    cases = []

    def run(name: str, mutate, expected: str) -> None:
        mutated = copy.deepcopy(candidate)
        mutated_markdown = markdown
        value = mutate(mutated, mutated_markdown)
        if isinstance(value, str):
            mutated_markdown = value
        errors = validate(base, mutated, mutated_markdown, map_payload)
        cases.append({"name": name, "expected_error": expected, "errors": errors,
                      "rejected": any(expected in error for error in errors)})

    run("duplicate_requirement", lambda d, m: d["requirements"].append(copy.deepcopy(d["requirements"][-1])), "duplicate-requirement-id")

    def behavior_control(d: dict, _: str) -> None:
        next(item for item in d["requirements"] if item["id"] == "U192")["acceptance"] += "; system selects participant beliefs"
    run("behavior_control_outcome", behavior_control, "behavior-control:U192")

    def missing_privacy(d: dict, _: str) -> None:
        item = next(item for item in d["requirements"] if item["id"] == "U194")
        item["invariant_refs"] = []
        item["rationale_refs"] = EXPECTED_INTENTS.copy()
        item["acceptance"] = "Contexts are listed without audience or protected-boundary semantics"
    run("missing_privacy_audience", missing_privacy, "privacy-audience:U194")

    def conformity_metric(d: dict, _: str) -> None:
        next(item for item in d["requirements"] if item["id"] == "U203")["acceptance"] += "; agreement_rate is a success signal"
    run("conformity_metric", conformity_metric, "behavior-control:U203")

    def unrelated_drift(d: dict, _: str) -> None:
        d["requirements"][0]["title"] += " altered"
    run("unrelated_predecessor_drift", unrelated_drift, "unrelated-predecessor-drift")

    run("generated_readable_mismatch", lambda d, m: "\n".join(line for line in m.splitlines() if not line.startswith("| U192 |")), "readable-parity")
    return cases


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--candidate-dir", type=Path, default=ROOT / "drafts")
    parser.add_argument("--base-ref", default=DEFAULT_BASE_REF)
    args = parser.parse_args()
    candidate_dir = args.candidate_dir if args.candidate_dir.is_absolute() else ROOT / args.candidate_dir
    candidate_json_path = candidate_dir / "hirc_requirements_v1_1-draft.json"
    candidate_md_path = candidate_dir / "hirc_requirements_v1_1-draft.md"
    base_json_bytes = git_file(args.base_ref, "drafts/hirc_requirements_v1_1-draft.json")
    base_md_bytes = git_file(args.base_ref, "drafts/hirc_requirements_v1_1-draft.md")
    base = json.loads(base_json_bytes.decode("utf-8"))
    candidate = json.loads(candidate_json_path.read_text(encoding="utf-8"))
    markdown = candidate_md_path.read_text(encoding="utf-8")
    map_payload = json.loads(MAP.read_text(encoding="utf-8"))
    errors = validate(base, candidate, markdown, map_payload)
    adverse = adverse_tests(base, candidate, markdown, map_payload)
    result = {
        "schema": "hirc.cultural-requirements-validation/1",
        "stone": "M03-S005",
        "before": {
            "git_ref": args.base_ref,
            "json_sha256": digest_bytes(base_json_bytes),
            "markdown_sha256": digest_bytes(base_md_bytes),
            "requirements": len(base["requirements"]),
            "revision_decisions": len(base["revision_decisions"]),
        },
        "after": {
            "json_sha256": digest(candidate_json_path),
            "markdown_sha256": digest(candidate_md_path),
            "requirements": len(candidate["requirements"]),
            "revision_decisions": len(candidate["revision_decisions"]),
        },
        "generator": {"path": "review/build_requirements_v1_1.py", "sha256": digest(GENERATOR)},
        "cultural_map": {"path": "review/revision-map-addendum-cultural-commons-v1.json", "sha256": digest(MAP)},
        "positive": {"accepted": not errors, "errors": errors},
        "adverse": adverse,
        "all_adverse_rejected": all(item["rejected"] for item in adverse),
        "claim": "Exact U192-U204/CIE-001-CIE-012 generator integration, separate I022/I023/I024 traces, unchanged predecessor semantics and machine/readable parity only; not consensus, implementation or runtime evidence.",
    }
    OUT.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps(result, indent=2))
    return 0 if not errors and result["all_adverse_rejected"] else 1


if __name__ == "__main__":
    raise SystemExit(main())

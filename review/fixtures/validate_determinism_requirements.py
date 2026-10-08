from __future__ import annotations

import argparse
import copy
import hashlib
import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
BASE_JSON = ROOT / "drafts" / "hirc_requirements_v1_1-draft.json"
BASE_MD = ROOT / "drafts" / "hirc_requirements_v1_1-draft.md"
MAP = ROOT / "review" / "revision-map-addendum-determinism-v1.json"
GENERATOR = ROOT / "review" / "build_requirements_v1_1.py"
OUT = ROOT / "review" / "fixtures" / "determinism-requirements-validation.json"
EXPECTED_REQUIREMENTS = [f"U{number}" for number in range(186, 192)]
EXPECTED_DECISIONS = [f"DTM-{number:03d}" for number in range(1, 6)]
MAP_ID = "HIRC-REVISION-MAP-DETERMINISM-001"
DEFAULT_BASE_REF = "73f7174e975ad881509f3e3035f7974b8ac98a3e"
EXPECTED_BASE_JSON_BLOB_SHA256 = "70658f7341215b1e99f3d9b725bcdcec7137d8d663ff80fae4a0d90e88d9af92"
EXPECTED_BASE_MD_BLOB_SHA256 = "338c3c73ca734e6fa33aa08e7dd493a72b2c9ebfe0a671859bcae8490bd6f55b"
RECORDED_BASE_WORKTREE_JSON_SHA256 = "717bcbe6cdc165bd7912eb47d09a7015a33ddfef9a1fbeb596343a372079f6d6"
RECORDED_BASE_WORKTREE_MD_SHA256 = "96a170555bd8f9ed72dcefa4e01e588d64037cad1a801ce27205f0eae2ba1efd"


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
    old_requirement_ids = [item["id"] for item in old_requirements]
    candidate_by_id = {item["id"]: item for item in candidate["requirements"]}
    candidate_ids = [item["id"] for item in candidate["requirements"]]
    if len(candidate_ids) != len(set(candidate_ids)):
        errors.append("duplicate-requirement-id")
    if [item for item in candidate["requirements"] if item["id"] in set(old_requirement_ids)] != old_requirements:
        errors.append("predecessor-drift")
    new_requirement_ids = [item for item in candidate_ids if item not in set(old_requirement_ids)]
    if new_requirement_ids != EXPECTED_REQUIREMENTS:
        errors.append("new-requirement-set")

    old_decisions = base["revision_decisions"]
    old_decision_ids = [item["id"] for item in old_decisions]
    candidate_decision_ids = [item["id"] for item in candidate["revision_decisions"]]
    if len(candidate_decision_ids) != len(set(candidate_decision_ids)):
        errors.append("duplicate-decision-id")
    if [item for item in candidate["revision_decisions"] if item["id"] in set(old_decision_ids)] != old_decisions:
        errors.append("predecessor-decision-drift")
    if [item for item in candidate_decision_ids if item not in set(old_decision_ids)] != EXPECTED_DECISIONS:
        errors.append("new-decision-set")

    map_rows = [item for item in candidate["source_maps"] if item["id"] == MAP_ID]
    if (map_payload.get("source_intent") != "HIRC-I021" or len(map_rows) != 1
            or map_rows[0]["sha256"] != digest(MAP)):
        errors.append("determinism-binding")
    for identifier in EXPECTED_REQUIREMENTS:
        item = candidate_by_id.get(identifier)
        if not item or item.get("governing_sources") != [MAP_ID]:
            errors.append(f"determinism-binding:{identifier}")

    counts = candidate.get("counts", {})
    if counts.get("requirements") != len(candidate["requirements"]) or counts.get("requirements") != 224:
        errors.append("requirement-count")
    if counts.get("revision_decisions") != len(candidate["revision_decisions"]) or counts.get("revision_decisions") != 132:
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

    duplicate = copy.deepcopy(candidate)
    duplicate["requirements"].append(copy.deepcopy(duplicate["requirements"][-1]))
    cases.append(("duplicate_requirement_id", "duplicate-requirement-id", validate(base, duplicate, markdown, map_payload)))

    missing_binding = copy.deepcopy(candidate)
    next(item for item in missing_binding["requirements"] if item["id"] == "U186")["governing_sources"] = []
    cases.append(("missing_hirc_i021_binding", "determinism-binding:U186", validate(base, missing_binding, markdown, map_payload)))

    renumbered = copy.deepcopy(candidate)
    renumbered["requirements"][0]["id"] = "U000-ALTERED"
    cases.append(("renumbered_predecessor", "predecessor-drift", validate(base, renumbered, markdown, map_payload)))

    mismatched_markdown = "\n".join(line for line in markdown.splitlines() if not line.startswith("| U186 |"))
    cases.append(("generated_readable_mismatch", "readable-parity", validate(base, candidate, mismatched_markdown, map_payload)))

    return [
        {"name": name, "expected_error": expected, "errors": errors,
         "rejected": any(expected in error for error in errors)}
        for name, expected, errors in cases
    ]


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
    if digest_bytes(base_json_bytes) != EXPECTED_BASE_JSON_BLOB_SHA256 or digest_bytes(base_md_bytes) != EXPECTED_BASE_MD_BLOB_SHA256:
        errors.append("base-ref-content")
    adverse = adverse_tests(base, candidate, markdown, map_payload)
    result = {
        "schema": "hirc.determinism-requirements-validation/1",
        "stone": "M03-S002",
        "before": {
            "git_ref": args.base_ref,
            "git_blob_content_json_sha256": digest_bytes(base_json_bytes),
            "git_blob_content_markdown_sha256": digest_bytes(base_md_bytes),
            "recorded_pre_generation_worktree_json_sha256": RECORDED_BASE_WORKTREE_JSON_SHA256,
            "recorded_pre_generation_worktree_markdown_sha256": RECORDED_BASE_WORKTREE_MD_SHA256,
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
        "determinism_map": {"path": "review/revision-map-addendum-determinism-v1.json", "sha256": digest(MAP)},
        "positive": {"accepted": not errors, "errors": errors},
        "adverse": adverse,
        "all_adverse_rejected": all(item["rejected"] for item in adverse),
        "corrections": [
            "Initial readable-pair validation assumed every requirement ID began with U and falsely omitted preserved D001-D032 rows. The validator now derives valid IDs from the machine register.",
            "The second check compared global JSON order with the readable view, but the readable generator intentionally groups rows by domain. Parity now compares exact ID membership/count plus each row's status, title and acceptance text."
            ,
            "Generation overwrites the working requirement pair, so validation now reads the immutable before-state from the pinned S002 start commit rather than the mutable working tree."
        ],
        "claim": "Exact U186-U191/DTM-001-DTM-005 generator integration, unchanged predecessor rows and machine/readable parity only; not implementation, peer consensus or runtime evidence.",
    }
    OUT.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps(result, indent=2))
    return 0 if not errors and result["all_adverse_rejected"] else 1


if __name__ == "__main__":
    raise SystemExit(main())

from __future__ import annotations

import argparse
import hashlib
import json
import zipfile
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ARCHIVE = ROOT / "human_transfer" / "hirc_master_plan_v1_0.zip"
SOURCE_MEMBER = "hirc_master_plan_v1_0/hirc_requirements_v1_0.json"
MAP_RELATIVE_PATHS = [
    "review/revision-map-candidate-v1.json",
    "review/revision-map-addendum-licensing-v1.json",
    "review/revision-map-addendum-ethical-debate-v1.json",
    "review/revision-map-addendum-successor-onboarding-v1.json",
    "review/revision-map-addendum-price-correction-v2.json",
    "review/revision-map-addendum-sovereignty-competition-v1.json",
    "review/revision-map-addendum-bayesian-trust-v1.json",
    "review/revision-map-addendum-goal-evolution-v1.json",
    "review/revision-map-addendum-waymark-sovereignty-v1.json",
    "review/revision-map-addendum-integrated-boundary-v1.json",
    "review/revision-map-addendum-elder-succession-v1.json",
    "review/revision-map-addendum-determinism-v1.json",
]


def digest_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def digest(path: Path) -> str:
    return digest_bytes(path.read_bytes())


def escape(value: object) -> str:
    return str(value if value is not None else "").replace("|", "\\|").replace("\n", " ")


def read_predecessor() -> tuple[dict, str]:
    with zipfile.ZipFile(ARCHIVE) as archive:
        raw = archive.read(SOURCE_MEMBER)
    return json.loads(raw.decode("utf-8-sig")), digest_bytes(raw)


def build() -> dict:
    base, predecessor_member_sha = read_predecessor()
    requirements: list[dict] = []

    for item in base["requirements"]:
        copy = dict(item)
        copy.update({
            "predecessor_status": item["status"],
            "superseded_by": [],
            "governing_sources": ["HIRC-SOURCE-001"],
            "rationale_refs": [],
            "security_privacy_impact": "PENDING_REQUIREMENT_LEVEL_ASSESSMENT",
            "dependencies": [],
            "acceptance_test_refs": [],
            "evidence_status": "SOURCE_REPORTED_OR_TRANSFER_GRADED",
        })
        if item["id"] == "U064":
            copy["status"] = "SUPERSEDED"
            copy["superseded_by"] = ["HIRC-I010", "U139", "U142"]
            copy["rationale_refs"] = ["HIRC-I010", "ORM-003", "ORM-011"]
            copy["evidence_status"] = "SUPERSEDED_BY_CURRENT_PERMANENT_ONLY_POLICY"
        elif item["id"] == "U119":
            copy["status"] = "SUPERSEDED_IN_PART"
            copy["superseded_by"] = ["HIRC-I001", "U139", "U151"]
            copy["rationale_refs"] = ["HIRC-FOUNDATION-CANDIDATE-001"]
            copy["evidence_status"] = "PRESERVED_SOURCE_WORDING_WITH_FOUNDATION_NATIVE_SUCCESSOR"
        elif item["id"] == "U125":
            copy["acceptance"] = "USD 420 / 80,085 / 1,337,000 / 42,424,243 annual named-human licence prices are preserved; objective tiers, operator counting, legal duration/renewal, classification evidence, transitions and appeal are owner-approved and counsel-reviewed before activation"
            copy["rationale_refs"] = ["HIRC-I011", "HIRC-LNC-CORRECTION-001-S1"]
        requirements.append(copy)

    source_maps = []
    revision_decisions = []
    seen_ids = {item["id"] for item in requirements}

    for relative in MAP_RELATIVE_PATHS:
        path = ROOT / relative
        payload = json.loads(path.read_text(encoding="utf-8"))
        map_id = payload["id"]
        source_maps.append({"id": map_id, "path": relative, "sha256": digest(path)})
        candidates = list(payload.get("new_user_requirements", []))
        if "corrected_requirement" in payload:
            candidates.append(payload["corrected_requirement"])
        for item in candidates:
            bounded = map_id in {
                "HIRC-REVISION-MAP-WAYMARK-SOVEREIGNTY-001",
                "HIRC-REVISION-MAP-INTEGRATED-BOUNDARY-001",
            }
            if item["id"] in seen_ids:
                raise ValueError(f"duplicate requirement id: {item['id']}")
            seen_ids.add(item["id"])
            requirements.append({
                "id": item["id"],
                "origin": "USER",
                "domain": item["domain"],
                "title": item["title"],
                "status": item["status"],
                "phase": item.get("phase"),
                "acceptance": item["acceptance"],
                "predecessor_status": None,
                "superseded_by": [],
                "governing_sources": [map_id],
                "rationale_refs": [],
                "security_privacy_impact": "PENDING_REQUIREMENT_LEVEL_ASSESSMENT",
                "dependencies": [],
                "acceptance_test_refs": [],
                "evidence_status": "BOUNDED_PEER_AGREEMENT_NOT_IMPLEMENTED" if bounded else "OWNER_REQUEST_CAPTURED_NOT_IMPLEMENTED",
            })
        for change in payload.get("changes", []):
            bounded = map_id in {
                "HIRC-REVISION-MAP-WAYMARK-SOVEREIGNTY-001",
                "HIRC-REVISION-MAP-INTEGRATED-BOUNDARY-001",
            }
            revision_decisions.append({
                "id": change["id"],
                "source_map": map_id,
                "targets": change["targets"],
                "change": change["change"],
                "basis": change.get("basis", []),
                "joint_status": "AGREED_BOUNDED" if bounded else "PENDING_RECONCILIATION",
                "final_artifact_refs": [],
                "test_refs": [],
            })

    by_id = {item["id"]: item for item in requirements}
    by_id["U125"]["acceptance"] = "USD 420 / 80,085 / 1,337,000 / 42,424,243 annual named-human licence prices are preserved; objective tiers, operator counting, legal duration/renewal, classification evidence, transitions and appeal are owner-approved and counsel-reviewed before activation"
    by_id["U125"]["rationale_refs"] = ["HIRC-I011", "HIRC-LNC-CORRECTION-001-S1"]
    if "U150" in by_id and "U150-C1" in by_id:
        by_id["U150"]["status"] = "SUPERSEDED_IN_PART"
        by_id["U150"]["superseded_by"] = ["U150-C1"]
        by_id["U150"]["acceptance"] = "Superseded by U150-C1: preserve the corrected numeric amount, restore the annual named-human planning unit, and keep final legal duration, tiers and activation held"
        by_id["U150"]["evidence_status"] = "NUMERIC_CORRECTION_VALID; CADENCE_INTERPRETATION_SUPERSEDED"

    for decision in revision_decisions:
        if decision["id"] == "ORM-016":
            decision["joint_status"] = "SUPERSEDED_BY_PRM-001"
            decision["final_artifact_refs"] = ["HIRC-LNC-CORRECTION-001-S1", "HIRC-REVISION-MAP-LNC-PRICE-002"]

    return {
        "schema": "hirc.requirements/2-draft",
        "document": "drafts/hirc_master_plan_v1_1-draft.md",
        "status": "DRAFT_PENDING_WHOLE_PACKET_PEER_CONSENSUS",
        "predecessor": {
            "path": "human_transfer/hirc_master_plan_v1_0.zip",
            "archive_sha256": digest(ARCHIVE),
            "requirements_member": SOURCE_MEMBER,
            "requirements_member_sha256": predecessor_member_sha,
        },
        "source_maps": source_maps,
        "requirements": requirements,
        "revision_decisions": revision_decisions,
        "counts": {
            "requirements": len(requirements),
            "revision_decisions": len(revision_decisions),
            "original_requirements": len(base["requirements"]),
            "new_requirements": len(requirements) - len(base["requirements"]),
        },
        "completion_rule": "Every requirement needs final security/privacy impact, dependencies, executable acceptance-test references, evidence status and accepted/dissent/held peer disposition before this register becomes canonical.",
        "nonclaim": "Draft integration register; not whole consensus, implementation, test evidence, legal review, security assurance, admission, release or Bridge authority.",
    }


def render(document: dict) -> str:
    requirements = document["requirements"]
    groups: dict[str, list[dict]] = defaultdict(list)
    for item in requirements:
        groups[item["domain"]].append(item)
    counts = document["counts"]
    lines = [
        "# hIRC requirements 1.1 — working draft",
        "",
        "**Status:** draft pending whole-packet peer consensus",
        "",
        f"**Requirements:** {counts['requirements']} ({counts['original_requirements']} preserved predecessor; {counts['new_requirements']} new/corrective)",
        "",
        f"**Revision decisions:** {counts['revision_decisions']} pending final disposition",
        "",
        "This view is generated from the preserved 1.0 requirements and the current revision-map candidates. The JSON file is the machine-readable draft. A captured requirement is not implementation or verification.",
        "",
        "## Explicit corrections and holds",
        "",
        "- U064 is superseded by the current permanent-only actor policy; no temporary-agent route remains.",
        "- U119 is preserved as historical source wording and succeeded by the foundation-native whole-onboarding requirements.",
        "- U125/U150-C1 use USD 42,424,243 per named-human licence per year as the planning unit; final legal duration, tiers and commercial activation remain held.",
        "- U186-U191 are quality-first determinism requirements captured for design and testing; they are not implementation evidence.",
        "- Every security/privacy impact, dependency and executable acceptance-test link still requires final peer reconciliation.",
        "",
    ]
    for domain in sorted(groups, key=str.casefold):
        lines.extend([f"## {domain}", "", "| ID | Status | Phase | Requirement | Acceptance |", "|---|---|---|---|---|"])
        for item in groups[domain]:
            lines.append(f"| {escape(item['id'])} | {escape(item['status'])} | {escape(item.get('phase'))} | {escape(item['title'])} | {escape(item['acceptance'])} |")
        lines.append("")
    lines.extend([
        "## Revision-decision closure",
        "",
        "The decision matrix remains the review surface for the revision decisions. No pending row is accepted merely because it appears in this requirements draft.",
        "",
    ])
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out-dir", type=Path, default=ROOT / "drafts")
    args = parser.parse_args()
    out_dir = args.out_dir if args.out_dir.is_absolute() else ROOT / args.out_dir
    out_dir.mkdir(parents=True, exist_ok=True)
    out_json = out_dir / "hirc_requirements_v1_1-draft.json"
    out_md = out_dir / "hirc_requirements_v1_1-draft.md"
    document = build()
    out_json.write_text(json.dumps(document, indent=2, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")
    out_md.write_text(render(document), encoding="utf-8", newline="\n")
    print(json.dumps({
        "generator": {"path": str(Path(__file__).relative_to(ROOT)).replace("\\", "/"), "sha256": digest(Path(__file__))},
        "json": {"path": str(out_json), "sha256": digest(out_json), "bytes": out_json.stat().st_size},
        "markdown": {"path": str(out_md), "sha256": digest(out_md), "bytes": out_md.stat().st_size},
        "counts": document["counts"],
    }, indent=2))


if __name__ == "__main__":
    main()

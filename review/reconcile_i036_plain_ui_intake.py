#!/usr/bin/env python3
"""Add HIRC-I036 to current coverage and the post-freeze intake boundary."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def identity(path: str) -> dict[str, object]:
    body = (ROOT / path).read_bytes()
    return {"path": path, "sha256": hashlib.sha256(body).hexdigest(), "bytes": len(body)}


def render_coverage(value: dict) -> str:
    lines = [
        "# hIRC intent coverage — working draft",
        "",
        "| Intent | Status | Coverage | Revision maps | Process/history | Evidence files | Acceptance checks |",
        "|---|---|---|---|---|---:|---:|",
    ]
    for row in value["rows"]:
        revision = ", ".join(row["revision_map_ids"]) or "—"
        process = ", ".join(row["process_or_history_artifact_ids"]) or "—"
        lines.append(
            f"| {row['intent_id']} | {row['status']} | {row['coverage']} | {revision} | {process} | "
            f"{len(row['evidence_paths'])} | {row['acceptance_check_count']} |"
        )
    lines.extend([
        "",
        "Unmapped intents: none.",
        "Missing evidence paths: none.",
        "",
        "Reference coverage does not prove correct interpretation or completion. Final closure still requires the appropriate accepted disposition and implementation/test evidence.",
        "",
    ])
    return "\n".join(lines)


def main() -> None:
    intent = json.loads((ROOT / "intent-register.json").read_text(encoding="utf-8"))
    i036 = next(item for item in intent["items"] if item["id"] == "HIRC-I036")
    coverage_path = ROOT / "review/intent-coverage-draft-v1.json"
    coverage = json.loads(coverage_path.read_text(encoding="utf-8"))
    coverage["intent_register"]["sha256"] = identity("intent-register.json")["sha256"]
    coverage["rows"] = [row for row in coverage["rows"] if row["intent_id"] != "HIRC-I036"]
    coverage["rows"].append({
        "intent_id": "HIRC-I036",
        "status": i036["status"],
        "kind": i036["kind"],
        "coverage": "PROCESS_OR_HISTORY_MAPPED",
        "revision_map_ids": [],
        "process_or_history_artifact_ids": ["HIRC-CURRENT-DESCRIPTION-001", "HIRC-INTENT-001"],
        "evidence_paths": ["intent-register.json", "HIRC-CURRENT-DESCRIPTION.md"],
        "missing_evidence_paths": [],
        "acceptance_check_count": len(i036["acceptance_check"]),
        "next_action": i036["next_action"],
    })
    coverage["rows"].sort(key=lambda row: row["intent_id"])
    coverage["unmapped_intent_ids"] = []
    coverage["missing_evidence_paths"] = []
    coverage_path.write_bytes((json.dumps(coverage, indent=2, ensure_ascii=False) + "\n").encode("utf-8"))
    (ROOT / "review/intent-coverage-draft-v1.md").write_text(render_coverage(coverage), encoding="utf-8", newline="\n")

    intake_path = ROOT / "review/m03-s014-post-freeze-intake-v1.json"
    intake = json.loads(intake_path.read_text(encoding="utf-8"))
    intake["items"] = [item for item in intake["items"] if item["intent_id"] != "HIRC-I036"]
    intake["items"].append({
        "intent_id": "HIRC-I036",
        "disposition": "ACTIVE_PLAIN_USER_INTERFACE_LANGUAGE_REQUIREMENT",
        "effect_on_frozen_s014": "NONE; this current product-language requirement and observed Bridge-dialog defect do not alter frozen S014 packet bytes, specialist evidence or review criteria",
        "next": "Carry plain copy, direct recovery actions and optional technical details into post-S015 UI work and tests.",
    })
    current = intake["current_post_frame_state"]
    current["intent_register"] = {**identity("intent-register.json"), "intent_count": 36}
    current["intent_coverage"] = identity("review/intent-coverage-draft-v1.json")
    current["current_description"] = identity("HIRC-CURRENT-DESCRIPTION.md")
    intake_path.write_bytes((json.dumps(intake, indent=2, ensure_ascii=False) + "\n").encode("utf-8"))
    print(json.dumps({"intent_count": len(intent["items"]), "coverage_rows": len(coverage["rows"]), "post_freeze_items": len(intake["items"])}))


if __name__ == "__main__":
    main()

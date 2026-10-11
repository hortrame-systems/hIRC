#!/usr/bin/env python3
"""Verify that post-freeze owner intake cannot silently replace the S014 frame."""

from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
INTAKE = ROOT / "review" / "m03-s014-post-freeze-intake-v1.json"
RESULT = ROOT / "review" / "fixtures" / "m03-s014-post-freeze-intake-validation-v1.json"


def sha(body: bytes) -> str:
    return hashlib.sha256(body).hexdigest()


def git_blob(ref: str, path: str) -> bytes:
    return subprocess.run(
        ["git", "show", f"{ref}:{path}"],
        cwd=ROOT,
        check=True,
        capture_output=True,
    ).stdout


def git_has(ref: str, path: str) -> bool:
    return (
        subprocess.run(
            ["git", "cat-file", "-e", f"{ref}:{path}"],
            cwd=ROOT,
            capture_output=True,
        ).returncode
        == 0
    )


def main() -> int:
    intake = json.loads(INTAKE.read_text(encoding="utf-8"))
    frozen = intake["frozen_s014_frame"]
    current = intake["current_post_frame_state"]

    frozen_intent = git_blob("HEAD", frozen["reviewed_intent"]["path"])
    frozen_coverage = git_blob("HEAD", frozen["reviewed_intent_coverage"]["path"])
    current_intent = (ROOT / current["intent_register"]["path"]).read_bytes()
    current_coverage = (ROOT / current["intent_coverage"]["path"]).read_bytes()
    current_description = (ROOT / current["current_description"]["path"]).read_bytes()

    frozen_intent_json = json.loads(frozen_intent.decode("utf-8"))
    current_intent_json = json.loads(current_intent.decode("utf-8"))
    frozen_ids = {item["id"] for item in frozen_intent_json["items"]}
    current_ids = {item["id"] for item in current_intent_json["items"]}

    checks = {
        "frozen_intent_sha": sha(frozen_intent) == frozen["reviewed_intent"]["sha256"],
        "frozen_intent_bytes": len(frozen_intent) == frozen["reviewed_intent"]["bytes"],
        "frozen_coverage_sha": sha(frozen_coverage) == frozen["reviewed_intent_coverage"]["sha256"],
        "frozen_coverage_bytes": len(frozen_coverage) == frozen["reviewed_intent_coverage"]["bytes"],
        "current_intent_sha": sha(current_intent) == current["intent_register"]["sha256"],
        "current_intent_bytes": len(current_intent) == current["intent_register"]["bytes"],
        "current_coverage_sha": sha(current_coverage) == current["intent_coverage"]["sha256"],
        "current_coverage_bytes": len(current_coverage) == current["intent_coverage"]["bytes"],
        "current_description_sha": sha(current_description) == current["current_description"]["sha256"],
        "current_description_bytes": len(current_description) == current["current_description"]["bytes"],
        "frozen_intent_count": len(frozen_intent_json["items"]) == 26,
        "current_intent_count": len(current_intent_json["items"]) == 36,
        "post_frame_ids_absent_from_frozen": not ({"HIRC-I027", "HIRC-I028", "HIRC-I029", "HIRC-I030", "HIRC-I031", "HIRC-I032", "HIRC-I033", "HIRC-I034", "HIRC-I035", "HIRC-I036"} & frozen_ids),
        "post_frame_ids_present_current": {"HIRC-I027", "HIRC-I028", "HIRC-I029", "HIRC-I030", "HIRC-I031", "HIRC-I032", "HIRC-I033", "HIRC-I034", "HIRC-I035", "HIRC-I036"} <= current_ids,
        "description_absent_from_frozen_head": not git_has("HEAD", "HIRC-CURRENT-DESCRIPTION.md"),
        "no_frozen_frame_effect": all(item["effect_on_frozen_s014"].startswith("NONE") for item in intake["items"]),
        "i029_deferred_after_s015": any(
            item["intent_id"] == "HIRC-I029"
            and item["disposition"] == "DEFERRED_TO_POST_S015_HOLISTIC_SELF_REVIEW"
            for item in intake["items"]
        ),
        "i030_routes_without_frame_change": any(
            item["intent_id"] == "HIRC-I030"
            and item["disposition"] == "ACTIVE_POST_FREEZE_COORDINATION_CONTROL"
            for item in intake["items"]
        ),
        "i031_retirement_without_frame_change": any(
            item["intent_id"] == "HIRC-I031"
            and item["disposition"] == "ACTIVE_POST_FREEZE_HIRC_ELDER_RETIREMENT_CORRECTION"
            for item in intake["items"]
        ),
        "i032_tor_irc_deferred_without_frame_change": any(
            item["intent_id"] == "HIRC-I032"
            and item["disposition"] == "DEFERRED_TO_POST_M03_TOR_IRC_BRIDGE_TRANSPORT_STONES"
            for item in intake["items"]
        ),
        "i033_sidebar_without_frame_change": any(
            item["intent_id"] == "HIRC-I033"
            and item["disposition"] == "CURRENT_SIDEBAR_ACTIVE_AND_RETIRED_SECTIONS_VERIFIED"
            for item in intake["items"]
        ),
        "i034_retirement_latch_without_frame_change": any(
            item["intent_id"] == "HIRC-I034"
            and item["disposition"] == "VERIFIED_COMPACTION_RESISTANT_RETIREMENT_LATCH"
            for item in intake["items"]
        ),
        "i035_four_pair_plan_without_frame_change": any(
            item["intent_id"] == "HIRC-I035"
            and item["disposition"] == "ACTIVE_FOUR_PAIR_NON_MBV_PARALLEL_TEAM_PLAN"
            and item["effect_on_frozen_s014"].startswith("NONE;")
            for item in intake["items"]
        ),
        "i036_plain_ui_language_without_frame_change": any(
            item["intent_id"] == "HIRC-I036"
            and item["disposition"] == "ACTIVE_PLAIN_USER_INTERFACE_LANGUAGE_REQUIREMENT"
            and item["effect_on_frozen_s014"].startswith("NONE;")
            for item in intake["items"]
        ),
    }
    failures = [name for name, value in checks.items() if not value]
    result = {
        "schema": "hirc.m03-s014-post-freeze-intake-validation/1",
        "status": "PASS" if not failures else "FAIL",
        "intake": "review/m03-s014-post-freeze-intake-v1.json",
        "frozen_ref": "HEAD",
        "frozen_intent_sha256": sha(frozen_intent),
        "current_intent_sha256": sha(current_intent),
        "checks": checks,
        "failures": failures,
        "nonclaim": "Frame-separation validation only; not S014 review, implementation, S015 closure or release.",
    }
    RESULT.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps(result, indent=2))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())

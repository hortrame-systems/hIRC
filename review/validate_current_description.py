#!/usr/bin/env python3
"""Validate the current hIRC owner-handoff description against governed sources."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read_text(relative: str) -> str:
    return (ROOT / relative).read_text(encoding="utf-8")


def read_json(relative: str):
    return json.loads(read_text(relative))


def digest(relative: str) -> tuple[str, int]:
    body = (ROOT / relative).read_bytes()
    return hashlib.sha256(body).hexdigest(), len(body)


def git(*args: str) -> str:
    return subprocess.run(
        ["git", *args],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output")
    args = parser.parse_args()

    description = read_text("HIRC-CURRENT-DESCRIPTION.md")
    readme = read_text("README.md")
    intents = read_json("intent-register.json")
    requirements = read_json("drafts/hirc_requirements_v1_1-draft.json")
    matrix = read_json("review/joint-consensus-matrix-draft-v11.json")
    stones = read_json("review/milestone-03-stone-register.json")
    coverage = read_json("review/intent-coverage-draft-v1.json")
    coverage_md = read_text("review/intent-coverage-draft-v1.md")
    ledger = read_json("review/ledger.json")
    licensing = read_text("drafts/hirc_licensing_status_v0_1-draft.md")
    product_recheck = read_text("review/waymark-m03-s014-product-recheck-v1.md")

    checks: list[dict] = []

    def check(name: str, condition: bool, observed) -> None:
        checks.append({"name": name, "pass": bool(condition), "observed": observed})

    intent_items = intents["items"]
    intent_ids = [item["id"] for item in intent_items]
    intent_by_id = {item["id"]: item for item in intent_items}
    coverage_by_id = {item["intent_id"]: item for item in coverage["rows"]}
    stone_by_id = {item["id"]: item for item in stones["stones"]}
    ledger_by_id = {item["id"]: item for item in ledger["artifacts"]}

    description_sha, description_bytes = digest("HIRC-CURRENT-DESCRIPTION.md")
    intent_sha, _ = digest("intent-register.json")

    check("readme-link", "(HIRC-CURRENT-DESCRIPTION.md)" in readme, "linked")
    check("intent-count", len(intent_items) == 36, len(intent_items))
    check("unique-intent-ids", len(intent_ids) == len(set(intent_ids)), len(set(intent_ids)))
    check("requirement-count", len(requirements["requirements"]) == 237, len(requirements["requirements"]))
    check("decision-count", len(matrix["decisions"]) == 144, len(matrix["decisions"]))
    check("current-matrix", matrix.get("id") == "HIRC-JOINT-CONSENSUS-DRAFT-011" and matrix.get("status") == "DRAFT_M03_METRIC_REPAIR_3_PASS_RECHECK_PENDING_SECURITY_PENDING", {"id": matrix.get("id"), "status": matrix.get("status")})
    check("i027-present", "HIRC-I027" in intent_by_id, intent_by_id.get("HIRC-I027", {}).get("status"))
    check("i027-verified", intent_by_id["HIRC-I027"]["status"] == "VERIFIED", intent_by_id["HIRC-I027"]["status"])
    check(
        "i027-description-evidence",
        "HIRC-CURRENT-DESCRIPTION.md" in intent_by_id["HIRC-I027"]["evidence"],
        intent_by_id["HIRC-I027"]["evidence"],
    )
    check("i028-present", "HIRC-I028" in intent_by_id, intent_by_id.get("HIRC-I028", {}).get("status"))
    check("i028-deferred", intent_by_id["HIRC-I028"]["status"] == "DEFERRED", intent_by_id["HIRC-I028"]["status"])
    check(
        "i028-interruption-options",
        all(
            term in description
            for term in (
                "Interrupt and cut",
                "Interrupt with high priority",
                "Interrupt with low priority",
                "Custom",
            )
        ),
        "four-options-present",
    )
    check("i029-present", "HIRC-I029" in intent_by_id, intent_by_id.get("HIRC-I029", {}).get("status"))
    check("i029-deferred", intent_by_id["HIRC-I029"]["status"] == "DEFERRED", intent_by_id["HIRC-I029"]["status"])
    check(
        "i029-authority-accountability",
        all(
            term in description
            for term in (
                "every authority",
                "refusal and",
                "tamper evidence",
                "deferred until after S015",
            )
        ),
        "deferred-authority-accountability-review-present",
    )
    check("i030-present", "HIRC-I030" in intent_by_id, intent_by_id.get("HIRC-I030", {}).get("status"))
    check("i030-active", intent_by_id["HIRC-I030"]["status"] == "ACTIVE", intent_by_id["HIRC-I030"]["status"])
    check(
        "i030-team-unstall-protocol",
        all(
            term in description
            for term in (
                "Team stalls, peer responsibility and coordination",
                "LUCENT is the hIRC team lead",
                "Internal resolution is the default",
                "Email to the owner is reserved",
            )
        ),
        "team-lead-unstall-protocol-present",
    )
    check("i031-present", "HIRC-I031" in intent_by_id, intent_by_id.get("HIRC-I031", {}).get("status"))
    check("i031-active", intent_by_id["HIRC-I031"]["status"] == "ACTIVE", intent_by_id["HIRC-I031"]["status"])
    check(
        "i031-elder-retirement-boundary",
        all(term in description for term in ("15 percent", "Elder / Retired", "retires from", "active hIRC work")),
        "15-percent-visible-retirement-present",
    )
    check("i032-present", "HIRC-I032" in intent_by_id, intent_by_id.get("HIRC-I032", {}).get("status"))
    check("i032-deferred", intent_by_id["HIRC-I032"]["status"] == "DEFERRED", intent_by_id["HIRC-I032"]["status"])
    check(
        "i032-private-tor-irc",
        all(term in description for term in ("Private Tor IRC transport", "Tor v3 onion service", "clearnet listener", "traffic-correlation")),
        "private-tor-irc-create-connect-boundary-present",
    )
    check("i033-present", "HIRC-I033" in intent_by_id, intent_by_id.get("HIRC-I033", {}).get("status"))
    check("i033-verified", intent_by_id["HIRC-I033"]["status"] == "VERIFIED", intent_by_id["HIRC-I033"]["status"])
    check(
        "i033-sidebar-separation",
        all(term in description for term in ("hIRC Team", "hIRC Elders — Retired", "Retired participants are excluded")),
        "active-and-retired-sidebar-separation-present",
    )
    check("i034-present", "HIRC-I034" in intent_by_id, intent_by_id.get("HIRC-I034", {}).get("status"))
    check("i034-verified", intent_by_id["HIRC-I034"]["status"] == "VERIFIED", intent_by_id["HIRC-I034"]["status"])
    check("i034-retirement-latch", all(term in description for term in ("Retirement is latched", "Compaction", "reactivate an Elder")), "compaction-resistant-retirement-present")
    check("i035-present", "HIRC-I035" in intent_by_id, intent_by_id.get("HIRC-I035", {}).get("status"))
    check("i035-active", intent_by_id["HIRC-I035"]["status"] == "ACTIVE", intent_by_id["HIRC-I035"]["status"])
    check(
        "i035-four-pair-plan",
        all(term in description for term in ("Four paired work lanes", "AEGIS + KEEL", "PORTICO + ORIEL", "ROOT-01A12170-SECURITY + pending RADICAL", "RADICAL + APOTHEM", "RADICAL switches to ROOT", "fit non-retired partner", "seven assigned non-MBV permanent participants")),
        "four-non-mbv-pairs-present",
    )
    check("coverage-register-hash", coverage["intent_register"]["sha256"] == intent_sha, coverage["intent_register"]["sha256"])
    check("coverage-count", len(coverage["rows"]) == 36, len(coverage["rows"]))
    check("coverage-i027", coverage_by_id["HIRC-I027"]["status"] == "VERIFIED", coverage_by_id["HIRC-I027"]["status"])
    check("coverage-no-unmapped", coverage["unmapped_intent_ids"] == [], coverage["unmapped_intent_ids"])
    check("coverage-no-missing", coverage["missing_evidence_paths"] == [], coverage["missing_evidence_paths"])
    check("coverage-readable-i027", "| HIRC-I027 | VERIFIED |" in coverage_md, "row-present")
    check("coverage-i030", coverage_by_id["HIRC-I030"]["status"] == "ACTIVE", coverage_by_id["HIRC-I030"]["status"])
    check("coverage-readable-i030", "| HIRC-I030 | ACTIVE |" in coverage_md, "row-present")
    check("coverage-i031", coverage_by_id["HIRC-I031"]["status"] == "ACTIVE", coverage_by_id["HIRC-I031"]["status"])
    check("coverage-readable-i031", "| HIRC-I031 | ACTIVE |" in coverage_md, "row-present")
    check("coverage-i032", coverage_by_id["HIRC-I032"]["status"] == "DEFERRED", coverage_by_id["HIRC-I032"]["status"])
    check("coverage-readable-i032", "| HIRC-I032 | DEFERRED |" in coverage_md, "row-present")
    check("coverage-i033", coverage_by_id["HIRC-I033"]["status"] == "VERIFIED", coverage_by_id["HIRC-I033"]["status"])
    check("coverage-readable-i033", "| HIRC-I033 | VERIFIED |" in coverage_md, "row-present")
    check("coverage-i034", coverage_by_id["HIRC-I034"]["status"] == "VERIFIED", coverage_by_id["HIRC-I034"]["status"])
    check("coverage-readable-i034", "| HIRC-I034 | VERIFIED |" in coverage_md, "row-present")
    check("coverage-i035", coverage_by_id["HIRC-I035"]["status"] == "ACTIVE", coverage_by_id["HIRC-I035"]["status"])
    check("coverage-readable-i035", "| HIRC-I035 | ACTIVE |" in coverage_md, "row-present")
    check("i036-present", "HIRC-I036" in intent_by_id, intent_by_id.get("HIRC-I036", {}).get("status"))
    check("i036-active", intent_by_id["HIRC-I036"]["status"] == "ACTIVE", intent_by_id["HIRC-I036"]["status"])
    check(
        "i036-plain-interface-language",
        all(term in description for term in ("Ordinary interface copy is plain and restrained", "Open settings", "Technical details")),
        "plain-user-copy-and-technical-details-boundary-present",
    )
    check("coverage-i036", coverage_by_id["HIRC-I036"]["status"] == "ACTIVE", coverage_by_id["HIRC-I036"]["status"])
    check("coverage-readable-i036", "| HIRC-I036 | ACTIVE |" in coverage_md, "row-present")

    passed_stones = [
        "M03-S001",
        "M03-S001A",
        *[f"M03-S{index:03d}" for index in range(2, 14)],
    ]
    check(
        "stones-s001-through-s013",
        all(stone_by_id[item]["status"] == "PASS" for item in passed_stones),
        {item: stone_by_id[item]["status"] for item in passed_stones},
    )
    check("stone-s014", stone_by_id["M03-S014"]["status"] == "PASS", stone_by_id["M03-S014"]["status"])
    check("stone-s015", stone_by_id["M03-S015"]["status"] == "PASS", stone_by_id["M03-S015"]["status"])

    check("description-counts", all(term in description for term in ("36 owner-linked items", "237 generated requirements", "144 decision rows")), "36/237/144")
    check(
        "description-implementation-scope",
        all(
            term in description
            for term in (
                "not a networked, sensitive-data, production or release-ready hIRC",
                "end-user UI remains read-only",
            )
        ),
        "developer-package-and-writable-cli-with-network-sensitive-production-release-holds",
    )
    check("description-price", "**42,424,243**" in description, "present")
    check("licensing-price", "**42,424,243**" in licensing and "42,424,242,423" in licensing, "current-and-superseded")
    check("product-recheck-pass", "Disposition: PASS for F01-F03" in product_recheck, "PASS F01-F03")
    check(
        "product-recheck-residuals",
        all(term in product_recheck for term in ("security", "privacy-engineering/dataflow", "metric/evaluator")),
        "three-open-dimensions",
    )

    ledger_entry = ledger_by_id["HIRC-CURRENT-DESCRIPTION-001"]
    check("ledger-description-hash", ledger_entry["sha256"] == description_sha, ledger_entry["sha256"])
    check("ledger-description-bytes", ledger_entry["bytes"] == description_bytes, ledger_entry["bytes"])
    check("ledger-intent-hash", ledger_by_id["HIRC-INTENT-001"]["sha256"] == intent_sha, ledger_by_id["HIRC-INTENT-001"]["sha256"])

    entrypoints = [
        "README.md",
        "intent-register.json",
        "drafts/hirc_master_plan_v1_1-draft.md",
        "drafts/hirc_master_plan_explained_v1_1-draft.md",
        "drafts/hirc_requirements_v1_1-draft.md",
        "drafts/hirc_requirements_v1_1-draft.json",
        "drafts/hirc_threat_model_v1_0-draft.md",
        "drafts/hirc_first_delivery_profile_v0_1-draft.md",
        "drafts/hirc_bridge_security_profile_v0_1-draft.md",
        "review/joint-consensus-matrix-draft-v11.json",
        "review/milestone-03-stone-register.md",
        "review/milestone-03-stone-register.json",
        "review/m03-integration-closure-v1.md",
        "review/waymark-m03-s014-product-recheck-v1.md",
        "review/ledger.json",
        "milestones/README.md",
    ]
    missing_entrypoints = [item for item in entrypoints if not (ROOT / item).is_file()]
    check("description-entrypoints", not missing_entrypoints, missing_entrypoints)

    head = git("rev-parse", "HEAD")
    remote = git("rev-parse", "origin/codex/hirc-master-plan-security")
    check("described-baseline-head", "1c525e3b464c58b6e037faaf6bb76626b32364e4" in description, head)
    check("described-content-commit", "df5b72713f0127e0789652f20870709827441c9f" in description, "content-commit-present")
    check("described-remote-head", "cc4af0dbd6c02cedf49ed1ea1e3da30732e0a4cf" in description and remote == "cc4af0dbd6c02cedf49ed1ea1e3da30732e0a4cf", remote)

    failures = [item["name"] for item in checks if not item["pass"]]
    result = {
        "schema": "hirc.current-description-validation/1",
        "status": "PASS" if not failures else "FAIL",
        "description": {
            "path": "HIRC-CURRENT-DESCRIPTION.md",
            "sha256": description_sha,
            "bytes": description_bytes,
        },
        "source_counts": {
            "intents": len(intent_items),
            "requirements": len(requirements["requirements"]),
            "decisions": len(matrix["decisions"]),
        },
        "git_frame": {"head": head, "public_branch": remote},
        "checks": checks,
        "failures": failures,
        "nonclaim": "Deterministic current-description consistency, not product implementation, S014 closure, security/privacy/statistical assurance, milestone completion or release.",
    }
    rendered = json.dumps(result, indent=2, ensure_ascii=False) + "\n"
    if args.output:
        output = (ROOT / args.output).resolve()
        if ROOT not in output.parents:
            raise SystemExit("output escapes repository")
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(rendered, encoding="utf-8", newline="\n")
    print(rendered, end="")
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())

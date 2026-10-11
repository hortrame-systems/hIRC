#!/usr/bin/env python3
"""Render the canonical hIRC team coordination register as readable Markdown."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "review/hirc-team-stall-register-v1.json"
OUTPUT = ROOT / "review/hirc-team-stall-register-v1.md"


def cell(value: object) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ")


def main() -> int:
    document = json.loads(SOURCE.read_text(encoding="utf-8"))
    controller = document["controller"]
    policy = document["hirc_elder_policy"]
    team_plan = document["parallel_team_plan"]
    heartbeat = team_plan["team_health_heartbeat"]
    onboarding = team_plan["onboarding_lane"]
    lines = [
        "# hIRC team stall and unstall register",
        "",
        f"**Status:** {cell(document['status'])}  ",
        f"**Source intent:** {cell(document['source_intent'])}  ",
        f"**Controller:** {cell(controller['actor'])} / {cell(controller['technical_id'])}, project generation {controller['project_generation']}",
        "",
        "This is a deterministic readable projection of the canonical JSON register. It does not grant identity, competence, consent, custody, source access or authority.",
        "",
        "## Retirement and team-health controls",
        "",
        f"The hIRC retirement boundary is **{policy['activation_percent']}% remaining** and is latched to the permanent participant identity. {cell(policy['retirement_latch'])}",
        "",
        f"The existing **{cell(heartbeat['automation_id'])}** heartbeat is {cell(heartbeat['state'])} at {cell(heartbeat['cadence'])}. {cell(heartbeat['notification'])}",
        "",
        f"KEEL owns the single onboarding queue `{cell(onboarding['id'])}`. {cell(onboarding['non_authority'])}",
        "",
        "## Active coordinated participants",
        "",
        "| Participant | State | Owned work |",
        "|---|---|---|",
    ]
    for participant in document["active_team"]:
        lines.append(f"| {cell(participant['actor'])} | {cell(participant['state'])} | {cell(participant['owned_work'])} |")
    lines.extend(["", "## Retired participants", "", "| Participant | Visible title | Basis | New work |", "|---|---|---|---|"])
    for participant in document["retired_elders"]:
        lines.append(
            f"| {cell(participant['actor'])} | {cell(participant['visible_title'])} | {cell(participant['basis'])} | {cell(participant['new_work'])} |"
        )
    lines.extend(["", "## Four work lanes", "", "| Lane | Members | State | Deliverable | Peer unstall |", "|---|---|---|---|---|"])
    for team in team_plan["teams"]:
        lines.append(
            f"| {cell(team['id'])} | {cell(' + '.join(team['members']))} | {cell(team.get('state', 'ACTIVE'))} | {cell(team['deliverable'])} | {cell(team['peer_unstall'])} |"
        )
    lines.extend(["", "## Replacement readiness assessments", "", "| Candidate | Target lane | State | Body access | Next action |", "|---|---|---|---|---|"])
    for candidate in team_plan.get("replacement_readiness", []):
        lines.append(
            f"| {cell(candidate['actor'])} | {cell(candidate['target_lane'])} | {cell(candidate['state'])} | {cell(candidate['body_access'])} | {cell(candidate['next_action'])} |"
        )
    reviewer_pool = team_plan.get("reviewer_onboarding_pool", {})
    lines.extend(["", "## Owner-selected reviewer onboarding pool", "", f"**State:** {cell(reviewer_pool.get('state', 'ABSENT'))}. {cell(reviewer_pool.get('non_authority', ''))}", "", "| Candidate | Target lane | State | Body access | Assignment |", "|---|---|---|---|---|"])
    for candidate in reviewer_pool.get("participants", []):
        lines.append(
            f"| {cell(candidate['actor'])} | {cell(candidate['target_lane'])} | {cell(candidate['state'])} | {cell(candidate['body_access'])} | {cell(candidate['assignment_created'])} |"
        )
    lines.extend(["", "## Current holds", "", "| Hold | State | Cause | Affected unit | Owners | Next action | Reopen when |", "|---|---|---|---|---|---|---|"])
    for hold in document["holds"]:
        lines.append(
            f"| {cell(hold['id'])} | {cell(hold['state'])} | {cell(', '.join(hold['cause']))} | {cell(hold['affected_unit'])} | {cell(hold['current_owner'])}; unstall: {cell(hold['unstall_owner'])} | {cell(hold['next_action'])} | {cell(hold['reopen_when'])} |"
        )
    lines.extend(["", "## Independently runnable sibling work", ""])
    for item in document["ready_sibling_work"]:
        lines.append(
            f"- **{cell(item['unit'])}** ({cell(item['state'])}, owner {cell(item['owner'])}): {cell(item['reason'])}"
        )
    lines.extend(
        [
            "",
            "## Boundaries",
            "",
            cell(document["notification_policy"]["internal"]),
            "",
            cell(document["notification_policy"]["email"]),
            "",
            cell(document["frozen_s014_effect"]),
            "",
            cell(document["nonclaim"]),
            "",
        ]
    )
    OUTPUT.write_text("\n".join(lines), encoding="utf-8", newline="\n")
    print(json.dumps({"status": "PASS", "path": OUTPUT.relative_to(ROOT).as_posix(), "active": len(document["active_team"]), "retired": len(document["retired_elders"]), "holds": len(document["holds"])}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

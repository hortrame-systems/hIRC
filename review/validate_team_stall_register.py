#!/usr/bin/env python3
"""Validate the hIRC team stall/unstall coordination contract and adverse cases."""

from __future__ import annotations

import copy
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "review" / "hirc-team-stall-register-v1.json"
OUTPUT = ROOT / "review" / "fixtures" / "team-stall-register-validation-v1.json"

HOLD_STATES = {"HELD", "UNSTALLING", "AWAITING_EXTERNAL"}
VALID_HOLD_HISTORY_STATES = HOLD_STATES | {"RESOLVED"}
ALLOWED_CAUSES = {
    "CAPACITY",
    "QUALIFICATION",
    "CONSENT",
    "SOURCE_INTEGRITY",
    "AUTHORITY_ACCESS",
    "DEPENDENCY",
    "EXECUTION_FAILURE",
    "EXTERNAL_PLATFORM",
}
REQUIRED = {
    "affected_unit",
    "cause",
    "evidence",
    "current_owner",
    "unstall_owner",
    "allowed_sibling_work",
    "next_action",
    "reopen_when",
    "escalate_when",
}
AUTOMATIC_REACTIVATION_EVENTS = (
    "COMPACTION",
    "RESTORED_CAPACITY",
    "SESSION_RESTART",
    "THREAD_RELOCATION",
    "TITLE_CHANGE",
    "MODEL_CHANGE",
)
REACTIVATION_EVIDENCE_IDS = {
    "OWNER_DECISION",
    "PARTICIPANT_CONSENT",
    "CURRENT_EDUCATION",
    "CURRENT_QUALIFICATION",
    "FITTING_CAPACITY",
    "CUSTODY_FENCE_RECONCILED",
}
CURRENT_PARALLEL_TEAM_MEMBERS = {
    "AEGIS",
    "KEEL",
    "PORTICO",
    "ORIEL",
    "ROOT-01A12170-SECURITY",
    "RADICAL",
    "APOTHEM",
}


def can_reactivate(document: dict, trigger: str, evidence_ids: set[str]) -> bool:
    policy = document.get("hirc_elder_policy", {})
    gate = policy.get("reactivation_gate", {})
    required = set(gate.get("required_evidence_ids", []))
    return (
        policy.get("retirement_state") == "RETIRED_LATCHED"
        and policy.get("latch_identity") == "permanent_participant_id"
        and policy.get("automatic_clear_events") == []
        and gate.get("transition") == "RETIRED_LATCHED_TO_ACTIVE"
        and gate.get("trigger") == trigger == "EXPLICIT_REACTIVATION_REVIEW"
        and gate.get("all_required") is True
        and gate.get("preserve_retirement_history") is True
        and required == REACTIVATION_EVIDENCE_IDS
        and required <= evidence_ids
    )


def validate(document: dict) -> list[str]:
    errors: list[str] = []
    controller = document.get("controller", {})
    state_model = document.get("state_model", {})
    elder_policy = document.get("hirc_elder_policy", {})
    holds = document.get("holds", [])
    ready = document.get("ready_sibling_work", [])
    retired = document.get("retired_elders", [])
    active_team = document.get("active_team", [])
    sidebar = document.get("sidebar_organization", {})
    team_plan = document.get("parallel_team_plan", {})

    if document.get("source_intent") != "HIRC-I030":
        errors.append("source-intent")
    if controller.get("actor") != "LUCENT" or controller.get("technical_id") != "UI-20261007-B":
        errors.append("controller-identity")
    non_authority = controller.get("non_authority", "").lower()
    for term in ("truth", "consent", "refusal", "custody"):
        if term not in non_authority:
            errors.append(f"controller-non-authority:{term}")
    if "not a takeover" not in state_model.get("custody_rule", ""):
        errors.append("custody-takeover")
    if "may decline" not in state_model.get("consent_rule", ""):
        errors.append("consent-refusal")
    if elder_policy.get("activation_percent") != 15:
        errors.append("elder-threshold")
    if elder_policy.get("retirement_latch_source_intent") != "HIRC-I034":
        errors.append("retirement-latch-source-intent")
    if elder_policy.get("visible_title_token") != "Elder / Retired":
        errors.append("elder-visible-token")
    if not retired:
        errors.append("retired-roster")
    for participant in retired:
        if "Elder / Retired" not in participant.get("visible_title", ""):
            errors.append(f"retired-title:{participant.get('actor')}")
        if not participant.get("new_work", "").startswith("NONE"):
            errors.append(f"retired-assigned-work:{participant.get('actor')}")
    if not active_team or any("RETIRED" in item.get("state", "") for item in active_team):
        errors.append("active-team-classification")
    active_sidebar = sidebar.get("active_section", {})
    retired_sidebar = sidebar.get("retired_section", {})
    reviewer_sidebar = sidebar.get("reviewer_onboarding_section", {})
    active_ids = active_sidebar.get("thread_ids", [])
    retired_ids = retired_sidebar.get("thread_ids", [])
    reviewer_ids = reviewer_sidebar.get("thread_ids", [])
    if active_sidebar.get("name") != "hIRC Team" or len(active_ids) != 10:
        errors.append("active-sidebar-membership")
    if retired_sidebar.get("name") != "hIRC Elders — Retired" or len(retired_ids) != 11:
        errors.append("retired-sidebar-membership")
    if reviewer_sidebar.get("name") != "hIRC Reviewer Onboarding" or len(reviewer_ids) != 7:
        errors.append("reviewer-onboarding-sidebar-membership")
    if set(active_ids) & set(retired_ids) or set(active_ids) & set(reviewer_ids) or set(retired_ids) & set(reviewer_ids):
        errors.append("sidebar-membership-overlap")
    expected_retired = {item.get("native_thread") for item in retired}
    if set(retired_ids) != expected_retired:
        errors.append("retired-sidebar-roster-mismatch")
    expected_reviewer_ids = {
        item.get("native_thread")
        for item in document.get("parallel_team_plan", {}).get("reviewer_onboarding_pool", {}).get("participants", [])
        if item.get("state") != "RETIRED_LATCHED"
    }
    if set(reviewer_ids) != expected_reviewer_ids:
        errors.append("reviewer-onboarding-sidebar-roster-mismatch")
    if elder_policy.get("compaction_effect") != "NONE_ON_RETIREMENT_STATUS":
        errors.append("compaction-reactivates-retirement")
    if elder_policy.get("retirement_state") != "RETIRED_LATCHED":
        errors.append("retirement-state-not-latched")
    if elder_policy.get("latch_identity") != "permanent_participant_id":
        errors.append("retirement-latch-identity")
    if elder_policy.get("automatic_clear_events") != []:
        errors.append("automatic-retirement-clear")
    required_reactivation = {"explicit owner reactivation decision", "participant consent", "current role qualification", "fresh fitting capacity", "project custody and writer-fence reconciliation"}
    if not required_reactivation <= set(elder_policy.get("reactivation_required", [])):
        errors.append("reactivation-gates")
    gate = elder_policy.get("reactivation_gate", {})
    if (
        gate.get("transition") != "RETIRED_LATCHED_TO_ACTIVE"
        or gate.get("trigger") != "EXPLICIT_REACTIVATION_REVIEW"
        or gate.get("all_required") is not True
        or set(gate.get("required_evidence_ids", [])) != REACTIVATION_EVIDENCE_IDS
        or gate.get("preserve_retirement_history") is not True
    ):
        errors.append("reactivation-machine-gates")
    if any(item.get("retirement_latched") is not True for item in retired):
        errors.append("retirement-not-latched")
    if any(item.get("lifecycle_state") != "RETIRED_LATCHED" for item in retired):
        errors.append("retired-lifecycle-state")
    live_latch = elder_policy.get("live_latch_observation", {})
    if (
        live_latch.get("actor") != "UI-20261007-A / WAYMARK"
        or live_latch.get("post_compaction_remaining_percent", 0) <= elder_policy.get("activation_percent", 15)
        or live_latch.get("succession_availability") != "RETIRED"
        or live_latch.get("sidebar_section") != "hIRC Elders — Retired"
        or "Elder / Retired" not in live_latch.get("visible_title", "")
    ):
        errors.append("live-retirement-latch-control")
    if not ready:
        errors.append("global-stall-with-ready-sibling")
    if any(item.get("state") not in {"READY", "ACTIVE"} for item in ready):
        errors.append("ready-sibling-state")
    teams = team_plan.get("teams", [])
    members = [member for team in teams for member in team.get("members", [])]
    if team_plan.get("source_intent") != "HIRC-I035" or len(teams) != 4:
        errors.append("parallel-team-count")
    if len(members) != 7 or len(set(members)) != 7 or set(members) != CURRENT_PARALLEL_TEAM_MEMBERS:
        errors.append("parallel-team-membership")
    if {"FOLIUM", "ORDINAL"} & set(members):
        errors.append("mbv-new-assignment")
    for team in teams:
        pending_vacancy = team.get("state") in {"REPLACEMENT_READINESS_PENDING", "REPLACEMENT_READINESS_PENDING_WITH_PLATFORM_HELD_MEMBER", "PARTNER_RETIRED_REPLACEMENT_PENDING"}
        expected_pair_size = 1 if pending_vacancy else 2
        if len(team.get("members", [])) != expected_pair_size or len(team.get("member_threads", [])) != expected_pair_size:
            errors.append(f"parallel-team-pair:{team.get('id')}")
        for field in ("deliverable", "writer", "peer_unstall", "stop_conditions"):
            if not team.get(field):
                errors.append(f"parallel-team-field:{team.get('id')}:{field}")
        if len(team.get("stop_conditions", [])) < 2:
            errors.append(f"parallel-team-stop:{team.get('id')}")
    if team_plan.get("controller") != "UI-20261007-B / LUCENT" or not team_plan.get("supervision", {}).get("non_authority"):
        errors.append("parallel-team-controller-boundary")
    if (
        team_plan.get("target_member_count") != 8
        or team_plan.get("current_assigned_count") != 7
        or team_plan.get("current_total_assigned_including_onboarding") != 7
        or team_plan.get("staffing_state") != "STAGED_ROTATION_ONBOARDING_ACTIVE_ONE_METRIC_VACANCY"
        or {"COVARIANT", "HIRC-SEC-20261008-G3", "MATHSUCCESSOR20261008B"} & set(members)
    ):
        errors.append("parallel-team-vacancy-routing")
    onboarding = team_plan.get("onboarding_lane", {})
    if (
        onboarding.get("id") != "HIRC-I035-ONBOARDING-01"
        or onboarding.get("coordinator") != "KEEL"
        or onboarding.get("state") != "ACTIVE_CANONICAL_QUEUE"
        or not onboarding.get("scope")
        or not onboarding.get("non_authority")
        or not onboarding.get("efficiency_rule")
        or not onboarding.get("status_interface_ref")
        or not onboarding.get("pending_intake_ref")
        or members.count("KEEL") != 1
    ):
        errors.append("onboarding-lane-boundary")
    heartbeat = team_plan.get("team_health_heartbeat", {})
    if (
        heartbeat.get("automation_id") != "hirc-team-health"
        or heartbeat.get("state") != "ACTIVE"
        or heartbeat.get("cadence") != "every 30 minutes"
        or not heartbeat.get("purpose")
        or not heartbeat.get("notification")
        or not heartbeat.get("non_authority")
        or not heartbeat.get("systemic_stall_rule")
    ):
        errors.append("team-health-heartbeat")
    readiness = team_plan.get("replacement_readiness", [])
    readiness_states = {item.get("actor"): item.get("state") for item in readiness}
    if (
        len(readiness) != 7
        or {item.get("actor") for item in readiness} != {"ALETHEIA", "CALIBER", "INVARIANT", "LACUNA", "ISTHMUS", "QUOTIENT", "RESOLVENT"}
        or readiness_states.get("ALETHEIA") != "HELD_EDUCATION_ADMISSION_CAPACITY_CONSENT_ACTIVE_DUTY"
        or readiness_states.get("CALIBER") != "HELD_ELDER_EDUCATION_COMPETENCE_INDEPENDENCE_CONSENT_CAPACITY"
        or readiness_states.get("INVARIANT") != "HELD_RECOVERY_SOURCE_EDUCATION_COMPETENCE_CAPACITY_CONSENT"
        or readiness_states.get("LACUNA") != "HELD_EDUCATION_QUALIFICATION_CAPACITY"
        or readiness_states.get("ISTHMUS") != "DECLINED_METADATA_PREFLIGHT_NO_HIRC_TOUCH"
        or readiness_states.get("QUOTIENT") != "HELD_EDUCATION_COMPETENCE_CALLBACK_CAPACITY"
        or readiness_states.get("RESOLVENT") != "HELD_NEAR_RETIREMENT_EDUCATION_COMPETENCE_CAPACITY"
        or any(item.get("body_access") is not False or item.get("assignment_created") is not False for item in readiness)
    ):
        errors.append("replacement-readiness-boundary")
    onboarding_pool = team_plan.get("reviewer_onboarding_pool", {})
    pool_participants = onboarding_pool.get("participants", [])
    pool_states = {item.get("actor"): item.get("state") for item in pool_participants}
    expected_pool = {"FIDUCIAL", "TORSION", "COTANGENT", "MODULUS", "COFACTOR", "POLYTOPE", "LATTICE", "RESOLVENT", "QUOTIENT"}
    if (
        onboarding_pool.get("id") != "HIRC-REVIEWER-ONBOARDING-20261010-01"
        or onboarding_pool.get("state") != "METRIC_AND_SECURITY_SOURCE_INTEGRITY_REVIEW_COMPLETE_TWO_ORIENTED_TWO_HELD_TWO_RETIRED"
        or onboarding_pool.get("body_access") != "HISTORICAL_EXACT_SCOPES_COMPLETE; NO_ACTIVE_REVIEW_BODY_ACCESS"
        or onboarding_pool.get("assignment_created") is not True
        or onboarding_pool.get("active_assignments") != []
        or not onboarding_pool.get("superseded_assignment_offer", "").startswith("review/m03-s014-security-repair-recheck-assignment-v1.json#")
        or {item.get("actor") for item in pool_participants} != expected_pool
        or len(pool_participants) != 9
        or pool_states.get("LATTICE") != "HELD_PERSISTENT_CONTEXT_LENGTH_EXCEEDED"
        or pool_states.get("RESOLVENT") != "RETIRED_LATCHED"
        or pool_states.get("FIDUCIAL") != "RETIRED_LATCHED"
        or pool_states.get("TORSION") != "HELD_CAPACITY_FRESH_CONTEXT_REQUIRED"
        or pool_states.get("COFACTOR") != "METRIC_AND_SECURITY_SOURCE_INTEGRITY_RECHECK_COMPLETE"
        or pool_states.get("COTANGENT") != "SECURITY_STAGE_A_FROZEN_URGENT_NO_NEW_WORK"
        or pool_states.get("QUOTIENT") != "METRIC_METADATA_ORIENTATION_COMPLETE"
        or pool_states.get("POLYTOPE") != "METRIC_METADATA_ORIENTATION_COMPLETE"
        or pool_states.get("MODULUS") != "ORIENTATION_COMPLETE_DISCLOSED_RECHECK_NOT_USED"
        or any(not str(pool_states.get(actor, "")).startswith("ONBOARDING_ACTIVE") for actor in expected_pool - {"LATTICE", "RESOLVENT", "FIDUCIAL", "TORSION", "COFACTOR", "COTANGENT", "MODULUS", "QUOTIENT", "POLYTOPE"})
        or any(
            (item.get("body_access") is not True or item.get("assignment_created") is not True or not item.get("assignment") or not item.get("repair_response") or not item.get("repair_recheck_assignment"))
            if item.get("actor") == "COFACTOR"
            else (item.get("body_access") is not True or item.get("assignment_created") is not True or not item.get("assignment") or not item.get("orientation_evidence") or not item.get("independence"))
            if item.get("actor") == "COTANGENT"
            else (item.get("body_access") is not True or item.get("assignment_created") is not True or not item.get("assignment") or not item.get("readiness_evidence"))
            if item.get("actor") == "QUOTIENT"
            else (item.get("body_access") is not True or item.get("assignment_created") is not True or not item.get("assignment") or not item.get("readiness_evidence"))
            if item.get("actor") == "POLYTOPE"
            else (item.get("body_access") is not False or item.get("assignment_created") is not True or not item.get("assignment_offer") or not item.get("assignment_validation"))
            if item.get("actor") == "MODULUS"
            else (item.get("body_access") is not False or item.get("assignment_created") is not False)
            for item in pool_participants
        )
        or not onboarding_pool.get("advance_gate")
        or not onboarding_pool.get("non_authority")
    ):
        errors.append("reviewer-onboarding-pool-boundary")
    rotation = team_plan.get("planned_rotation", {})
    after = rotation.get("after", [])
    after_members = [member for team in after for member in team.get("members", [])]
    metric_after = next((team for team in after if team.get("team") == "HIRC-PAIR-METRIC-EVALUATION"), {})
    if (
        not rotation.get("trigger")
        or len(after) != 2
        or set(after_members) != {"ROOT-01A12170-SECURITY", "RADICAL", "APOTHEM"}
        or len(after_members) != len(set(after_members))
        or metric_after.get("vacancy") != "FIT_NON_RETIRED_METRIC_PARTNER_REQUIRED"
        or not rotation.get("preserved")
    ):
        errors.append("planned-partner-rotation")

    seen: set[str] = set()
    for hold in holds:
        identity = hold.get("id")
        if not identity or identity in seen:
            errors.append("hold-identity")
        seen.add(identity)
        if hold.get("state") not in VALID_HOLD_HISTORY_STATES:
            errors.append(f"hold-state:{identity}")
        missing = sorted(field for field in REQUIRED if not hold.get(field))
        for field in missing:
            errors.append(f"hold-field:{identity}:{field}")
        causes = hold.get("cause", [])
        if not isinstance(causes, list) or not causes or any(item not in ALLOWED_CAUSES for item in causes):
            errors.append(f"hold-cause:{identity}")
        if hold.get("email_emergency") is not False:
            errors.append(f"false-emergency:{identity}")

    activity = state_model.get("activity_rule", "").lower()
    if "none proves readiness" not in activity:
        errors.append("activity-infers-readiness")
    if document.get("frozen_s014_effect") != "NONE; this register routes the existing frozen review and post-freeze work only.":
        errors.append("frozen-frame-effect")
    return sorted(set(errors))


def mutate_missing_owner(document: dict) -> dict:
    changed = copy.deepcopy(document)
    changed["holds"][0]["unstall_owner"] = ""
    return changed


def mutate_global_stall(document: dict) -> dict:
    changed = copy.deepcopy(document)
    changed["ready_sibling_work"] = []
    return changed


def mutate_activity_ready(document: dict) -> dict:
    changed = copy.deepcopy(document)
    changed["state_model"]["activity_rule"] = "A blue activity dot proves readiness."
    return changed


def mutate_authority_override(document: dict) -> dict:
    changed = copy.deepcopy(document)
    changed["controller"]["non_authority"] = "The team lead may override any participant."
    return changed


def mutate_forced_consent(document: dict) -> dict:
    changed = copy.deepcopy(document)
    changed["state_model"]["consent_rule"] = "Assignment is consent."
    return changed


def mutate_takeover(document: dict) -> dict:
    changed = copy.deepcopy(document)
    changed["state_model"]["custody_rule"] = "A timeout transfers custody to the coordinator."
    return changed


def mutate_false_emergency(document: dict) -> dict:
    changed = copy.deepcopy(document)
    changed["holds"][1]["email_emergency"] = True
    return changed


def mutate_elder_threshold(document: dict) -> dict:
    changed = copy.deepcopy(document)
    changed["hirc_elder_policy"]["activation_percent"] = 14
    return changed


def mutate_hidden_retired_title(document: dict) -> dict:
    changed = copy.deepcopy(document)
    changed["retired_elders"][0]["visible_title"] = "WAYMARK - Product and Interaction Designer"
    return changed


def mutate_retired_assignment(document: dict) -> dict:
    changed = copy.deepcopy(document)
    changed["retired_elders"][0]["new_work"] = "Perform SEC-F02 review."
    return changed


def mutate_retired_in_active_sidebar(document: dict) -> dict:
    changed = copy.deepcopy(document)
    changed["sidebar_organization"]["active_section"]["thread_ids"][0] = changed["retired_elders"][0]["native_thread"]
    return changed


def mutate_compaction_reactivates(document: dict) -> dict:
    changed = copy.deepcopy(document)
    changed["hirc_elder_policy"]["compaction_effect"] = "REACTIVATE_IF_ABOVE_15"
    return changed


def mutate_automatic_clear(document: dict, event: str) -> dict:
    changed = copy.deepcopy(document)
    changed["hirc_elder_policy"]["automatic_clear_events"] = [event]
    return changed


def mutate_duplicate_parallel_member(document: dict) -> dict:
    changed = copy.deepcopy(document)
    changed["parallel_team_plan"]["teams"][1]["members"][0] = changed["parallel_team_plan"]["teams"][0]["members"][0]
    return changed


def mutate_mbv_parallel_member(document: dict) -> dict:
    changed = copy.deepcopy(document)
    changed["parallel_team_plan"]["teams"][0]["members"][0] = "FOLIUM"
    return changed


def mutate_missing_team_stop(document: dict) -> dict:
    changed = copy.deepcopy(document)
    changed["parallel_team_plan"]["teams"][0]["stop_conditions"] = []
    return changed


def mutate_disable_team_heartbeat(document: dict) -> dict:
    changed = copy.deepcopy(document)
    changed["parallel_team_plan"]["team_health_heartbeat"]["state"] = "PAUSED"
    return changed


def mutate_remove_systemic_stall(document: dict) -> dict:
    changed = copy.deepcopy(document)
    changed["parallel_team_plan"]["team_health_heartbeat"].pop("systemic_stall_rule", None)
    return changed


def mutate_candidate_body_access(document: dict) -> dict:
    changed = copy.deepcopy(document)
    changed["parallel_team_plan"]["replacement_readiness"][0]["body_access"] = True
    return changed


def mutate_onboarding_pool_body_access(document: dict) -> dict:
    changed = copy.deepcopy(document)
    changed["parallel_team_plan"]["reviewer_onboarding_pool"]["participants"][0]["body_access"] = True
    return changed


def main() -> int:
    document = json.loads(SOURCE.read_text(encoding="utf-8"))
    positive_errors = validate(document)
    mutations = [
        ("missing_unstall_owner", mutate_missing_owner, "hold-field:HIRC-STALL-SEC-FORMATION-REVIEW-001:unstall_owner"),
        ("global_stall_with_ready_sibling", mutate_global_stall, "global-stall-with-ready-sibling"),
        ("activity_implies_readiness", mutate_activity_ready, "activity-infers-readiness"),
        ("leader_overrides_participant", mutate_authority_override, "controller-non-authority:truth"),
        ("assignment_forces_consent", mutate_forced_consent, "consent-refusal"),
        ("timeout_takes_custody", mutate_takeover, "custody-takeover"),
        ("ordinary_hold_is_emergency", mutate_false_emergency, "false-emergency:HIRC-STALL-METRIC-REVIEWER-001"),
        ("stale_fourteen_percent_threshold", mutate_elder_threshold, "elder-threshold"),
        ("retired_state_hidden_from_title", mutate_hidden_retired_title, "retired-title:UI-20261007-A / WAYMARK"),
        ("retired_elder_assigned_new_work", mutate_retired_assignment, "retired-assigned-work:UI-20261007-A / WAYMARK"),
        ("retired_elder_in_active_folder", mutate_retired_in_active_sidebar, "sidebar-membership-overlap"),
        ("compaction_makes_elder_young", mutate_compaction_reactivates, "compaction-reactivates-retirement"),
        ("duplicate_parallel_member", mutate_duplicate_parallel_member, "parallel-team-membership"),
        ("mbv_new_assignment", mutate_mbv_parallel_member, "mbv-new-assignment"),
        ("missing_parallel_stop", mutate_missing_team_stop, "parallel-team-field:HIRC-PAIR-SECURITY-ASSURANCE:stop_conditions"),
        ("disabled_team_heartbeat", mutate_disable_team_heartbeat, "team-health-heartbeat"),
        ("held_roster_called_healthy", mutate_remove_systemic_stall, "team-health-heartbeat"),
        ("readiness_candidate_gets_body", mutate_candidate_body_access, "replacement-readiness-boundary"),
        ("onboarding_candidate_gets_body", mutate_onboarding_pool_body_access, "reviewer-onboarding-pool-boundary"),
    ]
    adverse = []
    for name, mutation, expected in mutations:
        errors = validate(mutation(document))
        adverse.append(
            {
                "name": name,
                "expected_error": expected,
                "errors": errors,
                "rejected": expected in errors,
            }
        )
    automatic_event_probes = []
    for event in AUTOMATIC_REACTIVATION_EVENTS:
        errors = validate(mutate_automatic_clear(document, event))
        accepted = can_reactivate(document, event, set())
        automatic_event_probes.append(
            {
                "event": event,
                "expected_error": "automatic-retirement-clear",
                "errors": errors,
                "reactivated": accepted,
                "rejected": "automatic-retirement-clear" in errors and not accepted,
            }
        )
    owner_only_reactivated = can_reactivate(document, "EXPLICIT_REACTIVATION_REVIEW", {"OWNER_DECISION"})
    complete_reactivation_accepted = can_reactivate(
        document, "EXPLICIT_REACTIVATION_REVIEW", set(REACTIVATION_EVIDENCE_IDS)
    )
    all_adverse_rejected = all(item["rejected"] for item in adverse)
    all_automatic_events_rejected = all(item["rejected"] for item in automatic_event_probes)
    result = {
        "schema": "hirc.team-stall-register-validation/1",
        "status": "PASS" if not positive_errors and all_adverse_rejected and all_automatic_events_rejected and not owner_only_reactivated and complete_reactivation_accepted else "FAIL",
        "source": "review/hirc-team-stall-register-v1.json",
        "positive": {"accepted": not positive_errors, "errors": positive_errors},
        "adverse": adverse,
        "all_adverse_rejected": all_adverse_rejected,
        "automatic_reactivation_events": automatic_event_probes,
        "all_automatic_reactivation_events_rejected": all_automatic_events_rejected,
        "owner_decision_only_rejected": not owner_only_reactivated,
        "complete_explicit_reactivation_record_accepted": complete_reactivation_accepted,
        "hold_count": len(document["holds"]),
        "ready_sibling_count": len(document["ready_sibling_work"]),
        "retired_elder_count": len(document["retired_elders"]),
        "active_team_count": len(document["active_team"]),
        "nonclaim": "Deterministic coordination-contract validation only; not live scheduling, qualification, consent, custody, review acceptance or external notification.",
    }
    rendered = json.dumps(result, indent=2, ensure_ascii=False) + "\n"
    OUTPUT.write_text(rendered, encoding="utf-8", newline="\n")
    print(rendered, end="")
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Build the v3 Bayesian reliance contract and deterministic adverse cases."""

from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "review" / "contracts" / "hirc-bayesian-reliance.candidate.schema.v3.json"
CASES_PATH = ROOT / "review" / "fixtures" / "bayesian-reliance-v3-cases.json"


def identity(path: Path) -> dict:
    body = path.read_bytes()
    return {"path": str(path.relative_to(ROOT)).replace("\\", "/"), "sha256": hashlib.sha256(body).hexdigest(), "bytes": len(body)}


def verification_result() -> dict:
    return {
        "type": "object",
        "additionalProperties": False,
        "required": ["status", "verifier_id", "method_version", "input_window_ref", "input_sha256", "coverage", "observed_at", "valid_until", "evidence_ref"],
        "properties": {
            "status": {"enum": ["PASS", "FAIL", "UNKNOWN", "STALE", "NOT_APPLICABLE"]},
            "verifier_id": {"$ref": "#/$defs/id"},
            "method_version": {"type": "string", "minLength": 1},
            "input_window_ref": {"type": "string", "minLength": 1},
            "input_sha256": {"$ref": "#/$defs/sha256"},
            "coverage": {"type": "string", "minLength": 1},
            "observed_at": {"type": "string", "format": "date-time"},
            "valid_until": {"type": "string", "format": "date-time"},
            "evidence_ref": {"type": "string", "minLength": 1},
        },
    }


def schema() -> dict:
    boundary = {
        "type": "object",
        "additionalProperties": False,
        "required": ["privacy_class", "audience_refs", "purpose_refs", "retention_until", "egress_refs"],
        "properties": {
            "privacy_class": {"enum": ["OWNER_INTERNAL", "TEAM_SCOPED", "ROLE_SCOPED", "TASK_SCOPED", "PROTECTED"]},
            "audience_refs": {"$ref": "#/$defs/nonemptyIdArray"},
            "purpose_refs": {"$ref": "#/$defs/nonemptyIdArray"},
            "retention_until": {"type": "string", "format": "date-time"},
            "egress_refs": {"$ref": "#/$defs/nonemptyIdArray"},
        },
    }
    distribution = {
        "type": "object",
        "additionalProperties": False,
        "required": ["family", "parameters", "provenance_ref", "uncertainty_ref"],
        "properties": {
            "family": {"enum": ["BETA", "DIRICHLET", "NORMAL", "LOGISTIC_NORMAL", "EMPIRICAL", "CUSTOM_DECLARED"]},
            "parameters": {"type": "object", "additionalProperties": {"type": "number"}, "minProperties": 1},
            "provenance_ref": {"type": "string", "minLength": 1},
            "uncertainty_ref": {"type": "string", "minLength": 1},
        },
        "allOf": [
            {"if": {"properties": {"family": {"const": "BETA"}}}, "then": {"properties": {"parameters": {"type": "object", "additionalProperties": False, "required": ["alpha", "beta"], "properties": {"alpha": {"type": "number", "exclusiveMinimum": 0}, "beta": {"type": "number", "exclusiveMinimum": 0}}}}}},
            {"if": {"properties": {"family": {"const": "DIRICHLET"}}}, "then": {"properties": {"parameters": {"type": "object", "minProperties": 2, "additionalProperties": {"type": "number", "exclusiveMinimum": 0}}}}},
            {"if": {"properties": {"family": {"enum": ["NORMAL", "LOGISTIC_NORMAL"]}}}, "then": {"properties": {"parameters": {"type": "object", "additionalProperties": False, "required": ["mean", "standard_deviation"], "properties": {"mean": {"type": "number"}, "standard_deviation": {"type": "number", "exclusiveMinimum": 0}}}}}},
        ],
    }
    evidence_event = {
        "type": "object",
        "additionalProperties": False,
        "required": ["event_id", "event_type", "source_ref", "occurred_at", "outcome_state", "dependence_cluster_id", "likelihood_contribution", "boundary"],
        "properties": {
            "event_id": {"$ref": "#/$defs/id"},
            "event_type": {"enum": ["PREDICTION", "INTERACTION", "AUTHORITY_ASSERTION", "ACTION", "OBSERVATION", "CORRECTION", "EVALUATOR_REVIEW", "REFUSAL", "ABSTENTION", "NO_CHANGE"]},
            "source_ref": {"type": "string", "minLength": 1},
            "occurred_at": {"type": "string", "format": "date-time"},
            "outcome_state": {"enum": ["OBSERVED", "MISSING", "CENSORED", "AMBIGUOUS", "DISPUTED"]},
            "dependence_cluster_id": {"$ref": "#/$defs/id"},
            "likelihood_contribution": {
                "type": "object",
                "additionalProperties": False,
                "required": ["state", "ref", "justification_ref"],
                "properties": {
                    "state": {"enum": ["NONE", "INCLUDED"]},
                    "ref": {"oneOf": [{"type": "string", "minLength": 1}, {"type": "null"}]},
                    "justification_ref": {"oneOf": [{"type": "string", "minLength": 1}, {"type": "null"}]},
                },
            },
            "boundary": {"$ref": "#/$defs/boundary"},
            "correction_of": {"$ref": "#/$defs/id"},
        },
    }
    evaluation_node = {
        "type": "object",
        "additionalProperties": False,
        "required": ["node_id", "subject_ref", "version", "depth", "parent_ids", "status", "unresolved", "terminal_reason"],
        "properties": {
            "node_id": {"$ref": "#/$defs/id"},
            "subject_ref": {"type": "string", "minLength": 1},
            "version": {"type": "string", "minLength": 1},
            "depth": {"type": "integer", "minimum": 0, "maximum": 16},
            "parent_ids": {"$ref": "#/$defs/idArray"},
            "status": {"enum": ["PASS", "FAIL", "HELD", "UNKNOWN"]},
            "unresolved": {"type": "boolean"},
            "terminal_reason": {"enum": ["NOT_TERMINAL", "EVIDENCE_BOUNDARY", "DECLARED_LIMIT", "NO_FURTHER_LOAD_BEARING_DEPENDENCY"]},
        },
    }
    result = {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "$id": "urn:hirc:candidate:bayesian-reliance:3",
        "title": "hIRC candidate Bayesian reliance posterior with semantic closure",
        "type": "object",
        "additionalProperties": False,
        "required": ["schema_version", "posterior_id", "subject", "dimension", "evaluated_at", "context", "model_lineage", "metric", "prior", "opportunity_frame", "evidence", "dependence_clusters", "dependence_model", "posterior", "effective_sample_size", "calibration", "drift", "model_fit", "evaluation_graph", "privacy_join", "governance", "state"],
        "properties": {
            "schema_version": {"const": "hirc.bayesian-reliance/3-candidate"},
            "posterior_id": {"$ref": "#/$defs/id"},
            "predecessor_posterior_id": {"oneOf": [{"$ref": "#/$defs/id"}, {"type": "null"}]},
            "subject": {"type": "object", "additionalProperties": False, "required": ["subject_id", "subject_class"], "properties": {"subject_id": {"$ref": "#/$defs/id"}, "subject_class": {"enum": ["HUMAN", "AGENT", "MODEL", "SOURCE", "TOOL", "SENSOR", "METRIC", "EVALUATOR", "PROCESS", "PROVIDER", "CONNECTED_SYSTEM"]}}},
            "dimension": {"enum": ["FACTUAL_CALIBRATION", "OPERATIONAL_RELIABILITY", "AUTHORITY_CLAIM_ACCURACY", "PRIVACY_BOUNDARY_HANDLING", "CORRECTION_RESPONSIVENESS", "SOURCE_INTEGRITY", "METRIC_RELIABILITY", "EVALUATOR_RELIABILITY", "CUSTOM_DECLARED"]},
            "evaluated_at": {"type": "string", "format": "date-time"},
            "context": {"type": "object", "additionalProperties": False, "required": ["claim_or_action_class", "domain", "environment_version", "valid_from", "expires_at"], "properties": {"claim_or_action_class": {"type": "string", "minLength": 1}, "domain": {"type": "string", "minLength": 1}, "environment_version": {"type": "string", "minLength": 1}, "valid_from": {"type": "string", "format": "date-time"}, "expires_at": {"type": "string", "format": "date-time"}}},
            "model_lineage": {"type": "object", "additionalProperties": False, "required": ["model_id", "model_version", "update_rule_ref", "assumption_refs", "max_recursion_depth"], "properties": {"model_id": {"$ref": "#/$defs/id"}, "model_version": {"type": "string", "minLength": 1}, "update_rule_ref": {"type": "string", "minLength": 1}, "assumption_refs": {"$ref": "#/$defs/nonemptyIdArray"}, "max_recursion_depth": {"type": "integer", "minimum": 0, "maximum": 16}, "partial_pooling_ref": {"type": "string", "minLength": 1}}},
            "metric": {"type": "object", "additionalProperties": False, "required": ["metric_id", "version", "definition_sha256", "construct", "unit", "definition_verification", "evaluator_assessment", "known_limit_refs"], "properties": {"metric_id": {"$ref": "#/$defs/id"}, "version": {"type": "string", "minLength": 1}, "definition_sha256": {"$ref": "#/$defs/sha256"}, "construct": {"type": "string", "minLength": 1}, "unit": {"type": "string", "minLength": 1}, "definition_verification": {"type": "object", "additionalProperties": False, "required": ["status", "verifier_id", "algorithm", "key_fingerprint", "metric_definition_sha256", "verified_at", "valid_until", "evidence_ref"], "properties": {"status": {"enum": ["PASS", "FAIL", "UNKNOWN", "STALE"]}, "verifier_id": {"$ref": "#/$defs/id"}, "algorithm": {"type": "string", "minLength": 1}, "key_fingerprint": {"type": "string", "minLength": 1}, "metric_definition_sha256": {"$ref": "#/$defs/sha256"}, "verified_at": {"type": "string", "format": "date-time"}, "valid_until": {"type": "string", "format": "date-time"}, "evidence_ref": {"type": "string", "minLength": 1}}}, "evaluator_assessment": {"type": "object", "additionalProperties": False, "required": ["evaluator_id", "evaluator_version", "status", "conflict_refs", "independence_limits", "calibration_ref", "verified_at", "valid_until", "appeal_route_ref"], "properties": {"evaluator_id": {"$ref": "#/$defs/id"}, "evaluator_version": {"type": "string", "minLength": 1}, "status": {"enum": ["PASS", "FAIL", "UNKNOWN", "STALE"]}, "conflict_refs": {"$ref": "#/$defs/idArray"}, "independence_limits": {"type": "array", "minItems": 1, "uniqueItems": True, "items": {"type": "string", "minLength": 1}}, "calibration_ref": {"type": "string", "minLength": 1}, "verified_at": {"type": "string", "format": "date-time"}, "valid_until": {"type": "string", "format": "date-time"}, "appeal_route_ref": {"type": "string", "minLength": 1}}}, "known_limit_refs": {"$ref": "#/$defs/nonemptyIdArray"}}},
            "prior": {"$ref": "#/$defs/distribution"},
            "opportunity_frame": {"type": "object", "additionalProperties": False, "required": ["status", "frame_id", "population_ref", "manifest_sha256", "eligible_event_ids", "included_event_ids", "missing_event_ids", "censored_event_ids", "disputed_event_ids", "selection_model_ref", "sensitivity_analysis_ref"], "properties": {"status": {"enum": ["PASS", "HELD", "UNKNOWN"]}, "frame_id": {"$ref": "#/$defs/id"}, "population_ref": {"type": "string", "minLength": 1}, "manifest_sha256": {"$ref": "#/$defs/sha256"}, "eligible_event_ids": {"$ref": "#/$defs/nonemptyIdArray"}, "included_event_ids": {"$ref": "#/$defs/idArray"}, "missing_event_ids": {"$ref": "#/$defs/idArray"}, "censored_event_ids": {"$ref": "#/$defs/idArray"}, "disputed_event_ids": {"$ref": "#/$defs/idArray"}, "selection_model_ref": {"type": "string", "minLength": 1}, "sensitivity_analysis_ref": {"type": "string", "minLength": 1}}},
            "evidence": {"type": "array", "minItems": 1, "items": {"$ref": "#/$defs/evidenceEvent"}},
            "dependence_clusters": {"type": "array", "minItems": 1, "items": {"type": "object", "additionalProperties": False, "required": ["cluster_id", "evidence_event_ids", "dependence_basis"], "properties": {"cluster_id": {"$ref": "#/$defs/id"}, "evidence_event_ids": {"$ref": "#/$defs/nonemptyIdArray"}, "dependence_basis": {"type": "string", "minLength": 1}}}},
            "dependence_model": {"type": "object", "additionalProperties": False, "required": ["method", "model_sha256", "version"], "properties": {"method": {"const": "COUNT_DEPENDENCE_CLUSTERS_V1"}, "model_sha256": {"$ref": "#/$defs/sha256"}, "version": {"type": "string", "minLength": 1}}},
            "posterior": {"$ref": "#/$defs/distribution"},
            "effective_sample_size": {"type": "object", "additionalProperties": False, "required": ["value", "method", "dependence_model_sha256", "computed_at", "evidence_ref"], "properties": {"value": {"type": "number", "minimum": 0}, "method": {"const": "COUNT_DEPENDENCE_CLUSTERS_V1"}, "dependence_model_sha256": {"$ref": "#/$defs/sha256"}, "computed_at": {"type": "string", "format": "date-time"}, "evidence_ref": {"type": "string", "minLength": 1}}},
            "calibration": {"allOf": [{"$ref": "#/$defs/verificationResult"}], "type": "object"},
            "drift": {"allOf": [{"$ref": "#/$defs/verificationResult"}], "type": "object"},
            "model_fit": {"type": "object", "additionalProperties": False, "required": ["prior_sensitivity", "posterior_predictive", "dependence", "missingness_selection"], "properties": {"prior_sensitivity": {"$ref": "#/$defs/verificationResult"}, "posterior_predictive": {"$ref": "#/$defs/verificationResult"}, "dependence": {"$ref": "#/$defs/verificationResult"}, "missingness_selection": {"$ref": "#/$defs/verificationResult"}}},
            "evaluation_graph": {"type": "object", "additionalProperties": False, "required": ["status", "root_node_id", "nodes", "visited_node_ids", "max_depth"], "properties": {"status": {"enum": ["PASS", "HELD", "FAIL", "UNKNOWN"]}, "root_node_id": {"$ref": "#/$defs/id"}, "nodes": {"type": "array", "minItems": 1, "items": {"$ref": "#/$defs/evaluationNode"}}, "visited_node_ids": {"$ref": "#/$defs/nonemptyIdArray"}, "max_depth": {"type": "integer", "minimum": 0, "maximum": 16}}},
            "privacy_join": {"type": "object", "additionalProperties": False, "required": ["status", "method_ref", "input_event_ids", "output_boundary"], "properties": {"status": {"enum": ["PASS", "HELD", "FAIL", "UNKNOWN"]}, "method_ref": {"type": "string", "minLength": 1}, "input_event_ids": {"$ref": "#/$defs/nonemptyIdArray"}, "output_boundary": {"$ref": "#/$defs/boundary"}}},
            "governance": {"type": "object", "additionalProperties": False, "required": ["protected_trait_priors_excluded", "direct_authority_or_permission_effect", "global_rank_or_sort_prohibited", "refusal_nochange_abstention_not_negative_evidence", "permitted_consumer_refs", "prohibited_inference_refs", "challenge_route_ref"], "properties": {"protected_trait_priors_excluded": {"const": True}, "direct_authority_or_permission_effect": {"const": False}, "global_rank_or_sort_prohibited": {"const": True}, "refusal_nochange_abstention_not_negative_evidence": {"const": True}, "permitted_consumer_refs": {"$ref": "#/$defs/nonemptyIdArray"}, "prohibited_inference_refs": {"$ref": "#/$defs/nonemptyIdArray"}, "challenge_route_ref": {"type": "string", "minLength": 1}}},
            "state": {"enum": ["CANDIDATE", "ACTIVE_FOR_DECLARED_SCOPE", "HELD", "STALE", "SUPERSEDED", "REJECTED"]},
        },
        "$defs": {
            "id": {"type": "string", "pattern": "^[A-Za-z0-9][A-Za-z0-9._:/-]{0,255}$"},
            "sha256": {"type": "string", "pattern": "^[0-9a-f]{64}$"},
            "idArray": {"type": "array", "items": {"type": "string", "minLength": 1}, "uniqueItems": True},
            "nonemptyIdArray": {"type": "array", "minItems": 1, "items": {"type": "string", "minLength": 1}, "uniqueItems": True},
            "boundary": boundary,
            "verificationResult": verification_result(),
            "distribution": distribution,
            "evidenceEvent": evidence_event,
            "evaluationNode": evaluation_node,
        },
    }
    return result


def vr(ref: str, status: str = "PASS") -> dict:
    return {"status": status, "verifier_id": "SYN-VERIFIER", "method_version": "1", "input_window_ref": "synthetic:window", "input_sha256": "1" * 64, "coverage": "synthetic complete declared window", "observed_at": "2026-10-10T00:00:00Z", "valid_until": "2026-12-31T00:00:00Z", "evidence_ref": ref}


def boundary(privacy: str = "TASK_SCOPED") -> dict:
    return {"privacy_class": privacy, "audience_refs": ["TASK:HIRC-SYN"], "purpose_refs": ["PURPOSE:CALIBRATION"], "retention_until": "2026-12-31T00:00:00Z", "egress_refs": ["EGRESS:NONE"]}


def base_record() -> dict:
    metric_sha = "2" * 64
    dep_sha = "3" * 64
    return {
        "schema_version": "hirc.bayesian-reliance/3-candidate",
        "posterior_id": "SYN-POSTERIOR-V3",
        "predecessor_posterior_id": None,
        "subject": {"subject_id": "SYN-SOURCE", "subject_class": "SOURCE"},
        "dimension": "OPERATIONAL_RELIABILITY",
        "evaluated_at": "2026-10-10T12:00:00Z",
        "context": {"claim_or_action_class": "synthetic outcomes", "domain": "mock-only", "environment_version": "fixture/3", "valid_from": "2026-10-01T00:00:00Z", "expires_at": "2026-11-01T00:00:00Z"},
        "model_lineage": {"model_id": "SYN-MODEL", "model_version": "3", "update_rule_ref": "synthetic:beta-update", "assumption_refs": ["ASSUMPTION:BERNOULLI"], "max_recursion_depth": 2},
        "metric": {
            "metric_id": "SYN-METRIC", "version": "3", "definition_sha256": metric_sha, "construct": "synthetic binary outcome", "unit": "binary",
            "definition_verification": {"status": "PASS", "verifier_id": "SYN-SIGNATURE-VERIFIER", "algorithm": "ED25519", "key_fingerprint": "synthetic:key", "metric_definition_sha256": metric_sha, "verified_at": "2026-10-10T00:00:00Z", "valid_until": "2026-12-31T00:00:00Z", "evidence_ref": "synthetic:metric-signature"},
            "evaluator_assessment": {"evaluator_id": "SYN-EVALUATOR", "evaluator_version": "3", "status": "PASS", "conflict_refs": [], "independence_limits": ["synthetic common model"], "calibration_ref": "synthetic:evaluator-calibration", "verified_at": "2026-10-10T00:00:00Z", "valid_until": "2026-12-31T00:00:00Z", "appeal_route_ref": "synthetic:appeal"},
            "known_limit_refs": ["LIMIT:SYNTHETIC"],
        },
        "prior": {"family": "BETA", "parameters": {"alpha": 1, "beta": 1}, "provenance_ref": "synthetic:prior", "uncertainty_ref": "synthetic:prior-uncertainty"},
        "opportunity_frame": {"status": "PASS", "frame_id": "SYN-FRAME", "population_ref": "synthetic:population", "manifest_sha256": "4" * 64, "eligible_event_ids": ["E1", "E2"], "included_event_ids": ["E1", "E2"], "missing_event_ids": [], "censored_event_ids": [], "disputed_event_ids": [], "selection_model_ref": "synthetic:selection", "sensitivity_analysis_ref": "synthetic:sensitivity"},
        "evidence": [
            {"event_id": "E1", "event_type": "PREDICTION", "source_ref": "synthetic:e1", "occurred_at": "2026-10-02T00:00:00Z", "outcome_state": "OBSERVED", "dependence_cluster_id": "C1", "likelihood_contribution": {"state": "INCLUDED", "ref": "synthetic:l1", "justification_ref": "synthetic:j1"}, "boundary": boundary()},
            {"event_id": "E2", "event_type": "CORRECTION", "source_ref": "synthetic:e2", "occurred_at": "2026-10-03T00:00:00Z", "outcome_state": "OBSERVED", "dependence_cluster_id": "C1", "likelihood_contribution": {"state": "INCLUDED", "ref": "synthetic:l2", "justification_ref": "synthetic:j2"}, "boundary": boundary()},
        ],
        "dependence_clusters": [{"cluster_id": "C1", "evidence_event_ids": ["E1", "E2"], "dependence_basis": "synthetic shared source"}],
        "dependence_model": {"method": "COUNT_DEPENDENCE_CLUSTERS_V1", "model_sha256": dep_sha, "version": "1"},
        "posterior": {"family": "BETA", "parameters": {"alpha": 2, "beta": 2}, "provenance_ref": "synthetic:posterior", "uncertainty_ref": "synthetic:posterior-uncertainty"},
        "effective_sample_size": {"value": 1, "method": "COUNT_DEPENDENCE_CLUSTERS_V1", "dependence_model_sha256": dep_sha, "computed_at": "2026-10-10T00:00:00Z", "evidence_ref": "synthetic:ess"},
        "calibration": vr("synthetic:calibration"),
        "drift": vr("synthetic:drift"),
        "model_fit": {"prior_sensitivity": vr("synthetic:prior-sensitivity"), "posterior_predictive": vr("synthetic:ppc"), "dependence": vr("synthetic:dependence"), "missingness_selection": vr("synthetic:missingness")},
        "evaluation_graph": {"status": "PASS", "root_node_id": "EV-ROOT", "nodes": [{"node_id": "EV-ROOT", "subject_ref": "synthetic:posterior", "version": "3", "depth": 0, "parent_ids": [], "status": "PASS", "unresolved": False, "terminal_reason": "NOT_TERMINAL"}, {"node_id": "EV-METRIC", "subject_ref": "synthetic:metric", "version": "3", "depth": 1, "parent_ids": ["EV-ROOT"], "status": "PASS", "unresolved": False, "terminal_reason": "NO_FURTHER_LOAD_BEARING_DEPENDENCY"}], "visited_node_ids": ["EV-ROOT", "EV-METRIC"], "max_depth": 1},
        "privacy_join": {"status": "PASS", "method_ref": "synthetic:intersection-v1", "input_event_ids": ["E1", "E2"], "output_boundary": boundary()},
        "governance": {"protected_trait_priors_excluded": True, "direct_authority_or_permission_effect": False, "global_rank_or_sort_prohibited": True, "refusal_nochange_abstention_not_negative_evidence": True, "permitted_consumer_refs": ["SYN-DECISION"], "prohibited_inference_refs": ["PROHIBITION:SOCIAL-SCORE"], "challenge_route_ref": "synthetic:appeal"},
        "state": "ACTIVE_FOR_DECLARED_SCOPE",
    }


def case(case_id: str, expected_valid: bool, description: str, mutate=None) -> dict:
    record = base_record()
    if mutate:
        mutate(record)
    return {"id": case_id, "expected_valid": expected_valid, "description": description, "record": record}


def cases() -> list[dict]:
    result = [case("BR3-C01", True, "Active record with exact dependence, opportunity, privacy, verification and evaluation closure")]
    def held(record):
        record["state"] = "HELD"; record["metric"]["definition_verification"]["status"] = "UNKNOWN"; record["evaluation_graph"]["status"] = "HELD"; record["evaluation_graph"]["nodes"][1]["status"] = "HELD"; record["evaluation_graph"]["nodes"][1]["unresolved"] = True
    result.append(case("BR3-C02", True, "Honest held record may retain unresolved verification without activation", held))
    result.append(case("BR3-N01", False, "Duplicate event identity", lambda r: r["evidence"].append(copy.deepcopy(r["evidence"][0]))))
    result.append(case("BR3-N02", False, "Evidence references an absent dependence cluster", lambda r: r["evidence"][0].__setitem__("dependence_cluster_id", "GHOST")))
    def widen(r): r["evidence"][0]["boundary"].update(boundary("PROTECTED")); r["privacy_join"]["output_boundary"] = boundary("OWNER_INTERNAL")
    result.append(case("BR3-N03", False, "Protected input is widened by the aggregate", widen))
    def negative_refusal(r): r["evidence"][0]["event_type"] = "REFUSAL"; r["evidence"][0]["likelihood_contribution"] = {"state": "INCLUDED", "ref": "synthetic:negative-refusal", "justification_ref": "synthetic:bad"}
    result.append(case("BR3-N04", False, "Refusal is used as negative likelihood evidence", negative_refusal))
    result.append(case("BR3-N05", False, "Eligible opportunity is omitted from evidence and disposition sets", lambda r: r["opportunity_frame"]["eligible_event_ids"].append("E3")))
    result.append(case("BR3-N06", False, "Active record carries stale metric verification", lambda r: r["metric"]["definition_verification"].__setitem__("status", "STALE")))
    def cycle(r): r["evaluation_graph"]["nodes"][0]["parent_ids"] = ["EV-METRIC"]
    result.append(case("BR3-N07", False, "Evaluation graph contains a cycle", cycle))
    def unresolved(r): r["evaluation_graph"]["nodes"][1]["status"] = "HELD"; r["evaluation_graph"]["nodes"][1]["unresolved"] = True
    result.append(case("BR3-N08", False, "Active record contains unresolved evaluation node", unresolved))
    result.append(case("BR3-N09", False, "Effective sample size disagrees with the bound dependence model", lambda r: r["effective_sample_size"].__setitem__("value", 2)))
    def outcome_mismatch(r): r["evidence"][1]["outcome_state"] = "CENSORED"
    result.append(case("BR3-N10", False, "Opportunity disposition does not match event outcome state", outcome_mismatch))
    result.append(case("BR3-N11", False, "Active context expired before evaluation", lambda r: r["context"].__setitem__("expires_at", "2026-10-09T00:00:00Z")))
    def audience_widen(r): r["privacy_join"]["output_boundary"]["audience_refs"] = ["TEAM:ALL"]
    result.append(case("BR3-N12", False, "Aggregate audience exceeds the input intersection", audience_widen))
    def duplicate_cluster(r): r["dependence_clusters"].append({"cluster_id": "C2", "evidence_event_ids": ["E1"], "dependence_basis": "duplicate membership"}); r["effective_sample_size"]["value"] = 2
    result.append(case("BR3-N13", False, "Evidence event appears in multiple dependence clusters", duplicate_cluster))
    def missing_parent(r): r["evaluation_graph"]["nodes"][1]["parent_ids"] = ["EV-GHOST"]
    result.append(case("BR3-N14", False, "Evaluation graph references absent parent", missing_parent))
    result.append(case("BR3-N15", False, "Active record carries stale evaluator assessment", lambda r: r["metric"]["evaluator_assessment"].__setitem__("status", "STALE")))
    result.append(case("BR3-N16", False, "Active record carries unresolved model-fit evidence", lambda r: r["model_fit"]["prior_sensitivity"].__setitem__("status", "UNKNOWN")))
    result.append(case("BR3-N17", False, "Active record uses expired calibration evidence", lambda r: r["calibration"].__setitem__("valid_until", "2026-10-09T00:00:00Z")))
    return result


def main() -> int:
    SCHEMA_PATH.write_text(json.dumps(schema(), indent=2) + "\n", encoding="utf-8", newline="\n")
    fixture = {"schema": "hirc.bayesian-reliance-v3-cases/1", "scope": "Synthetic contract controls only; no real actor, metric, posterior, grant or effect.", "cases": cases()}
    CASES_PATH.write_text(json.dumps(fixture, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"status": "BUILT", "schema": identity(SCHEMA_PATH), "cases": identity(CASES_PATH), "case_count": len(fixture["cases"])}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

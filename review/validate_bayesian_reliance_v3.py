#!/usr/bin/env python3
"""Run structural and cross-field semantic controls for Bayesian reliance v3."""

from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "review" / "contracts" / "hirc-bayesian-reliance.candidate.schema.v3.json"
CASES_PATH = ROOT / "review" / "fixtures" / "bayesian-reliance-v3-cases.json"
OUTPUT = ROOT / "review" / "fixtures" / "bayesian-reliance-v3-validation.json"


def identity(path: Path) -> dict:
    body = path.read_bytes()
    return {"path": str(path.relative_to(ROOT)).replace("\\", "/"), "sha256": hashlib.sha256(body).hexdigest(), "bytes": len(body)}


def canonical_hash(value: dict) -> str:
    raw = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def moment(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def structural(record: dict) -> tuple[bool, str]:
    pwsh = shutil.which("pwsh")
    if not pwsh:
        raise RuntimeError("POWERSHELL_7_REQUIRED")
    schema_literal = str(SCHEMA_PATH).replace("'", "''")
    command = f"$schema='{schema_literal}'; $body=[Console]::In.ReadToEnd(); if(Test-Json -Json $body -SchemaFile $schema -ErrorAction SilentlyContinue){{'true'}}else{{'false'}}"
    run = subprocess.run(
        [pwsh, "-NoProfile", "-Command", command],
        input=json.dumps(record, ensure_ascii=False),
        text=True,
        capture_output=True,
        check=False,
    )
    return run.returncode == 0 and run.stdout.strip().lower() == "true", run.stderr.strip()


def duplicates(values: list[str]) -> bool:
    return len(values) != len(set(values))


def semantic(record: dict) -> list[str]:
    errors: list[str] = []
    events = record.get("evidence", [])
    event_ids = [item.get("event_id") for item in events]
    if duplicates(event_ids):
        errors.append("duplicate-event-id")
    event_set = set(event_ids)

    clusters = record.get("dependence_clusters", [])
    cluster_ids = [item.get("cluster_id") for item in clusters]
    if duplicates(cluster_ids):
        errors.append("duplicate-cluster-id")
    members: list[str] = []
    membership: dict[str, str] = {}
    for cluster in clusters:
        for event_id in cluster.get("evidence_event_ids", []):
            if event_id in membership:
                errors.append("event-in-multiple-clusters")
            membership[event_id] = cluster.get("cluster_id")
            members.append(event_id)
            if event_id not in event_set:
                errors.append("cluster-member-missing-event")
    if set(members) != event_set or len(members) != len(event_ids):
        errors.append("cluster-partition-not-exact")
    for event in events:
        if membership.get(event.get("event_id")) != event.get("dependence_cluster_id"):
            errors.append("event-cluster-reference-mismatch")

    dependence = record.get("dependence_model", {})
    ess = record.get("effective_sample_size", {})
    if dependence.get("method") != "COUNT_DEPENDENCE_CLUSTERS_V1" or ess.get("method") != dependence.get("method"):
        errors.append("dependence-method-mismatch")
    if ess.get("dependence_model_sha256") != dependence.get("model_sha256"):
        errors.append("dependence-model-identity-mismatch")
    if ess.get("value") != len(clusters):
        errors.append("effective-sample-size-not-recomputed")

    frame = record.get("opportunity_frame", {})
    partitions = [frame.get(name, []) for name in ("included_event_ids", "missing_event_ids", "censored_event_ids", "disputed_event_ids")]
    flat = [item for group in partitions for item in group]
    eligible = frame.get("eligible_event_ids", [])
    if duplicates(flat) or set(flat) != set(eligible) or len(flat) != len(eligible):
        errors.append("opportunity-disposition-partition-not-exact")
    if set(eligible) != event_set or len(eligible) != len(event_ids):
        errors.append("eligible-opportunity-evidence-coverage-not-exact")
    expected_bucket = {"OBSERVED": "included_event_ids", "AMBIGUOUS": "included_event_ids", "MISSING": "missing_event_ids", "CENSORED": "censored_event_ids", "DISPUTED": "disputed_event_ids"}
    for event in events:
        bucket = expected_bucket.get(event.get("outcome_state"))
        if bucket and event.get("event_id") not in frame.get(bucket, []):
            errors.append("event-outcome-opportunity-disposition-mismatch")

    for event in events:
        contribution = event.get("likelihood_contribution", {})
        if event.get("event_type") in {"REFUSAL", "ABSTENTION", "NO_CHANGE"} and contribution.get("state") != "NONE":
            errors.append("protected-disposition-used-as-likelihood")
        if contribution.get("state") == "NONE" and (contribution.get("ref") is not None or contribution.get("justification_ref") is not None):
            errors.append("none-contribution-carries-reference")
        if contribution.get("state") == "INCLUDED" and (not contribution.get("ref") or not contribution.get("justification_ref")):
            errors.append("included-contribution-missing-justification")

    privacy = record.get("privacy_join", {})
    if set(privacy.get("input_event_ids", [])) != event_set:
        errors.append("privacy-input-coverage-not-exact")
    boundaries = [event.get("boundary", {}) for event in events]
    output = privacy.get("output_boundary", {})
    for field in ("audience_refs", "purpose_refs", "egress_refs"):
        intersection = set(boundaries[0].get(field, [])) if boundaries else set()
        for item in boundaries[1:]:
            intersection &= set(item.get(field, []))
        if set(output.get(field, [])) != intersection:
            errors.append(f"privacy-{field}-not-exact-intersection")
    try:
        if boundaries and moment(output["retention_until"]) > min(moment(item["retention_until"]) for item in boundaries):
            errors.append("privacy-retention-widened")
    except (KeyError, TypeError, ValueError):
        errors.append("privacy-retention-invalid")
    if any(item.get("privacy_class") == "PROTECTED" for item in boundaries) and output.get("privacy_class") != "PROTECTED":
        errors.append("protected-privacy-class-widened")

    graph = record.get("evaluation_graph", {})
    nodes = graph.get("nodes", [])
    node_ids = [node.get("node_id") for node in nodes]
    node_map = {node.get("node_id"): node for node in nodes}
    if duplicates(node_ids):
        errors.append("duplicate-evaluation-node")
    root = graph.get("root_node_id")
    if root not in node_map:
        errors.append("evaluation-root-missing")
    elif node_map[root].get("parent_ids"):
        errors.append("evaluation-root-has-parent")
    for node in nodes:
        if any(parent not in node_map for parent in node.get("parent_ids", [])):
            errors.append("evaluation-parent-missing")
    visiting: set[str] = set()
    visited: set[str] = set()
    def visit(node_id: str) -> None:
        if node_id in visiting:
            errors.append("evaluation-cycle")
            return
        if node_id in visited or node_id not in node_map:
            return
        visiting.add(node_id)
        for parent in node_map[node_id].get("parent_ids", []):
            visit(parent)
        visiting.remove(node_id)
        visited.add(node_id)
    for node_id in node_ids:
        visit(node_id)
    if set(graph.get("visited_node_ids", [])) != set(node_ids):
        errors.append("evaluation-visited-set-incomplete")
    if nodes and graph.get("max_depth") != max(node.get("depth", -1) for node in nodes):
        errors.append("evaluation-max-depth-mismatch")
    if graph.get("max_depth", 99) > record.get("model_lineage", {}).get("max_recursion_depth", -1):
        errors.append("evaluation-depth-exceeds-lineage")
    for node in nodes:
        parents = node.get("parent_ids", [])
        known_parent_depths = [node_map[parent].get("depth", -1) for parent in parents if parent in node_map]
        if parents and not known_parent_depths:
            continue
        expected_depth = 0 if not parents else max(known_parent_depths) + 1
        if node.get("depth") != expected_depth:
            errors.append("evaluation-node-depth-mismatch")

    metric = record.get("metric", {})
    definition = metric.get("definition_verification", {})
    evaluator = metric.get("evaluator_assessment", {})
    if definition.get("metric_definition_sha256") != metric.get("definition_sha256"):
        errors.append("metric-definition-verification-target-mismatch")

    if record.get("state") == "ACTIVE_FOR_DECLARED_SCOPE":
        try:
            evaluated = moment(record["evaluated_at"])
            if not moment(record["context"]["valid_from"]) <= evaluated <= moment(record["context"]["expires_at"]):
                errors.append("active-context-not-current")
            verification_items = [definition, evaluator, record.get("calibration", {}), record.get("drift", {}), *record.get("model_fit", {}).values()]
            for item in verification_items:
                if item.get("status") != "PASS":
                    errors.append("active-verification-not-pass")
                if "observed_at" in item and "valid_until" in item and not moment(item["observed_at"]) <= evaluated <= moment(item["valid_until"]):
                    errors.append("active-verification-not-current")
            if frame.get("status") != "PASS" or privacy.get("status") != "PASS" or graph.get("status") != "PASS":
                errors.append("active-closure-status-not-pass")
        except (KeyError, TypeError, ValueError):
            errors.append("active-time-binding-invalid")
        if not record.get("model_lineage", {}).get("assumption_refs"):
            errors.append("active-assumptions-empty")
        if any(node.get("unresolved") or node.get("status") != "PASS" for node in nodes):
            errors.append("active-evaluation-node-unresolved")
    return sorted(set(errors))


def main() -> int:
    fixture = json.loads(CASES_PATH.read_text(encoding="utf-8"))
    results = []
    for case in fixture["cases"]:
        structural_valid, stderr = structural(case["record"])
        semantic_errors = semantic(case["record"]) if structural_valid else ["STRUCTURAL_REJECTION"]
        semantic_valid = structural_valid and not semantic_errors
        results.append({
            "id": case["id"],
            "expected_valid": case["expected_valid"],
            "structural_valid": structural_valid,
            "semantic_valid": semantic_valid,
            "expectation_pass": semantic_valid == case["expected_valid"],
            "semantic_errors": semantic_errors,
            "input_sha256": canonical_hash(case["record"]),
            "description": case["description"],
            "validator_stderr": stderr,
        })
    result = {
        "schema": "hirc.bayesian-reliance-v3-validation/1",
        "status": "PASS" if all(item["expectation_pass"] for item in results) else "FAIL",
        "schema_source": identity(SCHEMA_PATH),
        "case_source": identity(CASES_PATH),
        "validator": identity(Path(__file__)),
        "runtime": {"structural": "PowerShell 7 Test-Json draft 2020-12", "semantic": "Python standard-library deterministic cross-field validator"},
        "counts": {"total": len(results), "positive": sum(item["expected_valid"] for item in results), "adverse": sum(not item["expected_valid"] for item in results)},
        "results": results,
        "nonclaim": "Synthetic candidate-contract validation. It does not prove statistical validity, privacy outcomes, evaluator independence, deployed enforcement, authority or permission.",
    }
    OUTPUT.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"status": result["status"], "counts": result["counts"], "failures": [item["id"] for item in results if not item["expectation_pass"]], "output": identity(OUTPUT)}, indent=2))
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())

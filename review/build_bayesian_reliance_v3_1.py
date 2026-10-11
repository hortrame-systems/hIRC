#!/usr/bin/env python3
"""Build Bayesian reliance v3.1 for the four partial COFACTOR findings."""

from __future__ import annotations

import copy
import hashlib
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "review"))
import build_bayesian_reliance_v3 as v3  # noqa: E402

SCHEMA_PATH = ROOT / "review/contracts/hirc-bayesian-reliance.candidate.schema.v3.1.json"
CASES_PATH = ROOT / "review/fixtures/bayesian-reliance-v3.1-cases.json"


def digest(value: object) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")).hexdigest()


def identity(path: Path) -> dict:
    body = path.read_bytes(); return {"path": path.relative_to(ROOT).as_posix(), "sha256": hashlib.sha256(body).hexdigest(), "bytes": len(body)}


def uncertainty(ref: str, status: str = "PASS") -> dict:
    return {"status": status, "method": "BETA_EQUAL_TAIL_V1", "level": 0.95, "lower": 0.1, "upper": 0.9, "observed_at": "2026-10-10T00:00:00Z", "valid_until": "2026-12-31T00:00:00Z", "evidence_ref": ref}


def graph_hashes(record: dict) -> None:
    graph = record["evaluation_graph"]
    for node in graph["nodes"]:
        body = {key: value for key, value in node.items() if key != "node_sha256"}
        node["node_sha256"] = digest(body)
    body = {key: value for key, value in graph.items() if key != "graph_sha256"}
    graph["graph_sha256"] = digest(body)


def upgrade(record: dict) -> dict:
    record = copy.deepcopy(record)
    record["schema_version"] = "hirc.bayesian-reliance/3.1-candidate"
    record["prior"]["uncertainty"] = uncertainty("REF:PRIOR-UNCERTAINTY")
    record["prior"].pop("uncertainty_ref", None)
    record["posterior"]["uncertainty"] = uncertainty("REF:POSTERIOR-UNCERTAINTY")
    record["posterior"].pop("uncertainty_ref", None)
    record["metric"]["evaluator_assessment"]["evidence_ref"] = "REF:EVALUATOR-ASSESSMENT"
    record["privacy_join"]["privacy_class_policy"] = "MIXED_CLASSES_REQUIRE_PROTECTED_V1"
    load_bearing = [
        record["metric"]["definition_verification"]["evidence_ref"], record["metric"]["evaluator_assessment"]["evidence_ref"],
        record["prior"]["uncertainty"]["evidence_ref"], record["posterior"]["uncertainty"]["evidence_ref"],
        record["calibration"]["evidence_ref"], record["drift"]["evidence_ref"],
        *[item["evidence_ref"] for item in record["model_fit"].values()],
    ]
    record["reference_closure"] = [
        {"ref": ref, "sha256": hashlib.sha256(ref.encode("utf-8")).hexdigest(), "status": "PASS", "observed_at": "2026-10-10T00:00:00Z", "valid_until": "2026-12-31T00:00:00Z", "evidence_ref": "closure:" + ref}
        for ref in load_bearing
    ]
    graph_hashes(record)
    return record


def schema() -> dict:
    result = v3.schema()
    result["$id"] = "urn:hirc:candidate:bayesian-reliance:3.1"
    result["title"] = "hIRC candidate Bayesian reliance posterior with typed uncertainty and content-addressed closure"
    result["properties"]["schema_version"] = {"const": "hirc.bayesian-reliance/3.1-candidate"}
    result["required"].append("reference_closure")
    result["properties"]["reference_closure"] = {"type": "array", "minItems": 1, "items": {"type": "object", "additionalProperties": False, "required": ["ref", "sha256", "status", "observed_at", "valid_until", "evidence_ref"], "properties": {"ref": {"type": "string", "minLength": 1}, "sha256": {"$ref": "#/$defs/sha256"}, "status": {"enum": ["PASS", "FAIL", "UNKNOWN", "STALE"]}, "observed_at": {"type": "string", "format": "date-time"}, "valid_until": {"type": "string", "format": "date-time"}, "evidence_ref": {"type": "string", "minLength": 1}}}}
    result["$defs"]["uncertaintyResult"] = {"type": "object", "additionalProperties": False, "required": ["status", "method", "level", "lower", "upper", "observed_at", "valid_until", "evidence_ref"], "properties": {"status": {"enum": ["PASS", "FAIL", "UNKNOWN", "STALE"]}, "method": {"type": "string", "minLength": 1}, "level": {"type": "number", "exclusiveMinimum": 0, "maximum": 1}, "lower": {"type": "number"}, "upper": {"type": "number"}, "observed_at": {"type": "string", "format": "date-time"}, "valid_until": {"type": "string", "format": "date-time"}, "evidence_ref": {"type": "string", "minLength": 1}}}
    distribution = result["$defs"]["distribution"]
    distribution["required"].remove("uncertainty_ref")
    distribution["required"].append("uncertainty")
    distribution["properties"].pop("uncertainty_ref", None)
    distribution["properties"]["uncertainty"] = {"$ref": "#/$defs/uncertaintyResult"}
    evaluator = result["properties"]["metric"]["properties"]["evaluator_assessment"]
    evaluator["required"].append("evidence_ref")
    evaluator["properties"]["evidence_ref"] = {"type": "string", "minLength": 1}
    node = result["$defs"]["evaluationNode"]
    node["required"].append("node_sha256"); node["properties"]["node_sha256"] = {"$ref": "#/$defs/sha256"}
    graph = result["properties"]["evaluation_graph"]
    graph["required"].append("graph_sha256"); graph["properties"]["graph_sha256"] = {"$ref": "#/$defs/sha256"}
    privacy = result["properties"]["privacy_join"]
    privacy["required"].append("privacy_class_policy"); privacy["properties"]["privacy_class_policy"] = {"const": "MIXED_CLASSES_REQUIRE_PROTECTED_V1"}
    return result


def cases() -> list[dict]:
    inherited = []
    for row in v3.cases():
        record = upgrade(row["record"])
        inherited.append({"id": row["id"], "expected_valid": row["expected_valid"], "description": row["description"], "record": record})
    def new(case_id, description, mutate):
        record = upgrade(v3.base_record()); mutate(record); return {"id": case_id, "expected_valid": False, "description": description, "record": record}
    inherited.extend([
        new("BR31-N18", "Active posterior uncertainty is unresolved", lambda r: r["posterior"]["uncertainty"].__setitem__("status", "UNKNOWN")),
        new("BR31-N19", "Mixed non-protected input classes do not conservatively join to PROTECTED", lambda r: (r["evidence"][0]["boundary"].__setitem__("privacy_class", "TEAM_SCOPED"), r["evidence"][1]["boundary"].__setitem__("privacy_class", "TASK_SCOPED"), r["privacy_join"]["output_boundary"].__setitem__("privacy_class", "TASK_SCOPED"))),
        new("BR31-N20", "Evaluator assessment omits its evidence reference", lambda r: r["metric"]["evaluator_assessment"].pop("evidence_ref")),
        new("BR31-N21", "Reference closure omits evaluator assessment evidence", lambda r: r.__setitem__("reference_closure", [x for x in r["reference_closure"] if x["ref"] != "REF:EVALUATOR-ASSESSMENT"])),
        new("BR31-N22", "Load-bearing reference closure remains UNKNOWN", lambda r: r["reference_closure"][0].__setitem__("status", "UNKNOWN")),
        new("BR31-N23", "Evaluation node content changes without its content address", lambda r: r["evaluation_graph"]["nodes"][1].__setitem__("version", "tampered")),
        new("BR31-N24", "Evaluation graph carries an incorrect graph content address", lambda r: r["evaluation_graph"].__setitem__("graph_sha256", "0" * 64)),
    ])
    return inherited


def main() -> int:
    SCHEMA_PATH.write_text(json.dumps(schema(), indent=2) + "\n", encoding="utf-8", newline="\n")
    fixture = {"schema": "hirc.bayesian-reliance-v3.1-cases/1", "predecessor": v3.identity(v3.SCHEMA_PATH), "scope": "Synthetic candidate-contract repair only; no real metric, posterior, identity, permission or effect.", "cases": cases()}
    CASES_PATH.write_text(json.dumps(fixture, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"status": "BUILT", "schema": identity(SCHEMA_PATH), "cases": identity(CASES_PATH), "counts": {"total": len(fixture["cases"]), "positive": sum(x["expected_valid"] for x in fixture["cases"]), "adverse": sum(not x["expected_valid"] for x in fixture["cases"])}}, indent=2))
    return 0


if __name__ == "__main__": raise SystemExit(main())

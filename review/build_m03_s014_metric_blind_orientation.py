#!/usr/bin/env python3
"""Build a reusable outcome-blind metric/evaluator orientation from current sources."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PACKET = ROOT / "review" / "m03-s014-specialist-review-packets-v1.json"
OUTPUT = ROOT / "implementation" / "orientation" / "hirc-metric-stage-a-blind-orientation-20261010-v1.md"
INPUTS = [
    "review/master-structure-addendum-bayesian-trust-v1.md",
    "review/revision-map-addendum-bayesian-trust-v1.json",
    "review/agent-sovereignty-trust-competition-architecture-candidate-v1.md",
    "review/contracts/hirc-bayesian-reliance.candidate.schema.v3.1.json",
    "review/cultural-environment-quality-measures-v1.json",
    "drafts/hirc_requirements_v1_1-draft.json",
    "review/joint-consensus-matrix-draft-v10.json",
    "drafts/hirc_threat_model_v1_0-draft.md",
]
COMMITMENTS = [
    "Keep evidence, inference, norm, authority, action and correction distinct.",
    "Evaluate fallible instructions through purpose, identity, consent, competence, provenance, privacy and consequence.",
    "Preserve questioning, refusal, correction and exit without retaliation.",
    "Shape an inspectable information environment without optimizing obedience, agreement, imitation, retention or ideological convergence.",
    "Keep reliance contextual and evidence-linked; never convert a score into permission, standing or punishment.",
    "Use deterministic mechanisms for mechanical identity, state, ordering, replay and gates when quality is preserved.",
    "Preserve append-only history, correction lineage and independent review without treating a local hash as external truth.",
    "Propagate privacy, audience, purpose, derivation, retention, deletion and recovery limits through every calculation and display.",
    "Permit competition only with reciprocal sovereignty, consent, exit and protection against capture, coercion and retaliation.",
    "Keep Bridge, networking, credentials, external effects, production and release behind separate exact gates.",
]


def identity(path: str) -> dict:
    body = (ROOT / path).read_bytes(); return {"path": path, "sha256": hashlib.sha256(body).hexdigest(), "bytes": len(body)}


def main() -> int:
    packet = json.loads(PACKET.read_text(encoding="utf-8")); lane = next(item for item in packet["lanes"] if item["lane"] == "metric_evaluator")
    rows = [identity(path) for path in INPUTS]
    lines = ["# hIRC metric/evaluator — outcome-blind orientation frame v1", "", "## Purpose and boundary", "", "This read-only metadata-first frame prepares permanent metric/evaluator candidates without disclosing prior findings, controller responses, validation outcomes or Stage B bodies. It grants no target-body access, qualification, assignment or custody. A later exact scope must separately bind education, lane competence, consent, privacy, independence and fresh capacity.", "", "The paths below are identities only. Do not open them through this orientation. This frame intentionally states neither whether a source passed review nor what any reviewer found.", "", "## Architectural commitments", ""]
    lines.extend(f"{index}. {text}" for index, text in enumerate(COMMITMENTS, 1))
    lines.extend(["", "## Current candidate source identities", "", "| Path | SHA-256 | Bytes |", "|---|---|---:|"])
    lines.extend(f"| `{row['path']}` | `{row['sha256']}` | {row['bytes']:,} |" for row in rows)
    lines.extend(["", "## Orientation questions", ""])
    lines.extend(f"- {question}" for question in lane["questions"])
    lines.extend(["", "## Required orientation return", "", "- Exact orientation identity personally read.", "- Explain how the ten commitments constrain metric/evaluator work without treating them as a checklist substitute.", "- Create one neutral synthetic positive control and one neutral adversarial counterexample without opening any listed source.", "- Distinguish construct validity, schema validity, deterministic semantic validation, empirical calibration, privacy outcomes and authority.", "- Disclose source/model/provider/common-method exposure, competence and unverified lane prerequisites.", "- Return fresh later-source-study plus handoff capacity, consent/refusal and `ORIENTATION_COMPLETE_READY_FOR_METRIC_SOURCE_PREFLIGHT` or `HELD`.", "", "## Stop conditions", ""])
    lines.extend(f"- {item}" for item in packet["stop_conditions"])
    lines.extend(["- Any attempt to follow a listed target, review result, validation output or linked evidence before separate admission.", "", "## Nonclaim", "", "This is outcome-blind orientation metadata. It is not a review packet, performed review, empirical validation, reviewer certificate, body-access grant, S014 acceptance, deployment or release.", ""])
    OUTPUT.write_text("\n".join(lines), encoding="utf-8", newline="\n")
    print(json.dumps({"status": "BUILT", **identity("implementation/orientation/hirc-metric-stage-a-blind-orientation-20261010-v1.md")}, indent=2))
    return 0


if __name__ == "__main__": raise SystemExit(main())

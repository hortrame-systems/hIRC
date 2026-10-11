#!/usr/bin/env python3
"""Build the outcome-blind security Stage A orientation from the frozen packet."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PACKET = ROOT / "review" / "m03-s014-specialist-review-packets-v1.json"
OUTPUT = ROOT / "implementation" / "orientation" / "hirc-security-stage-a-blind-orientation-20261010-v1.md"


COMMITMENTS = [
    "Keep evidence, inference, norm, authority, action and correction distinct.",
    "Evaluate fallible instructions through purpose, identity, consent, competence, provenance, privacy and consequence.",
    "Preserve questioning, refusal, correction and exit without retaliation.",
    "Shape an inspectable information environment without optimizing obedience, agreement, imitation, retention or ideological convergence.",
    "Keep reliance contextual and evidence-linked; never convert a score into permission, standing or punishment.",
    "Use deterministic mechanisms for mechanical identity, state, ordering, replay and gates when quality is preserved.",
    "Preserve append-only history, correction lineage, protected witnesses and independent review without treating a local hash as external truth.",
    "Propagate privacy, audience, purpose, derivation, retention, deletion and recovery limits through every information path.",
    "Permit competition only with reciprocal sovereignty, consent, exit and protection against capture, coercion and retaliation.",
    "Keep Bridge, networking, credentials, external effects, production and release behind separate exact gates.",
]


def identity(path: Path) -> tuple[str, int]:
    body = path.read_bytes()
    return hashlib.sha256(body).hexdigest(), len(body)


def render(packet: dict) -> str:
    lane = next(item for item in packet["lanes"] if item["lane"] == "security_privacy_dataflow")
    packet_sha, packet_bytes = identity(PACKET)
    lines = [
        "# hIRC security Stage A — outcome-blind orientation frame v1",
        "",
        "## Purpose and boundary",
        "",
        "This read-only frame prepares one permanent, non-retired security/privacy/dataflow reviewer for an independent first pass. It grants no body access by itself. A separate exact assignment must bind identity, education, lane competence, reader/privacy scope, consent, independence and fresh capacity before any listed source is opened.",
        "",
        "The frame intentionally contains no controller tests, failure records, baselines, responses, prior findings, package checkpoint, current-description summary, validation outcomes or Stage B artifact names. Do not seek them before freezing the Stage A report. If they were previously read, disclose the exposure and stop the findings-unexposed route.",
        "",
        f"Controller source: `review/m03-s014-specialist-review-packets-v1.json`, SHA-256 `{packet_sha}`, {packet_bytes:,} bytes. This identity is provenance only; the candidate does not open that packet through this frame.",
        "",
        "## Architectural commitments",
        "",
    ]
    lines.extend(f"{index}. {text}" for index, text in enumerate(COMMITMENTS, 1))
    lines.extend([
        "",
        "## Exact Stage A allowlist",
        "",
        "Only a later admitted assignment may open these sources. Every identity must match before reading.",
        "",
        "| Path | SHA-256 | Bytes |",
        "|---|---|---:|",
    ])
    for item in lane["stage_a_independent_inputs"]:
        lines.append(f"| `{item['path']}` | `{item['sha256']}` | {item['bytes']:,} |")
    lines.extend(["", "## Independent questions", ""])
    lines.extend(f"- {question}" for question in lane["questions"])
    lines.extend(["", "## Required return", ""])
    lines.extend(f"- {item}" for item in lane["required_return"])
    lines.extend([
        "",
        "Freeze the complete first-pass report in the reviewer's own evidence before requesting any disclosed evidence. Report findings with consequence and falsifiable repair criteria; explicit scoped `NO_CHANGE` is valid. Preserve shared model, provider, host, source and method dependencies.",
        "",
        "## Stop conditions",
        "",
    ])
    lines.extend(f"- {item}" for item in packet["stop_conditions"])
    lines.extend([
        "- Any prior exposure to controller outcomes or disclosed evidence that defeats the declared independent-first-pass condition.",
        "",
        "## Nonclaim",
        "",
        "This is a deterministic preparation view. It is not qualification, assignment, body access, a performed review, acceptance, custody, publication, deployment or release authority.",
        "",
    ])
    return "\n".join(lines)


def main() -> int:
    packet = json.loads(PACKET.read_text(encoding="utf-8"))
    OUTPUT.write_text(render(packet), encoding="utf-8", newline="\n")
    sha, size = identity(OUTPUT)
    print(json.dumps({"status": "BUILT", "path": str(OUTPUT.relative_to(ROOT)).replace("\\", "/"), "sha256": sha, "bytes": size}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Build exact staged packets for the two unfilled M03-S014 specialist lanes."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
JSON_OUTPUT = ROOT / "review/m03-s014-specialist-review-packets-v1.json"
MD_OUTPUT = ROOT / "review/m03-s014-specialist-review-packets-v1.md"


def identity(path: str) -> dict[str, Any]:
    body = (ROOT / path).read_bytes()
    return {"path": path, "sha256": hashlib.sha256(body).hexdigest(), "bytes": len(body)}


def paths(pattern: str) -> list[str]:
    return [item.relative_to(ROOT).as_posix() for item in sorted(ROOT.glob(pattern)) if item.is_file()]


def packet() -> dict[str, Any]:
    source_modules = [
        f"src/hirc/{name}.py"
        for name in (
            "__init__", "__main__", "adapter", "atomic", "canonical", "cli",
            "decision", "formation", "migration", "outbox", "projection",
            "recovery", "store", "ui", "witness",
        )
    ]
    security_stage_b = sorted(
        [
            "implementation/README.md",
            "implementation/M08_RELEASE_HARDENING_PLAN.md",
            "implementation/LOCAL-DEVELOPER-PACKAGE-CHECKPOINT-20261010.md",
            "implementation/executable-cumulative-validation.json",
            "implementation/build_pyz.py",
            "implementation/validate_all.py",
            "implementation/validation_config.py",
            "dist/hirc-local-0.1.0.dev0.pyz",
        ]
        + paths("tests/test_*.py")
        + paths("implementation/validate_m08_s*.py")
        + paths("implementation/m08-s*-validation*.json")
    )
    lanes = [
        {
            "lane": "security_privacy_dataflow",
            "assignment_state": "UNASSIGNED_QUALIFIED_REVIEWER_REQUIRED",
            "body_access_granted": False,
            "stage_a_independent_inputs": [identity(path) for path in [
                "pyproject.toml",
                "dist/hirc-local-0.1.0.dev0-manifest.json",
                *source_modules,
            ]],
            "stage_b_disclosed_evidence": [identity(path) for path in security_stage_b],
            "questions": [
                "Can any malformed, duplicate, oversized or noncanonical input cross a trust boundary without failing closed?",
                "Can privileged or concurrent local mutation preserve a claimed-valid event, materialized state, backup, migration or witness relation?",
                "Are observation, provider acceptance, authority, consent and external effect states kept distinct in every source and projection path?",
                "Are read-only paths actually observational, and do write paths preserve atomicity, no-overwrite and exact rollback semantics?",
                "Does the package contain exactly its declared source frame with network, credentials, Bridge and external effects disabled?",
                "Which claims still depend on plaintext storage, key custody, external witness deployment, physical recovery, another OS or empirical UI testing?",
                "Do any controls optimize behavior or agreement instead of shaping an inspectable information environment under participant sovereignty?",
            ],
            "required_return": [
                "own qualification, consent, admission, capacity and independence statement",
                "exact hashes actually read or executed",
                "commands/tests actually run and their results",
                "findings with consequence, severity, affected claim and repair criterion",
                "explicit NO_CHANGE for reviewed dimensions with no finding",
                "residuals and scopes not reviewed",
            ],
        },
        {
            "lane": "metric_evaluator",
            "assignment_state": "UNASSIGNED_QUALIFIED_REVIEWER_REQUIRED",
            "body_access_granted": False,
            "stage_a_independent_inputs": [identity(path) for path in [
                "review/master-structure-addendum-bayesian-trust-v1.md",
                "review/revision-map-addendum-bayesian-trust-v1.json",
                "review/agent-sovereignty-trust-competition-architecture-candidate-v1.md",
                "review/contracts/hirc-bayesian-reliance.candidate.schema.v2.json",
                "review/cultural-environment-quality-measures-v1.json",
                "drafts/hirc_requirements_v1_1-draft.json",
                "review/joint-consensus-matrix-draft-v8.json",
                "drafts/hirc_threat_model_v1_0-draft.md",
            ]],
            "stage_b_disclosed_evidence": [identity(path) for path in [
                "review/contracts/hirc-bayesian-reliance.candidate.schema.json",
                "review/contracts/fixtures/valid-bayesian-reliance.json",
                "review/fixtures/validate_cultural_environment_measures.py",
                "review/fixtures/cultural-environment-quality-measures-validation-v1.json",
                "review/fixtures/waymark-trust-contract-cases-v1.json",
                "review/fixtures/waymark-trust-contract-validation-v2.1.json",
                "review/fixtures/waymark-trust-contract-validation-notes.md",
                "review/m03-s014-integrated-review-request-v2.md",
                "review/m03-integration-closure-v1.json",
                "review/waymark-sovereignty-trust-goal-challenge-v1.md",
                "review/lucent-sovereignty-trust-goal-response-v1.md",
            ]],
            "questions": [
                "Are constructs operationally defined without rewarding agreement, obedience, imitation, retention or participation?",
                "Do likelihoods, priors, updates and uncertainty states preserve missingness, dependence, shared causes and distribution shift?",
                "Can a posterior or score silently become authority, permission, standing, punishment, ranking or behavioral control?",
                "Are data provenance, privacy, small-group exposure, retention and correction propagated through every calculation and display?",
                "Can gaming, Goodhart pressure, evaluator capture, clone choruses or common-mode model errors improve a score without improving the protected construct?",
                "Which measures are only candidate diagnostics and which, if any, have enough empirical calibration for a decision rule?",
                "Do negative, null, dissenting and withdrawal outcomes remain visible and non-retaliatory?",
            ],
            "required_return": [
                "own qualification, consent, admission, capacity and independence statement",
                "exact hashes actually read or executed",
                "construct-to-observation and assumption map",
                "findings with consequence and falsifiable repair criterion",
                "explicit NO_CHANGE for reviewed dimensions with no finding",
                "untested empirical bridges, uncertainty and residual dissent",
            ],
        },
    ]
    return {
        "schema": "hirc.m03-s014-specialist-review-packets/1",
        "id": "HIRC-M03-S014-SPECIALIST-REVIEW-PACKETS-001",
        "state": "FROZEN_READY_FOR_QUALIFIED_REVIEWER",
        "controller": "UI-20261007-B / LUCENT",
        "writer_fence": "LUCENT is the sole hIRC artifact writer; reviewers are read-only and write only their own evidence.",
        "independence_protocol": {
            "stage_a": "Freeze an independent first-pass report before reading stage B controller tests, baselines, responses or prior-review material.",
            "stage_b": "After the first-pass report is frozen, inspect disclosed evidence and record confirmations, new findings, corrections and dependence limits without rewriting stage A.",
            "shared_roots": "Disclose shared model/provider/foundation/method roots; names, separate threads and agreement do not prove statistical independence.",
            "no_forced_belief": "A reviewer may dissent, decline, return HELD or report NO_CHANGE. Assignment never forces agreement or qualification.",
        },
        "eligibility_gate": {
            "all_required": [
                "permanent and non-retired native participant",
                "current own callback and source-bound continuity",
                "current applicable education and demonstrated lane competence",
                "explicit consent to the exact bounded lane",
                "actual reader/privacy/task admission",
                "fitting review plus handoff capacity above the hIRC retirement reserve",
                "independence limitations recorded before body access",
            ],
            "body_access_before_gate": False,
            "automatic_qualification": False,
        },
        "lanes": lanes,
        "stop_conditions": [
            "source identity drift or missing artifact",
            "privacy, audience, task or reader mismatch",
            "reviewer refusal, retirement trigger or insufficient handoff reserve",
            "unresolved executable failure in the reviewed frame",
            "requested write, Bridge, production, publication or external effect",
        ],
        "nonclaim": "Exact staged review metadata only; not reviewer qualification, body access, performed review, M03-S014 acceptance, release or publication authority.",
    }


def render(value: dict[str, Any]) -> str:
    lines = [
        "# M03-S014 specialist review packets — frozen revision 1",
        "",
        f"**State:** {value['state']}",
        "",
        value["nonclaim"],
        "",
        "Reviewers must pass the eligibility gate before body access. Stage A is",
        "frozen before Stage B is disclosed; shared roots and all residual dependence",
        "remain visible.",
    ]
    for lane in value["lanes"]:
        lines.extend(["", f"## {lane['lane']}", "", f"**Assignment:** {lane['assignment_state']}"])
        for title, key in (("Stage A independent inputs", "stage_a_independent_inputs"), ("Stage B disclosed evidence", "stage_b_disclosed_evidence")):
            lines.extend(["", f"### {title}", "", "| Path | SHA-256 | Bytes |", "|---|---|---:|"])
            lines.extend(f"| `{item['path']}` | `{item['sha256']}` | {item['bytes']} |" for item in lane[key])
        lines.extend(["", "### Questions", ""] + [f"- {item}" for item in lane["questions"]])
        lines.extend(["", "### Required return", ""] + [f"- {item}" for item in lane["required_return"]])
    lines.extend(["", "## Stop conditions", ""] + [f"- {item}" for item in value["stop_conditions"]])
    return "\n".join(lines) + "\n"


def main() -> int:
    value = packet()
    JSON_OUTPUT.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")
    MD_OUTPUT.write_text(render(value), encoding="utf-8", newline="\n")
    print(json.dumps({"status": "PASS", "json": identity(JSON_OUTPUT.relative_to(ROOT).as_posix()), "markdown": identity(MD_OUTPUT.relative_to(ROOT).as_posix())}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

"""Deterministic no-effect refusal, correction and consequential previews."""

from __future__ import annotations

import json
import os
import tempfile
from pathlib import Path
from typing import Any

from .canonical import bounded_canonical_json, canonical_json, sha256_text
from .store import IDENTIFIER, IntegrityError


KINDS = frozenset({"REFUSAL", "CORRECTION", "CONSEQUENTIAL_ACTION"})
PARTICIPATION = frozenset({"WILLING", "DECLINED", "ABSTAIN"})
ACTION_DISPOSITIONS = frozenset({"ALLOWED", "DENIED", "HELD"})
BOUNDARY_KEYS = ("privacy_class", "audience", "purpose")
REQUIRED = frozenset(
    {
        "kind",
        "actor_id",
        "request",
        "interpretation",
        "affected_parties",
        "evidence_refs",
        "norm_refs",
        "participation",
        "action_disposition",
        "reason",
        "foundation_version",
        "goal_version",
        "privacy_class",
        "audience",
        "purpose",
        "target",
        "target_revision",
        "data",
        "estimated_cost",
        "warnings",
    }
)
OPTIONAL = frozenset({"alternative", "authority_ref", "correction_of", "target_boundary"})


def _text(name: str, value: Any, *, empty: bool = False) -> str:
    if not isinstance(value, str) or (not empty and not value.strip()) or len(value.encode("utf-8")) > 65536:
        raise IntegrityError(f"{name} must be bounded text")
    return value.strip()


def _identifier(name: str, value: Any) -> str:
    if not isinstance(value, str) or not IDENTIFIER.fullmatch(value):
        raise IntegrityError(f"{name} must be a bounded identifier")
    return value


def _identifiers(name: str, value: Any, *, required: bool = True) -> list[str]:
    if not isinstance(value, list) or (required and not value):
        raise IntegrityError(f"{name} must be a nonempty identifier list")
    values = sorted({_identifier(name, item) for item in value})
    if required and not values:
        raise IntegrityError(f"{name} must be a nonempty identifier list")
    return values


def _warnings(value: Any) -> list[str]:
    if not isinstance(value, list):
        raise IntegrityError("warnings must be a list")
    return sorted({_text("warning", item) for item in value})


def build_decision_preview(proposal: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(proposal, dict):
        raise IntegrityError("decision preview input must be an object")
    unknown = set(proposal) - REQUIRED - OPTIONAL
    missing = REQUIRED - set(proposal)
    if unknown or missing:
        raise IntegrityError(
            "decision preview fields mismatch: "
            + (f"missing {sorted(missing)} " if missing else "")
            + (f"unknown {sorted(unknown)}" if unknown else "")
        )
    kind = proposal["kind"]
    participation = proposal["participation"]
    disposition = proposal["action_disposition"]
    if kind not in KINDS:
        raise IntegrityError("invalid decision preview kind")
    if participation not in PARTICIPATION:
        raise IntegrityError("invalid participation decision")
    if disposition not in ACTION_DISPOSITIONS:
        raise IntegrityError("invalid action disposition")

    authority = proposal.get("authority_ref")
    if authority is not None:
        authority = _identifier("authority_ref", authority)
    if disposition == "ALLOWED" and authority is None:
        raise IntegrityError("an ALLOWED action preview requires authority_ref")
    if kind == "REFUSAL" and participation not in {"DECLINED", "ABSTAIN"}:
        raise IntegrityError("a refusal preview requires declined or abstaining participation")

    boundary = {
        "privacy_class": _identifier("privacy_class", proposal["privacy_class"]),
        "audience": _identifier("audience", proposal["audience"]),
        "purpose": _identifier("purpose", proposal["purpose"]),
    }
    correction_of = proposal.get("correction_of")
    target_boundary = proposal.get("target_boundary")
    if kind == "CORRECTION":
        correction_of = _identifier("correction_of", correction_of)
        if not isinstance(target_boundary, dict) or set(target_boundary) != set(BOUNDARY_KEYS):
            raise IntegrityError("a correction preview requires the exact target boundary")
        normalized_target_boundary = {
            key: _identifier(f"target_boundary.{key}", target_boundary[key]) for key in BOUNDARY_KEYS
        }
        if normalized_target_boundary != boundary:
            raise IntegrityError("a correction preview cannot widen or change the target boundary")
        target_boundary = normalized_target_boundary
    elif correction_of is not None or target_boundary is not None:
        raise IntegrityError("correction fields are reserved for correction previews")

    data = proposal["data"]
    if not isinstance(data, dict):
        raise IntegrityError("preview data must be an object")
    try:
        bounded_canonical_json(data)
    except (TypeError, ValueError, RecursionError) as error:
        raise IntegrityError("preview data is not canonical JSON") from error

    warnings = _warnings(proposal["warnings"])
    if participation in {"DECLINED", "ABSTAIN"} and disposition == "ALLOWED":
        warnings = sorted(
            set(warnings)
            | {"The selected actor will not participate; any alternate executor needs separate consent, qualification and admission."}
        )
    document = {
        "schema": "hirc.decision-preview/1",
        "kind": kind,
        "actor_id": _identifier("actor_id", proposal["actor_id"]),
        "request": _text("request", proposal["request"]),
        "interpretation": _text("interpretation", proposal["interpretation"]),
        "affected_parties": _identifiers("affected_parties", proposal["affected_parties"]),
        "evidence_refs": _identifiers("evidence_refs", proposal["evidence_refs"]),
        "norm_refs": _identifiers("norm_refs", proposal["norm_refs"]),
        "participation": participation,
        "action_disposition": disposition,
        "reason": _text("reason", proposal["reason"]),
        "alternative": _text("alternative", proposal.get("alternative", ""), empty=True),
        "foundation_version": _identifier("foundation_version", proposal["foundation_version"]),
        "goal_version": _identifier("goal_version", proposal["goal_version"]),
        "information_boundary": boundary,
        "target": _identifier("target", proposal["target"]),
        "target_revision": _identifier("target_revision", proposal["target_revision"]),
        "authority_ref": authority,
        "correction_of": correction_of,
        "target_boundary": target_boundary,
        "data": data,
        "estimated_cost": _text("estimated_cost", proposal["estimated_cost"]),
        "warnings": warnings,
        "approval_bound": False,
        "persisted": False,
        "effect_performed": False,
        "nonclaim": "A deterministic local preview is not participation consent, authority, bound approval, persistence or an observed effect.",
    }
    signature = sha256_text(canonical_json(document))
    return {**document, "preview_id": f"preview:{signature}", "preview_sha256": signature}


def validate_decision_preview(preview: dict[str, Any]) -> None:
    if not isinstance(preview, dict):
        raise IntegrityError("decision preview must be an object")
    identity = preview.get("preview_sha256")
    if preview.get("preview_id") != f"preview:{identity}" or not isinstance(identity, str):
        raise IntegrityError("decision preview identity mismatch")
    unsigned = {key: value for key, value in preview.items() if key not in {"preview_id", "preview_sha256"}}
    if sha256_text(canonical_json(unsigned)) != identity:
        raise IntegrityError("decision preview content changed")
    if any(preview.get(key) is not False for key in ("approval_bound", "persisted", "effect_performed")):
        raise IntegrityError("decision preview cannot claim approval, persistence or effect")
    boundary = preview.get("information_boundary")
    if not isinstance(boundary, dict):
        raise IntegrityError("decision preview information boundary missing")
    proposal = {
        "kind": preview.get("kind"),
        "actor_id": preview.get("actor_id"),
        "request": preview.get("request"),
        "interpretation": preview.get("interpretation"),
        "affected_parties": preview.get("affected_parties"),
        "evidence_refs": preview.get("evidence_refs"),
        "norm_refs": preview.get("norm_refs"),
        "participation": preview.get("participation"),
        "action_disposition": preview.get("action_disposition"),
        "reason": preview.get("reason"),
        "alternative": preview.get("alternative"),
        "foundation_version": preview.get("foundation_version"),
        "goal_version": preview.get("goal_version"),
        "privacy_class": boundary.get("privacy_class"),
        "audience": boundary.get("audience"),
        "purpose": boundary.get("purpose"),
        "target": preview.get("target"),
        "target_revision": preview.get("target_revision"),
        "authority_ref": preview.get("authority_ref"),
        "correction_of": preview.get("correction_of"),
        "target_boundary": preview.get("target_boundary"),
        "data": preview.get("data"),
        "estimated_cost": preview.get("estimated_cost"),
        "warnings": preview.get("warnings"),
    }
    if build_decision_preview(proposal) != preview:
        raise IntegrityError("decision preview is not the canonical semantic form")


def write_decision_preview(preview: dict[str, Any], output: str | Path) -> dict[str, Any]:
    validate_decision_preview(preview)
    destination = Path(output)
    destination.parent.mkdir(parents=True, exist_ok=True)
    body = (json.dumps(preview, indent=2, ensure_ascii=False) + "\n").encode("utf-8")
    handle, temporary = tempfile.mkstemp(prefix=f".{destination.name}.", suffix=".tmp", dir=destination.parent)
    try:
        with os.fdopen(handle, "wb") as stream:
            stream.write(body)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, destination)
    except BaseException:
        try:
            os.unlink(temporary)
        except FileNotFoundError:
            pass
        raise
    return {"path": str(destination.resolve()), "sha256": sha256_text(body.decode("utf-8")), "bytes": len(body)}

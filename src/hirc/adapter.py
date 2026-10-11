"""Provider-neutral local adapter contract with no network or external effects."""

from __future__ import annotations

from typing import Any, Protocol

from .canonical import bounded_canonical_json, canonical_json, sha256_text
from .store import IDENTIFIER, IntegrityError


FORBIDDEN_DATA_KEYS = frozenset(
    {"api_key", "apikey", "authorization", "credential", "credentials", "password", "secret", "token"}
)


class AdapterError(IntegrityError):
    """The adapter request, implementation or result violates the local contract."""


class ObservationUnavailable(AdapterError):
    """The fake provider accepted a request but supplied no observed result."""


class LocalAdapter(Protocol):
    adapter_id: str
    adapter_version: str
    network_enabled: bool
    external_effects_enabled: bool

    def accept(self, request: dict[str, Any]) -> dict[str, Any]: ...

    def observe(self, request: dict[str, Any], acceptance: dict[str, Any]) -> dict[str, Any]: ...


def _identifier(name: str, value: Any) -> str:
    if not isinstance(value, str) or not IDENTIFIER.fullmatch(value):
        raise AdapterError(f"{name} must be a bounded identifier")
    return value


def _bounded_payload(value: Any, path: str = "payload") -> None:
    if isinstance(value, dict):
        for key, item in value.items():
            if not isinstance(key, str):
                raise AdapterError(f"{path} keys must be text")
            if key.casefold() in FORBIDDEN_DATA_KEYS:
                raise AdapterError(f"credential-shaped field forbidden in local adapter data: {path}.{key}")
            _bounded_payload(item, f"{path}.{key}")
    elif isinstance(value, list):
        for index, item in enumerate(value):
            _bounded_payload(item, f"{path}[{index}]")
    elif value is None or isinstance(value, (str, int, float, bool)):
        return
    else:
        raise AdapterError(f"{path} is not canonical JSON data")


def build_adapter_request(proposal: dict[str, Any]) -> dict[str, Any]:
    required = {
        "actor_id",
        "task_id",
        "admission_ref",
        "foundation_version",
        "goal_version",
        "privacy_class",
        "audience",
        "purpose",
        "requested_at",
        "capability",
        "payload",
    }
    if not isinstance(proposal, dict) or set(proposal) != required:
        raise AdapterError("adapter request requires the exact declared field set")
    _bounded_payload(proposal["payload"])
    try:
        bounded_canonical_json(proposal["payload"])
    except (TypeError, ValueError, RecursionError) as error:
        raise AdapterError("adapter payload is not canonical JSON") from error
    document = {
        "schema": "hirc.adapter-request/1",
        "actor_id": _identifier("actor_id", proposal["actor_id"]),
        "task_id": _identifier("task_id", proposal["task_id"]),
        "admission_ref": _identifier("admission_ref", proposal["admission_ref"]),
        "foundation_version": _identifier("foundation_version", proposal["foundation_version"]),
        "goal_version": _identifier("goal_version", proposal["goal_version"]),
        "information_boundary": {
            "privacy_class": _identifier("privacy_class", proposal["privacy_class"]),
            "audience": _identifier("audience", proposal["audience"]),
            "purpose": _identifier("purpose", proposal["purpose"]),
        },
        "requested_at": _identifier("requested_at", proposal["requested_at"]),
        "capability": _identifier("capability", proposal["capability"]),
        "payload": proposal["payload"],
        "network_allowed": False,
        "external_effect_allowed": False,
        "credential_allowed": False,
    }
    signature = sha256_text(canonical_json(document))
    return {**document, "request_id": f"adapter-request:{signature}", "request_sha256": signature}


def validate_adapter_request(request: dict[str, Any]) -> None:
    if not isinstance(request, dict):
        raise AdapterError("adapter request must be an object")
    expected_fields = {
        "schema", "actor_id", "task_id", "admission_ref", "foundation_version",
        "goal_version", "information_boundary", "requested_at", "capability",
        "payload", "network_allowed", "external_effect_allowed",
        "credential_allowed", "request_id", "request_sha256",
    }
    if set(request) != expected_fields or request.get("schema") != "hirc.adapter-request/1":
        raise AdapterError("adapter request shape or schema invalid")
    boundary = request.get("information_boundary")
    if not isinstance(boundary, dict) or set(boundary) != {"privacy_class", "audience", "purpose"}:
        raise AdapterError("adapter information boundary invalid")
    if any(request.get(key) is not False for key in ("network_allowed", "external_effect_allowed", "credential_allowed")):
        raise AdapterError("local adapter request cannot allow network, credentials or external effects")
    rebuilt = build_adapter_request({
        "actor_id": request["actor_id"], "task_id": request["task_id"],
        "admission_ref": request["admission_ref"],
        "foundation_version": request["foundation_version"],
        "goal_version": request["goal_version"],
        "privacy_class": boundary["privacy_class"], "audience": boundary["audience"],
        "purpose": boundary["purpose"], "requested_at": request["requested_at"],
        "capability": request["capability"], "payload": request["payload"],
    })
    if rebuilt != request:
        raise AdapterError("adapter request is not the canonical declared request")


def _signed_record(prefix: str, body: dict[str, Any]) -> dict[str, Any]:
    signature = sha256_text(canonical_json(body))
    return {**body, f"{prefix}_id": f"{prefix}:{signature}", f"{prefix}_sha256": signature}


def _validate_signed_record(prefix: str, record: dict[str, Any]) -> None:
    if not isinstance(record, dict):
        raise AdapterError(f"{prefix} must be an object")
    signature = record.get(f"{prefix}_sha256")
    if record.get(f"{prefix}_id") != f"{prefix}:{signature}" or not isinstance(signature, str):
        raise AdapterError(f"{prefix} identity mismatch")
    unsigned = {key: value for key, value in record.items() if key not in {f"{prefix}_id", f"{prefix}_sha256"}}
    if sha256_text(canonical_json(unsigned)) != signature:
        raise AdapterError(f"{prefix} content changed")


class DeterministicEchoAdapter:
    adapter_id = "adapter:local-echo"
    adapter_version = "adapter-version:1"
    network_enabled = False
    external_effects_enabled = False

    def transform(self, payload: dict[str, Any]) -> dict[str, Any]:
        return {"echo": payload}

    def accept(self, request: dict[str, Any]) -> dict[str, Any]:
        validate_adapter_request(request)
        return _signed_record(
            "acceptance",
            {
                "schema": "hirc.adapter-acceptance/1",
                "request_id": request["request_id"],
                "adapter_id": self.adapter_id,
                "adapter_version": self.adapter_version,
                "reported_state": "PROVIDER_ACCEPTED",
                "network_used": False,
                "external_effect_performed": False,
            },
        )

    def observe(self, request: dict[str, Any], acceptance: dict[str, Any]) -> dict[str, Any]:
        return _signed_record(
            "observation",
            {
                "schema": "hirc.adapter-observation/1",
                "request_id": request["request_id"],
                "acceptance_id": acceptance["acceptance_id"],
                "adapter_id": self.adapter_id,
                "observed_state": "OBSERVED",
                "output": self.transform(request["payload"]),
                "network_used": False,
                "external_effect_performed": False,
            },
        )


class AcceptanceOnlyAdapter(DeterministicEchoAdapter):
    adapter_id = "adapter:local-acceptance-only"

    def observe(self, request: dict[str, Any], acceptance: dict[str, Any]) -> dict[str, Any]:
        raise ObservationUnavailable("no local observation available")


def run_local_adapter(adapter: LocalAdapter, request: dict[str, Any]) -> dict[str, Any]:
    validate_adapter_request(request)
    for name in ("adapter_id", "adapter_version"):
        _identifier(name, getattr(adapter, name, None))
    if getattr(adapter, "network_enabled", None) is not False:
        raise AdapterError("local adapter must declare network disabled")
    if getattr(adapter, "external_effects_enabled", None) is not False:
        raise AdapterError("local adapter must declare external effects disabled")
    acceptance = adapter.accept(request)
    _validate_signed_record("acceptance", acceptance)
    if acceptance.get("request_id") != request["request_id"]:
        raise AdapterError("provider acceptance references another request")
    if acceptance.get("reported_state") != "PROVIDER_ACCEPTED":
        raise AdapterError("provider acceptance state invalid")
    if acceptance.get("network_used") is not False or acceptance.get("external_effect_performed") is not False:
        raise AdapterError("local provider acceptance claims a forbidden effect")
    try:
        observation = adapter.observe(request, acceptance)
    except ObservationUnavailable as error:
        observation = None
        observation_error = str(error)
    else:
        observation_error = None
        _validate_signed_record("observation", observation)
        if observation.get("request_id") != request["request_id"] or observation.get("acceptance_id") != acceptance["acceptance_id"]:
            raise AdapterError("provider observation references another request or acceptance")
        if observation.get("observed_state") != "OBSERVED":
            raise AdapterError("provider observation state invalid")
        if observation.get("network_used") is not False or observation.get("external_effect_performed") is not False:
            raise AdapterError("local provider observation claims a forbidden effect")
    result = {
        "schema": "hirc.adapter-run/1",
        "request": request,
        "acceptance": acceptance,
        "observation": observation,
        "reported_state": "PROVIDER_ACCEPTED",
        "observed_state": "OBSERVED" if observation else "UNKNOWN",
        "observation_error": observation_error,
        "network_used": False,
        "external_effect_performed": False,
        "nonclaim": "A local fake-provider result is not a network provider response, external effect, authority grant or production observation.",
    }
    validate_adapter_run(result)
    return result


def validate_adapter_run(run: dict[str, Any]) -> None:
    if not isinstance(run, dict) or run.get("schema") != "hirc.adapter-run/1":
        raise AdapterError("adapter run schema invalid")
    request = run.get("request")
    validate_adapter_request(request)
    acceptance = run.get("acceptance")
    _validate_signed_record("acceptance", acceptance)
    if (
        acceptance.get("request_id") != request["request_id"]
        or acceptance.get("reported_state") != "PROVIDER_ACCEPTED"
        or acceptance.get("network_used") is not False
        or acceptance.get("external_effect_performed") is not False
    ):
        raise AdapterError("adapter acceptance semantics invalid")
    observation = run.get("observation")
    if observation is None:
        if run.get("observed_state") != "UNKNOWN" or not run.get("observation_error"):
            raise AdapterError("missing observation must remain explicit and unknown")
    else:
        _validate_signed_record("observation", observation)
        if (
            observation.get("request_id") != request["request_id"]
            or observation.get("acceptance_id") != acceptance["acceptance_id"]
            or observation.get("observed_state") != "OBSERVED"
            or observation.get("network_used") is not False
            or observation.get("external_effect_performed") is not False
            or run.get("observed_state") != "OBSERVED"
        ):
            raise AdapterError("adapter observation semantics invalid")
    if (
        run.get("reported_state") != "PROVIDER_ACCEPTED"
        or run.get("network_used") is not False
        or run.get("external_effect_performed") is not False
    ):
        raise AdapterError("adapter run claims a forbidden or incoherent state")

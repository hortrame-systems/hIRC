from __future__ import annotations

import copy
import io
import json
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path
from unittest.mock import patch

from hirc.adapter import (
    AcceptanceOnlyAdapter,
    AdapterError,
    DeterministicEchoAdapter,
    build_adapter_request,
    run_local_adapter,
    validate_adapter_run,
    validate_adapter_request,
)
from hirc.cli import main
from hirc.canonical import DEFAULT_MAX_JSON_BYTES, canonical_json, sha256_text


def proposal(payload: dict | None = None) -> dict:
    return {
        "actor_id": "actor:local",
        "task_id": "task:hirc",
        "admission_ref": "admission:recorded",
        "foundation_version": "foundation:1",
        "goal_version": "goal:2",
        "privacy_class": "privacy:owner",
        "audience": "audience:owner",
        "purpose": "purpose:local-adapter",
        "requested_at": "time:20261010T000000Z",
        "capability": "capability:local-transform",
        "payload": payload or {"text": "hello"},
    }


class AdapterTests(unittest.TestCase):
    def test_same_request_is_deterministic(self) -> None:
        self.assertEqual(build_adapter_request(proposal()), build_adapter_request(proposal()))

    def test_nested_credential_shaped_fields_are_rejected(self) -> None:
        with self.assertRaises(AdapterError):
            build_adapter_request(proposal({"nested": {"api_key": "secret"}}))

    def test_adapter_payload_depth_and_size_limits_fail_closed(self) -> None:
        deep: dict = {}
        cursor = deep
        for _ in range(70):
            cursor["nested"] = {}
            cursor = cursor["nested"]
        for payload in (deep, {"text": "x" * 1_100_000}):
            with self.assertRaises(AdapterError):
                build_adapter_request(proposal(payload))

    def test_request_tampering_is_rejected(self) -> None:
        request = build_adapter_request(proposal())
        changed = copy.deepcopy(request)
        changed["payload"]["text"] = "changed"
        with self.assertRaises(AdapterError):
            validate_adapter_request(changed)

    def test_self_rehashed_noncanonical_request_shapes_are_rejected(self) -> None:
        def rehash(changed: dict) -> dict:
            unsigned = {
                key: value
                for key, value in changed.items()
                if key not in {"request_id", "request_sha256"}
            }
            signature = sha256_text(canonical_json(unsigned))
            changed["request_id"] = f"adapter-request:{signature}"
            changed["request_sha256"] = signature
            return changed

        mutations = {
            "wrong schema": lambda value: value.__setitem__("schema", "hirc.adapter-request/0"),
            "invalid actor": lambda value: value.__setitem__("actor_id", "actor with spaces"),
            "nonobject boundary": lambda value: value.__setitem__("information_boundary", "owner"),
            "extra field": lambda value: value.__setitem__("undeclared", False),
        }
        for name, mutate in mutations.items():
            with self.subTest(name=name):
                changed = copy.deepcopy(build_adapter_request(proposal()))
                mutate(changed)
                with self.assertRaises(AdapterError):
                    validate_adapter_request(rehash(changed))

    def test_direct_validation_bounds_self_rehashed_payload_before_acceptance(self) -> None:
        def rehash(changed: dict) -> dict:
            unsigned = {
                key: value
                for key, value in changed.items()
                if key not in {"request_id", "request_sha256"}
            }
            signature = sha256_text(canonical_json(unsigned))
            changed["request_id"] = f"adapter-request:{signature}"
            changed["request_sha256"] = signature
            return changed

        deep: dict = {}
        cursor = deep
        for _ in range(70):
            cursor["nested"] = {}
            cursor = cursor["nested"]
        for name, payload in (
            ("oversized", {"text": "x" * 1_100_000}),
            ("overdeep", deep),
        ):
            with self.subTest(name=name):
                changed = copy.deepcopy(build_adapter_request(proposal()))
                changed["payload"] = payload
                changed = rehash(changed)
                with patch("hirc.adapter.canonical_json", wraps=canonical_json) as canonical, self.assertRaises(AdapterError):
                    validate_adapter_request(changed)
                canonical.assert_not_called()

    def test_adapter_run_nested_effect_claim_is_rejected(self) -> None:
        run = run_local_adapter(DeterministicEchoAdapter(), build_adapter_request(proposal()))
        run["observation"]["external_effect_performed"] = True
        with self.assertRaises(AdapterError):
            validate_adapter_run(run)

    def test_acceptance_and_observation_remain_separate(self) -> None:
        result = run_local_adapter(DeterministicEchoAdapter(), build_adapter_request(proposal()))
        self.assertEqual(result["reported_state"], "PROVIDER_ACCEPTED")
        self.assertEqual(result["observed_state"], "OBSERVED")
        self.assertNotEqual(result["acceptance"]["acceptance_id"], result["observation"]["observation_id"])

    def test_acceptance_without_observation_stays_unknown(self) -> None:
        result = run_local_adapter(AcceptanceOnlyAdapter(), build_adapter_request(proposal()))
        self.assertEqual(result["reported_state"], "PROVIDER_ACCEPTED")
        self.assertEqual(result["observed_state"], "UNKNOWN")
        self.assertIsNone(result["observation"])

    def test_command_shaped_payload_remains_inert(self) -> None:
        shaped = "<script>alert(1)</script>; rm -rf /; file:///secret"
        result = run_local_adapter(DeterministicEchoAdapter(), build_adapter_request(proposal({"text": shaped})))
        self.assertEqual(result["observation"]["output"]["echo"]["text"], shaped)

    def test_adapter_declaring_network_or_effect_is_rejected(self) -> None:
        request = build_adapter_request(proposal())

        class Unsafe(DeterministicEchoAdapter):
            network_enabled = True

        class Effectful(DeterministicEchoAdapter):
            external_effects_enabled = True

        for adapter in (Unsafe(), Effectful()):
            with self.subTest(adapter=type(adapter).__name__), self.assertRaises(AdapterError):
                run_local_adapter(adapter, request)

    def test_acceptance_for_another_request_is_rejected(self) -> None:
        class Mismatched(DeterministicEchoAdapter):
            def accept(self, request):
                value = super().accept(request)
                value["request_id"] = "adapter-request:" + "f" * 64
                return value

        with self.assertRaises(AdapterError):
            run_local_adapter(Mismatched(), build_adapter_request(proposal()))

    def test_provider_contract_is_implementation_neutral(self) -> None:
        class Uppercase(DeterministicEchoAdapter):
            adapter_id = "adapter:local-uppercase"

            def transform(self, payload):
                return {"text": payload["text"].upper()}

        result = run_local_adapter(Uppercase(), build_adapter_request(proposal()))
        self.assertEqual(result["observation"]["output"]["text"], "HELLO")
        self.assertFalse(result["network_used"])
        self.assertFalse(result["external_effect_performed"])

    def test_cli_exposes_local_fake_and_acceptance_only_modes(self) -> None:
        temporary_root = Path(__file__).parent / ".tmp"
        temporary_root.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory(dir=temporary_root) as directory:
            source = Path(directory) / "adapter.json"
            source.write_text(json.dumps(proposal()), encoding="utf-8")
            for extra, observed in (([], "OBSERVED"), (["--acceptance-only"], "UNKNOWN")):
                output = io.StringIO()
                with redirect_stdout(output):
                    code = main(["adapter-run", "--input", str(source), *extra])
                self.assertEqual(code, 0)
                self.assertEqual(json.loads(output.getvalue())["observed_state"], observed)

    def test_cli_rejects_oversized_json_file_before_parsing(self) -> None:
        temporary_root = Path(__file__).parent / ".tmp"
        temporary_root.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory(dir=temporary_root) as directory:
            source = Path(directory) / "oversized.json"
            source.write_bytes(b" " * (DEFAULT_MAX_JSON_BYTES + 1))
            stderr = io.StringIO()
            with redirect_stderr(stderr):
                code = main(["adapter-run", "--input", str(source)])
            self.assertEqual(code, 2)
            self.assertIn("JSON file exceeds the local byte limit", stderr.getvalue())

    def test_cli_rejects_duplicate_json_keys(self) -> None:
        temporary_root = Path(__file__).parent / ".tmp"
        temporary_root.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory(dir=temporary_root) as directory:
            source = Path(directory) / "duplicate.json"
            body = json.dumps(proposal(), separators=(",", ":"))
            source.write_text('{"actor_id":"actor:forged",' + body[1:], encoding="utf-8")
            stderr = io.StringIO()
            with redirect_stderr(stderr):
                code = main(["adapter-run", "--input", str(source)])
            self.assertEqual(code, 2)
            self.assertIn("JSON file is not valid bounded UTF-8 JSON", stderr.getvalue())


if __name__ == "__main__":
    unittest.main()

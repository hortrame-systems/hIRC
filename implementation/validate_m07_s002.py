#!/usr/bin/env python3
"""Reproduce M07-S002 provider-neutral local no-effect adapter checks."""

from __future__ import annotations

import ast
import hashlib
import io
import json
import sys
import unittest
from pathlib import Path

from validation_config import ADAPTER_TESTS, FULL_SUITE_TESTS


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from hirc.adapter import (  # noqa: E402
    AcceptanceOnlyAdapter,
    DeterministicEchoAdapter,
    build_adapter_request,
    run_local_adapter,
)


OUTPUT = ROOT / "implementation/m07-s002-validation.json"
FILES = (
    "implementation/M07_FORMATION_ADAPTER_PLAN.md",
    "implementation/README.md",
    "src/hirc/adapter.py",
    "src/hirc/cli.py",
    "tests/test_adapter.py",
)
FORBIDDEN_IMPORTS = {"socket", "http", "urllib", "requests", "aiohttp", "subprocess"}


def identity(relative: str) -> dict[str, object]:
    body = (ROOT / relative).read_bytes()
    return {"path": relative, "sha256": hashlib.sha256(body).hexdigest(), "bytes": len(body)}


def imported_roots(path: Path) -> set[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    names: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            names.update(alias.name.split(".", 1)[0] for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            names.add(node.module.split(".", 1)[0])
    return names


def proposal() -> dict:
    return {
        "actor_id": "actor:validator",
        "task_id": "task:hirc",
        "admission_ref": "admission:recorded",
        "foundation_version": "foundation:1",
        "goal_version": "goal:2",
        "privacy_class": "privacy:owner",
        "audience": "audience:owner",
        "purpose": "purpose:m07-adapter-validation",
        "requested_at": "time:20261010T000000Z",
        "capability": "capability:local-transform",
        "payload": {"text": "local provider-neutral fixture"},
    }


def main() -> int:
    adapter_stream = io.StringIO()
    adapter_suite = unittest.defaultTestLoader.discover(str(ROOT / "tests"), pattern="test_adapter.py")
    adapter_tests = unittest.TextTestRunner(stream=adapter_stream, verbosity=2).run(adapter_suite)
    full_stream = io.StringIO()
    full_suite = unittest.defaultTestLoader.discover(str(ROOT / "tests"))
    full_tests = unittest.TextTestRunner(stream=full_stream, verbosity=1).run(full_suite)

    request = build_adapter_request(proposal())
    observed = run_local_adapter(DeterministicEchoAdapter(), request)
    uncertain = run_local_adapter(AcceptanceOnlyAdapter(), request)
    imports = imported_roots(ROOT / "src/hirc/adapter.py") & FORBIDDEN_IMPORTS
    checks = {
        "adapter_tests_pass": adapter_tests.wasSuccessful(),
        "adapter_test_count": adapter_tests.testsRun == ADAPTER_TESTS,
        "full_suite_pass": full_tests.wasSuccessful(),
        "full_suite_test_count": full_tests.testsRun == FULL_SUITE_TESTS,
        "network_process_imports_absent": not imports,
        "request_disables_network_effect_and_credentials": all(request[key] is False for key in ("network_allowed", "external_effect_allowed", "credential_allowed")),
        "acceptance_observation_separate": observed["reported_state"] == "PROVIDER_ACCEPTED" and observed["observed_state"] == "OBSERVED" and observed["acceptance"]["acceptance_id"] != observed["observation"]["observation_id"],
        "uncertain_observation_not_promoted": uncertain["reported_state"] == "PROVIDER_ACCEPTED" and uncertain["observed_state"] == "UNKNOWN" and uncertain["observation"] is None,
        "no_network_or_effect_claim": not observed["network_used"] and not observed["external_effect_performed"] and not uncertain["network_used"] and not uncertain["external_effect_performed"],
    }
    result = {
        "schema": "hirc.m07-s002-validation/1",
        "stone": "M07-S002",
        "status": "PASS" if all(checks.values()) else "FAIL",
        "checks": checks,
        "files": [identity(path) for path in FILES],
        "adapter_test_output": adapter_stream.getvalue().splitlines(),
        "full_suite_output": full_stream.getvalue().splitlines(),
        "request_id": request["request_id"],
        "observed_run": observed,
        "uncertain_run": uncertain,
        "forbidden_imports": sorted(imports),
        "surviving_limits": [
            "Only deterministic in-process fake providers are implemented; no production provider behavior is tested.",
            "Admission references are metadata and no credentials are accepted or loaded.",
            "No network, process, outbox dispatch, external effect or Bridge path exists in this stone."
        ],
        "nonclaim": "M07-S002 provider-neutral local fake-adapter evidence only."
    }
    OUTPUT.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps(result, indent=2))
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())

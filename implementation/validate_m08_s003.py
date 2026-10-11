#!/usr/bin/env python3
"""Reproduce M08-S003 deterministic package checks and release holds."""

from __future__ import annotations

import hashlib
import io
import json
import os
import subprocess
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path

from validation_config import EXPECTED_RELEASE_FAILURES, FULL_SUITE_TESTS


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "implementation"))
sys.path.insert(0, str(ROOT / "src"))

from build_pyz import build  # noqa: E402


OUTPUT = ROOT / "implementation/m08-s003-validation.json"
PACKAGE = ROOT / "dist/hirc-local-0.1.0.dev0.pyz"
MANIFEST = ROOT / "dist/hirc-local-0.1.0.dev0-manifest.json"
FILES = (
    "implementation/M08_RELEASE_HARDENING_PLAN.md",
    "implementation/README.md",
    "implementation/build_pyz.py",
    "tests/test_package.py",
    "implementation/m08-s003-package-validation-v1-failed.json",
)


def identity(relative: str) -> dict[str, object]:
    body = (ROOT / relative).read_bytes()
    return {"path": relative, "sha256": hashlib.sha256(body).hexdigest(), "bytes": len(body)}


def main() -> int:
    package_stream = io.StringIO()
    package_suite = unittest.defaultTestLoader.discover(str(ROOT / "tests"), pattern="test_package.py")
    package_tests = unittest.TextTestRunner(stream=package_stream, verbosity=2).run(package_suite)
    full_stream = io.StringIO()
    full_suite = unittest.defaultTestLoader.discover(str(ROOT / "tests"))
    full_tests = unittest.TextTestRunner(stream=full_stream, verbosity=1).run(full_suite)

    temp_root = ROOT / "tests/.tmp"
    temp_root.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(dir=temp_root) as directory:
        root = Path(directory)
        first, second = root / "first.pyz", root / "second.pyz"
        one, two = build(first), build(second)
        reproducible = first.read_bytes() == second.read_bytes() and one["sha256"] == two["sha256"]
    package_result = build(PACKAGE, MANIFEST)
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    environment = dict(os.environ); environment.pop("PYTHONPATH", None)
    help_result = subprocess.run([sys.executable, "-B", str(PACKAGE), "--help"], cwd=ROOT.parent, env=environment, text=True, capture_output=True, timeout=30)
    with zipfile.ZipFile(PACKAGE) as archive:
        archive_test = archive.testzip()
        names = archive.namelist()
    checks = {
        "package_tests_pass": package_tests.wasSuccessful(),
        "package_test_count": package_tests.testsRun == 4,
        "full_suite_pass": full_tests.wasSuccessful(),
        "full_suite_test_count": full_tests.testsRun == FULL_SUITE_TESTS,
        "three_expected_release_failures": len(full_tests.expectedFailures) == EXPECTED_RELEASE_FAILURES,
        "two_builds_identical": reproducible,
        "release_package_matches_manifest": package_result["sha256"] == manifest["sha256"] == identity("dist/hirc-local-0.1.0.dev0.pyz")["sha256"],
        "archive_crc_pass": archive_test is None,
        "entrypoint_and_manifest_present": "__main__.py" in names and "hirc-package-manifest.json" in names,
        "runs_without_pythonpath": help_result.returncode == 0 and "ui-snapshot" in help_result.stdout,
        "network_effect_disabled": package_result["network_or_external_effect_enabled"] is False,
        "sensitive_release_held": package_result["sensitive_data_release_allowed"] is False,
    }
    result = {
        "schema": "hirc.m08-s003-validation/1",
        "stone": "M08-S003",
        "status": "PASS_PACKAGE_SCOPE_RELEASE_HELD" if all(checks.values()) else "FAIL",
        "checks": checks,
        "files": [identity(path) for path in FILES]
        + [identity("dist/hirc-local-0.1.0.dev0.pyz"), identity("dist/hirc-local-0.1.0.dev0-manifest.json")],
        "package_test_output": package_stream.getvalue().splitlines(),
        "full_suite_output": full_stream.getvalue().splitlines(),
        "package": package_result,
        "release_holds": [
            "plaintext store and backup: encryption and key-custody design absent",
            "rendered browser, keyboard, screen-reader and human-usability evidence absent",
            "independent security/privacy review and penetration testing absent",
            "long soak, broader fuzzing, power-loss and cross-machine recovery incomplete",
            "protected external head witness for privileged truncation absent",
            "independently verifiable package-manifest signature absent",
            "M03 S014/S015 governance and public milestone closure incomplete"
        ],
        "nonclaim": "Reproducible dependency-free developer package only; not a sensitive-data, production or public release."
    }
    OUTPUT.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps(result, indent=2))
    return 0 if result["status"] == "PASS_PACKAGE_SCOPE_RELEASE_HELD" else 1


if __name__ == "__main__":
    raise SystemExit(main())

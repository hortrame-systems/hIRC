#!/usr/bin/env python3
"""Run executable validators sequentially, then bind their exact result files."""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path

from validation_config import EXPECTED_RELEASE_FAILURES, FULL_SUITE_TESTS


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "implementation/executable-cumulative-validation.json"
VALIDATORS = (
    ("M04-S001", "implementation/validate_m04_s001.py", "implementation/m04-s001-validation.json", {"PASS"}),
    ("M05-S001", "implementation/validate_m05_s001.py", "implementation/m05-s001-validation.json", {"PASS"}),
    ("ALPHA-RED-TEAM", "implementation/validate_alpha_integration_red_team.py", "implementation/alpha-integration-red-team-validation-v1.json", {"PASS"}),
    ("M06-S001", "implementation/validate_m06_s001.py", "implementation/m06-s001-validation.json", {"PASS"}),
    ("M06-S002", "implementation/validate_m06_s002.py", "implementation/m06-s002-validation.json", {"PASS"}),
    ("M06-S003", "implementation/validate_m06_s003.py", "implementation/m06-s003-validation.json", {"PASS"}),
    ("M07-S001", "implementation/validate_m07_s001.py", "implementation/m07-s001-validation.json", {"PASS"}),
    ("M07-S002", "implementation/validate_m07_s002.py", "implementation/m07-s002-validation.json", {"PASS"}),
    ("M07-S003", "implementation/validate_m07_s003.py", "implementation/m07-s003-validation.json", {"PASS"}),
    ("M08-S001", "implementation/validate_m08_s001.py", "implementation/m08-s001-validation.json", {"PASS"}),
    ("M08-S002", "implementation/validate_m08_s002.py", "implementation/m08-s002-validation.json", {"PASS"}),
    ("M08-S003", "implementation/validate_m08_s003.py", "implementation/m08-s003-validation.json", {"PASS_PACKAGE_SCOPE_RELEASE_HELD"}),
    ("M08-S004", "implementation/validate_m08_s004.py", "implementation/m08-s004-validation.json", {"PASS_TOOLING_SCOPE_KEY_CUSTODY_INTEGRATION_HELD"}),
    ("M08-S005", "implementation/validate_m08_s005.py", "implementation/m08-s005-validation.json", {"PASS_TOOLING_SCOPE_RELEASE_KEY_CUSTODY_HELD"}),
    ("M08-S006", "implementation/validate_m08_s006.py", "implementation/m08-s006-validation.json", {"PASS_ENCRYPTED_BACKUP_TOOLING_SCOPE_LIVE_STORAGE_CUSTODY_HELD"}),
    ("M08-S007", "implementation/validate_m08_s007.py", "implementation/m08-s007-validation.json", {"PASS_BOUNDED_LOCAL_SOAK_CRASH_SCOPE"}),
    ("M08-S008", "implementation/validate_m08_s008.py", "implementation/m08-s008-validation.json", {"PASS_LOCAL_INTEGRITY_REPAIR_SCOPE"}),
    ("M08-S009", "implementation/validate_m08_s009.py", "implementation/m08-s009-validation.json", {"PASS_ATOMIC_CREATE_IF_ABSENT_SCOPE"}),
    ("M08-S010", "implementation/validate_m08_s010.py", "implementation/m08-s010-validation.json", {"PASS_BOUNDED_JSON_FILE_INGRESS_SCOPE"}),
    ("M08-S011", "implementation/validate_m08_s011.py", "implementation/m08-s011-validation.json", {"PASS_READ_ONLY_VERIFICATION_SCOPE"}),
    ("M08-S012", "implementation/validate_m08_s012.py", "implementation/m08-s012-validation.json", {"PASS_CANONICAL_JSON_AMBIGUITY_REPAIR_SCOPE"}),
)


def identity(path: str) -> dict:
    body = (ROOT / path).read_bytes()
    return {"path": path, "sha256": hashlib.sha256(body).hexdigest(), "bytes": len(body)}


def main() -> int:
    bind_existing = "--bind-existing" in sys.argv[1:]
    results = []
    for stone, validator, output, accepted in VALIDATORS:
        if not bind_existing:
            completed = subprocess.run(
                [sys.executable, "-B", validator], cwd=ROOT, text=True, capture_output=True
            )
            if completed.returncode != 0:
                print(completed.stdout)
                print(completed.stderr, file=sys.stderr)
                raise SystemExit(completed.returncode)
        value = json.loads((ROOT / output).read_text(encoding="utf-8"))
        status = value.get("status")
        results.append({"stone": stone, "validator": identity(validator), "result": {**identity(output), "status": status}})
        if status not in accepted:
            raise SystemExit(f"{stone} returned unexpected status {status}")
        print(json.dumps({"stone": stone, "status": status, "reused": bind_existing}))
    value = {
        "schema": "hirc.executable-cumulative-validation/1",
        "status": "PASS_WITH_DECLARED_RELEASE_HOLDS",
        "validator_count": len(results),
        "results": results,
        "full_suite_tests": FULL_SUITE_TESTS,
        "expected_release_failures": EXPECTED_RELEASE_FAILURES,
        "binding_mode": "existing_exact_results" if bind_existing else "fresh_sequential_execution",
        "release_holds": [
            "plaintext storage and backup encryption/key custody",
            "rendered accessibility/usability",
            "independent security/privacy and penetration review",
            "broader crash/fuzz/soak/cross-machine recovery",
            "protected external head witness and signed release manifest",
            "M03 S014/S015 governance and public milestone closure"
        ],
        "nonclaim": "Cumulative local executable evidence only; no sensitive-data, production or public release acceptance."
    }
    OUTPUT.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"status": value["status"], "validators": len(results)}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

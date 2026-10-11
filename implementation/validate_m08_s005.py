#!/usr/bin/env python3
"""Reproduce M08-S005 encrypted-key Ed25519 release-signing checks."""

from __future__ import annotations

import hashlib
import io
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from validation_config import EXPECTED_RELEASE_FAILURES, FULL_SUITE_TESTS


ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"src"))
OUTPUT=ROOT/"implementation/m08-s005-validation.json"
NODE=shutil.which("node")
TOOL=ROOT/"implementation/release_sign.mjs"
FILES=("implementation/M08_RELEASE_HARDENING_PLAN.md","implementation/README.md","implementation/release_sign.mjs","tests/test_release_signing.py","dist/hirc-local-0.1.0.dev0-manifest.json")
PASS=b"validation release passphrase\n"


def identity(relative:str)->dict:
    body=(ROOT/relative).read_bytes();return {"path":relative,"sha256":hashlib.sha256(body).hexdigest(),"bytes":len(body)}


def invoke(*args:str,stdin:bytes=b"")->subprocess.CompletedProcess[bytes]:
    if not NODE: raise RuntimeError("Node.js unavailable")
    return subprocess.run([NODE,str(TOOL),*args],input=stdin,capture_output=True,cwd=ROOT,timeout=30)


def main()->int:
    signing_stream=io.StringIO(); signing_suite=unittest.defaultTestLoader.discover(str(ROOT/"tests"),pattern="test_release_signing.py"); signing_tests=unittest.TextTestRunner(stream=signing_stream,verbosity=2).run(signing_suite)
    full_stream=io.StringIO(); full_suite=unittest.defaultTestLoader.discover(str(ROOT/"tests")); full_tests=unittest.TextTestRunner(stream=full_stream,verbosity=1).run(full_suite)
    temp_root=ROOT/"tests/.tmp";temp_root.mkdir(parents=True,exist_ok=True)
    with tempfile.TemporaryDirectory(dir=temp_root) as directory:
        root=Path(directory); private=root/"private.pem"; public=root/"public.pem"; signature=root/"manifest.signature.json"
        generated=invoke("generate","--private",str(private),"--public",str(public),stdin=PASS)
        signed=invoke("sign","--private",str(private),"--manifest",str(ROOT/"dist/hirc-local-0.1.0.dev0-manifest.json"),"--output",str(signature),stdin=PASS)
        verified=invoke("verify","--public",str(public),"--manifest",str(ROOT/"dist/hirc-local-0.1.0.dev0-manifest.json"),"--signature",str(signature))
        envelope=json.loads(signature.read_text()) if signature.exists() else {}
        private_encrypted=private.exists() and b"ENCRYPTED PRIVATE KEY" in private.read_bytes()
    checks={"node_available":NODE is not None,"signing_tests_pass":signing_tests.wasSuccessful(),"signing_test_count":signing_tests.testsRun==6,"full_suite_pass":full_tests.wasSuccessful(),"full_suite_test_count":full_tests.testsRun==FULL_SUITE_TESTS,"three_expected_release_failures":len(full_tests.expectedFailures)==EXPECTED_RELEASE_FAILURES,"ephemeral_generate_sign_verify":generated.returncode==signed.returncode==verified.returncode==0,"private_key_encrypted":private_encrypted,"envelope_has_no_private_material":"private" not in json.dumps(envelope).lower() and "passphrase" not in json.dumps(envelope).lower()}
    result={"schema":"hirc.m08-s005-validation/1","stone":"M08-S005","status":"PASS_TOOLING_SCOPE_RELEASE_KEY_CUSTODY_HELD" if all(checks.values()) else "FAIL","checks":checks,"files":[identity(path) for path in FILES],"signing_test_output":signing_stream.getvalue().splitlines(),"full_suite_output":full_stream.getvalue().splitlines(),"control":{"public_key_fingerprint_sha256":envelope.get("public_key_fingerprint_sha256"),"manifest_sha256":envelope.get("manifest_sha256"),"actual_release_signature_published":False},"surviving_limits":["Only ephemeral test keys were generated; no actual release key or signature was created.","Release-key owner, authorization, OS-vault/HSM custody, escrow, rotation, revocation and publication remain open.","The signed object is exact manifest bytes; independent release review and M03 governance remain required."],"nonclaim":"M08-S005 Ed25519 signing/verification tooling only; not an authorized signed release."}
    OUTPUT.write_text(json.dumps(result,indent=2)+"\n",encoding="utf-8",newline="\n");print(json.dumps(result,indent=2));return 0 if result["status"].startswith("PASS_") else 1


if __name__=="__main__":raise SystemExit(main())

#!/usr/bin/env python3
"""Reproduce M08-S006 authenticated encrypted-backup envelope checks."""

from __future__ import annotations

import hashlib,io,json,shutil,subprocess,sys,tempfile,unittest
from pathlib import Path

from validation_config import EXPECTED_RELEASE_FAILURES, FULL_SUITE_TESTS

ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/"src"));OUTPUT=ROOT/"implementation/m08-s006-validation.json";NODE=shutil.which("node");TOOL=ROOT/"implementation/encrypted_backup.mjs";PASS=b"validation encrypted backup passphrase\n"
FILES=("implementation/M08_RELEASE_HARDENING_PLAN.md","implementation/README.md","implementation/encrypted_backup.mjs","tests/test_encrypted_backup.py","src/hirc/recovery.py")
from hirc.recovery import backup_store
from hirc.store import EventInput,Store

def identity(path:str)->dict:
    body=(ROOT/path).read_bytes();return {"path":path,"sha256":hashlib.sha256(body).hexdigest(),"bytes":len(body)}
def invoke(*args:str)->subprocess.CompletedProcess[bytes]:return subprocess.run([NODE,str(TOOL),*args],input=PASS,capture_output=True,cwd=ROOT,timeout=30)
def main()->int:
    stream=io.StringIO();suite=unittest.defaultTestLoader.discover(str(ROOT/"tests"),pattern="test_encrypted_backup.py");tests=unittest.TextTestRunner(stream=stream,verbosity=2).run(suite)
    full_stream=io.StringIO();full_suite=unittest.defaultTestLoader.discover(str(ROOT/"tests"));full=unittest.TextTestRunner(stream=full_stream,verbosity=1).run(full_suite)
    tmp=ROOT/"tests/.tmp";tmp.mkdir(parents=True,exist_ok=True)
    with tempfile.TemporaryDirectory(dir=tmp) as directory:
        root=Path(directory);store=Store(root/"store.sqlite3");store.initialize();store.append(EventInput(stream_id="note:encrypted",actor_id="actor:validator",event_type="note.recorded",category="EVIDENCE",foundation_version="foundation:1",goal_version="goal:1",privacy_class="privacy:owner",audience="audience:owner",purpose="purpose:encrypted-backup",occurred_at="2026-10-10T00:00:00Z",payload={"note":"encrypted backup"}));plain=root/"verified-backup.sqlite3";encrypted=root/"verified-backup.hircenc";restored=root/"restored.sqlite3";backup=backup_store(store.path,plain);enc=invoke("encrypt","--input",str(plain),"--output",str(encrypted));dec=invoke("decrypt","--input",str(encrypted),"--output",str(restored));restored_state=Store(restored).verify(read_only=True) if restored.exists() else {"valid":False,"head_hash":None};envelope=json.loads(encrypted.read_text()) if encrypted.exists() else {}
    checks={"node_available":NODE is not None,"encrypted_backup_tests_pass":tests.wasSuccessful(),"encrypted_backup_test_count":tests.testsRun==6,"full_suite_pass":full.wasSuccessful(),"full_suite_test_count":full.testsRun==FULL_SUITE_TESTS,"three_expected_release_failures":len(full.expectedFailures)==EXPECTED_RELEASE_FAILURES,"verified_backup_roundtrip":enc.returncode==dec.returncode==0 and restored_state["valid"] and restored_state["head_hash"]==backup["head_hash"],"aead_and_scrypt_declared":envelope.get("cipher")=="AES-256-GCM" and envelope.get("kdf",{}).get("name")=="scrypt","no_key_stored":"key" not in envelope and "passphrase" not in envelope}
    result={"schema":"hirc.m08-s006-validation/1","stone":"M08-S006","status":"PASS_ENCRYPTED_BACKUP_TOOLING_SCOPE_LIVE_STORAGE_CUSTODY_HELD" if all(checks.values()) else "FAIL","checks":checks,"files":[identity(p) for p in FILES],"encrypted_backup_test_output":stream.getvalue().splitlines(),"full_suite_output":full_stream.getvalue().splitlines(),"control":{"source_head":backup["head_hash"],"restored_head":restored_state["head_hash"],"actual_long_term_key_stored":False},"surviving_limits":["Live SQLite remains plaintext; only verified backup bytes are encrypted.","Passphrase/key custody, recovery, rotation, escrow and rate-limited operator UX are not implemented.","AES-GCM/scrypt parameters and tooling require independent cryptographic/security review before release."],"nonclaim":"M08-S006 encrypted-backup tooling only; not encrypted live storage or approved key custody."}
    OUTPUT.write_text(json.dumps(result,indent=2)+"\n",encoding="utf-8",newline="\n");print(json.dumps(result,indent=2));return 0 if result["status"].startswith("PASS_") else 1
if __name__=="__main__":raise SystemExit(main())

from __future__ import annotations

import json
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT=Path(__file__).resolve().parents[1];NODE=shutil.which("node");TOOL=ROOT/"implementation/encrypted_backup.mjs";PASS=b"correct horse battery staple\n"


@unittest.skipUnless(NODE,"Node.js required for encrypted-backup tooling")
class EncryptedBackupTests(unittest.TestCase):
    temporary_root=Path(__file__).parent/".tmp"
    @classmethod
    def setUpClass(cls)->None:cls.temporary_root.mkdir(parents=True,exist_ok=True)
    def invoke(self,*args:str,stdin:bytes=PASS)->subprocess.CompletedProcess[bytes]:return subprocess.run([NODE,str(TOOL),*args],input=stdin,capture_output=True,cwd=ROOT,timeout=30)
    def fixture(self,root:Path)->tuple[Path,Path,Path]:
        source,encrypted,restored=root/"backup.sqlite3",root/"backup.hircenc",root/"restored.sqlite3";source.write_bytes(b"SQLite format 3\x00"+bytes(range(256))*4);return source,encrypted,restored
    def test_roundtrip_exact_bytes(self)->None:
        with tempfile.TemporaryDirectory(dir=self.temporary_root) as directory:
            source,encrypted,restored=self.fixture(Path(directory));self.assertEqual(self.invoke("encrypt","--input",str(source),"--output",str(encrypted)).returncode,0);self.assertEqual(self.invoke("decrypt","--input",str(encrypted),"--output",str(restored)).returncode,0);self.assertEqual(source.read_bytes(),restored.read_bytes())
    def test_wrong_passphrase_is_rejected_without_output(self)->None:
        with tempfile.TemporaryDirectory(dir=self.temporary_root) as directory:
            source,encrypted,restored=self.fixture(Path(directory));self.invoke("encrypt","--input",str(source),"--output",str(encrypted));result=self.invoke("decrypt","--input",str(encrypted),"--output",str(restored),stdin=b"different passphrase value\n");self.assertNotEqual(result.returncode,0);self.assertFalse(restored.exists())
    def test_tampered_ciphertext_is_rejected(self)->None:
        with tempfile.TemporaryDirectory(dir=self.temporary_root) as directory:
            source,encrypted,restored=self.fixture(Path(directory));self.invoke("encrypt","--input",str(source),"--output",str(encrypted));value=json.loads(encrypted.read_text());ciphertext=value["ciphertext_base64"];replacement="A" if ciphertext[0]!="A" else "B";value["ciphertext_base64"]=replacement+ciphertext[1:];encrypted.write_text(json.dumps(value));self.assertNotEqual(self.invoke("decrypt","--input",str(encrypted),"--output",str(restored)).returncode,0);self.assertFalse(restored.exists())
    def test_short_passphrase_is_rejected(self)->None:
        with tempfile.TemporaryDirectory(dir=self.temporary_root) as directory:
            source,encrypted,_=self.fixture(Path(directory));self.assertNotEqual(self.invoke("encrypt","--input",str(source),"--output",str(encrypted),stdin=b"short\n").returncode,0);self.assertFalse(encrypted.exists())
    def test_targets_are_not_overwritten(self)->None:
        with tempfile.TemporaryDirectory(dir=self.temporary_root) as directory:
            source,encrypted,_=self.fixture(Path(directory));encrypted.write_bytes(b"keep");self.assertNotEqual(self.invoke("encrypt","--input",str(source),"--output",str(encrypted)).returncode,0);self.assertEqual(encrypted.read_bytes(),b"keep")
    def test_envelope_contains_no_passphrase_or_plaintext(self)->None:
        with tempfile.TemporaryDirectory(dir=self.temporary_root) as directory:
            source,encrypted,_=self.fixture(Path(directory));self.invoke("encrypt","--input",str(source),"--output",str(encrypted));body=encrypted.read_text();self.assertNotIn("correct horse",body);self.assertNotIn("SQLite format",body);self.assertFalse(json.loads(body).get("key_stored",False))


if __name__=="__main__":unittest.main()

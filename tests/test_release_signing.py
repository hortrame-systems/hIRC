from __future__ import annotations

import json
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
NODE = shutil.which("node")
TOOL = ROOT / "implementation/release_sign.mjs"
PASS = b"correct horse battery staple\n"


@unittest.skipUnless(NODE, "Node.js required for release-signing tooling")
class ReleaseSigningTests(unittest.TestCase):
    temporary_root = Path(__file__).parent / ".tmp"

    @classmethod
    def setUpClass(cls) -> None: cls.temporary_root.mkdir(parents=True, exist_ok=True)

    def invoke(self, *args: str, stdin: bytes = b"") -> subprocess.CompletedProcess[bytes]:
        return subprocess.run([NODE, str(TOOL), *args], input=stdin, capture_output=True, cwd=ROOT, timeout=30)

    def keys(self, root: Path, stem: str = "release") -> tuple[Path, Path]:
        private, public = root / f"{stem}.private.pem", root / f"{stem}.public.pem"
        result = self.invoke("generate", "--private", str(private), "--public", str(public), stdin=PASS)
        self.assertEqual(result.returncode, 0, result.stderr)
        return private, public

    def test_generate_sign_verify_exact_manifest(self) -> None:
        with tempfile.TemporaryDirectory(dir=self.temporary_root) as directory:
            root=Path(directory); private,public=self.keys(root); manifest=root/"manifest.json"; signature=root/"signature.json"; manifest.write_bytes(b'{"artifact":"abc"}\n')
            signed=self.invoke("sign","--private",str(private),"--manifest",str(manifest),"--output",str(signature),stdin=PASS); self.assertEqual(signed.returncode,0,signed.stderr)
            verified=self.invoke("verify","--public",str(public),"--manifest",str(manifest),"--signature",str(signature)); self.assertEqual(verified.returncode,0,verified.stderr); self.assertTrue(json.loads(verified.stdout)["valid"])

    def test_tampered_manifest_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory(dir=self.temporary_root) as directory:
            root=Path(directory); private,public=self.keys(root); manifest=root/"manifest"; signature=root/"sig"; manifest.write_bytes(b"one")
            self.assertEqual(self.invoke("sign","--private",str(private),"--manifest",str(manifest),"--output",str(signature),stdin=PASS).returncode,0); manifest.write_bytes(b"two")
            self.assertNotEqual(self.invoke("verify","--public",str(public),"--manifest",str(manifest),"--signature",str(signature)).returncode,0)

    def test_wrong_public_key_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory(dir=self.temporary_root) as directory:
            root=Path(directory); private,public=self.keys(root,"one"); _,other=self.keys(root,"two"); manifest=root/"manifest"; signature=root/"sig"; manifest.write_bytes(b"manifest")
            self.invoke("sign","--private",str(private),"--manifest",str(manifest),"--output",str(signature),stdin=PASS)
            self.assertNotEqual(self.invoke("verify","--public",str(other),"--manifest",str(manifest),"--signature",str(signature)).returncode,0)

    def test_wrong_passphrase_and_short_generation_passphrase_fail(self) -> None:
        with tempfile.TemporaryDirectory(dir=self.temporary_root) as directory:
            root=Path(directory); private,_=self.keys(root); manifest=root/"manifest"; manifest.write_bytes(b"manifest")
            self.assertNotEqual(self.invoke("sign","--private",str(private),"--manifest",str(manifest),"--output",str(root/"sig"),stdin=b"wrong passphrase value\n").returncode,0)
            self.assertNotEqual(self.invoke("generate","--private",str(root/"short"),"--public",str(root/"short.pub"),stdin=b"short\n").returncode,0)

    def test_targets_are_not_overwritten(self) -> None:
        with tempfile.TemporaryDirectory(dir=self.temporary_root) as directory:
            root=Path(directory); private=root/"key"; private.write_bytes(b"keep")
            result=self.invoke("generate","--private",str(private),"--public",str(root/"pub"),stdin=PASS); self.assertNotEqual(result.returncode,0); self.assertEqual(private.read_bytes(),b"keep")

    def test_signature_envelope_contains_no_private_key_or_passphrase(self) -> None:
        with tempfile.TemporaryDirectory(dir=self.temporary_root) as directory:
            root=Path(directory); private,_=self.keys(root); manifest=root/"manifest"; signature=root/"sig"; manifest.write_bytes(b"manifest"); self.invoke("sign","--private",str(private),"--manifest",str(manifest),"--output",str(signature),stdin=PASS)
            body=signature.read_text(); self.assertNotIn("PRIVATE KEY",body); self.assertNotIn("correct horse",body); self.assertEqual(json.loads(body)["algorithm"],"Ed25519")


if __name__=="__main__": unittest.main()

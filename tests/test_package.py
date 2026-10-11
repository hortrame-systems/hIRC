from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "implementation"))

from build_pyz import build  # noqa: E402


class PackageTests(unittest.TestCase):
    temporary_root = Path(__file__).parent / ".tmp"

    @classmethod
    def setUpClass(cls) -> None:
        cls.temporary_root.mkdir(parents=True, exist_ok=True)

    def run_package(self, package: Path, cwd: Path, *args: str) -> subprocess.CompletedProcess[str]:
        environment = dict(os.environ)
        environment.pop("PYTHONPATH", None)
        return subprocess.run([sys.executable, "-B", str(package), *args], cwd=cwd, env=environment, text=True, capture_output=True, timeout=30)

    def test_two_builds_are_byte_identical(self) -> None:
        with tempfile.TemporaryDirectory(dir=self.temporary_root) as directory:
            first, second = Path(directory) / "first.pyz", Path(directory) / "second.pyz"
            one, two = build(first), build(second)
            self.assertEqual(first.read_bytes(), second.read_bytes())
            self.assertEqual(one["sha256"], two["sha256"])

    def test_archive_has_only_declared_code_and_manifest(self) -> None:
        with tempfile.TemporaryDirectory(dir=self.temporary_root) as directory:
            package = Path(directory) / "hirc.pyz"
            result = build(package)
            with zipfile.ZipFile(package) as archive:
                names = archive.namelist()
                self.assertEqual(names, ["__main__.py", *[f"hirc/{path.name}" for path in sorted((ROOT / 'src/hirc').glob('*.py'), key=lambda value: value.name)], "hirc-package-manifest.json"])
                internal = json.loads(archive.read("hirc-package-manifest.json"))
            self.assertEqual(result["member_count"], len(names))
            self.assertFalse(internal["network_or_external_effect_enabled"])

    def test_package_runs_without_pythonpath_from_unrelated_directory(self) -> None:
        with tempfile.TemporaryDirectory(dir=self.temporary_root) as directory:
            root = Path(directory)
            package = root / "hirc.pyz"
            build(package)
            unrelated = root / "cwd"; unrelated.mkdir()
            result = self.run_package(package, unrelated, "--help")
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("ui-snapshot", result.stdout)
            self.assertIn("outbox-record", result.stdout)

    def test_packaged_cli_executes_local_work_loop(self) -> None:
        with tempfile.TemporaryDirectory(dir=self.temporary_root) as directory:
            root = Path(directory)
            package, database, snapshot = root / "hirc.pyz", root / "hirc.sqlite3", root / "briefing.html"
            build(package)
            init = self.run_package(package, root, "--db", str(database), "init")
            self.assertEqual(init.returncode, 0, init.stderr)
            record = self.run_package(package, root, "--db", str(database), "record", "--stream", "work:package", "--actor", "actor:owner", "--type", "work.created", "--category", "EVIDENCE", "--foundation", "foundation:1", "--goal", "goal:1", "--privacy", "privacy:owner", "--audience", "audience:owner", "--purpose", "purpose:package", "--occurred-at", "2026-10-10T00:00:00Z", "--payload-json", '{"work_id":"work:package","title":"Packaged","owner":"actor:owner","next_action":"Inspect"}')
            self.assertEqual(record.returncode, 0, record.stderr)
            verify = self.run_package(package, root, "--db", str(database), "verify")
            self.assertEqual(verify.returncode, 0, verify.stderr)
            ui = self.run_package(package, root, "--db", str(database), "ui-snapshot", "--output", str(snapshot))
            self.assertEqual(ui.returncode, 0, ui.stderr)
            self.assertTrue(snapshot.is_file())
            self.assertIn("Packaged", snapshot.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()

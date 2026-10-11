#!/usr/bin/env python3
"""Build a deterministic dependency-free hIRC Python zip application."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import tempfile
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FIXED_TIME = (2026, 10, 10, 0, 0, 0)
ENTRYPOINT = b"from hirc.cli import main\nraise SystemExit(main())\n"


def sha256(body: bytes) -> str:
    return hashlib.sha256(body).hexdigest()


def member(name: str, body: bytes) -> tuple[zipfile.ZipInfo, bytes]:
    info = zipfile.ZipInfo(name, FIXED_TIME)
    info.compress_type = zipfile.ZIP_DEFLATED
    info.external_attr = 0o100644 << 16
    info.create_system = 3
    return info, body


def build(output: str | Path, manifest_output: str | Path | None = None) -> dict:
    destination = Path(output)
    sources = []
    members: list[tuple[zipfile.ZipInfo, bytes]] = [member("__main__.py", ENTRYPOINT)]
    for path in sorted((ROOT / "src/hirc").glob("*.py"), key=lambda value: value.name):
        body = path.read_bytes()
        relative = f"hirc/{path.name}"
        sources.append({"path": f"src/{relative}", "sha256": sha256(body), "bytes": len(body)})
        members.append(member(relative, body))
    internal = {
        "schema": "hirc.pyz-source-manifest/1",
        "name": "hirc-local",
        "version": "0.1.0.dev0",
        "python": ">=3.11",
        "entrypoint_sha256": sha256(ENTRYPOINT),
        "sources": sources,
        "network_or_external_effect_enabled": False,
    }
    internal_body = (json.dumps(internal, indent=2, sort_keys=True) + "\n").encode("utf-8")
    members.append(member("hirc-package-manifest.json", internal_body))
    destination.parent.mkdir(parents=True, exist_ok=True)
    handle, temporary_name = tempfile.mkstemp(prefix=f".{destination.name}.", suffix=".tmp", dir=destination.parent)
    os.close(handle)
    temporary = Path(temporary_name)
    try:
        with zipfile.ZipFile(temporary, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
            for info, body in members:
                archive.writestr(info, body, compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)
        with temporary.open("r+b") as stream:
            stream.flush()
            os.fsync(stream.fileno())
        body = temporary.read_bytes()
        os.replace(temporary, destination)
    except BaseException:
        try:
            temporary.unlink()
        except FileNotFoundError:
            pass
        raise
    result = {
        "schema": "hirc.pyz-build/1",
        "artifact": destination.name,
        "sha256": sha256(body),
        "bytes": len(body),
        "member_count": len(members),
        "source_manifest_sha256": sha256(internal_body),
        "reproducible_inputs": {"fixed_zip_time": "2026-10-10T00:00:00Z", "compression": "deflate-9"},
        "network_or_external_effect_enabled": False,
        "sensitive_data_release_allowed": False,
    }
    if manifest_output is not None:
        manifest = Path(manifest_output)
        manifest.parent.mkdir(parents=True, exist_ok=True)
        manifest.write_text(json.dumps({**result, "sources": sources}, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True)
    parser.add_argument("--manifest")
    args = parser.parse_args()
    print(json.dumps(build(args.output, args.manifest), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

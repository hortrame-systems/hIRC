from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LEDGER = ROOT / "review" / "ledger.json"
OUT = ROOT / "review" / "fixtures" / "git-blob-ledger-portability-validation-v1.json"


def sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def main() -> int:
    ledger = json.loads(LEDGER.read_text(encoding="utf-8"))
    rows = []
    seen = set()
    for artifact in ledger["artifacts"]:
        candidates = []
        if "path" in artifact and "sha256" in artifact:
            candidates.append((artifact["id"], artifact["path"], artifact["sha256"], artifact.get("bytes")))
        candidates.extend((artifact["id"], item["path"], item["sha256"], item["bytes"]) for item in artifact.get("members", []))
        for artifact_id, relative, declared_sha, declared_bytes in candidates:
            key = (artifact_id, relative)
            if key in seen:
                continue
            seen.add(key)
            path = ROOT / relative
            if not path.is_file():
                rows.append({"artifact_id": artifact_id, "path": relative, "state": "MISSING_WORKING"})
                continue
            working = path.read_bytes()
            working_match = sha256(working) == declared_sha and (declared_bytes is None or len(working) == declared_bytes)
            try:
                committed = subprocess.check_output(["git", "show", f"HEAD:{relative}"], cwd=ROOT, stderr=subprocess.DEVNULL)
            except subprocess.CalledProcessError:
                state = "LOCAL_SOURCE" if relative.startswith("human_transfer/") and working_match else "MISSING_GIT"
                rows.append({
                    "artifact_id": artifact_id,
                    "path": relative,
                    "state": state,
                    "working_match": working_match,
                    "sha256": declared_sha,
                    "bytes": declared_bytes,
                })
            else:
                rows.append({
                    "artifact_id": artifact_id,
                    "path": relative,
                    "state": "TRACKED",
                    "working_match": working_match,
                    "git_match": sha256(committed) == declared_sha and (declared_bytes is None or len(committed) == declared_bytes),
                })

    tracked_errors = [row for row in rows if row["state"] == "TRACKED" and (not row["working_match"] or not row["git_match"])]
    unexpected_missing = [row for row in rows if row["state"] not in {"TRACKED", "LOCAL_SOURCE"}]
    local_sources = [row for row in rows if row["state"] == "LOCAL_SOURCE"]
    result = {
        "schema": "hirc.git-blob-ledger-portability-validation/1",
        "ledger_path": "review/ledger.json",
        "head": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip(),
        "checked_entries": len(rows),
        "tracked_entries": sum(row["state"] == "TRACKED" for row in rows),
        "local_source_entries": local_sources,
        "tracked_errors": tracked_errors,
        "unexpected_missing": unexpected_missing,
        "all_tracked_working_and_git_blobs_match": not tracked_errors,
        "only_declared_local_sources_absent_from_git": not unexpected_missing,
        "pass": not tracked_errors and not unexpected_missing,
        "claim": "Raw working/Git blob identity against the current artifact ledger. Local human_transfer originals are intentionally not Git/public artifacts. No semantic truth, source authenticity, permission or public-remote receipt is certified.",
    }
    OUT.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0 if result["pass"] else 1


if __name__ == "__main__":
    sys.exit(main())

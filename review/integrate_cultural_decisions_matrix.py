from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_BASE_REF = "75a173eb12dd13afa6805ed51c2c0944e0ec44e7"
MATRIX_RELATIVE = "review/joint-consensus-matrix-draft-v6.json"
MAP = ROOT / "review" / "revision-map-addendum-cultural-commons-v1.json"
DEFAULT_OUTPUT = ROOT / MATRIX_RELATIVE
MAP_ID = "HIRC-REVISION-MAP-CULTURAL-COMMONS-001"


def digest_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def digest(path: Path) -> str:
    return digest_bytes(path.read_bytes())


def git_file(ref: str, relative: str) -> bytes:
    return subprocess.check_output(["git", "show", f"{ref}:{relative}"], cwd=ROOT)


def build(base_ref: str) -> tuple[dict, str]:
    base_bytes = git_file(base_ref, MATRIX_RELATIVE)
    matrix = json.loads(base_bytes.decode("utf-8"))
    cultural = json.loads(MAP.read_text(encoding="utf-8"))
    if any(item["id"] == MAP_ID for item in matrix["source_maps"]):
        raise ValueError("cultural map already integrated in pinned base")

    matrix["source_maps"].append({
        "id": MAP_ID,
        "path": "review/revision-map-addendum-cultural-commons-v1.json",
        "sha256": digest(MAP),
    })
    for requirement in cultural["new_user_requirements"]:
        matrix["requirements"].append({
            "id": requirement["id"],
            "source_map": MAP_ID,
            "title": requirement["title"],
            "source_status": requirement["status"],
            "phase": requirement.get("phase"),
            "acceptance": requirement["acceptance"],
            "intent_refs": cultural["source_intents"],
            "invariant_refs": requirement["invariant_refs"],
            "lucent_position": "AUTHORED_CANDIDATE",
            "waymark_position": "NOT_REVIEWED_RETIRED_NO_PROXY",
            "joint_status": "PENDING_INDEPENDENT_PEER_REVIEW",
            "residual_dissent_or_hold": "No qualified independent permanent peer has reviewed this cultural-information requirement.",
        })
    for change in cultural["changes"]:
        matrix["decisions"].append({
            "id": change["id"],
            "source_map": MAP_ID,
            "targets": change["targets"],
            "proposal": change["change"],
            "basis": change.get("basis", []),
            "lucent_position": "AUTHORED_CANDIDATE",
            "waymark_position": "NOT_REVIEWED_RETIRED_NO_PROXY",
            "joint_status": "PENDING_INDEPENDENT_PEER_REVIEW",
            "joint_rationale": None,
            "residual_dissent_or_hold": "Independent product/security/privacy review and exact artifact/test traces remain required.",
        })

    matrix["open_holds"] = [
        {
            "id": "HOLD-LEGACY-U125-PRICE-LITERAL",
            "status": "OPEN",
            "scope": "pre-existing mechanically collated U125 requirement row",
            "reason": "The preserved U125 row contains a superseded source-map amount. PRICE-01 and U150-C1 carry the owner-corrected USD 42,424,243 annual named-human amount. Do not accept U125 until a separately governed correction reconciles the literal without rewriting peer history.",
        },
        {
            "id": "HOLD-S003-EARLY-REVIEW",
            "status": "OPEN",
            "scope": "DTM-001-DTM-005 matrix integration",
            "reason": "M03-S003 requires an actual independent security/semantic review of S002/S003 before PASS; determinism decisions are not integrated by S006.",
        },
        {
            "id": "HOLD-CULTURAL-PEER-REVIEW",
            "status": "OPEN",
            "scope": "U192-U204 and CIE-001-CIE-012",
            "reason": "WAYMARK is retired and supplied no review of these rows. A qualified consenting permanent peer must review them; historical agreement and retirement metadata are not proxies.",
        },
    ]
    matrix["completion_rule"] = "Every requirement and decision needs an actual qualified independent peer position, one joint status, rationale, residual dissent/hold and final artifact/test trace before whole consensus. Open holds must be closed or explicitly retained by an accepted scope branch."
    matrix["nonclaim"] = "Mechanical preservation plus five bounded historical agreements and newly authored peer-held cultural rows; not whole-packet consensus, source adoption, implementation, legal review, security assurance, cultural benefit or release authority."
    return matrix, digest_bytes(base_bytes)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-ref", default=DEFAULT_BASE_REF)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    output = args.output if args.output.is_absolute() else ROOT / args.output
    payload, base_sha = build(args.base_ref)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({
        "path": str(output),
        "sha256": digest(output),
        "bytes": output.stat().st_size,
        "base_ref": args.base_ref,
        "base_json_sha256": base_sha,
        "requirements": len(payload["requirements"]),
        "decisions": len(payload["decisions"]),
        "open_holds": len(payload["open_holds"]),
    }, indent=2))


if __name__ == "__main__":
    main()

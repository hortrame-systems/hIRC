#!/usr/bin/env python3
"""Validate the outcome-blind metric/evaluator orientation."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/"implementation/orientation/hirc-metric-stage-a-blind-orientation-20261010-v1.md"
PACKET=ROOT/"review/m03-s014-specialist-review-packets-v1.json"
CURRENT=["review/master-structure-addendum-bayesian-trust-v1.md","review/revision-map-addendum-bayesian-trust-v1.json","review/agent-sovereignty-trust-competition-architecture-candidate-v1.md","review/contracts/hirc-bayesian-reliance.candidate.schema.v3.1.json","review/cultural-environment-quality-measures-v1.json","drafts/hirc_requirements_v1_1-draft.json","review/joint-consensus-matrix-draft-v10.json","drafts/hirc_threat_model_v1_0-draft.md"]
FORBIDDEN_MARKERS=["six material findings","seventeen adverse","STAGE_B_CONFIRMS","MTR-A-F01","MTR-B-F01","PASS_LOCAL_REPAIR","waymark-trust-contract-validation","m03-s014-metric-review-response","m03-s014-metric-stage-a-report","m03-s014-metric-stage-b-report"]


def ident(path:Path,display:str)->dict:
    body=path.read_bytes();return {"path":display,"sha256":hashlib.sha256(body).hexdigest(),"bytes":len(body)}


def main()->int:
    parser=argparse.ArgumentParser();parser.add_argument("--output");args=parser.parse_args();text=SOURCE.read_text(encoding="utf-8");packet=json.loads(PACKET.read_text(encoding="utf-8"));lane=next(item for item in packet["lanes"] if item["lane"]=="metric_evaluator")
    row_errors=[]
    for path in CURRENT:
        row=ident(ROOT/path,path);rendered=f"| `{path}` | `{row['sha256']}` | {row['bytes']:,} |"
        if text.count(rendered)!=1:row_errors.append(path)
    forbidden_paths=[item["path"] for item in lane["stage_b_disclosed_evidence"] if item["path"] in text]
    markers=[item for item in FORBIDDEN_MARKERS if item in text]
    missing_questions=[q for q in lane["questions"] if text.count(q)!=1]
    checks=[
        {"name":"exact-current-identity-rows","pass":not row_errors,"observed":row_errors},
        {"name":"no-stage-b-paths","pass":not forbidden_paths,"observed":forbidden_paths},
        {"name":"no-review-outcome-markers","pass":not markers,"observed":markers},
        {"name":"orientation-questions","pass":not missing_questions,"observed":missing_questions},
        {"name":"body-closed-language","pass":all(term in text for term in ("Do not open them","grants no target-body access","before separate admission","outcome-blind orientation metadata")),"observed":"required boundary phrases"},
    ]
    result={"schema":"hirc.m03-s014-metric-blind-orientation-validation/1","status":"PASS" if all(c["pass"] for c in checks) else "FAIL","orientation":ident(SOURCE,"implementation/orientation/hirc-metric-stage-a-blind-orientation-20261010-v1.md"),"checks":checks,"nonclaim":"Deterministic outcome-blind orientation validation only; not body access, review, empirical validation or S014 acceptance."}
    rendered=json.dumps(result,indent=2)+"\n"
    if args.output:(ROOT/args.output).write_text(rendered,encoding="utf-8",newline="\n")
    print(rendered,end="");return 0 if result["status"]=="PASS" else 1


if __name__=="__main__":raise SystemExit(main())

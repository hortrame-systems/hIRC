#!/usr/bin/env python3
"""Validate the metric repair-2 response and exact sources."""

from __future__ import annotations
import argparse,hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];SOURCE=ROOT/"review/m03-s014-metric-review-response-v2.json";RID="HIRC-M03-S014-BAYESIAN-RELIANCE-V3_1-REPAIR-002"
def ident(path:Path)->dict:
    body=path.read_bytes();return {"path":path.relative_to(ROOT).as_posix(),"sha256":hashlib.sha256(body).hexdigest(),"bytes":len(body)}
def main()->int:
    p=argparse.ArgumentParser();p.add_argument("--output");args=p.parse_args();d=json.loads(SOURCE.read_text(encoding="utf-8"));checks=[];errs=[]
    for e in d["sources"]:
        o=ident(ROOT/e["path"])
        if o!=e:errs.append({"expected":e,"observed":o})
    checks.append({"name":"exact-source-frame","pass":not errs,"observed":errs})
    ids={x["id"] for x in d["finding_dispositions"]};checks.append({"name":"all-findings-disposed","pass":ids=={"MTR-A-F01","MTR-A-F02","MTR-A-F03","MTR-A-F04","MTR-A-F05","MTR-A-F06","MTR-B-F01","MTR-R-F01"} and all(x.get("decision") for x in d["finding_dispositions"]),"observed":sorted(ids)})
    v31=json.loads((ROOT/"review/fixtures/bayesian-reliance-v3.1-validation.json").read_text(encoding="utf-8"));matrix=json.loads((ROOT/"review/fixtures/m03-metric-matrix-repair-validation-v2.json").read_text(encoding="utf-8"));event=json.loads((ROOT/"review/fixtures/m03-s014-metric-recheck-write-event-validation-v1.json").read_text(encoding="utf-8"))
    checks.append({"name":"repair-validations","pass":v31.get("status")=="PASS" and v31.get("counts")=={"total":26,"positive":2,"adverse":24} and matrix.get("status")=="PASS" and matrix.get("output",{}).get("path")=="review/joint-consensus-matrix-draft-v10.json" and matrix.get("selected_readback",{}).get("exact_utf8_bytes") is True and event.get("status")=="PASS","observed":{"v3.1":v31.get("status"),"matrix":matrix.get("status"),"event":event.get("status")}})
    req=json.loads((ROOT/"drafts/hirc_requirements_v1_1-draft.json").read_text(encoding="utf-8"));rows={x["id"]:x for x in req["requirements"]};checks.append({"name":"requirement-bindings","pass":all(rows[i].get("dependencies")==[RID] and rows[i].get("acceptance_test_refs") for i in d["controls"]["requirements"]["ids"]),"observed":d["controls"]["requirements"]["ids"]})
    checks.append({"name":"recheck-2-closed","pass":d["id"]==RID and d["state"]=="CONTROLLER_REPAIR_2_PASS_PEER_RECHECK_REQUIRED" and d["recheck_2"]["body_access_granted"] is False and len(d["open_residuals"])>=6 and "S014 closure" in d["nonclaim"],"observed":{"state":d["state"],"residuals":len(d["open_residuals"])}})
    result={"schema":"hirc.m03-s014-metric-repair-response-validation/2","status":"PASS" if all(x["pass"] for x in checks) else "FAIL","response":ident(SOURCE),"checks":checks,"nonclaim":"Deterministic controller repair-2 validation only; not peer recheck-2, runtime/empirical validation or S014 acceptance."};rendered=json.dumps(result,indent=2)+"\n";
    if args.output:(ROOT/args.output).write_text(rendered,encoding="utf-8",newline="\n")
    print(rendered,end="");return 0 if result["status"]=="PASS" else 1
if __name__=="__main__":raise SystemExit(main())

#!/usr/bin/env python3
from __future__ import annotations
import argparse,hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];S=ROOT/"review/m03-s014-metric-review-response-v3.json";RID="HIRC-M03-S014-BAYESIAN-RELIANCE-V3_2-REPAIR-003"
def ident(p:Path)->dict:
 b=p.read_bytes();return {"path":p.relative_to(ROOT).as_posix(),"sha256":hashlib.sha256(b).hexdigest(),"bytes":len(b)}
def main()->int:
 p=argparse.ArgumentParser();p.add_argument("--output");a=p.parse_args();d=json.loads(S.read_text(encoding="utf-8"));errs=[]
 for e in d["sources"]:
  if ident(ROOT/e["path"])!=e:errs.append(e["path"])
 v=json.loads((ROOT/"review/fixtures/bayesian-reliance-v3.2-validation.json").read_text());m=json.loads((ROOT/"review/fixtures/m03-metric-matrix-repair-validation-v2.json").read_text());c=json.loads((ROOT/"review/fixtures/m03-s014-matrix-reviewer-correction-validation-v1.json").read_text());req=json.loads((ROOT/"drafts/hirc_requirements_v1_1-draft.json").read_text());rows={x["id"]:x for x in req["requirements"]}
 checks=[{"name":"sources","pass":not errs,"observed":errs},{"name":"validations","pass":v.get("status")==m.get("status")==c.get("status")=="PASS" and v.get("counts")=={"total":29,"positive":2,"adverse":27},"observed":[v.get("status"),m.get("status"),c.get("status")]},{"name":"requirements","pass":all(rows[i].get("dependencies")==[RID] for i in d["controls"]["requirements"]["ids"]),"observed":d["controls"]["requirements"]["ids"]},{"name":"closed","pass":d["id"]==RID and d["state"]=="CONTROLLER_REPAIR_3_PASS_PEER_RECHECK_REQUIRED" and d["recheck_3"]["body_access_granted"] is False and len(d["open_residuals"])>=5,"observed":d["state"]}]
 result={"schema":"hirc.m03-s014-metric-repair-response-validation/3","status":"PASS" if all(x["pass"] for x in checks) else "FAIL","response":ident(S),"checks":checks,"nonclaim":"Controller repair-3 validation only; not peer recheck-3, runtime/empirical validation or S014 acceptance."};r=json.dumps(result,indent=2)+"\n";
 if a.output:(ROOT/a.output).write_text(r,encoding="utf-8",newline="\n")
 print(r,end="");return 0 if result["status"]=="PASS" else 1
if __name__=="__main__":raise SystemExit(main())

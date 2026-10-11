#!/usr/bin/env python3
"""Validate v3.2 including actual synthetic evidence resolution."""
from __future__ import annotations
import hashlib,json,shutil,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/"review"))
import validate_bayesian_reliance_v3_1 as v31  # noqa:E402
SCHEMA=ROOT/"review/contracts/hirc-bayesian-reliance.candidate.schema.v3.2.json";CASES=ROOT/"review/fixtures/bayesian-reliance-v3.2-cases.json";RESOLVER=ROOT/"review/fixtures/bayesian-reliance-v3.2-evidence-resolver.json";OUTPUT=ROOT/"review/fixtures/bayesian-reliance-v3.2-validation.json"
def ident(p:Path)->dict:
 b=p.read_bytes();return {"path":p.relative_to(ROOT).as_posix(),"sha256":hashlib.sha256(b).hexdigest(),"bytes":len(b)}
def canon(v)->bytes:return json.dumps(v,sort_keys=True,separators=(",",":"),ensure_ascii=False).encode("utf-8")
def structural(r):
 pwsh=shutil.which("pwsh");literal=str(SCHEMA).replace("'","''");cmd=f"$s='{literal}';$b=[Console]::In.ReadToEnd();if(Test-Json -Json $b -SchemaFile $s -ErrorAction SilentlyContinue){{'true'}}else{{'false'}}";x=subprocess.run([pwsh,"-NoProfile","-Command",cmd],input=json.dumps(r),text=True,capture_output=True);return x.returncode==0 and x.stdout.strip().lower()=="true",x.stderr.strip()
def semantic(r,resolver):
 errors=v31.semantic(r);by={x["ref"]:x for x in resolver}
 for item in r.get("reference_closure",[]):
  row=by.get(item.get("ref"))
  if not row:errors.append("reference-evidence-unresolved");continue
  raw=canon(row["payload"])
  if row["locator"]!=item.get("resolver_locator"):errors.append("reference-resolver-locator-mismatch")
  if hashlib.sha256(raw).hexdigest()!=item.get("content_sha256") or row["content_sha256"]!=item.get("content_sha256"):errors.append("reference-content-hash-mismatch")
  if len(raw)!=item.get("content_bytes") or row["content_bytes"]!=item.get("content_bytes"):errors.append("reference-content-bytes-mismatch")
 return sorted(set(errors))
def main()->int:
 f=json.loads(CASES.read_text(encoding="utf-8"));resolver=json.loads(RESOLVER.read_text(encoding="utf-8"))["entries"];rows=[]
 for c in f["cases"]:
  sv,stderr=structural(c["record"]);errs=semantic(c["record"],resolver) if sv else ["STRUCTURAL_REJECTION"];valid=sv and not errs;rows.append({"id":c["id"],"expected_valid":c["expected_valid"],"structural_valid":sv,"semantic_valid":valid,"expectation_pass":valid==c["expected_valid"],"semantic_errors":errs,"input_sha256":v31.canonical(c["record"]),"description":c["description"],"validator_stderr":stderr})
 result={"schema":"hirc.bayesian-reliance-v3.2-validation/1","status":"PASS" if all(x["expectation_pass"] for x in rows) else "FAIL","predecessor_validation":ident(ROOT/"review/fixtures/bayesian-reliance-v3.1-validation.json"),"schema_source":ident(SCHEMA),"case_source":ident(CASES),"resolver_source":ident(RESOLVER),"validator":ident(Path(__file__)),"counts":{"total":len(rows),"positive":sum(x["expected_valid"] for x in rows),"adverse":sum(not x["expected_valid"] for x in rows)},"results":rows,"nonclaim":"Synthetic resolver-backed contract validation; not external truth, empirical/statistical/privacy/runtime/authority validation or permission."};OUTPUT.write_text(json.dumps(result,indent=2)+"\n",encoding="utf-8",newline="\n");print(json.dumps({"status":result["status"],"counts":result["counts"],"failures":[x["id"] for x in rows if not x["expectation_pass"]],"output":ident(OUTPUT)},indent=2));return 0 if result["status"]=="PASS" else 1
if __name__=="__main__":raise SystemExit(main())

#!/usr/bin/env python3
"""Validate Bayesian reliance v3.1 structural and semantic closure."""

from __future__ import annotations

import hashlib,json,shutil,subprocess,sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/"review"))
import validate_bayesian_reliance_v3 as v3  # noqa:E402
SCHEMA=ROOT/"review/contracts/hirc-bayesian-reliance.candidate.schema.v3.1.json";CASES=ROOT/"review/fixtures/bayesian-reliance-v3.1-cases.json";OUTPUT=ROOT/"review/fixtures/bayesian-reliance-v3.1-validation.json"

def ident(path:Path)->dict:
    body=path.read_bytes();return {"path":path.relative_to(ROOT).as_posix(),"sha256":hashlib.sha256(body).hexdigest(),"bytes":len(body)}
def canonical(value)->str:return hashlib.sha256(json.dumps(value,sort_keys=True,separators=(",",":"),ensure_ascii=False).encode("utf-8")).hexdigest()
def structural(record:dict)->tuple[bool,str]:
    pwsh=shutil.which("pwsh");
    if not pwsh:raise RuntimeError("POWERSHELL_7_REQUIRED")
    literal=str(SCHEMA).replace("'","''");command=f"$s='{literal}';$b=[Console]::In.ReadToEnd();if(Test-Json -Json $b -SchemaFile $s -ErrorAction SilentlyContinue){{'true'}}else{{'false'}}"
    run=subprocess.run([pwsh,"-NoProfile","-Command",command],input=json.dumps(record),text=True,capture_output=True,check=False);return run.returncode==0 and run.stdout.strip().lower()=="true",run.stderr.strip()
def semantic(record:dict)->list[str]:
    errors=v3.semantic(record)
    evaluated=v3.moment(record["evaluated_at"])
    required_refs={record["metric"]["definition_verification"]["evidence_ref"],record["metric"]["evaluator_assessment"].get("evidence_ref"),record["prior"]["uncertainty"]["evidence_ref"],record["posterior"]["uncertainty"]["evidence_ref"],record["calibration"]["evidence_ref"],record["drift"]["evidence_ref"],*[x["evidence_ref"] for x in record["model_fit"].values()]}
    required_refs.discard(None);closure=record.get("reference_closure",[]);refs=[x.get("ref") for x in closure];mapping={x.get("ref"):x for x in closure}
    if len(refs)!=len(set(refs)):errors.append("duplicate-reference-closure")
    if not required_refs<=set(refs):errors.append("load-bearing-reference-closure-incomplete")
    if record.get("state")=="ACTIVE_FOR_DECLARED_SCOPE":
        for ref in required_refs:
            item=mapping.get(ref,{})
            if item.get("status")!="PASS":errors.append("active-reference-closure-not-pass")
            try:
                if not v3.moment(item["observed_at"])<=evaluated<=v3.moment(item["valid_until"]):errors.append("active-reference-closure-not-current")
            except (KeyError,TypeError,ValueError):errors.append("active-reference-closure-time-invalid")
        for distribution_name in ("prior","posterior"):
            item=record[distribution_name]["uncertainty"]
            if item.get("status")!="PASS":errors.append("active-uncertainty-not-pass")
            try:
                if not item["lower"]<=item["upper"]:errors.append("uncertainty-interval-inverted")
                if not v3.moment(item["observed_at"])<=evaluated<=v3.moment(item["valid_until"]):errors.append("active-uncertainty-not-current")
            except (KeyError,TypeError,ValueError):errors.append("uncertainty-invalid")
    classes={event["boundary"]["privacy_class"] for event in record.get("evidence",[])};out=record.get("privacy_join",{}).get("output_boundary",{}).get("privacy_class")
    if len(classes)>1 and out!="PROTECTED":errors.append("mixed-privacy-classes-not-protected")
    if len(classes)==1 and out!=next(iter(classes)):errors.append("uniform-privacy-class-not-preserved")
    graph=record.get("evaluation_graph",{})
    for node in graph.get("nodes",[]):
        body={k:v for k,v in node.items() if k!="node_sha256"}
        if node.get("node_sha256")!=canonical(body):errors.append("evaluation-node-hash-mismatch")
    body={k:v for k,v in graph.items() if k!="graph_sha256"}
    if graph.get("graph_sha256")!=canonical(body):errors.append("evaluation-graph-hash-mismatch")
    return sorted(set(errors))
def main()->int:
    fixture=json.loads(CASES.read_text(encoding="utf-8"));rows=[]
    for case in fixture["cases"]:
        sv,stderr=structural(case["record"]);errs=semantic(case["record"]) if sv else ["STRUCTURAL_REJECTION"];valid=sv and not errs
        rows.append({"id":case["id"],"expected_valid":case["expected_valid"],"structural_valid":sv,"semantic_valid":valid,"expectation_pass":valid==case["expected_valid"],"semantic_errors":errs,"input_sha256":canonical(case["record"]),"description":case["description"],"validator_stderr":stderr})
    result={"schema":"hirc.bayesian-reliance-v3.1-validation/1","status":"PASS" if all(x["expectation_pass"] for x in rows) else "FAIL","predecessor_validation":ident(ROOT/"review/fixtures/bayesian-reliance-v3-validation.json"),"schema_source":ident(SCHEMA),"case_source":ident(CASES),"validator":ident(Path(__file__)),"counts":{"total":len(rows),"positive":sum(x["expected_valid"] for x in rows),"adverse":sum(not x["expected_valid"] for x in rows)},"results":rows,"nonclaim":"Synthetic candidate-contract validation only; not empirical/statistical/privacy/runtime/authority validation or permission."}
    OUTPUT.write_text(json.dumps(result,indent=2)+"\n",encoding="utf-8",newline="\n");print(json.dumps({"status":result["status"],"counts":result["counts"],"failures":[x["id"] for x in rows if not x["expectation_pass"]],"output":ident(OUTPUT)},indent=2));return 0 if result["status"]=="PASS" else 1
if __name__=="__main__":raise SystemExit(main())

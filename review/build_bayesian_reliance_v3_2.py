#!/usr/bin/env python3
"""Build v3.2 with actual synthetic reference-resolution evidence."""
from __future__ import annotations
import copy,hashlib,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/"review"))
import build_bayesian_reliance_v3_1 as v31  # noqa:E402
SCHEMA=ROOT/"review/contracts/hirc-bayesian-reliance.candidate.schema.v3.2.json";CASES=ROOT/"review/fixtures/bayesian-reliance-v3.2-cases.json";RESOLVER=ROOT/"review/fixtures/bayesian-reliance-v3.2-evidence-resolver.json"
def canon(v)->bytes:return json.dumps(v,sort_keys=True,separators=(",",":"),ensure_ascii=False).encode("utf-8")
def ident(p:Path)->dict:
 b=p.read_bytes();return {"path":p.relative_to(ROOT).as_posix(),"sha256":hashlib.sha256(b).hexdigest(),"bytes":len(b)}
def resolver_rows(record:dict)->list[dict]:
 rows=[]
 for item in record["reference_closure"]:
  ref=item["ref"];payload={"schema":"synthetic.verification-evidence/1","ref":ref,"observed_result":"PASS","basis":"bounded synthetic evidence for resolver testing"};raw=canon(payload);rows.append({"ref":ref,"locator":"resolver:"+ref,"content_sha256":hashlib.sha256(raw).hexdigest(),"content_bytes":len(raw),"payload":payload})
 return rows
def upgrade(record:dict,resolver:list[dict])->dict:
 r=copy.deepcopy(record);r["schema_version"]="hirc.bayesian-reliance/3.2-candidate";by={x["ref"]:x for x in resolver}
 for item in r["reference_closure"]:
  row=by[item["ref"]];item["content_sha256"]=row["content_sha256"];item["content_bytes"]=row["content_bytes"];item["resolver_locator"]=row["locator"];item.pop("sha256",None)
 return r
def main()->int:
 base=v31.upgrade(v31.v3.base_record());resolver=resolver_rows(base);RESOLVER.write_text(json.dumps({"schema":"hirc.synthetic-evidence-resolver/1","entries":resolver},indent=2)+"\n",encoding="utf-8",newline="\n")
 schema=v31.schema();schema["$id"]="urn:hirc:candidate:bayesian-reliance:3.2";schema["title"]="hIRC candidate Bayesian reliance posterior with externally resolved evidence closure";schema["properties"]["schema_version"]={"const":"hirc.bayesian-reliance/3.2-candidate"};entry=schema["properties"]["reference_closure"]["items"];entry["required"]=["ref","content_sha256","content_bytes","resolver_locator","status","observed_at","valid_until","evidence_ref"];entry["properties"].pop("sha256",None);entry["properties"].update({"content_sha256":{"$ref":"#/$defs/sha256"},"content_bytes":{"type":"integer","minimum":1},"resolver_locator":{"type":"string","minLength":1}});SCHEMA.write_text(json.dumps(schema,indent=2)+"\n",encoding="utf-8",newline="\n")
 cases=[]
 for row in v31.cases():cases.append({**row,"record":upgrade(row["record"],resolver)})
 def adverse(i,desc,mut):
  r=upgrade(v31.upgrade(v31.v3.base_record()),resolver);mut(r);cases.append({"id":i,"expected_valid":False,"description":desc,"record":r})
 adverse("BR32-N25","Closure names an unresolved evidence reference",lambda r:(r["metric"]["evaluator_assessment"].__setitem__("evidence_ref","FAKE:UNRESOLVED"),r["reference_closure"][1].__setitem__("ref","FAKE:UNRESOLVED"),r["reference_closure"][1].__setitem__("resolver_locator","resolver:FAKE:UNRESOLVED")))
 adverse("BR32-N26","Closure content digest does not match resolved evidence",lambda r:r["reference_closure"][0].__setitem__("content_sha256","0"*64))
 adverse("BR32-N27","Closure byte count does not match resolved evidence",lambda r:r["reference_closure"][0].__setitem__("content_bytes",1))
 CASES.write_text(json.dumps({"schema":"hirc.bayesian-reliance-v3.2-cases/1","predecessor":ident(v31.SCHEMA_PATH),"resolver":ident(RESOLVER),"scope":"Synthetic resolver-backed candidate controls only; no real identity, metric, permission or effect.","cases":cases},indent=2)+"\n",encoding="utf-8",newline="\n")
 print(json.dumps({"status":"BUILT","schema":ident(SCHEMA),"cases":ident(CASES),"resolver":ident(RESOLVER),"counts":{"total":len(cases),"positive":sum(x["expected_valid"] for x in cases),"adverse":sum(not x["expected_valid"] for x in cases)}},indent=2));return 0
if __name__=="__main__":raise SystemExit(main())

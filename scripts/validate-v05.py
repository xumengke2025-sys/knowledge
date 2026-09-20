import json,pathlib,hashlib
R=pathlib.Path(__file__).resolve().parents[1]
IDS=["embodied-intelligence","commercial-space-satcom","low-altitude-economy","wide-bandgap-semiconductor","solid-state-battery","synthetic-biology-biomanufacturing","industrial-machine-tools","smart-sensors-mems"]
REQUIRED_RUNTIME={"moss_company_search","moss_company_profile","moss_company_get_annual_reports","moss_company_get_patents","moss_company_get_listed_financial_data","moss_company_get_news","moss_company_get_certificates_v2","moss_industry_search_nodes","moss_industry_get_chain"}
FORBIDDEN={"moss_company_get_contact","create_task","create_opportunity","transition_opportunity","claim_opportunity","reassign_opportunity","push_to_dept"}
def load(p): return json.loads(p.read_text(encoding="utf-8"))
def h(t): return hashlib.sha256(t.encode()).hexdigest()
for iid in IDS:
 d=R/"industries"/iid
 bench=load(d/"benchmark.json"); radar=load(d/"radar-sources.json"); pack=load(d/"expert-pack.json")
 play=(d/"company-assessment-playbook.md").read_text(encoding="utf-8")
 assert bench["version"] in ["0.5.0","0.5.1","0.5.2"] and len(bench["dimensions"])>=7
 assert all(x["metrics"] for x in bench["dimensions"])
 assert radar["version"]=="0.5.0" and len(radar["signal_types"])>=8
 assert "moss_company_get_patents" in play and "benchmark" in play.lower()
 tools=set(pack["tools_whitelist"]); assert REQUIRED_RUNTIME<=tools,(iid,REQUIRED_RUNTIME-tools); assert not (FORBIDDEN & tools)
 assert any("技术评价基准" in x for x in pack["knowledge_scope"])
 assert any("企业快速研判手册" in x for x in pack["knowledge_scope"])
 assert set(pack["expert_profile"]["tools"])==tools
bundle=load(R/"firmbuddy/import-bundle.json");assert str(bundle["version"]).startswith(("0.5.","0.6."))
assert len(bundle["documents"])==52,(len(bundle["documents"]),len(bundle["equipments"]))
assert len(bundle["equipments"])==52
docs={d["logical_key"]:d for d in bundle["documents"]}; eq={e["logical_key"]:e for e in bundle["equipments"]}
for iid in IDS:
 for suffix,typ in [("benchmark","core_spec"),("playbook","supplement")]:
  k=f"{iid}:{suffix}";assert k in docs and k in eq
  assert h(docs[k]["text"])==docs[k]["sha256"]
  assert eq[k]["type"]==typ and eq[k]["slot"]==typ
runtime=load(R/"firmbuddy/runtime-company-intelligence.json")
assert REQUIRED_RUNTIME<=set(runtime["read_only_tools"])
cov=load(R/"coverage-v0.5.json");assert cov["documents"]==52 and cov["equipments"]==52 and cov["experts"]==8
print("PASS",json.dumps({"industries":8,"documents":52,"equipments":52,"runtime_tools":len(runtime["read_only_tools"])},ensure_ascii=False))

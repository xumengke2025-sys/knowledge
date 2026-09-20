import json,pathlib
R=pathlib.Path(__file__).resolve().parents[1]
IDS=["embodied-intelligence","commercial-space-satcom","low-altitude-economy","wide-bandgap-semiconductor","solid-state-battery","synthetic-biology-biomanufacturing","industrial-machine-tools","smart-sensors-mems"]
def load(p):return json.loads(p.read_text(encoding="utf-8"))
for iid in IDS:
 d=R/"industries"/iid;b=load(d/"benchmark.json");f=load(d/"financial-technology-signals.json")
 assert b.get("version") in ["0.5.1","0.5.2"] and len(b.get("maturity_model",[]))>=6
 assert len({x["stage_id"] for x in b["maturity_model"]})==len(b["maturity_model"])
 assert all(x.get("evidence_required") and x.get("anti_inference") for x in b["maturity_model"])
 assert f.get("version") in ["0.5.1","0.5.2"] and len(f.get("signals",[]))>=6
 assert all(x.get("fields") and x.get("interpretation") and x.get("pitfall") for x in f["signals"])
 text=(d/"company-assessment-playbook.md").read_text(encoding="utf-8")
 assert "行业特定成熟度模型" in text and "财务—技术交叉信号" in text
bundle=load(R/"firmbuddy/import-bundle.json")
assert str(bundle["version"]).startswith(("0.5.","0.6."))
for iid in IDS:
 b=next(x for x in bundle["documents"] if x["logical_key"]==iid+":benchmark")
 p=next(x for x in bundle["documents"] if x["logical_key"]==iid+":playbook")
 assert "行业特定成熟度模型" in b["text"]
 assert "财务—技术交叉信号" in p["text"]
print("PASS",json.dumps({"industries":8,"maturity_models":8,"financial_signal_models":8},ensure_ascii=False))

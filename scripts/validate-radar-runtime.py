import json,pathlib,hashlib
R=pathlib.Path(__file__).resolve().parents[1]
IDS=["embodied-intelligence","commercial-space-satcom","low-altitude-economy","wide-bandgap-semiconductor","solid-state-battery","synthetic-biology-biomanufacturing","industrial-machine-tools","smart-sensors-mems"]
def load(p):return json.loads(p.read_text(encoding="utf-8"))
def h(t):return hashlib.sha256(t.encode()).hexdigest()
bundle=load(R/"firmbuddy/import-bundle.json");assert bundle["version"]=="0.5.2"
for iid in IDS:
 pack=load(R/"industries"/iid/"expert-pack.json")
 assert "get_industry_radar" in pack["tools_whitelist"]
 assert pack.get("radar_mode",{}).get("status")=="candidate_only"
 assert "get_industry_radar" in pack["expert_profile"]["tools"]
 text=(R/"industries"/iid/"company-assessment-playbook.md").read_text(encoding="utf-8")
 assert "## 行业最新动向 Radar" in text and "candidate" in text
 doc=next(x for x in bundle["documents"] if x["logical_key"]==iid+":playbook")
 assert doc["text"]==text and h(text)==doc["sha256"]
plugin=(R/"firmbuddy/technology-intelligence/plugin.mjs").read_text(encoding="utf-8")
assert "get_industry_radar" in plugin and "radar.json" in plugin
manifest=load(R/"firmbuddy/technology-intelligence/plugin.json");assert manifest["version"]=="0.5.2"
print("PASS",json.dumps({"experts":8,"radar_tool":"get_industry_radar","bundle_version":"0.5.2"},ensure_ascii=False))

import json, pathlib, hashlib, re
R=pathlib.Path(__file__).resolve().parents[1]
AS_OF="2026-09-20"
INDUSTRIES={
"embodied-intelligence":"具身智能与人形机器人",
"commercial-space-satcom":"商业航天与卫星互联网",
"low-altitude-economy":"低空经济",
"wide-bandgap-semiconductor":"第三代/宽禁带半导体",
"solid-state-battery":"固态电池与下一代电池材料",
"synthetic-biology-biomanufacturing":"合成生物学与生物制造",
"industrial-machine-tools":"工业母机与高端数控",
"smart-sensors-mems":"高端智能传感器与MEMS",
}
def load(p): return json.loads(p.read_text(encoding="utf-8"))
def dump(p,x): p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
def sha(t): return hashlib.sha256(t.encode()).hexdigest()
bundle=load(R/"firmbuddy/import-bundle.json")
bundle["version"]="0.4.0"; bundle["as_of"]=AS_OF
bundle["space"]["description"]="先进科技产业技术、公司证据、学术机制与专利导航；阅读、来源和覆盖限制逐项标明。"
# idempotently replace v0.4 academic entries
bundle["documents"]=[d for d in bundle["documents"] if not d["logical_key"].endswith(":academic")]
bundle["equipments"]=[e for e in bundle["equipments"] if not e["logical_key"].endswith(":academic")]
for iid,name in INDUSTRIES.items():
    text=(R/"industries"/iid/"research/expert-knowledge.md").read_text(encoding="utf-8")
    key=f"{iid}:academic"
    bundle["documents"].append({
        "logical_key":key,"industry_id":iid,"title":f"{name}｜学术机制与研究证据",
        "sourceType":"research","text":text,"sha256":sha(text),
        "tags":[iid,"academic","mechanism","research"],"space_key":"technology-intelligence"
    })
    bundle["equipments"].append({
        "logical_key":key,"name":f"{name}｜学术机制与研究证据","type":"research","slot":"research",
        "document_keys":[key],"expert_key":f"industry-{iid}",
        "applicableBusinessDomains":["industry_research"],"applicableExpertCategories":["行业研究系列"],
        "exportPolicy":"excerpt"
    })
    packp=R/"industries"/iid/"expert-pack.json"
    pack=load(packp)
    scope=pack.setdefault("knowledge_scope",[])
    academic_name=f"{name}｜学术机制与研究证据"
    if academic_name not in scope: scope.append(academic_name)
    dump(packp,pack)
dump(R/"firmbuddy/import-bundle.json",bundle)
# validate-upgrade expects the old document count; update only that guard.
vp=R/"scripts/validate-upgrade.py"
s=vp.read_text(encoding="utf-8")
s2=re.sub(r"assert len\(keys\)==len\(bundle\['documents'\]\)==\d+","assert len(keys)==len(bundle['documents'])==36",s)
if s2==s and "==36" not in s: raise SystemExit("validate-upgrade document-count guard not found")
vp.write_text(s2,encoding="utf-8")
# README: add current academic upgrade note without destroying Codex content
rp=R/"README.md"; txt=rp.read_text(encoding="utf-8")
marker="## v0.4 学术装备层"
block="""## v0.4 学术装备层\n\n2026-09-20 新增 8 行业学术机制知识：精选论文索引、机制卡、文献地图、前沿主题、学术试炼题，并以独立 `research` Knowledge Equipment 绑定到对应行业专家。论文不替代上市公司披露；详见 `ACADEMIC-GOVERNANCE.md` 与 `QUALITY-V0.4.md`。\n\n"""
if marker not in txt:
    if txt.startswith("#"):
        pos=txt.find("\n")+1
        txt=txt[:pos]+"\n"+block+txt[pos:]
    else: txt=block+txt
rp.write_text(txt,encoding="utf-8")
print("academic v0.4 applied",len(bundle["documents"]),len(bundle["equipments"]))

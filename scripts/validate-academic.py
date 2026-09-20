import json,pathlib,hashlib
R=pathlib.Path(__file__).resolve().parents[1]
IDS=["embodied-intelligence","commercial-space-satcom","low-altitude-economy","wide-bandgap-semiconductor","solid-state-battery","synthetic-biology-biomanufacturing","industrial-machine-tools","smart-sensors-mems"]
def load(p): return json.loads(p.read_text(encoding="utf-8"))
def jsonl(p): return [json.loads(x) for x in p.read_text(encoding="utf-8").splitlines() if x.strip()]
total_papers=total_mechs=reviewed=0
global_papers=set()
for iid in IDS:
    d=R/"industries"/iid
    nodes={x["id"] for x in load(d/"taxonomy.json")["nodes"]}
    papers=jsonl(d/"research/academic-papers.jsonl"); mechs=jsonl(d/"research/mechanisms.jsonl")
    lit=load(d/"research/literature-map.json"); fronts=load(d/"research/frontier-topics.json")
    evals=jsonl(d/"research/evaluation-academic.jsonl"); text=(d/"research/expert-knowledge.md").read_text(encoding="utf-8")
    assert len(papers)>=7,(iid,"papers",len(papers))
    assert len(mechs)>=6,(iid,"mechanisms",len(mechs))
    assert len(evals)==len(mechs)
    pids={p["id"] for p in papers}; assert len(pids)==len(papers)
    assert not (pids & global_papers); global_papers |= pids
    for p in papers:
        assert p["reading_status"] in ["metadata_only","abstract_reviewed","sections_reviewed","full_text_reviewed"]
        assert set(p["node_ids"])<=nodes,(iid,p["id"],set(p["node_ids"])-nodes)
        if p["reading_status"]!="metadata_only":
            assert p["summary"] and p["limitations"]
        assert p["id"] in text
    mids={m["id"] for m in mechs}; assert len(mids)==len(mechs)
    for m in mechs:
        assert set(m["node_ids"])<=nodes,(iid,m["id"],set(m["node_ids"])-nodes)
        assert set(m["support_paper_ids"])<=pids,(iid,m["id"])
        assert m["id"] in text and m["false_inference"] in text
    assert set(lit["mechanism_to_papers"])==mids
    assert len(fronts["topics"])==len(mechs)
    pack=load(d/"expert-pack.json")
    assert any("学术机制与研究证据" in x for x in pack.get("knowledge_scope",[])),iid
    total_papers+=len(papers); total_mechs+=len(mechs); reviewed+=sum(p["reading_status"]!="metadata_only" for p in papers)
bundle=load(R/"firmbuddy/import-bundle.json")
assert bundle["version"] in ["0.4.0","0.5.0","0.5.1","0.5.2"]
assert len(bundle["documents"])>=36 and len(bundle["equipments"])>=36
docs={d["logical_key"]:d for d in bundle["documents"]}
eq={e["logical_key"]:e for e in bundle["equipments"]}
for iid in IDS:
    key=f"{iid}:academic"; assert key in docs and key in eq
    d=docs[key]; assert d["sourceType"]=="research"
    assert hashlib.sha256(d["text"].encode()).hexdigest()==d["sha256"]
    e=eq[key]; assert e["type"]=="research" and e["slot"]=="research" and e["document_keys"]==[key]
    assert e["expert_key"]==f"industry-{iid}"
cat=load(R/"academic-catalog.json")
assert sum(x["papers"] for x in cat["industries"])==total_papers
assert sum(x["mechanisms"] for x in cat["industries"])==total_mechs
print("PASS",json.dumps({"papers":total_papers,"reviewed_papers":reviewed,"mechanisms":total_mechs,"academic_equipments":8},ensure_ascii=False))

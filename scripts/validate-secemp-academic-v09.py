#!/usr/bin/env python3
import hashlib, json, pathlib

R=pathlib.Path(__file__).resolve().parents[1]
mf=json.loads((R/"sources/secemp-arxiv/section-reviewed-v09.json").read_text(encoding="utf-8"))
assert mf["version"]=="0.9.0"
by_ind={}
for row in mf["papers"]:
    by_ind.setdefault(row["industry_id"],[]).append(row)
assert len(mf["papers"])==8
assert all(len(v)==1 for v in by_ind.values())

def jsonl(p):
    return [json.loads(x) for x in p.read_text(encoding="utf-8").splitlines() if x.strip()]

for iid, rows in by_ind.items():
    research=R/"industries"/iid/"research"
    papers={p["id"]:p for p in jsonl(research/"academic-papers.jsonl")}
    notes={p["id"]:p for p in jsonl(research/"paper-section-notes.jsonl")}
    evidence={p["paper_id"]:p for p in jsonl(research/"paper-evidence-candidates.jsonl")}
    expert=(research/"expert-knowledge.md").read_text(encoding="utf-8")
    for row in rows:
        p=papers[row["id"]]
        assert p["reading_status"]=="sections_reviewed"
        sr=p["section_review"]
        assert sr["secemp_text_sha256"]==row["secemp_text_sha256"]
        assert evidence[row["paper_id"]]["source_text_sha256"]==row["secemp_text_sha256"]
        assert len(sr["reviewed_sections"])>=3
        assert sr["method_note"] and sr["experiment_note"]
        assert sr["metrics"] and sr["key_findings"] and sr["limitations"]
        assert sr["expert_questions"] and sr["cannot_infer"]
        assert notes[row["id"]]["paper_id"]==row["paper_id"]
        assert row["id"] in expert and "SecEmp 深读证据卡" in expert
        assert row["secemp_text_sha256"] in expert

catalog=json.loads((R/"academic-catalog.json").read_text(encoding="utf-8"))
assert catalog["version"]=="0.9.0"
assert len(catalog["industries"])==8
assert sum(x["secemp_section_reviewed_papers"] for x in catalog["industries"])==8
assert all(x["secemp_section_reviewed_papers"]==1 for x in catalog["industries"])

bundle=json.loads((R/"firmbuddy/import-bundle.json").read_text(encoding="utf-8"))
docs={d["logical_key"]:d for d in bundle["documents"]}
for iid in by_ind:
    key=f"{iid}:academic"
    text=(R/"industries"/iid/"research"/"expert-knowledge.md").read_text(encoding="utf-8")
    assert docs[key]["text"]==text
    assert docs[key]["sha256"]==hashlib.sha256(text.encode()).hexdigest()
    assert "academic-v0.9" in docs[key].get("tags",[])
    assert "sections-reviewed" in docs[key].get("tags",[])

print(json.dumps({"status":"PASS","version":"0.9.0","section_reviewed_papers":8},ensure_ascii=False))

#!/usr/bin/env python3
import hashlib
import json
import pathlib

R = pathlib.Path(__file__).resolve().parents[1]
REVIEW = json.loads((R / "sources/secemp-arxiv/reviewed-v08.json").read_text(encoding="utf-8"))
V09 = R / "sources/secemp-arxiv/section-reviewed-v09.json"
V09_IDS = set()
if V09.exists():
    v09 = json.loads(V09.read_text(encoding="utf-8"))
    V09_IDS = {x["id"] for x in v09.get("papers", [])}
IDS = list(REVIEW["industries"])

def jsonl(path):
    return [json.loads(x) for x in path.read_text(encoding="utf-8").splitlines() if x.strip()]

assert REVIEW["version"] == "0.8.0"
assert REVIEW["source_dataset"] == "secemp9/arxiv-complete"

reviewed_papers = 0
reviewed_mechanisms = 0
for iid in IDS:
    research = R / "industries" / iid / "research"
    papers = {p["id"]: p for p in jsonl(research / "academic-papers.jsonl")}
    mechs = {m["id"]: m for m in jsonl(research / "mechanisms.jsonl")}
    expert = (research / "expert-knowledge.md").read_text(encoding="utf-8")

    additions = REVIEW["industries"][iid]
    assert len(additions["papers"]) == 2, iid
    assert len(additions["mechanisms"]) == 1, iid

    for src in additions["papers"]:
        p = papers[src["id"]]
        for k, v in src.items():
            if k == "reading_status" and src["id"] in V09_IDS:
                assert p.get(k) in {"abstract_reviewed", "sections_reviewed"}, (iid, src["id"], "invalid review-depth upgrade")
            else:
                assert p.get(k) == v, (iid, src["id"], k, "v0.8 field drift")
        if src["id"] in V09_IDS:
            assert p["reading_status"] == "sections_reviewed", (iid, p["id"], "v0.9 section review missing")
        else:
            assert p["reading_status"] == "abstract_reviewed", (iid, p["id"], "unexpected review-depth change")
        assert p["source_dataset"] == "secemp9/arxiv-complete"
        assert p["secemp_paper_text_available"] is True
        assert p["summary"] and p["limitations"]
        assert p["id"] in expert
        assert "full_text_reviewed" not in json.dumps(p, ensure_ascii=False)
        reviewed_papers += 1

    for src in additions["mechanisms"]:
        m = mechs[src["id"]]
        assert m == src, (iid, src["id"], "stable mechanism differs from reviewed manifest")
        assert len(m["support_paper_ids"]) >= 2, (iid, m["id"], "mechanism needs multi-paper support")
        assert all(pid in {p["id"] for p in additions["papers"]} for pid in m["support_paper_ids"])
        assert m["id"] in expert and m["false_inference"] in expert
        reviewed_mechanisms += 1

catalog = json.loads((R / "academic-catalog.json").read_text(encoding="utf-8"))
assert catalog["version"] in {"0.8.0", "0.9.0"}
assert catalog["as_of"] == "2026-09-22"
assert len(catalog["industries"]) == 8
assert sum(x["secemp_reviewed_papers"] for x in catalog["industries"]) == reviewed_papers
assert all(x["secemp_reviewed_papers"] == 2 for x in catalog["industries"])

bundle = json.loads((R / "firmbuddy/import-bundle.json").read_text(encoding="utf-8"))
docs = {d["logical_key"]: d for d in bundle["documents"]}
for iid in IDS:
    key = f"{iid}:academic"
    doc = docs[key]
    text = (R / "industries" / iid / "research" / "expert-knowledge.md").read_text(encoding="utf-8")
    assert doc["text"] == text, (iid, "FirmBuddy academic document drift")
    assert doc["sha256"] == hashlib.sha256(text.encode()).hexdigest()
    assert "secemp" in doc.get("tags", [])
    assert "academic-v0.8" in doc.get("tags", [])

print(json.dumps({
    "status": "PASS",
    "version": REVIEW["version"],
    "secemp_reviewed_papers": reviewed_papers,
    "new_mechanisms": reviewed_mechanisms,
    "catalog_papers": sum(x["papers"] for x in catalog["industries"]),
    "catalog_mechanisms": sum(x["mechanisms"] for x in catalog["industries"]),
}, ensure_ascii=False))

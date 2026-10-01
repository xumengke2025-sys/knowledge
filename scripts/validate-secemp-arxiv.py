#!/usr/bin/env python3
import json
import pathlib

R = pathlib.Path(__file__).resolve().parents[1]
IDS = [
    "embodied-intelligence",
    "commercial-space-satcom",
    "low-altitude-economy",
    "wide-bandgap-semiconductor",
    "solid-state-battery",
    "synthetic-biology-biomanufacturing",
    "industrial-machine-tools",
    "smart-sensors-mems",
]

def load(path):
    return json.loads(path.read_text(encoding="utf-8"))

cfg = load(R / "sources/secemp-arxiv/source-config.json")
assert cfg["dataset"] == "secemp9/arxiv-complete"
assert cfg["snapshot"]["metadata"] == "2026-08-30"
assert cfg["snapshot"]["files"] == "2026-09-05"
assert cfg["configs"]["metadata"]["rows"] == 3148796
assert cfg["configs"]["paper_text"]["papers"] == 2856227
assert cfg["policy"]["commit_raw_full_text"] is False
assert cfg["policy"]["auto_promote_candidates"] is False

for iid in IDS:
    d = R / "industries" / iid
    taxonomy = load(d / "taxonomy.json")
    nodes = {x["id"] for x in taxonomy["nodes"]}
    pack = load(d / "research/secemp-query-pack.json")
    assert pack["version"] == "0.7.0", iid
    assert pack["industry_id"] == iid, iid
    assert pack["source_dataset"] == "secemp9/arxiv-complete", iid
    assert pack["min_score"] >= 3, iid
    assert len(pack["term_groups"]) >= 4, iid
    all_terms = []
    referenced_nodes = set()
    for g in pack["term_groups"]:
        assert g["node_ids"], (iid, g)
        referenced_nodes |= set(g["node_ids"])
        assert set(g["node_ids"]) <= nodes, (iid, set(g["node_ids"]) - nodes)
        assert len(g["terms"]) >= 2, (iid, g)
        for t in g["terms"]:
            term = t if isinstance(t, str) else t["term"]
            assert term.strip() and len(term.strip()) >= 3
            all_terms.append(term.strip().lower())
    assert len(all_terms) == len(set(all_terms)), (iid, "duplicate terms")
    assert referenced_nodes, iid

# Generated candidate pools, when present, must remain review-only and map to taxonomy.
for iid in IDS:
    p = R / "industries" / iid / "research/arxiv-candidates.jsonl"
    if not p.exists():
        continue
    nodes = {x["id"] for x in load(R / "industries" / iid / "taxonomy.json")["nodes"]}
    for line_no, line in enumerate(p.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        row = json.loads(line)
        mapped = set(row.get("taxonomy_node_ids") or [])
        assert mapped, (iid, line_no, "candidate_without_taxonomy_node")
        assert mapped <= nodes, (iid, line_no, mapped - nodes)
        assert row.get("verification_status") == "candidate", (iid, line_no)
        assert row.get("reading_status") == "metadata_only", (iid, line_no)
        assert row.get("promote_to_stable_knowledge") is False, (iid, line_no)

for p in R.rglob("*"):
    if not p.is_file() or ".git" in p.parts or ".cache" in p.parts:
        continue
    rel = p.relative_to(R).as_posix()
    if rel.endswith("paper-text.jsonl") or "/paper-text-cache/" in rel:
        raise AssertionError(f"raw paper_text must not be committed: {rel}")

print(json.dumps({"status": "PASS", "dataset": cfg["dataset"], "query_packs": len(IDS)}, ensure_ascii=False))

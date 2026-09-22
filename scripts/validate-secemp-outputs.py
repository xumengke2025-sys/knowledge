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

def jsonl(path):
    return [json.loads(x) for x in path.read_text(encoding="utf-8").splitlines() if x.strip()]

candidate_summary = load(R / "radar/secemp-arxiv-summary.json")
triage_summary = load(R / "radar/secemp-paper-text-triage-summary.json")

assert candidate_summary["dataset"] == "secemp9/arxiv-complete"
assert triage_summary["dataset"] == "secemp9/arxiv-complete"

candidate_counts = {x["industry_id"]: x["candidates"] for x in candidate_summary["industries"]}
triage_counts = {x["industry_id"]: x for x in triage_summary["industries"]}
assert set(candidate_counts) == set(IDS)
assert set(triage_counts) == set(IDS)

total_candidates = 0
total_triage = 0
total_text_available = 0

for iid in IDS:
    research = R / "industries" / iid / "research"
    candidates = jsonl(research / "arxiv-candidates.jsonl")
    evidence = jsonl(research / "paper-evidence-candidates.jsonl")

    assert len(candidates) == candidate_counts[iid], (iid, len(candidates), candidate_counts[iid])
    assert len(candidates) >= 20, (iid, "candidate pool unexpectedly small", len(candidates))
    assert evidence, (iid, "missing paper_text evidence triage")
    assert len(evidence) == triage_counts[iid]["records"], (iid, len(evidence), triage_counts[iid]["records"])

    for row in candidates:
        assert row.get("source_dataset") == "secemp9/arxiv-complete", (iid, row.get("paper_id"))
        assert row.get("verification_status") == "candidate", (iid, row.get("paper_id"))
        assert row.get("reading_status") == "metadata_only", (iid, row.get("paper_id"))
        assert row.get("promote_to_stable_knowledge") is False, (iid, row.get("paper_id"))
        assert row.get("taxonomy_node_ids"), (iid, row.get("paper_id"), "missing taxonomy mapping")
        assert "text" not in row, (iid, row.get("paper_id"), "raw text leaked into candidate pool")

    available = 0
    for row in evidence:
        assert row.get("source_dataset") == "secemp9/arxiv-complete", (iid, row.get("paper_id"))
        assert row.get("source_config") == "paper_text", (iid, row.get("paper_id"))
        assert row.get("verification_status") == "needs_review", (iid, row.get("paper_id"))
        assert row.get("reading_status") == "metadata_only", (iid, row.get("paper_id"))
        assert row.get("taxonomy_node_ids"), (iid, row.get("paper_id"), "missing taxonomy mapping")
        assert "text" not in row and "abstract" not in row, (iid, row.get("paper_id"), "verbatim corpus content leaked")
        if row.get("paper_text_available"):
            available += 1
            assert row.get("source_text_sha256"), (iid, row.get("paper_id"), "missing source hash")
            assert isinstance(row.get("machine_triage"), dict), (iid, row.get("paper_id"))
            assert row.get("promote_to_stable_knowledge") is False, (iid, row.get("paper_id"))

    assert available == triage_counts[iid]["paper_text_available"], (iid, available, triage_counts[iid]["paper_text_available"])
    total_candidates += len(candidates)
    total_triage += len(evidence)
    total_text_available += available

assert triage_summary["paper_text_rows_found"] >= 1
assert triage_summary["unique_papers_requested"] >= total_triage

print(json.dumps({
    "status": "PASS",
    "industries": len(IDS),
    "candidates": total_candidates,
    "triage_records": total_triage,
    "paper_text_available": total_text_available,
}, ensure_ascii=False))

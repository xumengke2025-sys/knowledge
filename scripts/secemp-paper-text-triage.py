#!/usr/bin/env python3
"""Build non-verbatim evidence triage cards from selected SecEmp paper_text rows.

This script reads the top metadata candidates already committed under each industry,
fetches only those exact paper IDs from SecEmp paper_text, and writes compact
machine-triage records. Raw paper text is never written to the repository.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import pathlib
import re
from collections import defaultdict

ROOT = pathlib.Path(__file__).resolve().parents[1]
DATASET = "secemp9/arxiv-complete"
HF_TABLE = f"hf://datasets/{DATASET}/paper_text/*.parquet"
INDUSTRIES = [
    "embodied-intelligence",
    "commercial-space-satcom",
    "low-altitude-economy",
    "wide-bandgap-semiconductor",
    "solid-state-battery",
    "synthetic-biology-biomanufacturing",
    "industrial-machine-tools",
    "smart-sensors-mems",
]

SECTION_PATTERNS = {
    "method": r"\\(?:sub)*section\*?\{[^}]*?(method|approach|architecture|model)[^}]*\}",
    "experiment": r"\\(?:sub)*section\*?\{[^}]*?(experiment|evaluation|setup)[^}]*\}",
    "result": r"\\(?:sub)*section\*?\{[^}]*?(result|benchmark|performance)[^}]*\}",
    "limitation": r"\\(?:sub)*section\*?\{[^}]*?(limitation|failure|discussion)[^}]*\}",
    "conclusion": r"\\(?:sub)*section\*?\{[^}]*?(conclusion|future work)[^}]*\}",
}
SIGNALS = {
    "benchmark_terms": ["benchmark", "baseline", "dataset", "test set", "validation set"],
    "metric_terms": ["accuracy", "precision", "recall", "f1", "success rate", "latency", "throughput", "rmse", "mae", "cycle life", "ionic conductivity"],
    "evidence_design_terms": ["ablation", "simulation", "real-world", "prototype", "pilot", "experiment", "measurement"],
}

def load_jsonl(path: pathlib.Path):
    if not path.exists():
        return []
    return [json.loads(x) for x in path.read_text(encoding="utf-8").splitlines() if x.strip()]

def write_jsonl(path: pathlib.Path, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("".join(json.dumps(x, ensure_ascii=False) + "\n" for x in rows), encoding="utf-8")

def duckdb_connect():
    try:
        import duckdb
    except Exception as exc:
        raise SystemExit("duckdb is required: pip install duckdb") from exc
    con = duckdb.connect()
    try:
        con.execute("INSTALL httpfs")
    except Exception:
        pass
    try:
        con.execute("LOAD httpfs")
    except Exception:
        pass
    return con

def q(v: str) -> str:
    return "'" + v.replace("'", "''") + "'"

def build(top_per_industry: int):
    selected = []
    memberships = defaultdict(list)
    for iid in INDUSTRIES:
        p = ROOT / "industries" / iid / "research" / "arxiv-candidates.jsonl"
        rows = load_jsonl(p)[:top_per_industry]
        for rank, row in enumerate(rows, start=1):
            pid = row.get("paper_id")
            if not pid:
                continue
            selected.append(pid)
            memberships[pid].append({
                "industry_id": iid,
                "candidate_rank": rank,
                "relevance_score": row.get("relevance_score"),
                "taxonomy_node_ids": row.get("taxonomy_node_ids") or [],
            })

    ids = list(dict.fromkeys(selected))
    if not ids:
        raise SystemExit("no SecEmp candidate IDs available; run discover-all first")
    if len(ids) > 160:
        raise SystemExit("triage-all intentionally capped at 160 unique paper IDs")

    values = ",".join(q(x) for x in ids)
    sql = f"""
    SELECT paper_id, title, abstract, primary_category, license, resolution,
           text_encoding, text_sha256, text
    FROM {q(HF_TABLE)}
    WHERE paper_id IN ({values})
    """
    con = duckdb_connect()
    try:
        cur = con.execute(sql)
        cols = [d[0] for d in cur.description]
        papers = [dict(zip(cols, row)) for row in cur.fetchall()]
    finally:
        con.close()

    found = {p["paper_id"]: p for p in papers}
    outputs = defaultdict(list)
    as_of = dt.datetime.now(dt.timezone.utc).isoformat()

    for pid, links in memberships.items():
        p = found.get(pid)
        if not p:
            for link in links:
                outputs[link["industry_id"]].append({
                    "paper_id": pid,
                    "source_dataset": DATASET,
                    "source_config": "paper_text",
                    "paper_text_available": False,
                    "verification_status": "needs_review",
                    "reading_status": "metadata_only",
                    **link,
                })
            continue

        text = p.get("text") or ""
        lower = text.lower()
        sections = [name for name, pattern in SECTION_PATTERNS.items() if re.search(pattern, text, re.I)]
        signal_hits = {k: [term for term in terms if term in lower] for k, terms in SIGNALS.items()}

        for link in links:
            outputs[link["industry_id"]].append({
                "paper_id": pid,
                "title": p.get("title"),
                "primary_category": p.get("primary_category"),
                "license": p.get("license"),
                "source_dataset": DATASET,
                "source_config": "paper_text",
                "source_text_sha256": p.get("text_sha256"),
                "resolution": p.get("resolution"),
                "paper_text_available": True,
                "machine_triage": {
                    "sections_detected": sections,
                    "signal_terms": signal_hits,
                    "text_chars": len(text),
                },
                "verification_status": "needs_review",
                "reading_status": "metadata_only",
                "promote_to_stable_knowledge": False,
                "review_required": [
                    "人工或模型阅读相关章节，填写方法、实验条件、基线、指标、局限与失败模式",
                    "机器章节/术语检测只用于排队，不构成论文结论",
                    "论文证据不得直接生成上市公司事实、商业化阶段或技术实力排名",
                ],
                "triaged_at": as_of,
                **link,
            })

    summary = {
        "version": "0.7.1",
        "as_of": as_of,
        "dataset": DATASET,
        "top_per_industry": top_per_industry,
        "unique_papers_requested": len(ids),
        "paper_text_rows_found": len(found),
        "industries": [],
    }
    for iid in INDUSTRIES:
        path = ROOT / "industries" / iid / "research" / "paper-evidence-candidates.jsonl"
        rows = outputs[iid]
        write_jsonl(path, rows)
        summary["industries"].append({
            "industry_id": iid,
            "records": len(rows),
            "paper_text_available": sum(bool(x.get("paper_text_available")) for x in rows),
            "output": path.relative_to(ROOT).as_posix(),
        })

    sp = ROOT / "radar" / "secemp-paper-text-triage-summary.json"
    sp.parent.mkdir(parents=True, exist_ok=True)
    sp.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return summary

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--top-per-industry", type=int, default=8)
    args = ap.parse_args()
    n = max(1, min(20, args.top_per_industry))
    print(json.dumps(build(n), ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()

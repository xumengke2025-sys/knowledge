#!/usr/bin/env python3
"""SecEmp arXiv corpus adapter for FirmBuddy Knowledge.

The script deliberately separates discovery from promotion:
- discover: query SecEmp metadata/sample and emit candidate metadata only.
- fetch-text: fetch exact paper_text rows into .cache/ for local/CI review.
- evidence: derive a non-verbatim machine triage record from cached paper_text.

No command auto-promotes a paper into stable academic-papers/mechanisms.
"""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import pathlib
import re
from typing import Any, Iterable

ROOT = pathlib.Path(__file__).resolve().parents[1]
DATASET = "secemp9/arxiv-complete"
HF_ROOT = f"hf://datasets/{DATASET}"
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
SNAPSHOT = {"metadata": "2026-08-30", "files": "2026-09-05"}

def load_json(path: pathlib.Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))

def write_jsonl(path: pathlib.Path, rows: Iterable[dict[str, Any]]) -> int:
    path.parent.mkdir(parents=True, exist_ok=True)
    rows = list(rows)
    path.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows), encoding="utf-8")
    return len(rows)

def pack_path(industry_id: str) -> pathlib.Path:
    return ROOT / "industries" / industry_id / "research" / "secemp-query-pack.json"

def load_pack(industry_id: str) -> dict[str, Any]:
    p = pack_path(industry_id)
    if not p.exists():
        raise SystemExit(f"missing query pack: {p}")
    return load_json(p)

def sql_quote(value: str) -> str:
    return "'" + str(value).replace("'", "''") + "'"

def normalized_terms(pack: dict[str, Any]) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    seen: set[str] = set()
    for group in pack.get("term_groups", []):
        nodes = group.get("node_ids", [])
        for item in group.get("terms", []):
            if isinstance(item, str):
                term, weight = item, 1
            else:
                term, weight = item["term"], int(item.get("weight", 1))
            key = term.strip().lower()
            if not key or key in seen:
                continue
            seen.add(key)
            out.append({"term": key, "weight": weight, "node_ids": nodes})
    return out

def _duckdb_connect():
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

def score_expr(pack: dict[str, Any], has_categories: bool) -> str:
    terms = normalized_terms(pack)
    parts: list[str] = []
    for t in terms:
        q = sql_quote(t["term"])
        w = int(t["weight"])
        parts.append(
            f"(CASE WHEN contains(lower(coalesce(title,'')), {q}) THEN {3*w} ELSE 0 END"
            f" + CASE WHEN contains(lower(coalesce(abstract,'')), {q}) THEN {w} ELSE 0 END)"
        )
    if has_categories and pack.get("preferred_categories"):
        checks = []
        for cat in pack.get("preferred_categories", []):
            q = sql_quote(cat)
            checks.append(f"list_contains(string_split(coalesce(categories,''), ' '), {q})")
        parts.append("CASE WHEN (" + " OR ".join(checks) + ") THEN 4 ELSE 0 END")
    for term in pack.get("negative_terms", []):
        q = sql_quote(term.lower())
        parts.append(
            f"CASE WHEN contains(lower(coalesce(title,'') || ' ' || coalesce(abstract,'')), {q}) THEN -5 ELSE 0 END"
        )
    return " + ".join(parts) if parts else "0"

def term_filter_expr(pack: dict[str, Any]) -> str:
    parts = []
    for t in normalized_terms(pack):
        q = sql_quote(t["term"])
        parts.append(
            f"(contains(lower(coalesce(title,'')), {q}) OR contains(lower(coalesce(abstract,'')), {q}))"
        )
    return "(" + " OR ".join(parts) + ")" if parts else "false"

def match_details(row: dict[str, Any], pack: dict[str, Any]) -> tuple[list[str], list[str]]:
    text = ((row.get("title") or "") + " " + (row.get("abstract") or "")).lower()
    nodes: list[str] = []
    matched_terms: list[str] = []
    for group in pack.get("term_groups", []):
        group_hits = []
        for item in group.get("terms", []):
            term = item if isinstance(item, str) else item.get("term", "")
            if term and term.lower() in text:
                group_hits.append(term)
        if group_hits:
            nodes.extend(group.get("node_ids", []))
            matched_terms.extend(group_hits)
    return list(dict.fromkeys(nodes)), list(dict.fromkeys(matched_terms))

def match_nodes(row: dict[str, Any], pack: dict[str, Any]) -> list[str]:
    return match_details(row, pack)[0]

def discover(industry_id: str, limit: int, source: str, out: pathlib.Path | None) -> dict[str, Any]:
    pack = load_pack(industry_id)
    if source not in {"metadata", "sample"}:
        raise SystemExit("source must be metadata or sample")
    has_categories = source == "metadata"
    score = score_expr(pack, has_categories)
    term_filter = term_filter_expr(pack)
    min_score = int(pack.get("min_score", 4))
    table = f"{HF_ROOT}/{source}/*.parquet"
    if source == "metadata":
        columns = """
          paper_id, title, authors, abstract, categories, primary_category,
          license, doi, journal_ref, n_versions, first_version_date,
          latest_version_date, arxiv_abs_url
        """
    else:
        columns = """
          paper_id, title, NULL AS authors, abstract, NULL AS categories,
          primary_category, license, NULL AS doi, NULL AS journal_ref,
          NULL AS n_versions, NULL AS first_version_date,
          NULL AS latest_version_date,
          ('https://arxiv.org/abs/' || paper_id) AS arxiv_abs_url
        """
    sql = f"""
    SELECT {columns}, ({score})::INTEGER AS relevance_score
    FROM {sql_quote(table)}
    WHERE {term_filter} AND ({score}) >= {min_score}
    ORDER BY relevance_score DESC, coalesce(latest_version_date, DATE '1900-01-01') DESC, paper_id DESC
    LIMIT {int(limit)}
    """
    con = _duckdb_connect()
    try:
        cur = con.execute(sql)
        cols = [d[0] for d in cur.description]
        raw_rows = [dict(zip(cols, row)) for row in cur.fetchall()]
    finally:
        con.close()

    now = dt.datetime.now(dt.timezone.utc).isoformat()
    rows: list[dict[str, Any]] = []
    for r in raw_rows:
        for k, v in list(r.items()):
            if isinstance(v, (dt.date, dt.datetime)):
                r[k] = v.isoformat()
        nodes, matched_terms = match_details(r, pack)
        if not nodes or not matched_terms:
            continue
        r.update({
            "industry_id": industry_id,
            "taxonomy_node_ids": nodes,
            "matched_terms": matched_terms,
            "source_dataset": DATASET,
            "source_config": source,
            "dataset_snapshot": SNAPSHOT,
            "discovered_at": now,
            "verification_status": "candidate",
            "reading_status": "metadata_only",
            "promote_to_stable_knowledge": False,
            "review_required": [
                "确认论文实际落入taxonomy节点，而不是仅关键词命中",
                "阅读摘要；高价值论文再读取SecEmp paper_text或正式发表版本",
                "提取方法、实验条件、基线、指标、局限与失败模式",
                "禁止仅凭论文标题、作者单位或论文数量形成企业结论",
            ],
        })
        rows.append(r)

    if out is None:
        out = ROOT / "industries" / industry_id / "research" / "arxiv-candidates.jsonl"
    count = write_jsonl(out, rows)
    return {"industry_id": industry_id, "source": source, "candidates": count, "output": str(out)}

def discover_all(limit: int, source: str) -> dict[str, Any]:
    results = [discover(iid, limit, source, None) for iid in INDUSTRIES]
    summary = {
        "version": "0.7.0",
        "as_of": dt.date.today().isoformat(),
        "dataset": DATASET,
        "dataset_snapshot": SNAPSHOT,
        "source_config": source,
        "industries": results,
        "notice": "候选池不是稳定知识；必须经人工/模型复核后才能提升 reading_status 或进入 mechanisms。",
    }
    p = ROOT / "radar" / "secemp-arxiv-summary.json"
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return summary

def parse_ids(args: argparse.Namespace) -> list[str]:
    ids = list(args.paper_id or [])
    if args.ids_file:
        for line in pathlib.Path(args.ids_file).read_text(encoding="utf-8").splitlines():
            s = line.strip()
            if s and not s.startswith("#"):
                ids.append(s)
    ids = list(dict.fromkeys(ids))
    if not ids:
        raise SystemExit("provide --paper-id or --ids-file")
    if len(ids) > 200:
        raise SystemExit("fetch-text is intentionally capped at 200 paper IDs per run")
    bad = [x for x in ids if ".." in x or "\\" in x or "\x00" in x]
    if bad:
        raise SystemExit(f"unsafe paper ids: {bad[:3]}")
    return ids

def ensure_cache_output(path: pathlib.Path) -> pathlib.Path:
    rp = path.resolve()
    cache = (ROOT / ".cache").resolve()
    try:
        rp.relative_to(cache)
    except ValueError as exc:
        raise SystemExit("raw SecEmp paper_text may only be written under repository .cache/") from exc
    path.parent.mkdir(parents=True, exist_ok=True)
    return path

def fetch_text(ids: list[str], out: pathlib.Path) -> dict[str, Any]:
    out = ensure_cache_output(out)
    values = ",".join(sql_quote(x) for x in ids)
    table = f"{HF_ROOT}/paper_text/*.parquet"
    sql = f"""
    SELECT paper_id, title, abstract, primary_category, license, resolution,
           text_encoding, text_sha256, text
    FROM {sql_quote(table)}
    WHERE paper_id IN ({values})
    """
    con = _duckdb_connect()
    try:
        cur = con.execute(sql)
        cols = [d[0] for d in cur.description]
        rows = [dict(zip(cols, row)) for row in cur.fetchall()]
    finally:
        con.close()
    write_jsonl(out, rows)
    return {"requested": len(ids), "found": len(rows), "output": str(out)}

SECTION_PATTERNS = {
    "method": r"\\(?:sub)*section\*?\{[^}]*?(method|approach|architecture|model)[^}]*\}",
    "experiment": r"\\(?:sub)*section\*?\{[^}]*?(experiment|evaluation|setup)[^}]*\}",
    "result": r"\\(?:sub)*section\*?\{[^}]*?(result|benchmark|performance)[^}]*\}",
    "limitation": r"\\(?:sub)*section\*?\{[^}]*?(limitation|failure|discussion)[^}]*\}",
    "conclusion": r"\\(?:sub)*section\*?\{[^}]*?(conclusion|future work)[^}]*\}",
}
SIGNALS = {
    "benchmarks": ["benchmark", "baseline", "dataset", "test set", "validation set"],
    "metrics": ["accuracy", "precision", "recall", "f1", "success rate", "latency", "throughput", "rmse", "mae", "bleu", "psnr"],
    "evidence_design": ["ablation", "randomized", "control group", "simulation", "real-world", "prototype", "pilot"],
}

def evidence_from_cache(path: pathlib.Path, out: pathlib.Path) -> dict[str, Any]:
    rows = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        p = json.loads(line)
        text = p.get("text") or ""
        lower = text.lower()
        sections = [k for k, pat in SECTION_PATTERNS.items() if re.search(pat, text, flags=re.I)]
        signal_hits = {k: [t for t in vals if t in lower] for k, vals in SIGNALS.items()}
        rows.append({
            "paper_id": p.get("paper_id"),
            "title": p.get("title"),
            "source_dataset": DATASET,
            "source_config": "paper_text",
            "source_text_sha256": p.get("text_sha256") or hashlib.sha256(text.encode("utf-8")).hexdigest(),
            "license": p.get("license"),
            "resolution": p.get("resolution"),
            "machine_triage": {
                "sections_detected": sections,
                "signal_terms": signal_hits,
                "text_chars": len(text),
            },
            "reading_status": "metadata_only",
            "verification_status": "needs_review",
            "claims": [],
            "limitations": [],
            "expert_use": [],
            "review_required": [
                "阅读论文相关章节并记录实验条件、比较基线与适用边界",
                "不得把机器章节识别结果当作已验证论文结论",
                "稳定知识只保存自写研究卡与必要短引文，不保存SecEmp全文",
            ],
        })
    write_jsonl(out, rows)
    return {"papers": len(rows), "output": str(out)}

def main() -> None:
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)

    d = sub.add_parser("discover")
    d.add_argument("--industry", choices=INDUSTRIES, required=True)
    d.add_argument("--limit", type=int, default=120)
    d.add_argument("--source", choices=["metadata", "sample"], default="metadata")
    d.add_argument("--out", type=pathlib.Path)

    da = sub.add_parser("discover-all")
    da.add_argument("--limit", type=int, default=120)
    da.add_argument("--source", choices=["metadata", "sample"], default="metadata")

    f = sub.add_parser("fetch-text")
    f.add_argument("--paper-id", action="append")
    f.add_argument("--ids-file")
    f.add_argument("--out", type=pathlib.Path, default=ROOT / ".cache" / "secemp-arxiv" / "paper-text.jsonl")

    e = sub.add_parser("evidence")
    e.add_argument("--input", type=pathlib.Path, default=ROOT / ".cache" / "secemp-arxiv" / "paper-text.jsonl")
    e.add_argument("--out", type=pathlib.Path, required=True)

    args = ap.parse_args()
    if args.cmd == "discover":
        result = discover(args.industry, max(1, min(1000, args.limit)), args.source, args.out)
    elif args.cmd == "discover-all":
        result = discover_all(max(1, min(1000, args.limit)), args.source)
    elif args.cmd == "fetch-text":
        result = fetch_text(parse_ids(args), args.out)
    else:
        result = evidence_from_cache(args.input, args.out)
    print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()

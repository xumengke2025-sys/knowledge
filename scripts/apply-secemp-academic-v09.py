#!/usr/bin/env python3
from __future__ import annotations

import collections
import hashlib
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
AS_OF = "2026-09-22"
MANIFEST = ROOT / "sources" / "secemp-arxiv" / "section-reviewed-v09.json"

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

def load_json(path):
    return json.loads(path.read_text(encoding="utf-8"))

def load_jsonl(path):
    if not path.exists():
        return []
    return [json.loads(x) for x in path.read_text(encoding="utf-8").splitlines() if x.strip()]

def dump_json(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

def dump_jsonl(path, rows):
    path.write_text("".join(json.dumps(x, ensure_ascii=False) + "\n" for x in rows), encoding="utf-8")

def sha256(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()

def upsert(rows, additions, key):
    order = [x[key] for x in rows]
    by = {x[key]: x for x in rows}
    for x in additions:
        if x[key] not in by:
            order.append(x[key])
        by[x[key]] = x
    return [by[k] for k in order]

def render_section_cards(existing_text, notes):
    marker = "## SecEmp 深读证据卡（sections_reviewed）"
    if marker in existing_text:
        existing_text = existing_text.split(marker, 1)[0].rstrip() + "\n\n"
    lines = [marker, "", "> 仅列出已完成章节级复核的论文。SecEmp paper_text 提供正文版本锚点；研究结论由已审阅章节形成，不使用机器关键词命中代替阅读。", ""]
    for n in notes:
        lines += [
            f"### {n['id']}｜{n['title']}",
            "",
            f"**已复核章节**：{'；'.join(n['reviewed_sections'])}",
            "",
            f"**方法/模型**：{n['method_note']}",
            "",
            f"**实验/数据条件**：{n['experiment_note']}",
            "",
            f"**基线**：{'；'.join(n['baselines'])}",
            "",
            f"**指标**：{'；'.join(n['metrics'])}",
            "",
            f"**关键发现**：{'；'.join(n['key_findings'])}",
            "",
            f"**局限**：{'；'.join(n['limitations'])}",
            "",
            f"**专家继续追问**：{'；'.join(n['expert_questions'])}",
            "",
            f"**不能据此推出**：{'；'.join(n['cannot_infer'])}",
            "",
            f"**SecEmp正文锚点**：{n['secemp_text_sha256']}",
            "",
        ]
    return existing_text.rstrip() + "\n\n" + "\n".join(lines).rstrip() + "\n"

def main():
    mf = load_json(MANIFEST)
    assert mf["version"] == "0.9.0"
    grouped = collections.defaultdict(list)
    for row in mf["papers"]:
        grouped[row["industry_id"]].append(row)
    assert set(grouped) == set(INDUSTRIES)

    for iid in INDUSTRIES:
        research = ROOT / "industries" / iid / "research"
        ppath = research / "academic-papers.jsonl"
        papers = load_jsonl(ppath)
        by_id = {p["id"]: p for p in papers}
        notes = []

        for review in grouped[iid]:
            pid = review["id"]
            assert pid in by_id, (iid, pid)
            p = dict(by_id[pid])
            assert p.get("paper_id") == review["paper_id"], (iid, pid, "paper_id mismatch")
            p["reading_status"] = "sections_reviewed"
            p["section_review"] = {
                "as_of": AS_OF,
                "reviewed_sections": review["reviewed_sections"],
                "method_note": review["method_note"],
                "experiment_note": review["experiment_note"],
                "baselines": review["baselines"],
                "metrics": review["metrics"],
                "key_findings": review["key_findings"],
                "limitations": review["limitations"],
                "expert_questions": review["expert_questions"],
                "cannot_infer": review["cannot_infer"],
                "secemp_text_sha256": review["secemp_text_sha256"],
                "secemp_resolution": review["secemp_resolution"],
                "review_sources": review["review_sources"],
            }
            by_id[pid] = p
            note = dict(review)
            note["title"] = p["title"]
            notes.append(note)

        papers = [by_id[p["id"]] for p in papers]
        dump_jsonl(ppath, papers)

        existing_notes = load_jsonl(research / "paper-section-notes.jsonl")
        dump_jsonl(research / "paper-section-notes.jsonl", upsert(existing_notes, notes, "id"))

        lit_path = research / "literature-map.json"
        lit = load_json(lit_path)
        lit["as_of"] = AS_OF
        lit["reading_status_counts"] = dict(collections.Counter(p.get("reading_status", "metadata_only") for p in papers))
        dump_json(lit_path, lit)

        expert_path = research / "expert-knowledge.md"
        expert = expert_path.read_text(encoding="utf-8")
        # Keep rendered paper status consistent with the structured academic record.
        for review in grouped[iid]:
            p = by_id[review["id"]]
            old_status = f"{review['id']} [{p['title']}]({p['url']})；abstract_reviewed；SecEmp正文可用，仅完成机器预审"
            new_status = f"{review['id']} [{p['title']}]({p['url']})；sections_reviewed；SecEmp正文已完成章节复核"
            expert = expert.replace(old_status, new_status)
        expert_path.write_text(render_section_cards(expert, notes), encoding="utf-8")

    catalog_path = ROOT / "academic-catalog.json"
    catalog = load_json(catalog_path)
    catalog["version"] = "0.9.0"
    catalog["as_of"] = AS_OF
    for item in catalog["industries"]:
        papers = load_jsonl(ROOT / "industries" / item["industry_id"] / "research" / "academic-papers.jsonl")
        item["papers"] = len(papers)
        item["reviewed_papers"] = sum(p.get("reading_status") != "metadata_only" for p in papers)
        item["section_reviewed_papers"] = sum(p.get("reading_status") == "sections_reviewed" for p in papers)
        item["secemp_section_reviewed_papers"] = sum(
            p.get("reading_status") == "sections_reviewed" and p.get("source_dataset") == "secemp9/arxiv-complete"
            for p in papers
        )
    dump_json(catalog_path, catalog)

    bundle_path = ROOT / "firmbuddy" / "import-bundle.json"
    bundle = load_json(bundle_path)
    bundle["as_of"] = AS_OF
    docs = {d["logical_key"]: d for d in bundle["documents"]}
    for iid in INDUSTRIES:
        key = f"{iid}:academic"
        text = (ROOT / "industries" / iid / "research" / "expert-knowledge.md").read_text(encoding="utf-8")
        docs[key]["text"] = text
        docs[key]["sha256"] = sha256(text)
        docs[key]["tags"] = list(dict.fromkeys((docs[key].get("tags") or []) + ["academic-v0.9", "sections-reviewed"]))
    dump_json(bundle_path, bundle)

    print(json.dumps({
        "status": "APPLIED",
        "version": mf["version"],
        "section_reviewed_papers": len(mf["papers"]),
        "catalog_papers": sum(x["papers"] for x in catalog["industries"]),
        "catalog_mechanisms": sum(x["mechanisms"] for x in catalog["industries"]),
    }, ensure_ascii=False))

if __name__ == "__main__":
    main()

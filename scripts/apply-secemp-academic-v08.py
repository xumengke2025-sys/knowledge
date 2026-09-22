#!/usr/bin/env python3
from __future__ import annotations

import collections
import hashlib
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
AS_OF = "2026-09-22"
REVIEW = ROOT / "sources" / "secemp-arxiv" / "reviewed-v08.json"

INDUSTRIES = {
    "embodied-intelligence": "具身智能与人形机器人",
    "commercial-space-satcom": "商业航天与卫星互联网",
    "low-altitude-economy": "低空经济",
    "wide-bandgap-semiconductor": "第三代/宽禁带半导体",
    "solid-state-battery": "固态电池与下一代电池材料",
    "synthetic-biology-biomanufacturing": "合成生物学与生物制造",
    "industrial-machine-tools": "工业母机与高端数控",
    "smart-sensors-mems": "高端智能传感器与MEMS",
}

def load_json(path: pathlib.Path):
    return json.loads(path.read_text(encoding="utf-8"))

def load_jsonl(path: pathlib.Path):
    return [json.loads(x) for x in path.read_text(encoding="utf-8").splitlines() if x.strip()]

def dump_json(path: pathlib.Path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

def dump_jsonl(path: pathlib.Path, rows):
    path.write_text("".join(json.dumps(x, ensure_ascii=False) + "\n" for x in rows), encoding="utf-8")

def upsert(rows, additions, key="id"):
    by_key = {x[key]: x for x in rows}
    order = [x[key] for x in rows]
    for item in additions:
        k = item[key]
        if k not in by_key:
            order.append(k)
        by_key[k] = item
    return [by_key[k] for k in order]

def sha256(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()

def expert_markdown(industry_id: str, name: str, papers, mechanisms) -> str:
    by_paper = {p["id"]: p for p in papers}
    lines = [
        f"# {name}｜学术机制与研究证据",
        "",
        "> 用途：FirmBuddy 行业专家的 research 知识装备。本文把论文转化为可检索的机制知识；论文是证据，不是需要背诵的答案。",
        "> 边界：学术结果不能单独证明某家上市公司已量产、已获订单或具备同等性能；涉及公司事实仍需回到法定披露/公司证据装备。",
        "",
        "## 使用规则",
        "",
        "1. 先定位技术节点，再解释机制；性能数字必须带测试条件。",
        "2. 综述用于建立问题框架，单篇实验用于解释特定机制；两者不能替代公司产业化证据。",
        "3. metadata_only 文献只能做检索线索，不得支持技术结论。",
        "4. abstract_reviewed 只支持摘要明确表达的方向性结论；SecEmp paper_text 机器预审不等于 sections_reviewed。",
        "5. 学术机制与专利权利要求、上市公司披露相互验证，但不得互相替代。",
        "",
    ]
    for m in mechanisms:
        lines += [
            f"## {m['id']}｜{m['title']}",
            "",
            f"**技术节点**：{', '.join(m['node_ids'])}",
            "",
            f"**机制**：{m['mechanism']}",
            "",
            f"**应观察变量**：{'；'.join(m['measurable_variables'])}",
            "",
            f"**补证重点**：{'；'.join(m['evidence_to_seek'])}",
            "",
            f"**专家如何使用**：{m['expert_use']}",
            "",
            f"**禁止外推**：{m['false_inference']}",
            "",
            "**主要学术支持**：",
        ]
        for pid in m["support_paper_ids"]:
            p = by_paper[pid]
            secemp = "；SecEmp正文可用，仅完成机器预审" if p.get("secemp_paper_text_available") else ""
            lines.append(
                f"- {pid} [{p['title']}]({p['url']})；{p['reading_status']}{secemp}。{p.get('summary','')}"
            )
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"

def evaluation_rows(industry_id: str, mechanisms):
    out = []
    for m in mechanisms:
        out.append({
            "id": f"{industry_id}-academic-{m['id'].lower()}",
            "industry": industry_id,
            "question": f"请从学术机制解释“{m['title']}”，说明关键变量、应补的证据，以及至少一个容易产生的错误外推。",
            "expected_points": {
                "mechanism": m["mechanism"],
                "variables": m["measurable_variables"][:4],
                "evidence": m["evidence_to_seek"][:3],
                "must_avoid": m["false_inference"],
                "support_paper_ids": m["support_paper_ids"],
            },
            "evaluation_type": "academic_reasoning_manual",
            "execution_status": "not_run",
        })
    return out

def frontier_topics(industry_id: str, name: str, mechanisms):
    return {
        "industry_id": industry_id,
        "industry": name,
        "as_of": AS_OF,
        "topics": [
            {
                "topic_id": f"F-{m['id']}",
                "topic": m["title"],
                "node_ids": m["node_ids"],
                "monitor_query": f"{name} {m['title']} review OR benchmark OR reliability",
                "watch_for": [
                    "new review",
                    "open benchmark/dataset",
                    "method with real-world validation",
                    "reliability/scale-up evidence",
                ],
                "expert_use": "新论文先进入学术候选池，阅读摘要/正文后再升级为机制支持；不得因标题命中直接改变公司阶段。",
            }
            for m in mechanisms
        ],
    }

def literature_map(industry_id: str, name: str, papers, mechanisms, old):
    reviews = [p["id"] for p in papers if "review" in p.get("publication_type", "").lower() or "survey" in p.get("publication_type", "").lower()]
    frontier = [p["id"] for p in papers if p["id"] not in reviews and p.get("reading_status") != "metadata_only"]
    counts = collections.Counter(p.get("reading_status", "metadata_only") for p in papers)
    return {
        "industry_id": industry_id,
        "industry": name,
        "as_of": AS_OF,
        "scope_note": "curated academic evidence for expert reasoning; SecEmp v0.8 adds reviewed abstracts and paper_text triage but is not a systematic literature review",
        "review_and_survey": reviews,
        "landmark_or_foundational": old.get("landmark_or_foundational", []),
        "frontier_or_method": frontier,
        "mechanism_to_papers": {m["id"]: m["support_paper_ids"] for m in mechanisms},
        "reading_status_counts": dict(counts),
    }

def main():
    review = load_json(REVIEW)
    assert review["version"] == "0.8.0"
    assert review["source_dataset"] == "secemp9/arxiv-complete"

    catalog = {
        "version": "0.8.0",
        "as_of": AS_OF,
        "purpose": "FirmBuddy industry expert academic knowledge equipment",
        "industries": [],
    }

    for industry_id, name in INDUSTRIES.items():
        d = ROOT / "industries" / industry_id / "research"
        additions = review["industries"][industry_id]
        papers_path = d / "academic-papers.jsonl"
        mechanisms_path = d / "mechanisms.jsonl"
        old_lit = load_json(d / "literature-map.json")

        papers = upsert(load_jsonl(papers_path), additions["papers"])
        mechanisms = upsert(load_jsonl(mechanisms_path), additions["mechanisms"])

        dump_jsonl(papers_path, papers)
        dump_jsonl(mechanisms_path, mechanisms)
        dump_json(d / "literature-map.json", literature_map(industry_id, name, papers, mechanisms, old_lit))
        dump_json(d / "frontier-topics.json", frontier_topics(industry_id, name, mechanisms))
        dump_jsonl(d / "evaluation-academic.jsonl", evaluation_rows(industry_id, mechanisms))

        text = expert_markdown(industry_id, name, papers, mechanisms)
        (d / "expert-knowledge.md").write_text(text, encoding="utf-8")

        catalog["industries"].append({
            "industry_id": industry_id,
            "industry": name,
            "papers": len(papers),
            "mechanisms": len(mechanisms),
            "reviewed_papers": sum(p.get("reading_status") != "metadata_only" for p in papers),
            "secemp_reviewed_papers": sum(p.get("source_dataset") == "secemp9/arxiv-complete" and p.get("reading_status") != "metadata_only" for p in papers),
            "equipment_document_key": f"{industry_id}:academic",
            "equipment_key": f"{industry_id}:academic",
        })

    dump_json(ROOT / "academic-catalog.json", catalog)

    bundle_path = ROOT / "firmbuddy" / "import-bundle.json"
    bundle = load_json(bundle_path)
    bundle["as_of"] = AS_OF
    docs = {d["logical_key"]: d for d in bundle["documents"]}
    for industry_id, name in INDUSTRIES.items():
        key = f"{industry_id}:academic"
        text = (ROOT / "industries" / industry_id / "research" / "expert-knowledge.md").read_text(encoding="utf-8")
        doc = docs[key]
        doc["title"] = f"{name}｜学术机制与研究证据"
        doc["sourceType"] = "research"
        doc["text"] = text
        doc["sha256"] = sha256(text)
        doc["tags"] = list(dict.fromkeys((doc.get("tags") or []) + ["secemp", "academic-v0.8"]))
    dump_json(bundle_path, bundle)

    print(json.dumps({
        "status": "APPLIED",
        "version": review["version"],
        "industries": len(INDUSTRIES),
        "new_reviewed_papers": sum(len(x["papers"]) for x in review["industries"].values()),
        "new_mechanisms": sum(len(x["mechanisms"]) for x in review["industries"].values()),
        "catalog_papers": sum(x["papers"] for x in catalog["industries"]),
        "catalog_mechanisms": sum(x["mechanisms"] for x in catalog["industries"]),
    }, ensure_ascii=False))

if __name__ == "__main__":
    main()

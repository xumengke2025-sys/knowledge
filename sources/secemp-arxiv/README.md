# SecEmp arXiv 主语料层（v0.7）

本目录把 `secemp9/arxiv-complete` 接入 FirmBuddy Knowledge，定位是**历史全量学术语料底座**，不是把 arXiv 全文复制进 GitHub。

## 数据职责

- `metadata`：3148796 篇论文的全量发现层，负责标题、摘要、分类、版本日期、DOI、许可与原文地址。
- `paper_text`：2856227 篇论文的已拼装 TeX 文本，只对高价值候选按 `paper_id` 读取，用于方法、实验条件、指标、局限和失败模式复核。
- `versions`：需要核对版本时使用。
- `latex/pdf/source`：仅作特殊兜底，不进入日常流水线。

快照口径：metadata 2026-08-30；文件镜像 2026-09-05。该数据集是一次性快照，因此仓库现有 OpenAlex/Crossref Radar 继续负责新增论文发现。

## 标准流水线

```text
SecEmp metadata
  -> industries/*/research/secemp-query-pack.json
  -> arxiv-candidates.jsonl              # candidate / metadata_only
  -> 人工或模型主题复核
  -> SecEmp paper_text（仅按 paper_id 读取到 .cache/）
  -> paper-evidence.jsonl                 # 自写研究卡，不保存全文
  -> academic-papers.jsonl
  -> mechanisms.jsonl / literature-map.json
  -> expert-knowledge.md
  -> FirmBuddy academic Knowledge Equipment
```

## 使用

安装依赖：

```bash
pip install duckdb
```

发现单行业候选：

```bash
python scripts/secemp-arxiv.py discover \
  --industry embodied-intelligence \
  --source metadata --limit 120
```

批量构建 8 行业候选池：

```bash
python scripts/secemp-arxiv.py discover-all --source metadata --limit 120
```

按 arXiv ID 获取少量全文到本地缓存：

```bash
python scripts/secemp-arxiv.py fetch-text \
  --paper-id 2307.15818 \
  --out .cache/secemp-arxiv/paper-text.jsonl
```

生成不含全文的机器预审记录：

```bash
python scripts/secemp-arxiv.py evidence \
  --input .cache/secemp-arxiv/paper-text.jsonl \
  --out /tmp/paper-evidence-triage.jsonl
```

机器预审记录**不能自动提升** `reading_status`，也不能直接生成企业技术结论。

## 版权与证据边界

SecEmp 的组织层与 arXiv metadata 可以按其说明使用，但论文正文的许可逐篇不同。`paper_text`/PDF/LaTeX 只能作为研究输入；仓库稳定层保存自写研究卡、机制卡、索引、来源链接和必要短引文。论文作者单位、论文数量、标题热度不得推导为上市公司合作关系、商业化阶段或技术实力排名。

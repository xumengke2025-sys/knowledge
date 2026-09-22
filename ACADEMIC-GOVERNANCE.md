# 学术知识治理（v0.7）

日期：2026-09-22

## 目标

本层不是“论文收藏夹”，而是把学术证据转化为 FirmBuddy 行业专家可检索、可引用、可装备、可试炼的机制知识。

## 五层对象

1. `academic-papers.jsonl`：经过筛选的论文/综述/数据论文；保存标识、阅读状态、摘要式研究卡和外推边界。
2. `mechanisms.jsonl`：把多篇文献支持的机理、变量、补证方法和错误外推整理成专家知识单元。
3. `literature-map.json`：综述/经典/前沿及机制—论文映射。
4. `frontier-topics.json`：持续监测主题和检索式，不自动把新论文写成知识事实。
5. `expert-knowledge.md`：真正进入 FirmBuddy Knowledge Equipment 的可读知识文档。

## SecEmp arXiv 主语料层

`secemp9/arxiv-complete` 自 v0.7 起作为历史全量 arXiv 主语料源：

- `metadata` 用于行业候选发现，不因为命中就提升为稳定知识；
- `paper_text` 只对高价值候选按 `paper_id` 读取，用于方法、实验、指标、局限和失败模式复核；
- `versions` 用于需要时核对版本；
- `latex/pdf/source` 不是默认研究路径，不批量下载进仓库；
- SecEmp 为一次性快照，现有 OpenAlex/Crossref Radar 继续承担增量发现。

每个行业通过 `research/secemp-query-pack.json` 把关键词、arXiv 分类和现有 taxonomy 节点绑定。流水线输出的 `arxiv-candidates.jsonl` 均为候选池，不自动写入 `academic-papers.jsonl`、`mechanisms.jsonl` 或 FirmBuddy 稳定装备。机器对 `paper_text` 的章节识别、术语命中或结构化预审也不自动改变 `reading_status`。

## 阅读状态

- `metadata_only`：只核实书目，不支持机制结论。
- `abstract_reviewed`：已阅读公开摘要/页面信息，可支持摘要明确表达的方向性机制，不支持未披露实验细节。
- `sections_reviewed`：已阅读公开正文的相关章节，可在其条件范围内支持更具体判断。
- `full_text_reviewed`：完整阅读全文并做方法/结果/局限复核。当前仅在确有完整阅读证据时使用。

## 专家使用纪律

- 学术论文解释“为什么/在什么条件下”，公司披露回答“谁/做到什么阶段”；两类证据不能替代。
- 论文性能数字必须连同材料、设备、环境、样本量、基线或任务一起使用。
- 预印本、会议论文、综述、数据论文和正式同行评议研究分开标记。
- 不用论文作者单位推导上市公司合作、供应链或商业化关系。
- 不用引用数、论文数或专利数直接生成技术实力排名。
- 版权受限正文不在本仓库重分发；保存自写研究卡、必要短引文和合法原文链接。

## 装备策略

每个行业新增独立 `research` 装备：`<industry>:academic`。它与已有的 core / company / research / patent 装备并存。这样学术层可以单独版本化、升级和回滚，不改变公司事实装备。

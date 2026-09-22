# v0.8 SecEmp 学术知识编译层质量报告

日期：2026-09-22

## 本轮目标

v0.7 已解决“如何从 SecEmp 全量 arXiv 快照中发现论文并读取 paper_text”的问题；v0.8 继续解决“如何把论文真正变成行业专家长期知识”的问题。

本轮新增一条明确的晋级链：

SecEmp candidate → paper_text machine triage → reviewed manifest → academic-papers → mechanisms → literature-map / evaluation → expert-knowledge → FirmBuddy academic Knowledge Equipment。

## 已完成

- 从 8 行业 SecEmp 候选池中选取 16 篇高价值论文进入明确复核清单，每行业 2 篇。
- 16 篇全部只晋级到 abstract_reviewed；虽然对应 SecEmp paper_text 可用，但机器章节/指标预审不被记作 sections_reviewed 或 full_text_reviewed。
- 每行业新增 1 个由至少 2 篇论文共同支持的机制知识单元，共新增 8 个机制。
- academic-catalog 升级至 v0.8.0：当前共 76 篇学术研究卡、57 个机制单元。
- 自动重建 8 行业 literature-map、frontier-topics、evaluation-academic、expert-knowledge。
- 自动同步 FirmBuddy import-bundle 中 8 个 academic research 装备的正文、SHA256 和标签。
- 新增确定性编译器 scripts/apply-secemp-academic-v08.py 与 GitHub Actions 自动编译流程。
- 新增 validate-secemp-academic-v08.py，验证复核清单、稳定知识、机制支持链及 FirmBuddy 装备一致性。

## 证据纪律

1. arxiv-candidates.jsonl 仍是 candidate，不自动进入稳定知识。
2. paper-evidence-candidates.jsonl 只表示正文是否可用及机器预审信号，不自动改变 reading_status。
3. reviewed-v08.json 是本轮稳定知识晋级白名单；只有经过明确复核的论文才能由编译器写入 academic-papers。
4. 本轮 SecEmp 论文统一为 abstract_reviewed；不把 paper_text 可用性冒充人工/模型全文复核。
5. 新机制至少由两篇本轮复核论文共同支持，并保留 false_inference 与 evidence_to_seek。
6. 学术知识仍不能替代上市公司信披、专利法律状态或运行时企业数据。

## 当前结果

- 学术研究卡：76
- 机制知识单元：57
- 本轮 SecEmp 稳定晋级论文：16
- 本轮新增跨论文机制：8
- 每个行业 SecEmp 稳定晋级论文：2

## 下一层

v0.9 可以继续把 paper_text 从“机器预审”提升为受控的 section review：只对高价值论文提取方法、实验设置、基线、指标和局限的结构化研究笔记，并保留逐项来源范围；达到条件后再把个别论文从 abstract_reviewed 晋级为 sections_reviewed。

# v0.7 SecEmp arXiv 学术语料层质量报告

日期：2026-09-22

## 本轮新增

- 将 `secemp9/arxiv-complete` 接入为 Knowledge 的历史全量 arXiv 主语料源。
- 固化数据快照口径：metadata 截止 2026-08-30，文件镜像截止 2026-09-05。
- 新增 8 行业 `secemp-query-pack.json`，所有检索词均映射到现有 taxonomy 节点。
- 新增 `scripts/secemp-arxiv.py`：支持 metadata/sample 候选发现、按 arXiv ID 获取少量 `paper_text` 到 `.cache/`、生成非全文的机器预审记录。
- 新增 `scripts/validate-secemp-arxiv.py`，校验数据源配置、行业查询包、taxonomy 映射及“禁止提交原始全文”边界。
- 新增 GitHub Actions：PR 只跑公开 sample 烟测；主分支相关变更、月度计划或手动触发时构建 8 行业候选池。
- 保留 OpenAlex/Crossref Radar：SecEmp 是一次性历史快照，前者继续承担新增学术信号发现。

## 数据边界

SecEmp `metadata` 作为发现层，`paper_text` 仅按高价值论文 ID 读取用于复核。GitHub 不保存 SecEmp 原始全文、PDF、LaTeX/source 批量副本。候选记录默认 `verification_status=candidate`、`reading_status=metadata_only`，不得自动进入稳定机制知识。

## 晋级门槛

1. 关键词/分类命中只进入 `arxiv-candidates.jsonl`。
2. 主题相关性复核后才可进入人工阅读队列。
3. 至少 `abstract_reviewed` 才能支持摘要明确表达的方向性判断。
4. 需要机制、性能或工程边界结论时，优先读取 `paper_text` 或正式发表版本，记录实验条件、基线、指标、局限和失败模式。
5. 论文不能替代上市公司信披；作者单位、论文数量、标题热度不能推导企业合作、产业化阶段或技术实力排名。

## 尚未完成

- v0.7 首次合并后由 Actions 执行全量 metadata 候选池构建；候选池生成成功不等于完成论文精读。
- `paper_text` 的全文证据抽取当前只提供机器预审骨架，稳定 `paper-evidence` 仍需进一步阅读/模型复核。
- SecEmp 快照不自动更新，2026-08-30 之后的新论文仍由现有 Radar 捕获并交叉核验。

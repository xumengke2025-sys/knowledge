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

## 首次真实运行结果

2026-09-22 已完成一轮 GitHub Actions 端到端运行并成功将结果落库：

- 8 行业 metadata 候选池：具身智能 120、商业航天 120、低空经济 120、宽禁带半导体 120、固态电池 120、合成生物 120、工业母机 97、智能传感器/MEMS 120，共 937 条候选。
- 对每个行业前 8 条候选执行 SecEmp `paper_text` 预审，共请求 64 篇；41 篇获得 `paper_text`。
- 正文可用数：具身智能 8/8、商业航天 8/8、低空经济 7/8、宽禁带半导体 3/8、固态电池 4/8、合成生物 5/8、工业母机 4/8、智能传感器/MEMS 2/8。
- `paper-evidence-candidates.jsonl` 仅保存章节识别、指标/基线/实验设计信号、文本哈希、许可和审核状态，不保存 SecEmp 原始全文。
- 已增加生成任务并发互斥与竞态安全写回；最终刷新工作流、仓库质量门禁均通过。

## 仍需持续深化

- `paper_text` 当前是机器预审层，不等于已完成人工/模型精读；稳定 `academic-papers.jsonl`、`mechanisms.jsonl` 仍须经过晋级门槛。
- 部分行业候选论文没有可用 `paper_text`，需按许可与可用性回退到 arXiv 页面、PDF/LaTeX 或正式发表版本。
- SecEmp 快照不自动更新，2026-08-30 之后的新论文继续由现有 OpenAlex/Crossref Radar 捕获并交叉核验。

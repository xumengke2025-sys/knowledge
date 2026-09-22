# v0.9 SecEmp Section Review 质量报告

日期：2026-09-22

## 目标

v0.9 不继续扩大稳定论文数量，而是提高证据深度：从 v0.8 的 `abstract_reviewed` 中，每个行业选择 1 篇高价值 SecEmp 论文，完成方法、实验/数据条件、基线、指标、结果和局限的章节级复核。

## 本轮完成

- 8 个行业各 1 篇，共 8 篇 SecEmp 论文由 `abstract_reviewed` 晋级为 `sections_reviewed`。
- 每篇均保留 SecEmp `paper_text` 的 SHA256 作为正文版本锚点，并对照 arXiv HTML 的可读章节进行复核。
- 每行业新增 `paper-section-notes.jsonl`，记录：
  - reviewed_sections
  - method_note
  - experiment_note
  - baselines
  - metrics
  - key_findings
  - limitations
  - expert_questions
  - cannot_infer
- 8 份 `expert-knowledge.md` 新增“SecEmp 深读证据卡”，并同步进入 FirmBuddy academic Knowledge Equipment。
- `academic-catalog.json` 升级至 v0.9.0，增加 `section_reviewed_papers` 与 `secemp_section_reviewed_papers` 统计。
- 新增 `scripts/apply-secemp-academic-v09.py`、`scripts/validate-secemp-academic-v09.py` 和对应 GitHub Actions。
- 修复 v0.8/v0.9 验证器的版本兼容：v0.8 保证原始复核字段不漂移，v0.9 白名单允许阅读深度从摘要复核合法升级到章节复核。
- 修复专家文档展示状态与结构化 reading_status 不一致的问题。

## 本轮 8 篇深读样本

| 行业 | 稳定论文ID | arXiv ID | 深读重点 |
|---|---|---|---|
| 具身智能 | EI-P09 | 2502.19645 | VLA 微调、LIBERO、ALOHA、推理效率与局限 |
| 商业航天 | CS-P09 | 2208.02683 | TN-NTN 系统模型、UAV 卸载、上下行结果 |
| 低空经济 | LA-P08 | 2604.06093 | eVTOL 功率模型、冲突解脱、能量长尾与模型局限 |
| 宽禁带半导体 | WBG-P08 | 2502.19315 | AlBN/GaN 外延、HEMT 工艺、电学/C-V 与接触限制 |
| 固态电池 | SSB-P10 | 2510.09861 | CHGNet 微调、DFT/MD、离子电导与训练域限制 |
| 合成生物 | SB-P09 | 1911.11091 | ART、贝叶斯推荐、DBTL 案例与假设失效 |
| 工业母机 | IMT-P09 | 2510.03261 | FEM 数据、时序网络 benchmark、跨工况泛化 |
| MEMS | SEN-P09 | 2002.02234 | 非线性模态耦合、扫频测量、瞬态仿真 |

## 当前学术层规模

- 稳定学术研究卡：76
- 机制知识单元：57
- 全库 sections_reviewed：12
- 本轮新增 SecEmp sections_reviewed：8
- SecEmp metadata 候选池：937
- paper_text 首轮预审记录：64，其中 41 篇正文可用

## 晋级纪律

1. `paper_text` 可用不等于正文已读。
2. 只有 `section-reviewed-v09.json` 中明确列出的论文可以晋级为 `sections_reviewed`。
3. 每条章节复核必须记录实验/数据条件和限制，不允许只保存结果数字。
4. 深读证据卡只能强化行业机制判断，不能替代上市公司披露、专利法律状态和运行时企业事实。
5. v0.9 不使用 `full_text_reviewed`；只有完整阅读全文并完成方法、结果、局限的全面复核后才允许进入该状态。

## 下一层

下一阶段应从“每行业 1 篇深读样本”扩展到“围绕关键机制的证据组”：优先让每个高价值机制拥有 2–4 篇 `sections_reviewed` 论文，并补齐 benchmark/dataset、工程测试条件和相互矛盾结果，从而形成更强的技术比较与企业补证能力。

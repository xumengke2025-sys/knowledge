# v0.4 学术装备层质量报告

日期：2026-09-20

## 本轮变化

- 8 个行业新增独立学术装备层，不覆盖 v0.3 的公司、政策、技术树和专利工作。
- 新增 60 条精选学术文献记录，其中 57 条至少完成摘要/相关章节阅读。
- 新增 49 条机制知识卡，每条包含技术节点、机制、可测变量、补证重点、产业判断用途、禁止外推和支持论文。
- 每行业新增 literature map、frontier topics、academic evaluation 和 `expert-knowledge.md`。
- FirmBuddy 导入包新增 8 份 academic 文档和 8 件 `research` 装备，绑定到 8 位行业专家的 Loadout。
- 学术论文不用于自动抬升上市公司成熟度，不生成商机或投资结论。

## 验收边界

本版本显著提升学术深度，但仍不是系统综述或全量文献数据库。论文集合采用“经典/综述/前沿/工程验证”的目的性抽样；新论文进入机制卡前必须经过阅读状态升级和外推边界审查。

运行 `python scripts/validate-academic.py` 验证结构、节点映射、论文引用、装备文档哈希和专家范围。

## FirmBuddy 实际兼容验收

已在目标 FirmBuddy 基线 `f774ae95b3e8b9dd231a465e037f0c597d698f48` 上通过真实隔离集成测试：使用目标工程的 `StorageService`、`KnowledgeService`、SQLite 迁移与检索器，将 v0.4 导入包写入临时数据库。

- 36 份文档、36 件装备、8 位专家全部导入成功；其中 8 件为新增 academic research 装备。
- 8 位专家 Loadout 均包含预期装备；具身智能新增 academic 装备也完成绑定。
- 8 个行业均通过 `KnowledgeService.search` 返回真实 `KB:` citation，并可还原到对应 DocumentVersion/Chunk。
- 重复导入幂等、文档/装备版本升级、历史 chunks 保留、CAS 冲突拒绝均通过。
- 真实 LLM 专家回答、生产数据库导入、生产专家发布未执行，因此不据此声明线上专家效果已验收。

机器可读结果见 `firmbuddy/validation-result-v0.4.json`。

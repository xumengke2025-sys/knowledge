> v0.2历史记录。当前版本请参阅 ../QUALITY-V0.3.md 与 IMPORT-V0.3.md。

# FirmBuddy 导入映射（基于当前 firmbuddy 代码扫描）

本映射针对 `xumengke2025-sys/firmbuddy` 当前结构设计。

## 1. 专家

FirmBuddy 当前专家结构支持：

- `category = 行业研究系列`
- `expert_profile`: `audience / scope / boundaries / method / criteria / clarifications / sources / evidence / outputStyle / outputRequirements / sampleQuestion / acceptance / businessDomain`
- `tools_whitelist`
- `knowledge_scope`
- Expert Revision / 培养流程

本仓库每个行业的 `expert-pack.json` 已按该逻辑生成，建议导入后通过 FirmBuddy 的“培养专家”流程，而不是直接覆盖线上 Active Revision。

默认业务归属：

```json
{
  "primary": "industry_research",
  "secondary": ["institutional"],
  "status": "suggested"
}
```

## 2. 知识库 / Knowledge Equipment

当前 FirmBuddy KnowledgeSpace 支持 Document → immutable Version → Chunk → Citation → Equipment → Expert Loadout。

建议映射：

| 本仓库 | FirmBuddy |
|---|---|
| 政策/标准源 | Document(source_type=`regulator`) |
| 上市公司法定信披 | Document(source_type=`other`, metadata.document_kind=`listed_company_filing`) |
| 行业技术树 | Equipment(type=`core_spec`) |
| 政策与标准 | Equipment(type=`regulatory`) |
| 公司技术事实卡/行业研究 | Equipment(type=`research`) |
| 专利检索策略 | Equipment(type=`research`) |

`facts.jsonl` 是结构化索引，不替代原文 citation。正式使用时仍应把对应官方原文或可引用摘录版本入库。

## 3. 专家 Loadout 建议

每个行业专家的默认三槽：

1. 核心规范：技术树 + 术语 + 成熟阶段词典
2. 监管规则：产业政策/标准体系
3. 研究资料：上市公司事实卡 + 专利导航策略

不建议把全部行业都永久装备给同一个专家；按行业建立独立专家或独立 Loadout，减少检索串扰。

## 4. 与现有 `industry-research` 插件的关系

当前插件已经有 `get_industry_framework / search_industry_insights / read_industry_evidence / inspect_company_technology`。本仓库可以作为它的下一代数据源，但不要直接覆盖现有 `knowledge.json` 大文件；推荐先导入 KnowledgeSpace，再逐步让行业插件转向受控 citation 检索。

## 5. 本版本明确不做

- 商机触发器
- 商机评分
- 证券业务需求假设
- 销售话术
- 客户行动建议

这些都属于 FirmBuddy 的上层业务应用，不进入本仓库科技事实底座。

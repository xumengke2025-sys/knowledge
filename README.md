# FirmBuddy 先进科技行业知识库

面向 **中国大陆上市公司** 的科技情报与行业专家训练底座，服务于 FirmBuddy 的「知识库—专家」体系。

> 当前版本：**v0.2.0（深度样板版）**  
> 截止日期：2026-09-19  
> 重点样板：**具身智能与人形机器人**

## 1. 这个仓库解决什么问题

本仓库不是“概念股名单”，也不是券商买卖建议库，而是把公开科技情报整理成可训练、可追溯、可持续更新的数据资产：

**行业技术树 → 上市公司 Universe → 公司技术落位 → 产品/研发/产业化阶段 → 专利与发明人线索 → 标准/政策 → 原始证据 → FirmBuddy 专家训练包**

当前明确 **不包含商机触发规则、客户需求推断或证券业务推荐**。

## 2. 数据口径

- 公司范围：A股、科创板、创业板、北交所的中国大陆上市公司；IPO审核中公司单独标记，不与已上市公司混同。
- 来源优先级：监管/交易所/上市公司法定披露 > 公司官方IR/业绩说明会 > 国家标准/专利公开数据 > 高可信行业机构 > 媒体。
- 公司阶段：严格区分 `研究/研发 → 样机/产品发布 → 送样 → 客户验证 → 小批量 → 批量 → 规模化`。
- 专利：本仓库当前提供 **代表性专利地图 + 检索策略**，不冒充法律意义上的全量专利数据库。全量统计必须完成申请人归一、同族去重、法律状态校验后才能发布。
- “候选公司”只表示值得继续核验，不自动训练成确定事实。

## 3. 行业目录

| 行业 | 目录 | 当前状态 |
|---|---|---|
| 具身智能与人形机器人 | `industries/embodied-intelligence/` | **深度样板**：扩大上市公司 Universe、公司事实、代表性专利地图、标准与训练集 |
| 商业航天/卫星互联网 | `industries/commercial-space-satcom/` | 中等覆盖 + 扩展候选池 |
| 低空经济 | `industries/low-altitude-economy/` | 中等覆盖 + 扩展候选池 |
| 第三代/宽禁带半导体 | `industries/wide-bandgap-semiconductor/` | 中等覆盖 + 扩展候选池 |
| 固态电池/下一代电池材料 | `industries/solid-state-battery/` | 中等覆盖 + 扩展候选池 |
| 合成生物/生物制造 | `industries/synthetic-biology-biomanufacturing/` | 中等覆盖 + 扩展候选池 |
| 工业母机/高端数控 | `industries/industrial-machine-tools/` | 中等覆盖 + 扩展候选池 |
| 高端智能传感器/MEMS | `industries/smart-sensors-mems/` | 中等覆盖 + 扩展候选池 |

## 4. 单行业标准目录

```text
industries/<industry>/
├── README.md                  # 行业说明、覆盖边界、使用方式
├── taxonomy.json              # 技术树
├── company-universe.json      # 上市公司池：verified/candidate/excluded
├── facts.jsonl                # 可训练事实卡，必须带 source_id
├── sources.json               # 原始来源索引
├── patent-search.md           # 专利导航检索策略
├── patents/                   # 代表性专利与技术主题（样板行业）
├── company-cards/             # 深度公司科技情报卡（样板行业）
├── expert-pack.json           # FirmBuddy 专家包
└── training-set.jsonl         # 试炼题/反例/证据纪律
```

## 5. FirmBuddy 适配

本仓库专家包已经按 FirmBuddy 现有 `expert-personas` 契约设计，包含：

- `category = 行业研究系列`
- `expert_profile`
- `knowledge_scope`
- `tools_whitelist`
- `businessDomain.primary = industry_research`
- 严格证据与时间口径
- 明确禁用商机判断

导入映射见 `firmbuddy/IMPORT-MAPPING.md`。

## 6. 质量状态

`QUALITY-REPORT.md` 和 `coverage-report.json` 记录当前覆盖率和未完成项。任何“全量覆盖”声明都必须满足：

1. 公司 Universe 有明确候选生成口径；
2. 每个 verified 公司至少一个 A/B 级来源；
3. 所有事实卡 source_id 均可解析；
4. 专利数量统计经过申请人归一、同族去重、法律状态校验；
5. 自动校验脚本通过；
6. 抽样人工复核通过。

当前版本 **不声称已经覆盖所有相关上市公司或全部专利**，但已将具身智能提升为可训练的深度样板，并将其余行业从“3家公司样板”扩展为可持续核验的候选 Universe。

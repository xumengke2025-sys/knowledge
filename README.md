# FirmBuddy 先进科技行业知识库

## v0.4 学术装备层

2026-09-20 新增 8 行业学术机制知识：精选论文索引、机制卡、文献地图、前沿主题、学术试炼题，并以独立 `research` Knowledge Equipment 绑定到对应行业专家。论文不替代上市公司披露；详见 `ACADEMIC-GOVERNANCE.md` 与 `QUALITY-V0.4.md`。


面向 **中国大陆上市公司** 的科技情报与行业专家训练底座，服务于 FirmBuddy 的「知识库—专家」体系。

> 当前版本：**v0.3.0（七行业研究与FirmBuddy接入准备版）**  
> 截止日期：2026-09-19  
> 本次深化：**具身智能以外的七行业**；原具身智能样板保留。

新增139个技术树节点的完整定义（含保留节点）、42个技术机制/条件专题、24条本轮核查摘录，以及14篇学术文献记录，其中9篇已读摘要或部分正文。公司池沿用104条行业内公司记录，并未宣称新增104家验证公司。

[FirmBuddy接入说明](firmbuddy/IMPORT-V0.3.md)包含插件、可调用研究技能、专家配置、28份文档及28件知识装备。已使用FirmBuddy真实Service与隔离数据库验证导入、检索、引用、幂等及版本升级；**生产导入和模型实际问答尚未运行**。七行业专利批量查询失败，检索方案和失败日志保留，未形成完整专利图谱。

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
| 商业航天/卫星互联网 | [技术研究](industries/commercial-space-satcom/technical-dossier.md) | 链路预算、载荷、星间链路与网络 |
| 低空经济 | [技术研究](industries/low-altitude-economy/technical-dossier.md) | 构型、任务功率、通导监、适航边界 |
| 第三代/宽禁带半导体 | [技术研究](industries/wide-bandgap-semiconductor/technical-dossier.md) | 长晶、缺陷、器件可靠性与封装 |
| 固态电池/下一代电池材料 | [技术研究](industries/solid-state-battery/technical-dossier.md) | 电解质、界面、测试条件与制造 |
| 合成生物/生物制造 | [技术研究](industries/synthetic-biology-biomanufacturing/technical-dossier.md) | DBTL、TRY、放大、纯化与经济性 |
| 工业母机/高端数控 | [技术研究](industries/industrial-machine-tools/technical-dossier.md) | 五轴、几何/热误差与切削稳定 |
| 高端智能传感器/MEMS | [技术研究](industries/smart-sensors-mems/technical-dossier.md) | 测量链、噪声、工艺、封装与校准 |

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

新接入包见 [IMPORT-V0.3.md](firmbuddy/IMPORT-V0.3.md)。旧IMPORT-MAPPING.md保留作历史参考，以新说明和当前目标工程代码为准。

## 6. 质量状态

`QUALITY-REPORT.md` 和 `coverage-report.json` 记录当前覆盖率和未完成项。任何“全量覆盖”声明都必须满足：

1. 公司 Universe 有明确候选生成口径；
2. 每个 verified 公司至少一个 A/B 级来源；
3. 所有事实卡 source_id 均可解析；
4. 专利数量统计经过申请人归一、同族去重、法律状态校验；
5. 自动校验脚本通过；
6. 抽样人工复核通过。

当前版本 **不声称已经覆盖所有相关上市公司或全部专利**，但已将具身智能提升为可训练的深度样板，并将其余行业从“3家公司样板”扩展为可持续核验的候选 Universe。


## v0.5 行业专家操作系统

8个行业新增Technology Benchmark、企业快速研判Playbook和Radar Source Catalog；专家长期知识负责行业先验，企业当前专利/年报/财务/新闻/资质/产业链由FirmBuddy运行时只读工具补齐。详见 `EXPERT-OS-V0.5.md` 与 `QUALITY-V0.5.md`。

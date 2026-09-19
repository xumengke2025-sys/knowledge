# 固态电池与下一代电池材料

## 定位

围绕全固态/半固态电池的材料体系、固体电解质、锂金属负极、电芯工艺与产业化阶段，尤其强调“实验室—中试—验证—量产”的阶段差异。

**与专精特新/先进产业的适配：** 战略性新兴产业 / 新能源 / 新材料 / 低空与机器人交叉应用。

## 技术树

| 节点ID | 名称 | 说明 |
|---|---|---|
| `sulfide-electrolyte` | 硫化物电解质 | 硫化物粉体、硫化锂原料、界面稳定 |
| `oxide-electrolyte` | 氧化物电解质 | LLZO/LATP等氧化物固体电解质 |
| `polymer-electrolyte` | 聚合物/复合电解质 | 聚合物、复合固态电解质 |
| `cathode` | 正极材料 | 高镍、富锂锰基、正极包覆/界面工程 |
| `anode` | 负极材料 | 锂金属、硅基等 |
| `cell-process` | 电芯与制造工艺 | 叠片、压力管理、干法/湿法、封装 |
| `pilot-line` | 中试与量产 | 中试线、验证线、量产线 |
| `applications` | 应用 | 汽车、储能、无人机/eVTOL、机器人 |

## 首批上市公司样本

| 代码 | 公司 | 技术节点 | 公开阶段 | 核心证据 |
|---|---|---|---|---|
| 002460 | 赣锋锂业 | sulfide-electrolyte, oxide-electrolyte, anode, cell-process, applications | 多环节研发/生产/商业化推进 | SSB-COMP-002460-2025AR |
| 002074 | 国轩高科 | cell-process, pilot-line | 全固态中试线已建设投产 | SSB-COMP-002074-2025AR |
| 300073 | 当升科技 | cathode, sulfide-electrolyte, oxide-electrolyte, applications | 材料批量供货/客户批量验证 | SSB-COMP-300073-2025AR |

## 核心来源

| source_id | 来源 | 发布者 | 日期 | 等级 |
|---|---|---|---|---|
| SSB-COMP-002460-2025AR | 赣锋锂业2025年年度报告 | 巨潮资讯/赣锋锂业 | 2026-03-31 | A |
| SSB-COMP-002074-2025AR | 国轩高科2025年年度报告 | 巨潮资讯/国轩高科 | 2026-04-29 | A |
| SSB-COMP-300073-2025AR | 当升科技2025年年度报告 | 巨潮资讯/当升科技 | 2026-03-31 | A |

## 使用说明

- 先读 `taxonomy.json`，再用 `company-universe.json` 做公司落位；
- 关键判断只引用 `facts.jsonl` 中带 source_id 的事实；
- 专利分析从 `patent-search.md` 开始，但正式地图必须做申请人归一和同族去重；
- `expert-pack.json` 用于 FirmBuddy 行业专家创建/培养；
- `training-set.jsonl` 用于试炼和回归，不包含商机题。


## v0.2 覆盖说明

本版本将上市公司 Universe 从少量样本扩展为“已验证样本 + 候选核验池”。`candidate` 仅用于后续检索补证，不能直接作为 FirmBuddy 确定事实。该行业当前深度低于具身智能样板，后续应按同一标准逐步补齐公司卡与代表性专利。

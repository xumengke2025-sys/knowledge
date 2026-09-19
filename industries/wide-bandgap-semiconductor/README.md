# 第三代/宽禁带半导体

## 定位

重点覆盖SiC、GaN等宽禁带半导体，从晶体生长、衬底、外延、器件、模块到制造装备和关键耗材。

**与专精特新/先进产业的适配：** 战略性新兴产业 / 集成电路 / 先进材料 / 新能源汽车与功率电子。

## 技术树

| 节点ID | 名称 | 说明 |
|---|---|---|
| `crystal-growth` | 晶体生长 | SiC/GaN晶体、长晶技术 |
| `substrate` | 衬底 | 6/8/12英寸SiC衬底、GaN相关衬底 |
| `epitaxy` | 外延 | SiC/GaN外延片与外延工艺 |
| `device` | 功率/射频器件 | SiC MOSFET、SBD、GaN HEMT |
| `module` | 功率模块 | 车规、工业、储能等功率模块 |
| `equipment` | 制造装备 | 长晶、切磨抛、外延、检测装备 |
| `consumables` | 材料耗材 | 高纯石墨、石英、陶瓷等 |

## 首批上市公司样本

| 代码 | 公司 | 技术节点 | 公开阶段 | 核心证据 |
|---|---|---|---|---|
| 688234 | 天岳先进 | crystal-growth, substrate | 大尺寸SiC衬底持续技术推进 | WBG-MKT-001 |
| 300316 | 晶盛机电 | equipment, substrate, consumables | 装备+材料多环节产业化 | WBG-COMP-300316-2025AR |
| 600703 | 三安光电 | substrate, epitaxy, device | SiC垂直产业链持续建设/量产验证 | WBG-COMP-600703-2024ESG |

## 核心来源

| source_id | 来源 | 发布者 | 日期 | 等级 |
|---|---|---|---|---|
| WBG-MKT-001 | 科创板公司2024年度经营业绩概览 | 上海证券交易所 | 2025-04-30 | A |
| WBG-COMP-300316-2025AR | 晶盛机电2025年年度报告 | 巨潮资讯/晶盛机电 | 2026-04-11 | A |
| WBG-COMP-600703-2024ESG | 三安光电2024年度可持续发展报告 | 上交所/三安光电 | 2025-08-02 | A |

## 使用说明

- 先读 `taxonomy.json`，再用 `company-universe.json` 做公司落位；
- 关键判断只引用 `facts.jsonl` 中带 source_id 的事实；
- 专利分析从 `patent-search.md` 开始，但正式地图必须做申请人归一和同族去重；
- `expert-pack.json` 用于 FirmBuddy 行业专家创建/培养；
- `training-set.jsonl` 用于试炼和回归，不包含商机题。


## v0.2 覆盖说明

本版本将上市公司 Universe 从少量样本扩展为“已验证样本 + 候选核验池”。`candidate` 仅用于后续检索补证，不能直接作为 FirmBuddy 确定事实。该行业当前深度低于具身智能样板，后续应按同一标准逐步补齐公司卡与代表性专利。

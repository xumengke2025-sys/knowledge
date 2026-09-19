# FirmBuddy 接入说明 v0.5

## 目标
v0.5 的行业专家遵循“行业先验长期装备 + 企业事实运行时获取”。

### 长期装备
每位专家共 7 件行业知识装备：
1. 技术原理与路线（core）
2. 上市公司历史案例/证据（company calibration）
3. 学术研究卡（research）
4. 专利导航方法（supplement）
5. 学术机制与研究证据（academic）
6. 技术评价基准（benchmark）
7. 企业快速研判手册（playbook）

### 运行时企业数据
专家白名单包含 16 个只读能力，核心包括：
- 主体：`moss_company_search`、`moss_company_profile`
- 年报：`moss_company_get_annual_reports`
- 专利：`moss_company_get_patents`
- 财务：`moss_company_get_listed_financial_data`
- 新闻：`moss_company_get_news`、`moss_public_opinion_search`
- 资质：`moss_company_get_certificates_v2`
- 产业链：`moss_industry_search_nodes`、`moss_industry_get_chain`
- 政策：`moss_policy_search_projects`
- 本地回退：`search_company`、`get_financial_summary`、`get_company_announcements`、`get_industry_landscape`、`generate_company_profile`

联系方式、任务创建、商机创建/状态流转、协同推送等高敏感或有副作用工具没有加入行业专家运行时白名单。

## 正式导入
沿用 `firmbuddy/import-knowledge.mjs`：
1. 先在目标 FirmBuddy 发布/确认8位行业专家，读回真实 expert ID。
2. 生成 `expert-map.json`。
3. 备份生产数据库并停服维护。
4. 执行 `import-knowledge.mjs --apply`。
5. 读回每位专家 Loadout，确认7件装备及其版本。
6. 确认目标环境 MOSS MCP 已连接，且实际 tools/list 包含专家要求的 MOSS 工具。
7. 用真实企业做端到端问答验收。

## 企业问答验收建议
每行业至少选择：
- 龙头/规模化企业1家
- 技术型中型企业1家
- 仅“概念相关”但证据弱的企业1家

要求专家能够正确区分：行业先验、当前企业事实、推断、未知；不能因为知识库里有历史案例就跳过运行时取数。

## 已验证
隔离 SQLite + FirmBuddy KnowledgeService 全链路已通过，见 `validation-result-v0.5.json`。

## 尚未验证
生产 MOSS 在线状态、生产数据库导入、真实 LLM 企业问答尚未执行。

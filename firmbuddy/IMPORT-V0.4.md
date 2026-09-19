# FirmBuddy 学术知识装备接入 v0.4

v0.4 在 v0.3 现有 28 件知识装备基础上，为 8 个行业各增加一件独立 `research` 学术装备。

## 新增对象

- 文档逻辑键：`<industry>:academic`
- 装备逻辑键：`<industry>:academic`
- 类型/槽位：`research`
- 内容源：`industries/<industry>/research/expert-knowledge.md`
- 专家：对应 `industry-<industry_id>` 专家

## 为什么独立装备

学术研究更新频率、证据性质和版本管理与公司披露不同。独立装备可单独升级和回滚，不会因为新增论文让公司事实文档产生无意义的新版本。

## 专家运行逻辑

1. 技术原理/路线/瓶颈问题：优先检索 academic + core。
2. 上市公司“做到了什么”：优先 company，必要时用 academic 解释机制。
3. 专利问题：patent 负责权利要求/检索边界，academic 解释技术机理。
4. 学术论文不能单独证明公司量产、订单、收入或客户关系。
5. 引用时使用 KnowledgeService 返回的实际 KB citation；论文 ID 只作为学术文献内部定位。

正式导入仍使用 `firmbuddy/import-knowledge.mjs`，发布专家和生产数据库导入步骤沿用 v0.3。

## 已验证的实际导入行为

针对 FirmBuddy 基线 `f774ae95b3e8b9dd231a465e037f0c597d698f48` 已执行隔离 SQLite + KnowledgeService 全链路验证，结果 PASS：36 文档、36 装备、8 专家、8 academic 装备；8 个专家均能从自身 Loadout 检索到真实 KB citation。详细结果见 `validation-result-v0.4.json`。

该验证不等于生产导入：正式环境仍需备份数据库、读取真实专家 ID 建立 `expert-map.json`，再执行 `import-knowledge.mjs --apply`。

# firmbuddy 接入参考

以下路径于2026-09-19依据 xumengke2025-sys/firmbuddy 的当前代码重新核对。它们是发现入口；每次执行仍记录实际提交、运行地址和能力列表，不沿用旧行业名单、端口或专家ID。

## 六层交付与真实加载方式

| 层 | 实际对象/入口 | 导入前准备 | 验收 |
|---|---|---|---|
| 专家 | expert_profile、persona、tools_whitelist、ExpertRevision | 专业范围、基础知识、方法、例题与工具需求 | 字段校验、正式创建/更新、读回 |
| 插件 | plugins/*/plugin.json + plugin.mjs；getTools() | 复用工具或最小新增只读工具、所需数据 | 工具注册、参数和返回、未知输入处理 |
| 技能 | 通过实际工具读取的研究工作规范 | 输入、适用问题、步骤、证据要求和输出 | 实际调用及分页完整性 |
| 知识库 | KnowledgeSpace → Document → 不可变 DocumentVersion → Chunk | 稳定逻辑键、sourceType、文本、来源和定位、哈希 | 正式入库、检索、引用还原 |
| 装备 | EquipmentVersion → sourceDocumentVersions；LoadoutRevision | 按用途组合文档、类型/槽位、目标专家 | 版本准确、装备读回、授权范围内检索 |
| 验收 | 真实工具与聊天轨迹 | 概念/比较/公司/原文/缺证据问题 | 数据正确、工具调用与专业回答分开报告 |

当前仓库可见 brokerage-skills 的 get_brokerage_skill 从 guides.json 分页读取规范，但这不是任意 SKILL.md 通用加载器。行业工作规范不要塞进无关券商技能；优先复用行业框架，确需按需技能时提供独立、名称清晰的只读工具，并加入专家白名单。Codex自身的 skill 与 FirmBuddy运行时工作技能不是同一注册体系。

## M12版本化知识与装备

以 src/knowledge/knowledge-service.mjs、src/storage/knowledge-repositories.mjs 和 src/server.mjs 为契约；docs/implementation/M12-KNOWLEDGE-EQUIPMENT-2026-09-15.md 仅为说明，执行以代码为准。

- createSpace 要求合法 scope。导入先按逻辑键/名称找到本次空间，避免重跑生成同名重复空间。
- ingestAttachment 使用受控附件；新增版本须传既有 documentId。仅相同内容但每次创建新文档不构成幂等。
- 文档来源类型如 research、regulator、company_manual、ai_generated；整理者生成的综合说明不能伪装成原始研究。
- 装备 type 与 Loadout slot：core_spec、regulatory、product_capability、case_experience、research、client_material、supplement。公开行业资料通常按原理、公司证据、研究和专利导航组合，不为凑槽位复制材料。
- sourceDocumentVersions 使用真实 {documentId, documentVersion}，在服务创建后回填；KB:documentId:vN:chunkId 只引用实际检索返回值。
- 装备升级新增版本；Loadout需要 expectedLoadoutRevision，与当前修订CAS匹配。409应重新读取并评估，不能盲目覆盖。客户空间资料不用于永久装备。
- search_knowledge 的组织/身份/专家范围由服务端注入，不能通过模型参数伪造。知识装备不能扩大工具权限。
- GET/POST /api/knowledge/spaces；GET/POST /api/knowledge/documents；POST /api/knowledge/documents/:id/versions；GET/POST /api/equipments；POST /api/equipments/:id/versions；GET /api/loadouts/expert/:expertId；POST /api/loadouts/equip。请求/返回字段以当前路由核对。

准备包应提供离线计划/预演模式、正式导入模式、映射状态文件和读回验证。尽量用现有 Service/API，不直接INSERT数据库或覆盖全部persona。离线测试可以使用独立临时数据库；不要因测试触碰用户现有运行库。

## 配置与接口

- `web/js/expert-profile.mjs` 的 `emptyExpertProfile`、`validateExpertProfile`、`expertProfilePayload`、`compileExpertProfile` 是前后端共用标准。注意字段长度，详细知识留在工具数据中。
- `EXPERT_CATEGORIES` 控制分类；大会场配色在 `web/js/experts-hall.js`。本次新增“行业研究系列”。
- `GET /api/agents/capabilities` 获取实际工具列表，校验白名单。
- `GET /api/personas` 查已有专家；`POST /api/agents` 创建、`PATCH /api/agents/:id` 更新。用 `expertProfilePayload(profile)` 构造请求。
- `POST /api/chat` 请求含 `message`、`expertId`，可选 `sessionId`。SSE 返回 `session`、`tool_call`、`tool_result`、`delta`、`done`、`error`。检查工具结果和回答，不能只看 HTTP 200。
- 大厅路由 `/#/experts`。图表工具可能自动加入白名单，不要误判为无关变化。

## 专业知识插件

`plugins/industry-research/` 提供 `get_industry_framework`（专业基础）、`search_industry_insights`（检索）、`read_industry_evidence`（原文上下文）、`industry_corpus_status`（覆盖）。读取工具接受检索 ID，可省略 `insight-` 前缀，不接受任意路径。

数据是 `data/frameworks.json` 与 `data/knowledge.json`。前者包含 frameworks 数组，后者包含 sources、insights、industries、coverage；洞见保留 claim、quote、context、conditions、source_id、locator。增量按稳定ID合并，保留其他行业；不要用七行业包覆盖用户原有知识。新行业扩展定义和筛选，不将未知行业默认归入量子计算。沿用普通 Agent 对话，不新增回答二次审查或机械删句。

行业插件的原文检索与M12 search_knowledge是不同加载路径：前者读取插件文件，后者依赖已装备DocumentVersion。选用其中一种或两者协同时明确权威源与同步关系，不能因为插件返回数据就宣称M12装备已导入。

## 已有构建脚本

- `scripts/industry-corpus.py` 及 legacy/OCR/archive 辅助脚本负责解析。包含本次路径假设，复用前参数化；不要盲目覆盖后补的清单和解析结果。
- `scripts/distill-industry.mjs` 按分块及输入哈希续跑语义整理。
- `scripts/industry-coverage.mjs` 对比来源、应读分块与实际记录，排除和未转写音频单列。
- `scripts/build-industry-knowledge.mjs` 核查摘录能命中原文，区分核对过的改写和直接摘录。
- `scripts/build-industry-experts.mjs` 按系统标准生成配置；随新行业调整定义和例题。
- `scripts/publish-industry-experts.mjs` 备份、创建/更新、读回分类与权限。
- `scripts/verify-industry-live.mjs` 保存实际 SSE 问答和工具结果；例题随行业调整。

`output/industry-distillation/` 保存清单、解析、分块记录、试答与发布记录。原始摘录和业务资料留在项目里，不随个人 skill 分发。

## 运行

核对实际服务及配置，不打印密钥。数据/插件可用 `POST /api/plugins/industry-research/reload` 热加载；分类等模块被缓存时才重启相应服务。先确认进程与工程归属，Windows 后台启动隐藏窗口。

本次 Windows 旧 `.doc` 用 Word 只读转换；`tar.exe` 的 RAR 列表采用 GB18030。它们是环境选择，不是所有系统的必需依赖。

## 公司技术识别

行业插件的 inspect_company_technology 按公司名和已核实简称检索明确提及该公司的技术原文，供专家推导路线、产品和特色。它不自动认证主体关系或技术路线。配合现有企业搜索、画像及专利接口核查；区分目标、竞品和供应商，区分研发与已推出产品，标注历史时点。专利标题和经营范围不能单独证明产品路线或独有优势。新工具需要加入专家白名单，并经实际对话验证。

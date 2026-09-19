# 七行业专家接入包 v0.3

这是一套已做真实Service离线验收的接入准备包。没有修改生产FirmBuddy、发布专家或执行LLM问答。原有具身智能数据保留。

## 已准备对象

|层|交付物|加载方式|
|---|---|---|
|专家|七行业expert-pack.json|使用目标工程expertProfilePayload生成正式API请求；运行时查重创建/更新|
|插件|technology-intelligence/|放入目标工程plugins；通过现有插件管理机制加载并核验capabilities|
|技能|七份research-method.md|插件get_technology_research_method按需读取；不是仅放置SKILL.md|
|知识库|import-bundle.json中的28份文档|受控附件→KnowledgeService.ingestAttachment→DocumentVersion→Chunk|
|装备|28个装备定义，每专家4件|core_spec、product_capability、research、supplement；绑定确定文档版本|
|验收|validation-result.json、56道evaluation题|离线真实Service已跑；模型回答题尚未运行|

插件使用独立名称和数据文件，不覆盖现有industry-research知识。其引用为source_id/URL。M12的search_knowledge只引用服务实际返回的KB标识。测试记录中的KB标识属于隔离测试数据库，不能复制为生产引用。

## 导入步骤

1. 核对目标工程提交、运行模式、实际组织、专家目录及`GET /api/agents/capabilities`。备份现有应用与数据库。选择停服维护窗口使用本Service导入器，或将同一计划接到现有HTTP流程。
2. 把`technology-intelligence/`整个目录安装为目标工程`plugins/technology-intelligence/`。已有同名插件时先比较版本并备份。按目标系统支持的方式加载，确认四个工具实际注册。
3. 在本knowledge仓库运行`node scripts/prepare-experts.mjs --firmbuddy <目标工程> --output <请求包文件>`。准备阶段仅校验配置；发布时必须用真实capabilities再校验工具。通过`POST /api/agents`或`PATCH /api/agents/:id`发布，按稳定名称查重；不直接覆盖personas.json。读回实际ID、分类和工具白名单。
4. 建立`expert-map.json`，键为`industry-<industry_id>`，值为步骤3读回的实际专家ID。不要沿用测试ID。
5. `node firmbuddy/import-knowledge.mjs`默认只显示计划，不打开数据库。正式执行：

```text
node firmbuddy/import-knowledge.mjs --apply --firmbuddy <目标工程> --db <明确的现有数据库> --org <实际组织> --expert-map <映射文件> --result <导入记录文件>
```

6. 读回每专家Loadout、文档与装备版本。重跑时按空间/文档/装备稳定名称和文档哈希复用；发现同名歧义则停止。更新文档生成新版本并更新本包装备，其他装备保留；CAS冲突不强制覆盖。操作失败后先检查导入记录和实际状态，再重跑。
7. 启动服务，用正式聊天接口执行各行业`research/evaluation.jsonl`。核查实际工具轨迹、引用、技术推导和缺证据处理；不能以离线检索PASS代替模型专业能力验收。

## 实际通过的验证

`scripts/test-firmbuddy.mjs`使用目标工程真实KnowledgeService、StorageService、SQLite迁移、分块器和检索器，数据库位于新建临时目录。验证七行业插件检索与技能读取、七专家配置字段、28份文档与28件装备、每专家4件装备、实际KB引用还原、重复导入幂等、文档与装备V2、旧版本分块保留、CAS冲突拒绝。没有使用模拟知识服务。

复验方式：设置`FIRMBUDDY_ROOT`指向目标工程，再运行`node scripts/test-firmbuddy.mjs`。如需保存记录设置`RESULT_FILE`。测试生成的临时数据库只用于验收。

## 资料范围

139个技术节点和42个机制/条件专题；原有104条行业内公司记录保留为公司池，不是104家新增验证公司。24条公司/交易所摘录核查；14篇书目中9篇已读摘要或部分正文，5篇仅书目；没有声称全文精读或系统综述。专利批量查询失败，检索计划和缺口透明保留。公司原有事实卡、阶段和法律主体关系并未全部重新认证。

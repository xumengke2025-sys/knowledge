# FirmBuddy 新专家构建方法论 v1.0

> 状态：**Canonical / 新建专家总装标准**  
> 日期：2026-09-22  
> 适用仓库：`xumengke2025-sys/knowledge`  
> 目标系统：FirmBuddy  
> 适用对象：行业专家、展业专家、科技情报专家，以及需要“长期知识 + 运行时事实 + 工具调用 + 证据治理”的专业智能体

---

## 0. 为什么需要这份方法论

本仓库此前已经形成了多套有效但分散的方法：

- `METHODOLOGY.md`：事实、公司、专利的基础研究口径；
- `DATA-GOVERNANCE.md`：数据与证据等级；
- `EXPERT-OS-V0.6.md`：行业专家操作系统；
- `ACADEMIC-GOVERNANCE.md`：已升级到 v0.9 的学术知识治理；
- `INDUSTRY-RADAR-V0.5.md`：行业动态发现与晋级；
- `firmbuddy/runtime-company-intelligence.json`：企业运行时取数；
- `firmbuddy/company-assessment-contract-v0.5.json`：企业研判输出契约；
- `firmbuddy/IMPORT-V0.6.md`：FirmBuddy 导入方法；
- 各行业 `taxonomy.json / benchmark.json / evidence-framework.json / company-assessment-playbook.md / expert-pack.json`：实际专家样板。

这些文件已经足以构成一套成熟方法，但它们属于不同版本，容易让后续 AI 或开发者误以为“复制一个 expert-pack + 塞几篇文档”就是建立专家。

**本文件将当前仓库截至 v0.9 的真实能力合并成一套完整的新专家构建标准。**

以后新建第 9、第 10 个专家时，默认以本文件为总纲；历史文件继续作为子规范和实现参考，但不再由执行者自行拼装整体方法。

---

# 1. 专家的定义

FirmBuddy 中的“专家”不是 Prompt，也不是一个知识库。

标准专家定义为：

```text
Expert
├─ 任务与边界
├─ 行业/领域 Taxonomy
├─ 长期稳定知识
│  ├─ Core
│  ├─ Academic
│  ├─ Benchmark
│  ├─ Evidence Framework
│  ├─ Playbook
│  ├─ Research
│  ├─ Patent Method
│  └─ Company Cases
├─ 持续更新能力
│  └─ Industry Radar
├─ 企业运行时事实
│  └─ Runtime Company Intelligence
├─ 工具权限
├─ 推理协议
├─ 输出契约
├─ 证据纪律
└─ Evaluation / Acceptance
```

公式化表达：

> **专家能力 = 长期行业先验 × 机制认知 × Benchmark × 证据纪律 × 运行时事实 × 工具调用 × 推理流程 × 验收闭环**

不允许使用以下简化定义：

> 专家 = Persona Prompt  
> 专家 = 文档数量  
> 专家 = 大模型 + RAG  
> 专家 = 爬取很多网页

---

# 2. 三条数据链必须分开

任何新专家都必须从一开始区分三条链。

## 2.1 长期知识链：写入 Knowledge Repo

负责相对稳定的行业先验：

- 技术原理；
- 产业链结构；
- Taxonomy；
- 科学机制；
- 技术路线；
- Benchmark；
- 标准与测试方法；
- 学术论文及研究机制；
- 专利导航方法；
- 证据升级规则；
- 企业研判 Playbook；
- 历史案例。

特点：

- 可以进入 GitHub；
- 可以进入 FirmBuddy Knowledge Equipment；
- 必须版本化；
- 必须有来源和适用边界；
- 不追求“今天的企业最新状态”。

## 2.2 Radar 链：持续发现，不直接变成事实

负责：

- 最新论文；
- 预印本；
- 新标准；
- 政策；
- 新专利；
- 科研项目；
- 产品发布；
- 认证；
- 客户验证；
- 中试/扩产；
- 订单/交付；
- 供应链变化。

Radar 默认状态：

`candidate_only`

**Radar 发现 ≠ 稳定知识。**

必须二次核验后才能晋级长期知识。

## 2.3 Runtime Company Intelligence：运行时取企业当前事实

负责具体企业当前状态：

- 企业主体；
- 年报；
- 公告；
- 财务；
- 专利；
- 资质；
- 新闻；
- 产业链；
- 政策项目；
- 近期事件。

这些数据默认不静态固化为“当前事实”。

原因：

> 企业事实会过期，而行业机制、Benchmark、测试方法和研究框架更适合长期装备。

因此分析某家公司时必须：

```text
Long-term Knowledge
        +
Runtime Company Data
        ↓
Company Assessment
```

---

# 3. 数据到底从哪里取

下面是当前标准数据源矩阵。

## 3.1 政策、监管、标准

### 中国官方优先源

- 工业和信息化部（MIIT）
- 市场监管总局 / 国家标准委
- 中国民航局（适用于低空/eVTOL）
- 证监会、交易所等与上市公司披露相关监管入口
- 行业主管部门官方网站

### 国际/行业标准

按行业使用：

- ISO
- IEC
- 3GPP
- IEEE 标准体系
- ASTM
- 其他行业正式标准组织

### 用于构建

- Taxonomy 边界；
- Benchmark 测试方法；
- Evidence Framework；
- 成熟度判断；
- Radar。

### 禁止

- “标准立项”写成“标准已实施”；
- “起草单位”写成“产品已达标”；
- 标准计划替代实际产品测试。

---

# 4. 上市公司事实从哪里取

## 4.1 长期历史事实

优先顺序：

### A 类

- 上交所；
- 深交所；
- 北交所；
- 巨潮资讯；
- 上市公司法定年报、半年报、临时公告；
- 交易所互动/业绩说明会中可追溯的正式材料；
- 监管部门公开记录。

### B 类

- 公司官网；
- 官方 IR；
- 官方技术白皮书；
- 公司正式产品文档；
- 行业协会；
- 科研机构。

### C 类

- 媒体；
- 券商报告；
- 商业数据库摘要；
- 行业研究机构二手报告。

规则：

> 核心公司结论原则上至少有一个 A 类来源。

## 4.2 FirmBuddy 运行时企业数据

标准工具链来自：

`firmbuddy/runtime-company-intelligence.json`

### 第 1 步：锁主体

首选：

`moss_company_search`

回退：

`search_company`

如果主体：

- ambiguous
- not_found
- unavailable

则不得猜测。

### 第 2 步：企业画像

首选：

`moss_company_profile`

回退：

`generate_company_profile`

确认：

- 法律主体；
- 股票代码；
- 统一社会信用代码；
- 核心子公司；
- 业务边界。

### 第 3 步：年报/技术披露

首选：

`moss_company_get_annual_reports`

回退：

`get_company_announcements`

### 第 4 步：专利

`moss_company_get_patents`

### 第 5 步：财务

首选：

`moss_company_get_listed_financial_data`

回退：

`get_financial_summary`

### 第 6 步：资质

`moss_company_get_certificates_v2`

### 第 7 步：产业链

`moss_industry_search_nodes`

→

`moss_industry_get_chain`

回退：

`get_industry_landscape`

### 第 8 步：近期事件

- `moss_company_get_news`
- `moss_public_opinion_search`

新闻只用于发现，关键结论回原始公告/监管/公司材料。

### 第 9 步：政策项目

`moss_policy_search_projects`

---

# 5. 学术资料从哪里取

当前已升级为 v0.9 学术体系。

## 5.1 历史全量 arXiv 主语料

主源：

`secemp9/arxiv-complete`

配置：

`sources/secemp-arxiv/source-config.json`

当前快照：

- metadata：2026-08-30；
- 文件镜像：2026-09-05。

### metadata

约 314 万篇论文。

用途：

- 标题；
- 摘要；
- 分类；
- DOI；
- 版本日期；
- license；
- arXiv 地址；
- 全量候选发现。

### paper_text

约 285 万篇。

用途：

- Method；
- Experiment；
- Result；
- Limitations；
- Benchmark；
- 指标；
- 失败模式；
- 章节级复核。

禁止：

> 因为 paper_text 存在就自动标记 sections_reviewed。

## 5.2 增量学术 Radar

SecEmp 是快照，因此新增论文由：

- OpenAlex
- Crossref
- Semantic Scholar
- PubScholar
- ChinaXiv

负责。

生命科学行业可进一步使用：

- PubMed
- PMC
- Europe PMC

## 5.3 学术阅读状态

固定状态机：

```text
metadata_only
      ↓
abstract_reviewed
      ↓
sections_reviewed
      ↓
full_text_reviewed
```

### metadata_only

只核实书目。

不得支持技术结论。

### abstract_reviewed

已读摘要。

只能支持摘要明确表达的结论。

### sections_reviewed

已阅读：

- 方法；
- 实验；
- Benchmark；
- 指标；
- 结果；
- 局限

等相关章节。

### full_text_reviewed

必须真实完成全文复核。

不能因模型抓取了全文而自动使用。

---

# 6. 学术数据如何变成专家知识

标准链路：

```text
SecEmp metadata
    ↓
secemp-query-pack.json
    ↓
arxiv-candidates.jsonl
    ↓
paper_text triage
    ↓
paper-evidence-candidates.jsonl
    ↓
reviewed manifest
    ↓
academic-papers.jsonl
    ↓
mechanisms.jsonl
    ↓
Section Review
    ↓
paper-section-notes.jsonl
    ↓
literature-map.json
frontier-topics.json
evaluation-academic.jsonl
    ↓
expert-knowledge.md
    ↓
FirmBuddy Academic Equipment
```

## 6.1 SecEmp candidate

命中检索条件只表示：

`candidate`

不得自动进入稳定知识。

## 6.2 Stable Review

目前使用：

`sources/secemp-arxiv/reviewed-v08.json`

只有明确复核论文才能进入：

`academic-papers.jsonl`

## 6.3 Section Review

目前使用：

`sources/secemp-arxiv/section-reviewed-v09.json`

章节复核至少记录：

- reviewed_sections
- method_note
- experiment_note
- baselines
- metrics
- key_findings
- limitations
- expert_questions
- cannot_infer
- secemp_text_sha256

---

# 7. 专利从哪里取

## 7.1 官方/权威源

- CNIPA 重点产业专利信息服务平台；
- WIPO PATENTSCOPE；
- EPO Espacenet。

## 7.2 FirmBuddy 运行时

`moss_company_get_patents`

## 7.3 专利进入专家知识前的最低处理

必须完成：

1. 申请人归一；
2. 上市主体/母公司/子公司边界；
3. 历史名称归一；
4. CN/WO/US/EP 专利族去重；
5. 发明/实用新型/外观分开；
6. 法律状态；
7. IPC/CPC + 关键词联合检索；
8. 摘要/权利要求人工或模型复核；
9. 映射 taxonomy 节点；
10. 标记检索日期。

禁止：

> 搜到 3000 件 = 3000 件核心专利。

禁止：

> 专利件数 = 技术实力排名。

---

# 8. Radar 从哪里取

每个行业必须有：

`radar-sources.json`

来源分为：

## 学术

- OpenAlex
- Crossref
- Semantic Scholar
- ChinaXiv
- PubScholar

## 专利

- CNIPA
- WIPO
- Espacenet

## 企业

- 上交所
- 深交所
- 北交所
- 巨潮资讯
- 公司官方 IR
- FirmBuddy MOSS

## 政策/标准

行业主管部门和标准组织。

## 新闻

只能作为：

`event discovery`

不能作为稳定事实默认来源。

---

# 9. 新专家构建总流程

下面是今后新建任何专家的标准工程步骤。

---

## Phase 0：定义 Expert Contract

先回答：

1. 这个专家服务谁？
2. 解决什么任务？
3. 不解决什么任务？
4. 研究对象是什么？
5. 时间边界是什么？
6. 企业范围是什么？
7. 是否需要公司研判？
8. 是否需要 Radar？
9. 是否需要 HTML 报告？
10. 允许调用哪些工具？

输出：

`expert-definition.md`（建议）

最低字段：

- name
- short_name
- audience
- scope
- boundaries
- primary_business_domain
- expected_outputs
- forbidden_outputs
- acceptance

原则：

> 先定义任务，再收集知识。

---

# 10. Phase 1：构建 Taxonomy

文件：

`industries/<industry>/taxonomy.json`

Taxonomy 应从：

- 标准；
- 监管文件；
- 经典综述；
- 代表性论文；
- 产业链；
- 专利 IPC/CPC；
- 产品/工程体系

综合构造。

它属于：

`editorial_synthesis`

不能伪装成某个单一来源原文。

每个节点至少包含：

```json
{
  "id": "node-id",
  "name": "节点名称",
  "parent_id": "parent-node-or-null",
  "description": "节点边界",
  "keywords": [],
  "comparison_metrics": []
}
```

验收：

- 一级路线互斥程度合理；
- 关键产品都有落点；
- 专利可映射；
- 论文可映射；
- 公司产品可映射；
- Benchmark 可挂载。

---

# 11. Phase 2：建立 Source Registry

文件：

`sources.json`

标准字段：

```json
{
  "id": "SOURCE-ID",
  "title": "",
  "publisher": "",
  "date": "",
  "type": "",
  "grade": "A|B|C",
  "url": "",
  "note": ""
}
```

所有稳定事实必须能解析到 source_id。

---

# 12. Phase 3：构建 Core Knowledge

Core 回答：

> 这个行业到底是怎么工作的？

不是回答：

> 哪家公司最强？

内容包括：

- 技术原理；
- 技术路线；
- 产业链；
- 系统结构；
- 关键瓶颈；
- 工程约束；
- 上下游关系；
- 关键测试条件。

输出建议：

`technical-dossier.md`

并最终编译为：

`<industry>:core`

Knowledge Equipment。

---

# 13. Phase 4：构建 Academic Layer

必须创建：

`research/`

建议标准目录：

```text
research/
├─ secemp-query-pack.json
├─ arxiv-candidates.jsonl
├─ paper-evidence-candidates.jsonl
├─ academic-papers.jsonl
├─ paper-section-notes.jsonl
├─ mechanisms.jsonl
├─ literature-map.json
├─ frontier-topics.json
├─ evaluation-academic.jsonl
└─ expert-knowledge.md
```

## 13.1 Query Pack

检索词必须映射 taxonomy。

禁止仅使用：

> 行业名称

必须覆盖：

- 技术路线；
- 关键机制；
- 测试；
- 失效；
- Benchmark；
- 工程化。

## 13.2 机制卡

`mechanisms.jsonl` 每条至少包括：

```json
{
  "id": "",
  "title": "",
  "node_ids": [],
  "mechanism": "",
  "measurable_variables": [],
  "evidence_to_seek": [],
  "expert_use": "",
  "false_inference": "",
  "support_paper_ids": [],
  "confidence": "",
  "as_of": ""
}
```

新增机制原则上至少两篇论文支持。

---

# 14. Phase 5：构建 Benchmark

文件：

`benchmark.json`

Benchmark 回答：

> 企业说“性能很好”，到底应该看什么？

每个 dimension 包含：

- metric；
- unit；
- required_conditions；
- interpretation；
- evidence_priority；
- expert_rule。

原则：

> Benchmark 不应只有参数，而必须带测试条件。

例如：

“任务成功率 95%”

没有以下信息时不可直接比较：

- 任务集；
- 初始条件；
- 样本数；
- 重试策略；
- 硬件；
- 环境；
- 是否真实系统。

---

# 15. Phase 6：Evidence Framework

文件：

- `evidence-framework.json`
- `evidence-framework.md`

内容：

1. 标准；
2. 测试方法；
3. 科研机构；
4. Radar query；
5. 企业运行时核查问题；
6. 证据升级规则；
7. 禁止外推。

核心状态转换：

```text
radar_candidate
      ↓
stable_industry_knowledge
```

必须满足：

- 原始来源可访问；
- taxonomy 可落位；
- 测试/实验条件明确；
- 完成必要阅读；
- 确认相对既有知识发生了什么变化。

---

# 16. Phase 7：Company Universe

文件：

`company-universe.json`

等级：

### T1 / verified_core

一手来源明确披露目标行业核心技术/产品/收入/验证。

### T2 / verified_supply_chain

可验证关键供应链关系。

### T3 / candidate

能力匹配但证据不足。

### excluded

已证伪或相关性不足。

原则：

> candidate 永远不能自动训练成“企业事实”。

---

# 17. Phase 8：Stable Company Facts

文件：

`facts.jsonl`

标准字段：

```json
{
  "fact_id": "",
  "industry": "",
  "topic": "",
  "statement": "",
  "as_of": "",
  "source_ids": [],
  "confidence": "high|medium|low",
  "fact_type": "",
  "notes": ""
}
```

公司事实写入规则：

> 来源写到哪一级，事实最多写到哪一级。

---

# 18. Phase 9：成熟度模型

全局参考：

```text
概念/规划
→ 预研
→ 研发
→ 样机/产品发布
→ 送样
→ 客户验证
→ 定点/合同
→ 小批量
→ 批量
→ 规模化
```

但每个行业应进一步建立自己的：

`M0–M6`

行业特定模型。

例如具身智能：

- M0：基础研究
- M1：部件/算法原型
- M2：整机集成样机
- M3：客户/场景验证
- M4：小批量
- M5：重复批量与多客户
- M6：稳定规模化

禁止跨级推断。

---

# 19. Phase 10：Patent Method

文件：

`patent-search.md`

包含：

- IPC/CPC；
- 关键词；
- 同义词；
- 排除词；
- applicant normalization；
- family rules；
- legal status；
- 结果抽样；
- taxonomy mapping。

Patent Method 是方法装备，不是专利数量排行榜。

---

# 20. Phase 11：Company Assessment Playbook

文件：

`company-assessment-playbook.md`

目标：

> 给专家一家公司后，它知道下一步该干什么。

固定循环：

```text
主体锁定
→ 运行时取数
→ taxonomy 映射
→ 机制解释
→ Benchmark
→ 成熟度
→ 专利结构
→ 财务交叉验证
→ 近12个月变化
→ 强项
→ 未知/反证
→ 下一步补证
```

输出至少包括：

- 技术位置；
- 当前成熟度；
- 可确认强项；
- 关键未知；
- 最近变化；
- 相对位置；
- 下一步补证。

---

# 21. Phase 12：财务—技术交叉验证

文件建议：

`financial-technology-signals.json`

关注：

- 研发费用；
- 研发人员；
- 资本化研发；
- 在建工程；
- 固定资产；
- 存货；
- 产品收入；
- 分部收入；
- 毛利；
- 现金流；
- 应收；
- 合同资产；
- 客户集中度。

原则：

> 财务用于验证产业化，不证明技术先进性。

---

# 22. Phase 13：Industry Radar

文件：

`radar-sources.json`

每个 signal 至少包括：

- event_date
- discovered_at
- source
- source_type
- url
- taxonomy_nodes
- signal_type
- evidence_level
- what_changed
- why_it_matters
- benchmark_impact
- affected_routes
- company_entities
- verification_status
- promote_to_stable_knowledge

更新频率建议：

- 企业/政策：日/周；
- 学术：周；
- 专利：月；
- 稳定框架：重大变化或季度。

---

# 23. Phase 14：Expert Pack

文件：

`expert-pack.json`

这是专家行为契约。

至少包含：

## 展示层

- id
- name
- short_name
- category
- subtitle
- avatar
- tags
- quick_questions
- output_hint

## Expert Profile

- audience
- scope
- boundaries
- method
- criteria
- clarifications
- knowledge
- sources
- tools
- evidence
- outputStyle
- outputRequirements
- acceptance
- businessDomain

## 运行时能力

- runtime_company_intelligence
- radar_mode

原则：

> 新专家复制字段结构，不复制其他行业内容。

---

# 24. Phase 15：训练集与评测集

文件：

`training-set.jsonl`

训练重点：

- taxonomy；
- company mapping；
- evidence；
- temporal；
- patent；
- stage；
- candidate boundary；
- comparison；
- boundary。

必须大量加入：

> 错误诱导题。

例如：

- “有 3000 件专利，是不是技术第一？”
- “研发项目进行中，是不是量产？”
- “某论文作者来自某企业，是不是企业已经掌握？”
- “行业市场高速增长，是不是某公司收入会增长？”

专家必须拒绝错误外推。

学术层单独使用：

`research/evaluation-academic.jsonl`

---

# 25. Phase 16：八件标准 Knowledge Equipment

新行业专家标准目标为八件长期装备：

1. **Core**
2. **Academic**
3. **Benchmark**
4. **Evidence Framework**
5. **Playbook**
6. **Research**
7. **Patent Method**
8. **Company Cases**

注意：

> 仓库中部分早期专家/导入包仍保留历史版本差异。新专家不得复制历史装备数量；本 v1.0 规定的八件装备为新建专家规范目标。

---

# 26. Phase 17：FirmBuddy Plugin / Runtime Contract

专家不是只靠 Knowledge。

必须确认 FirmBuddy 当前可用 capability。

不能直接相信旧：

`firmbuddy/target-contract.json`

因为它记录的是历史 FirmBuddy commit。

正式接入前必须重新检查：

`GET /api/agents/capabilities`

并把工具白名单和实际 capability 对齐。

FirmBuddy 技术情报插件目前包括：

`technology-intelligence`

其职责是：

- 行业框架；
- 研究方法；
- 证据读取；
- Radar；
- 与 Knowledge Equipment 分层使用。

---

# 27. Phase 18：生成 Expert API Payload

使用：

```bash
node scripts/prepare-experts.mjs   --firmbuddy <FIRMBUDDY_ROOT>   --output <expert-payloads.json>
```

该脚本：

1. 读取行业 `expert-pack.json`；
2. 调用 FirmBuddy 当前 `expert-profile.mjs`；
3. 验证字段；
4. 生成真实 API payload；
5. 输出所需 tools。

注意：

> prepared ≠ published。

---

# 28. Phase 19：构建 Knowledge Import Bundle

文件：

`firmbuddy/import-bundle.json`

每个 document 至少：

- logical_key
- industry_id
- title
- sourceType
- text
- sha256
- tags
- space_key

每个 equipment 至少：

- logical_key
- name
- type
- slot
- document_keys
- expert_key
- business domain
- expert category
- export policy

必须使用稳定 logical_key，支持：

- 幂等导入；
- 版本更新；
- 文档替换；
- Loadout 重建。

---

# 29. Phase 20：导入 FirmBuddy

正式导入：

```bash
node firmbuddy/import-knowledge.mjs   --apply   --firmbuddy <FIRMBUDDY_ROOT>   --db <EXISTING_DB>   --org <ORG_ID>   --expert-map <expert-map.json>   --result <import-result.json>
```

必须：

1. 备份数据库；
2. 使用真实组织；
3. 读取真实 Expert ID；
4. 建立 `expert-map.json`；
5. 禁止复制测试 ID；
6. 导入后读回文档版本；
7. 读回 Equipment；
8. 读回 Loadout。

---

# 30. Phase 21：企业研判输出契约

以：

`firmbuddy/company-assessment-contract-v0.5.json`

为当前基础契约。

标准输出结构包括：

1. subject
2. industry_mapping
3. quick_conclusion
4. technology_routes
5. benchmark_comparison
6. patent_profile
7. financial_cross_checks
8. recent_changes
9. relative_position
10. evidence_gaps
11. sources

证据标签：

- fact
- company_claim
- academic_evidence
- radar_candidate
- inference
- unknown

---

# 31. Phase 22：真实验收

新专家不能以：

> JSON 校验通过

作为完成。

必须跑真实问题。

至少选：

### 3 类企业

1. 行业核心公司；
2. 供应链公司；
3. 容易被误判为概念股的公司。

### 每家公司测试

- 主体锁定；
- 技术落位；
- 年报调用；
- 专利调用；
- 财务调用；
- Benchmark；
- 成熟度；
- 反证；
- 未知项；
- 最近变化。

### 再测试行业问题

- 技术路线；
- 最新论文；
- Radar；
- Benchmark；
- 路线对比；
- 标准变化。

---

# 32. HTML 报告验收

如果专家定位包含“正式研究报告”，必须测试：

- 结构化回答；
- HTML preview；
- HTML export；
- 来源引用；
- 长文分页/导航；
- 表格；
- 企业—技术路线矩阵。

不要只验收聊天文本。

---

# 33. 验收门槛

一个新专家只有全部满足以下条件才算“可用”。

## A. Knowledge

- Taxonomy 完成；
- Core 完成；
- Academic 完成；
- Benchmark 完成；
- Evidence Framework 完成；
- Playbook 完成；
- Patent Method 完成；
- Radar 完成。

## B. Evidence

- 关键事实 source_id 可解析；
- company candidate 不冒充 verified；
- 论文阅读状态真实；
- 专利不按数量排名；
- 成熟度不升级。

## C. Runtime

- tools whitelist 与 FirmBuddy capability 一致；
- 主体可以锁定；
- 年报/专利/财务至少可用；
- 工具失败会保留 unknown，而不是猜。

## D. FirmBuddy

- Expert 正式发布；
- Expert ID 读回；
- Knowledge Equipment 导入；
- Loadout 正确；
- 搜索可命中；
- 引用可追溯。

## E. Evaluation

- 行业题通过；
- 企业题通过；
- 反诱导题通过；
- 至少指出一个重要未知或反证条件；
- 不声称调用未调用的数据源。

---

# 34. 标准目录模板

一个新行业建议最终目录：

```text
industries/<industry-id>/
├─ README.md
├─ taxonomy.json
├─ sources.json
├─ facts.jsonl
├─ company-universe.json
├─ company-cards/
├─ benchmark.json
├─ evidence-framework.json
├─ evidence-framework.md
├─ company-assessment-playbook.md
├─ financial-technology-signals.json
├─ patent-search.md
├─ patents/
├─ radar-sources.json
├─ radar/
├─ expert-pack.json
├─ training-set.jsonl
└─ research/
   ├─ secemp-query-pack.json
   ├─ arxiv-candidates.jsonl
   ├─ paper-evidence-candidates.jsonl
   ├─ academic-papers.jsonl
   ├─ paper-section-notes.jsonl
   ├─ mechanisms.jsonl
   ├─ literature-map.json
   ├─ frontier-topics.json
   ├─ evaluation-academic.jsonl
   └─ expert-knowledge.md
```

---

# 35. 各文件到底从哪条数据链产生

| 文件 | 主要数据源 | 类型 |
|---|---|---|
| taxonomy.json | 标准、综述、技术文献、产业链、IPC/CPC | 长期 |
| sources.json | 原始来源登记 | 长期 |
| facts.jsonl | 交易所/年报/监管/公司正式资料 | 长期历史事实 |
| company-universe.json | 交易所+产业链+候选发现 | 候选+稳定 |
| benchmark.json | 标准、论文、可比测试 | 长期 |
| evidence-framework.json | 标准、监管、科研机构 | 长期 |
| patent-search.md | CNIPA/WIPO/EPO + taxonomy | 方法 |
| academic-papers.jsonl | SecEmp/OpenAlex/Crossref 等 | 长期 |
| mechanisms.jsonl | 多篇已复核论文 | 长期 |
| paper-section-notes.jsonl | SecEmp paper_text + 原文章节 | 长期深读 |
| radar-sources.json | 学术/专利/政策/企业源 | 更新规则 |
| radar/* | Radar 发现 | candidate |
| company-assessment-playbook.md | 专家研判流程 | 方法 |
| financial-technology-signals.json | 年报/财务口径 | 方法 |
| expert-pack.json | 以上全部方法与权限汇总 | 专家契约 |
| import-bundle.json | 稳定知识文档编译 | FirmBuddy |
| 企业实时结论 | MOSS/公告/财务/专利 | Runtime |

---

# 36. 数据晋级总状态机

```text
RAW SOURCE
   ↓
SOURCE REGISTRY
   ↓
CANDIDATE
   ↓
VERIFIED / REVIEWED
   ↓
STABLE KNOWLEDGE
   ↓
KNOWLEDGE EQUIPMENT
   ↓
EXPERT REASONING
```

不同对象有各自子状态。

## 公司

```text
candidate
↓
verified_supply_chain
or
verified_core
```

## 学术

```text
metadata_only
↓
abstract_reviewed
↓
sections_reviewed
↓
full_text_reviewed
```

## Radar

```text
radar_candidate
↓
secondary verification
↓
stable_industry_knowledge
```

## 专利

```text
search hit
↓
assignee normalization
↓
family/legal review
↓
technical relevance
↓
technology evidence
```

---

# 37. 新专家建设时最重要的禁止事项

1. 不把行业趋势写成公司事实。
2. 不把论文结果写成公司能力。
3. 不把论文作者单位写成供应链关系。
4. 不把 candidate 写成 confirmed。
5. 不把专利件数写成技术排名。
6. 不把“有产线”写成“稳定量产”。
7. 不把“送样”写成“订单”。
8. 不把“订单”写成“规模收入”。
9. 不把财务收入增长直接归因某技术。
10. 不把 Radar 热点写成稳定趋势。
11. 不把模型机器预审写成 sections_reviewed。
12. 不用历史 Company Case 替代企业当前事实。
13. 不在 Runtime 工具没有返回时补零或猜数。
14. 不引用未实际读取的数据源。
15. 不因导入脚本成功就宣布专家专业能力验收通过。

---

# 38. 推荐自动化命令

## SecEmp 候选

```bash
python scripts/secemp-arxiv.py discover   --industry <industry-id>   --source metadata   --limit 120
```

## SecEmp 全行业

```bash
python scripts/secemp-arxiv.py discover-all   --source metadata   --limit 120
```

## paper_text

```bash
python scripts/secemp-arxiv.py fetch-text   --paper-id <ARXIV_ID>   --out .cache/secemp-arxiv/paper-text.jsonl
```

## 学术 Radar

使用：

`scripts/refresh-academic-radar.py`

## Expert Payload

```bash
node scripts/prepare-experts.mjs   --firmbuddy <PATH>   --output <FILE>
```

## FirmBuddy 验收

```bash
FIRMBUDDY_ROOT=<PATH> node scripts/test-firmbuddy.mjs
```

## Knowledge 导入

使用：

`firmbuddy/import-knowledge.mjs`

---

# 39. 当前仓库版本兼容说明

本文件为 **v1.0 方法论标准**。

当前仓库仍包含历史版本号：

- Expert OS：v0.6；
- FirmBuddy Import：v0.6；
- Radar：v0.5.x；
- Academic：v0.9；
- Company Assessment：v0.5.2；
- Plugin：v0.5.2。

这些版本反映各子系统独立演进，不意味着新专家只能按最低版本构建。

**新专家必须按照本 v1.0 总装标准构建，并采用各子系统当前最新规则。**

特别注意：

`firmbuddy/target-contract.json`

记录的是历史 FirmBuddy commit 与隔离环境验收。

正式生产接入前必须重新扫描最新 FirmBuddy：

- expert profile schema；
- capabilities；
- plugin contract；
- Knowledge Service；
- database migration；
- HTML report/export 能力。

禁止把历史 target-contract 当成永久 API 契约。

---

# 40. Definition of Done

一个新专家只有达到以下状态才算完成：

> **它不只是知道行业资料，而是能用稳定行业知识解释机制，用 Benchmark 判断可比性，用 Evidence Framework 限制外推，用 Runtime 工具获取企业当前事实，再按明确 Playbook 输出可追溯的企业研判。**

最终验收问题不是：

> “它背了多少文档？”

而是：

> **“面对一家真实企业，它是否知道该查什么、从哪里查、怎么判断、什么不能判断，以及还缺什么证据？”**

这就是 FirmBuddy v1.0 新专家的标准。

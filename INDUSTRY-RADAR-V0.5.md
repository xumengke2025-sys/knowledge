# Industry Radar 运行规范 v0.5

## 目标
行业专家不仅知道“行业是什么”，还要能解释“最近发生了什么、为什么重要、是否改变原有判断”。

## 两阶段机制
### 发现层
按 `industries/<industry>/radar-sources.json` 的渠道和查询包持续发现：
- 政策与监管
- 国家/行业/国际标准
- 同行评议论文、预印本、数据集
- 专利与专利族
- 科研项目与机构成果
- 产品发布与技术演示
- 认证/适航/客户验证
- 中试/扩产/产线
- 订单/交付
- 关键团队与供应链变化

### 稳定知识层
只有完成二次核验的重大信号才升级为长期知识。升级必须回答：
1. 落在哪个 taxonomy 节点？
2. 是新机制、新性能、工程化、产业化还是商业事件？
3. 与既有 benchmark 的哪一维有关？
4. 是单点结果还是多源/可复现证据？
5. 会改变哪条行业判断？改变条件是什么？

## 信息源策略
- **标准/监管**：工信部、市场监管总局/国家标准委、民航局、ISO/IEC/3GPP等。
- **学术**：OpenAlex做发现与图谱，Crossref校验DOI，Semantic Scholar补引用关系；中文科研用PubScholar/ChinaXiv；生命科学可扩展PubMed/PMC/Europe PMC。
- **专利**：CNIPA重点产业平台为中国重点产业入口，WIPO/EPO做专利族与国际交叉核验。
- **企业**：交易所/巨潮/公司法定披露优先；FirmBuddy MOSS做运行时聚合与主体化查询。
- **新闻**：只作为事件发现；关键技术/交付/产能结论回到一手来源。

## 输出格式
每个Radar信号至少包含：
- event_date / discovered_at
- source / source_type / url
- taxonomy_nodes
- signal_type
- evidence_level
- what_changed
- why_it_matters
- benchmark_impact
- affected_routes
- company_entities（若有）
- verification_status
- promote_to_stable_knowledge: true/false

## 更新频率
政策/标准/企业事件：日/周；学术与预印本：周；专利族：月；稳定行业框架：重大变化触发或季度复核。

## 红线
热点不等于趋势；单篇论文不等于路线胜出；专利申请不等于产品；项目立项不等于量产；媒体转载不构成多源验证。

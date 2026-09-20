# v0.5 行业专家操作系统质量报告

日期：2026-09-20

## 目标
把8个行业专家从“行业资料问答”升级为“行业先验 + 运行时企业证据”的企业快速研判专家。

## 新增
- 8份Technology Benchmark；每项指标都要求绑定测试对象、环境、负载、测量方法和样本条件。
- 8份Company Assessment Playbook；统一主体锁定→年报→专利→财务→资质→产业链→近期事件→政策的只读取数链。
- 8份Radar Source Catalog；覆盖监管/标准、论文/预印本、专利、交易所/企业、科研机构和新闻信号。
- 每位专家新增两件知识装备：benchmark(core_spec) + playbook(supplement)。
- 专家白名单新增运行时企业只读工具，不加入联系方式、任务、商机状态变更等高敏感/有副作用工具。

## 设计边界
长期知识不追求记住全部企业。企业当前专利、年报、财务、新闻和产业链由FirmBuddy运行时获取。旧公司案例用于校准分析方法，不自动代表当前企业状态。

## 验收
运行 scripts/validate-v05.py。正式FirmBuddy还需在目标运行环境核验MCP是否连接、实际工具capability以及企业问答轨迹。

## FirmBuddy 实际兼容验收

已在 FirmBuddy 当前代码基线（测试前父提交 `8b6d49958ffc49e80f80be0c6c798689997932c1`）的 GitHub Actions 中执行真实隔离集成测试，运行结果 **PASS**（run `35477219129`）。

- 52 份 Knowledge Documents、52 件 Knowledge Equipments 导入临时 SQLite 成功。
- 8 位行业专家均建立 Loadout；每位都包含 academic、benchmark、playbook 等预期装备。
- 8 行业均通过目标工程真实 `KnowledgeService.search` 返回可还原的 `KB:` citation。
- 16 个企业运行时只读工具名均在目标 FirmBuddy 当前工具目录/MOSS 工具目录中得到验证。
- 7 个高敏感/有业务副作用工具明确不在行业专家白名单。
- 重复导入幂等、文档/装备版本升级、历史 chunks 保留、CAS 冲突拒绝均通过。

机器可读结果：`firmbuddy/validation-result-v0.5.json`。

### 仍未执行
- 未连接生产 MOSS 实例实际查询某一家企业，因此“工具存在”不等于生产数据源此刻在线。
- 未把 v0.5 导入生产 FirmBuddy 数据库。
- 未执行真实 LLM 的完整企业问答回归；当前证明的是知识装备、工具授权和检索链路兼容。


## v0.5.1 行业化深化
- 8行业均新增行业特定成熟度模型，避免用同一“研发/验证/量产”口径跨行业误判。
- 8行业均新增财务—技术交叉信号，用研发、存货、在建工程、应收、毛利、现金流等验证产业化，但禁止以财务单独证明技术先进性。

## v0.5.2 Radar运行时接入
- technology-intelligence插件增加get_industry_radar，只读返回近期candidate前沿信号。
- 8位专家均加入Radar工具和Radar研判协议；candidate未二次核验前不得升级为稳定知识或企业事实。
- Playbook成为装备内容，因此Radar使用规则随专家Loadout进入FirmBuddy。

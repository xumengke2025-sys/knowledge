# 第三代/宽禁带半导体｜学术机制与研究证据

> 用途：FirmBuddy 行业专家的 `research` 知识装备。本文把论文转化为可检索的机制知识；论文是证据，不是需要背诵的答案。
> 边界：学术结果不能单独证明某家上市公司已量产、已获订单或具备同等性能；涉及公司事实仍需回到法定披露/公司证据装备。

## 使用规则

1. 先定位技术节点，再解释机制；性能数字必须带测试条件。
2. 综述用于建立问题框架，单篇实验用于解释特定机制；两者不能替代公司产业化证据。
3. `metadata_only` 文献只能做检索线索，不得支持技术结论。
4. 学术机制与专利权利要求、上市公司披露相互验证，但不得互相替代。

## WBG-M01｜衬底缺陷通过外延和器件区域放大为良率与可靠性问题

**技术节点**：crystal-growth, substrate, sic-epitaxy

**机制**：SiC晶体中的位错、微管、基面缺陷和表面损伤会影响外延缺陷、器件有效面积和可靠性。大尺寸化提高理论产出，但也放大温场、应力和晶圆均匀性控制难度。

**应观察变量**：缺陷密度；晶圆翘曲；厚度均匀性；外延缺陷；有效芯片数；良率

**补证重点**：晶体/衬底质量指标；外延后缺陷转化；客户验证；量产良率

**专家如何使用**：讨论8/12英寸路线时必须把面积优势与良率、设备和材料利用率一起看。

**禁止外推**：发布大尺寸样片不能直接等同稳定量产或成本下降。

**主要学术支持**：
- `WBG-P06` [Silicon carbide MOSFETs: A critical review of applications, technological advancements, and future perspectives](https://doi.org/10.1016/j.micrna.2025.208126)；abstract_reviewed。综合制造、器件结构、可靠性和应用演进，为SiC MOSFET技术节点梳理提供参考。

## WBG-M02｜SiC MOS界面决定沟道迁移率和阈值稳定性，是器件可靠性核心

**技术节点**：sic-mosfet, qualification

**机制**：SiC/SiO2界面态和栅氧质量影响沟道迁移率、阈值漂移、栅极可靠性和长期稳定。平面/沟槽结构还要权衡单元密度与栅氧电场。

**应观察变量**：阈值漂移；栅漏电；沟道迁移率；BTI；短路耐受时间；雪崩能力

**补证重点**：高温栅偏/负偏测试；短路/雪崩测试；统计样本量

**专家如何使用**：公司披露低Ron时仍需追问栅可靠性和短路鲁棒性。

**禁止外推**：室温静态Ron低不能证明车规寿命更好。

**主要学术支持**：
- `WBG-P02` [Review and Outlook on GaN and SiC Power Devices: Industrial State-of-the-Art, Applications, and Perspectives](https://doi.org/10.1109/TED.2023.3346369)；abstract_reviewed。比较商用SiC/GaN器件结构、应用和可靠性，包括GaN动态Ron/阈值稳定性及SiC栅氧/短路问题。
- `WBG-P05` [Degradation mechanism and reliability tests for silicon carbide power MOSFETs: challenges and progress](https://doi.org/10.1016/j.chip.2025.100188)；abstract_reviewed。综述SiC MOSFET芯片与封装层面的退化机制、阈值电压、栅漏电等可靠性评价。

## WBG-M03｜GaN陷阱效应使动态Ron与静态Ron不是同一件事

**技术节点**：gan-hemt

**机制**：高电场关态可引发陷阱充放电，开通后表现为动态导通电阻升高；测试延迟、偏置、电压和温度都会改变观测结果。

**应观察变量**：静态Ron；动态Ron；关态应力电压；恢复时间；阈值漂移

**补证重点**：动态双脉冲方法；测试延迟；温度与电压；器件结构

**专家如何使用**：评价GaN产品时必须看动态条件和栅结构。

**禁止外推**：数据表静态Ron不能直接代表高频变换器真实损耗。

**主要学术支持**：
- `WBG-P01` [Characterisation and Modeling of Gallium Nitride Power Semiconductor Devices Dynamic On-State Resistance](https://doi.org/10.1109/TPEL.2017.2730260)；sections_reviewed。把GaN HEMT动态导通电阻与关态偏置、陷阱捕获/释放时间联系起来，说明静态数据表不足以描述开关工作状态。
- `WBG-P02` [Review and Outlook on GaN and SiC Power Devices: Industrial State-of-the-Art, Applications, and Perspectives](https://doi.org/10.1109/TED.2023.3346369)；abstract_reviewed。比较商用SiC/GaN器件结构、应用和可靠性，包括GaN动态Ron/阈值稳定性及SiC栅氧/短路问题。

## WBG-M04｜高速开关把封装寄生、电磁兼容和热设计推到系统瓶颈

**技术节点**：advanced-package, module

**机制**：SiC/GaN的高dv/dt和di/dt使寄生电感、电容、共模电流和门极振荡更敏感；更小芯片面积又提高热流密度。

**应观察变量**：回路寄生电感；dv/dt；di/dt；热阻；结温；功率循环寿命；EMI

**补证重点**：模块布局；双面散热/烧结互联；功率循环和温循；系统EMI

**专家如何使用**：不能只比较芯片额定值；模块和系统集成决定可用工作区。

**禁止外推**：“采用SiC芯片”不等于系统效率和可靠性自动领先。

**主要学术支持**：
- `WBG-P03` [Industry perspective on power electronics for electric vehicles](https://www.nature.com/articles/s44287-024-00055-4)；abstract_reviewed。从器件、变换器和模块讨论Si/SiC/GaN在800V电驱、OBC/DC-DC中的效率、成本和可靠性权衡。
- `WBG-P04` [Packaging and integration of silicon carbide power devices](https://www.nature.com/articles/s44287-026-00263-0)；abstract_reviewed。聚焦SiC高温高压、高速开关和高热流密度下的封装材料、互联、电磁和散热挑战。
- `WBG-P07` [Conventional, wide-bandgap, and hybrid power converters: A comprehensive review](https://doi.org/10.1016/j.rser.2025.115419)；abstract_reviewed。从开关器件到系统级变换器比较Si、SiC、GaN及混合方案的效率、热管理、成本和可靠性。

## WBG-M05｜系统效率收益依赖开关频率、拓扑和磁性/散热的协同设计

**技术节点**：module, qualification

**机制**：高频开关可减小磁性器件和被动件，但开关损耗、驱动损耗、EMI和热管理同时变化。SiC和GaN在不同电压/功率区间的优势不同。

**应观察变量**：效率地图；开关频率；功率密度；器件损耗分解；磁性件体积；冷却能力

**补证重点**：同一拓扑/负载/温度的A-B比较；系统体积和成本；效率全工况

**专家如何使用**：评价车载或储能应用时使用系统级效率地图，不只看器件峰值。

**禁止外推**：材料理论优值不能直接等同整机续航提升。

**主要学术支持**：
- `WBG-P03` [Industry perspective on power electronics for electric vehicles](https://www.nature.com/articles/s44287-024-00055-4)；abstract_reviewed。从器件、变换器和模块讨论Si/SiC/GaN在800V电驱、OBC/DC-DC中的效率、成本和可靠性权衡。
- `WBG-P07` [Conventional, wide-bandgap, and hybrid power converters: A comprehensive review](https://doi.org/10.1016/j.rser.2025.115419)；abstract_reviewed。从开关器件到系统级变换器比较Si、SiC、GaN及混合方案的效率、热管理、成本和可靠性。

## WBG-M06｜车规/工业可靠性要从加速应力映射到真实任务谱

**技术节点**：qualification

**机制**：HTGB/HTRB、功率循环、温度循环、短路与雪崩等加速测试分别覆盖不同失效机制，实际寿命还取决于结温波动和任务谱。

**应观察变量**：应力电压；温度；循环次数；结温摆幅；失效率；寿命模型参数

**补证重点**：AEC-Q/客户规范；任务谱；Weibull/寿命模型；失效解析

**专家如何使用**：公司宣称通过某项可靠性测试时，应明确测试对象、条件和覆盖的失效机制。

**禁止外推**：单一测试通过不能证明所有车规工况和寿命目标。

**主要学术支持**：
- `WBG-P02` [Review and Outlook on GaN and SiC Power Devices: Industrial State-of-the-Art, Applications, and Perspectives](https://doi.org/10.1109/TED.2023.3346369)；abstract_reviewed。比较商用SiC/GaN器件结构、应用和可靠性，包括GaN动态Ron/阈值稳定性及SiC栅氧/短路问题。
- `WBG-P05` [Degradation mechanism and reliability tests for silicon carbide power MOSFETs: challenges and progress](https://doi.org/10.1016/j.chip.2025.100188)；abstract_reviewed。综述SiC MOSFET芯片与封装层面的退化机制、阈值电压、栅漏电等可靠性评价。

## 论文清单与阅读边界

### WBG-P01｜Characterisation and Modeling of Gallium Nitride Power Semiconductor Devices Dynamic On-State Resistance
- 年份：2018；类型：journal-article；阅读状态：`sections_reviewed`
- 标识：10.1109/TPEL.2017.2730260
- 研究卡：把GaN HEMT动态导通电阻与关态偏置、陷阱捕获/释放时间联系起来，说明静态数据表不足以描述开关工作状态。
- 局限：结果依赖具体器件和测试条件，不能推广到所有GaN路线。
- 技术节点：gan-hemt

### WBG-P02｜Review and Outlook on GaN and SiC Power Devices: Industrial State-of-the-Art, Applications, and Perspectives
- 年份：2024；类型：journal-review；阅读状态：`abstract_reviewed`
- 标识：10.1109/TED.2023.3346369
- 研究卡：比较商用SiC/GaN器件结构、应用和可靠性，包括GaN动态Ron/阈值稳定性及SiC栅氧/短路问题。
- 局限：综述跨产品比较仍需统一电压、温度、频率和封装条件。
- 技术节点：sic-mosfet, gan-hemt, qualification

### WBG-P03｜Industry perspective on power electronics for electric vehicles
- 年份：2024；类型：journal-review；阅读状态：`abstract_reviewed`
- 标识：10.1038/s44287-024-00055-4
- 研究卡：从器件、变换器和模块讨论Si/SiC/GaN在800V电驱、OBC/DC-DC中的效率、成本和可靠性权衡。
- 局限：行业视角不能替代单一厂商的车规认证、良率和成本数据。
- 技术节点：sic-mosfet, gan-hemt, module

### WBG-P04｜Packaging and integration of silicon carbide power devices
- 年份：2026；类型：journal-review；阅读状态：`abstract_reviewed`
- 标识：10.1038/s44287-026-00263-0
- 研究卡：聚焦SiC高温高压、高速开关和高热流密度下的封装材料、互联、电磁和散热挑战。
- 局限：封装方案必须结合功率循环、绝缘和热循环验证，不能仅凭低寄生设计判断寿命。
- 技术节点：advanced-package, module

### WBG-P05｜Degradation mechanism and reliability tests for silicon carbide power MOSFETs: challenges and progress
- 年份：2026；类型：journal-review；阅读状态：`abstract_reviewed`
- 标识：10.1016/j.chip.2025.100188
- 研究卡：综述SiC MOSFET芯片与封装层面的退化机制、阈值电压、栅漏电等可靠性评价。
- 局限：寿命与退化参数依赖应力条件，不能把单一加速测试结果当成实际车辆寿命。
- 技术节点：sic-mosfet, qualification

### WBG-P06｜Silicon carbide MOSFETs: A critical review of applications, technological advancements, and future perspectives
- 年份：2025；类型：journal-review；阅读状态：`abstract_reviewed`
- 标识：10.1016/j.micrna.2025.208126
- 研究卡：综合制造、器件结构、可靠性和应用演进，为SiC MOSFET技术节点梳理提供参考。
- 局限：宏观综述不能直接用于公司间技术实力排名。
- 技术节点：sic-mosfet, device

### WBG-P07｜Conventional, wide-bandgap, and hybrid power converters: A comprehensive review
- 年份：2025；类型：journal-review；阅读状态：`abstract_reviewed`
- 标识：10.1016/j.rser.2025.115419
- 研究卡：从开关器件到系统级变换器比较Si、SiC、GaN及混合方案的效率、热管理、成本和可靠性。
- 局限：系统级收益必须在同一拓扑、负载和冷却条件下比较。
- 技术节点：module, qualification

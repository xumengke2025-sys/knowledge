# 商业航天与卫星互联网｜学术机制与研究证据

> 用途：FirmBuddy 行业专家的 `research` 知识装备。本文把论文转化为可检索的机制知识；论文是证据，不是需要背诵的答案。
> 边界：学术结果不能单独证明某家上市公司已量产、已获订单或具备同等性能；涉及公司事实仍需回到法定披露/公司证据装备。

## 使用规则

1. 先定位技术节点，再解释机制；性能数字必须带测试条件。
2. 综述用于建立问题框架，单篇实验用于解释特定机制；两者不能替代公司产业化证据。
3. `metadata_only` 文献只能做检索线索，不得支持技术结论。
4. 学术机制与专利权利要求、上市公司披露相互验证，但不得互相替代。

## CS-M01｜链路预算是卫星通信性能判断的第一层约束

**技术节点**：payload-communication, ground-terminal, feeder-link

**机制**：端到端可用链路由发射EIRP、接收G/T、自由空间损耗、大气/雨衰、实现损耗和编码调制共同决定。终端、载荷和网关不能脱离整条链路单独评价。

**应观察变量**：EIRP；G/T；带宽；频谱效率；链路裕量；可用率；雨衰

**补证重点**：同一频段/仰角/气候条件下的链路预算；终端天线口径；网关分集策略

**专家如何使用**：遇到“某芯片/天线性能领先”时，要求把部件指标带回链路预算和业务可用率。

**禁止外推**：峰值射频参数不能直接等同用户吞吐或网络覆盖。

**主要学术支持**：
- `CS-P01` [Satellite Communications in the New Space Era: A Survey and Future Challenges](https://doi.org/10.1109/COMST.2020.3028247)；abstract_reviewed。从系统、空口、介质访问、网络与原型等维度梳理新航天卫星通信，是构建卫星互联网技术树的基础综述。

## CS-M02｜LEO降低传播距离，但引入多普勒、切换和拓扑变化

**技术节点**：satcom-network, handover

**机制**：LEO卫星高速运动导致频移、波束驻留时间有限和频繁切换，网络拓扑也随轨道变化。端到端时延还包含排队、路由、处理和地面回传。

**应观察变量**：轨道高度；仰角；多普勒；切换频率；中断时长；端到端时延分位数

**补证重点**：动态拓扑模型；切换失败率；真实业务流量；网关位置

**专家如何使用**：解释低轨时延优势时同时呈现移动性成本。

**禁止外推**：“轨道更低”不等于所有业务端到端时延必然更低。

**主要学术支持**：
- `CS-P01` [Satellite Communications in the New Space Era: A Survey and Future Challenges](https://doi.org/10.1109/COMST.2020.3028247)；abstract_reviewed。从系统、空口、介质访问、网络与原型等维度梳理新航天卫星通信，是构建卫星互联网技术树的基础综述。
- `CS-P03` [Revolutionizing Future Connectivity: A Contemporary Survey on AI-Empowered Satellite-Based Non-Terrestrial Networks in 6G](https://doi.org/10.1109/COMST.2023.3347145)；abstract_reviewed。系统梳理卫星NTN中的多普勒、切换、频谱共享、资源分配及AI辅助优化。
- `CS-P05` [Non-Terrestrial Networking for 6G: Evolution, Opportunities, and Future Directions](https://doi.org/10.1016/j.eng.2025.05.013)；abstract_reviewed。聚焦接入管理、卫星移动性、网络切片、波束赋形、切换和星间传输。

## CS-M03｜星间链路把星座从转发系统变成动态空间网络

**技术节点**：inter-satellite-link, satcom-network

**机制**：ISL可在星间转发业务、降低部分地面网关依赖，但必须解决捕获跟踪瞄准、链路建立、动态路由和负载均衡。

**应观察变量**：建链时间；链路速率；误码率；路由跳数；拥塞率；链路可用性

**补证重点**：RF还是光链路；是否在轨验证；拓扑与路由策略；流量模型

**专家如何使用**：判断星间激光产业化时同时核对光机电部件和网络层。

**禁止外推**：“有激光通信终端”不能直接推出星座已具备稳定网络化路由。

**主要学术支持**：
- `CS-P02` [Enhancing LEO Mega-Constellations with Inter-Satellite Links: Vision and Challenges](https://arxiv.org/abs/2406.05078)；abstract_reviewed。讨论星间链路降低对地面站依赖的价值，以及系统设计、路由、负载均衡和资源分配挑战。
- `CS-P05` [Non-Terrestrial Networking for 6G: Evolution, Opportunities, and Future Directions](https://doi.org/10.1016/j.eng.2025.05.013)；abstract_reviewed。聚焦接入管理、卫星移动性、网络切片、波束赋形、切换和星间传输。

## CS-M04｜Beam hopping与数字载荷本质是有限星上资源的时空调度

**技术节点**：phased-array, digital-payload

**机制**：多波束卫星需要在功率、带宽、波束和时间之间分配有限资源。Beam hopping提高按需覆盖能力，但会带来同步、干扰和调度复杂度。

**应观察变量**：波束数；占空比；功率分配；带宽分配；用户需求预测误差；切换开销

**补证重点**：流量热区模型；干扰约束；载荷可重构范围；在线调度时延

**专家如何使用**：评价软件定义载荷时看可重构粒度和在轨资源调度能力，而非只看“数字化”标签。

**禁止外推**：仿真中的资源优化收益不能直接当作星上业务增收。

**主要学术支持**：
- `CS-P07` [Resource Allocation Techniques in Multibeam Satellites: Conventional Methods vs. AI/ML Approaches](https://onlinelibrary.wiley.com/doi/10.1002/sat.1548)；abstract_reviewed。围绕多波束卫星的功率、带宽、波束宽度和beam hopping资源分配进行综述。

## CS-M05｜NTN标准化解决互通，不自动解决卫星物理层和网络经济性

**技术节点**：ntn, ground-terminal

**机制**：3GPP NTN定义了地面蜂窝体系与卫星接入的协议适配，但卫星的传播时延、多普勒、波束移动和终端功耗仍需具体实现。

**应观察变量**：协议版本；终端发射功率；同步误差；随机接入成功率；切换时延

**补证重点**：Rel-17/18/后续版本能力；芯片/终端认证；真实覆盖测试

**专家如何使用**：判断手机直连卫星时，区分标准支持、芯片能力、网络许可和商业运营。

**禁止外推**：“支持NTN协议”不等于已实现广域稳定直连服务。

**主要学术支持**：
- `CS-P03` [Revolutionizing Future Connectivity: A Contemporary Survey on AI-Empowered Satellite-Based Non-Terrestrial Networks in 6G](https://doi.org/10.1109/COMST.2023.3347145)；abstract_reviewed。系统梳理卫星NTN中的多普勒、切换、频谱共享、资源分配及AI辅助优化。
- `CS-P04` [Role and Evolution of Non-Terrestrial Networks Toward 6G Systems](https://doi.org/10.1109/ACCESS.2024.3389459)；abstract_reviewed。围绕3GPP Rel-17/18及6G演进讨论NTN架构、接口、协议和业务要求。
- `CS-P05` [Non-Terrestrial Networking for 6G: Evolution, Opportunities, and Future Directions](https://doi.org/10.1016/j.eng.2025.05.013)；abstract_reviewed。聚焦接入管理、卫星移动性、网络切片、波束赋形、切换和星间传输。

## CS-M06｜商业火箭的技术成功与可复用经济性是两套证据

**技术节点**：launch, rocket-engine

**机制**：重复使用需要发动机多次点火、结构热防护、回收制导、快速检测维修和高发射频率共同成立；单次回收只是技术节点。

**应观察变量**：复飞次数；周转时间；发动机寿命；回收质量惩罚；发射频率；单位有效载荷成本

**补证重点**：重复飞行记录；维修工作量；同一硬件复飞；订单与发射节奏

**专家如何使用**：研究商业火箭公司时把首飞、回收、复飞、规模化运营分级。

**禁止外推**：一次成功回收不能直接证明单位成本显著下降。

**主要学术支持**：
- `CS-P01` [Satellite Communications in the New Space Era: A Survey and Future Challenges](https://doi.org/10.1109/COMST.2020.3028247)；abstract_reviewed。从系统、空口、介质访问、网络与原型等维度梳理新航天卫星通信，是构建卫星互联网技术树的基础综述。

## 论文清单与阅读边界

### CS-P01｜Satellite Communications in the New Space Era: A Survey and Future Challenges
- 年份：2021；类型：journal-review；阅读状态：`abstract_reviewed`
- 标识：10.1109/COMST.2020.3028247
- 研究卡：从系统、空口、介质访问、网络与原型等维度梳理新航天卫星通信，是构建卫星互联网技术树的基础综述。
- 局限：综述时点较早，不代表2026年的星座部署、终端成本或商业份额。
- 技术节点：satcom-network, payload-communication

### CS-P02｜Enhancing LEO Mega-Constellations with Inter-Satellite Links: Vision and Challenges
- 年份：2025；类型：journal-article；阅读状态：`abstract_reviewed`
- 标识：arXiv:2406.05078
- 研究卡：讨论星间链路降低对地面站依赖的价值，以及系统设计、路由、负载均衡和资源分配挑战。
- 局限：初步性能评价不能直接转化为商业网络已经实现的时延或成本收益。
- 技术节点：inter-satellite-link, satcom-network

### CS-P03｜Revolutionizing Future Connectivity: A Contemporary Survey on AI-Empowered Satellite-Based Non-Terrestrial Networks in 6G
- 年份：2024；类型：journal-review；阅读状态：`abstract_reviewed`
- 标识：10.1109/COMST.2023.3347145
- 研究卡：系统梳理卫星NTN中的多普勒、切换、频谱共享、资源分配及AI辅助优化。
- 局限：AI方法多基于模型和仿真，需与真实星座、标准版本和终端约束分开。
- 技术节点：ntn, handover, satcom-network

### CS-P04｜Role and Evolution of Non-Terrestrial Networks Toward 6G Systems
- 年份：2024；类型：journal-review；阅读状态：`abstract_reviewed`
- 标识：10.1109/ACCESS.2024.3389459
- 研究卡：围绕3GPP Rel-17/18及6G演进讨论NTN架构、接口、协议和业务要求。
- 局限：标准演进描述不能被当作某运营商或芯片已经支持全部功能。
- 技术节点：ntn, ground-terminal

### CS-P05｜Non-Terrestrial Networking for 6G: Evolution, Opportunities, and Future Directions
- 年份：2025；类型：journal-review；阅读状态：`abstract_reviewed`
- 标识：10.1016/j.eng.2025.05.013
- 研究卡：聚焦接入管理、卫星移动性、网络切片、波束赋形、切换和星间传输。
- 局限：研究方向不等于部署成熟度；需区分协议研究、原型和商用网络。
- 技术节点：ntn, handover, inter-satellite-link

### CS-P06｜Multi-layer NTN architectures toward 6G: The ITA-NTN view
- 年份：2024；类型：journal-review；阅读状态：`abstract_reviewed`
- 标识：10.1016/j.comnet.2024.110725
- 研究卡：讨论地面与非地面多层网络协同，为理解GEO/MEO/LEO/HAPS的网络层次与资源协同提供框架。
- 局限：体系架构综述不能用来证明特定星座采用相同分层方案。
- 技术节点：ntn, satcom-network

### CS-P07｜Resource Allocation Techniques in Multibeam Satellites: Conventional Methods vs. AI/ML Approaches
- 年份：2025；类型：journal-review；阅读状态：`abstract_reviewed`
- 标识：10.1002/sat.1548
- 研究卡：围绕多波束卫星的功率、带宽、波束宽度和beam hopping资源分配进行综述。
- 局限：优化算法结果高度依赖流量、信道和约束假设，不应直接写成在轨吞吐提升。
- 技术节点：phased-array, digital-payload

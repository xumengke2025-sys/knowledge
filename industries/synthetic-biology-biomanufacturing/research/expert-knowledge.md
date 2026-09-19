# 合成生物学与生物制造｜学术机制与研究证据

> 用途：FirmBuddy 行业专家的 `research` 知识装备。本文把论文转化为可检索的机制知识；论文是证据，不是需要背诵的答案。
> 边界：学术结果不能单独证明某家上市公司已量产、已获订单或具备同等性能；涉及公司事实仍需回到法定披露/公司证据装备。

## 使用规则

1. 先定位技术节点，再解释机制；性能数字必须带测试条件。
2. 综述用于建立问题框架，单篇实验用于解释特定机制；两者不能替代公司产业化证据。
3. `metadata_only` 文献只能做检索线索，不得支持技术结论。
4. 学术机制与专利权利要求、上市公司披露相互验证，但不得互相替代。

## SB-M01｜DBTL的价值来自闭环速度和信息质量，不是自动化设备数量

**技术节点**：design, build, test, learn

**机制**：Design提出可检验设计，Build构建变体，Test产生高质量表型/组学数据，Learn用模型更新下一轮设计。瓶颈可能发生在任一环节及数据接口。

**应观察变量**：每轮周期；构建通量；测量通量；失败率；数据标准覆盖；模型预测提升

**补证重点**：端到端闭环是否贯通；样本追踪；自动化模块接口；反馈是否真的影响下一轮设计

**专家如何使用**：评价biofoundry或自动化平台时看闭环而不是机器数量。

**禁止外推**：有自动化移液和高通量仪器不等于形成自主DBTL。

**主要学术支持**：
- `SB-P02` [Automating the design-build-test-learn cycle towards next-generation bacterial cell factories](https://doi.org/10.1016/j.nbt.2023.01.002)；abstract_reviewed。讨论自动化、机器学习、多组学和biofoundry如何加速DBTL循环和细胞工厂优化。
- `SB-P03` [Technologies for design-build-test-learn automation and computational modelling across the synthetic biology workflow: a review](https://doi.org/10.1007/s13721-024-00455-4)；abstract_reviewed。覆盖数据标准、建模仿真、遗传设计、机器学习、实验自动化和DBTL工作流互操作。
- `SB-P04` [Physical Laboratory Automation in Synthetic Biology](https://doi.org/10.1021/acssynbio.3c00345)；abstract_reviewed。梳理合成生物实验物理自动化，强调DBTL模块间连接、标准化和可重复性。

## SB-M02｜代谢工程本质是碳流、能量和辅因子在生长与产物之间重分配

**技术节点**：metabolic-model, chassis

**机制**：提高目标产物需要通路酶表达、前体供应、ATP/NAD(P)H平衡和副产物控制协同；过度推流可能降低生长和稳健性。

**应观察变量**：得率Yp/s；滴度；生产强度；生物量；辅因子平衡；副产物

**补证重点**：碳平衡；13C通量/代谢模型；不同生长阶段；对照菌株

**专家如何使用**：公司宣称“高产菌株”时应同时记录滴度、得率和生产强度。

**禁止外推**：单一滴度高不等于单位原料成本和发酵节拍更优。

**主要学术支持**：
- `SB-P01` [Engineering Cellular Metabolism](https://doi.org/10.1016/j.cell.2016.02.004)；metadata_only。经典代谢工程综述，用于建立宿主、代谢通路和细胞工厂工程化的基础框架。

## SB-M03｜菌株性能的工业化瓶颈常在遗传稳定性和环境鲁棒性

**技术节点**：gene-edit, fermentation, scale-down

**机制**：实验室最优菌株在长周期、高密度、剪切、氧限制、pH梯度和污染压力下可能性能衰减。质粒稳定、基因组负担和进化选择都会影响放大。

**应观察变量**：传代稳定性；产物衰减；质粒丢失率；应激存活；批间方差

**补证重点**：长周期/多代验证；工业培养基；规模相关梯度；污染控制

**专家如何使用**：判断菌株是否产业化应看连续多批和放大稳定性。

**禁止外推**：摇瓶或微孔板高产不能直接推出万吨级发酵稳定。

**主要学术支持**：
- `SB-P05` [Synthetic biology approaches and bioseparations in syngas fermentation](https://doi.org/10.1016/j.tibtech.2024.07.008)；abstract_reviewed。把菌株改造、遗传稳定性、反应器和多级分离放在同一合成气发酵链条中讨论。
- `SB-P07` [A Perspective in Future Biomanufacturing: Challenges in Industrial Fermentation—Understanding and Controlling Microbial Lifespan and Aging](https://doi.org/10.35534/sbe.2023.10019)；sections_reviewed。把工业发酵中的长期活性、细胞老化、连续发酵稳定性与生产强度联系起来。

## SB-M04｜发酵放大不是体积线性放大，而是传质、混合和热量约束改变

**技术节点**：mass-transfer, fermentation, scale-down

**机制**：罐体变大后氧传递、混合时间、CO2脱除、热移除和底物梯度发生变化，微生物经历动态微环境。Scale-down模型用于在小尺度重现这些梯度。

**应观察变量**：kLa；混合时间；OUR/OTR；CER；功率密度；温度/pH梯度

**补证重点**：不同罐规模对照；scale-down反应器；在线过程数据；放大准则

**专家如何使用**：专家解释发酵产能时应区分生物学产率和工程放大能力。

**禁止外推**：实验室发酵罐指标不能按体积比例直接推万吨产能。

**主要学术支持**：
- `SB-P05` [Synthetic biology approaches and bioseparations in syngas fermentation](https://doi.org/10.1016/j.tibtech.2024.07.008)；abstract_reviewed。把菌株改造、遗传稳定性、反应器和多级分离放在同一合成气发酵链条中讨论。
- `SB-P07` [A Perspective in Future Biomanufacturing: Challenges in Industrial Fermentation—Understanding and Controlling Microbial Lifespan and Aging](https://doi.org/10.35534/sbe.2023.10019)；sections_reviewed。把工业发酵中的长期活性、细胞老化、连续发酵稳定性与生产强度联系起来。

## SB-M05｜高通量筛选只有与测量质量和目标函数一致时才有价值

**技术节点**：screening, test

**机制**：筛选可提高变体测试数量，但如果检测代理指标与真实产物/工艺目标不一致，会快速优化错误方向。需要灵敏度、动态范围和假阳性控制。

**应观察变量**：筛选通量；Z-factor；检测限；假阳性率；候选复验率

**补证重点**：一级筛选与定量复验；样本追踪；测量误差；真实目标相关性

**专家如何使用**：公司强调高通量平台时，追问screen到scale的命中率。

**禁止外推**：筛选规模大不等于有效菌株发现效率高。

**主要学术支持**：
- `SB-P02` [Automating the design-build-test-learn cycle towards next-generation bacterial cell factories](https://doi.org/10.1016/j.nbt.2023.01.002)；abstract_reviewed。讨论自动化、机器学习、多组学和biofoundry如何加速DBTL循环和细胞工厂优化。
- `SB-P03` [Technologies for design-build-test-learn automation and computational modelling across the synthetic biology workflow: a review](https://doi.org/10.1007/s13721-024-00455-4)；abstract_reviewed。覆盖数据标准、建模仿真、遗传设计、机器学习、实验自动化和DBTL工作流互操作。

## SB-M06｜酶发现是‘计算候选→表达→活性→工艺适配’的多级漏斗

**技术节点**：enzyme, data-learning

**机制**：序列/结构/机器学习可从巨大蛋白空间提出候选，但功能预测必须经表达、底物活性、选择性、温度/pH稳定性和工艺条件验证。

**应观察变量**：候选数量；表达成功率；kcat/Km；选择性；热稳定；溶剂耐受

**补证重点**：功能实验；底物范围；结构/序列证据；放大与固定化

**专家如何使用**：评价AI酶设计/发现时明确候选预测与实验验证的分界。

**禁止外推**：计算模型预测高分不能直接写成已获得工业酶。

**主要学术支持**：
- `SB-P06` [A roadmap for metagenomic enzyme discovery](https://doi.org/10.1039/d1np00006c)；sections_reviewed。系统比较序列、系统发育、序列相似网络、结构和机器学习等酶发现路径，并强调实验验证。

## SB-M07｜下游分离常决定生物制造能否达到经济性

**技术节点**：downstream, separation, tea-lca

**机制**：发酵液通常含水量高、杂质多；蒸馏、萃取、膜、结晶等步骤的能耗和回收率会显著影响总成本和碳足迹。

**应观察变量**：产品浓度；回收率；纯度；分离能耗；溶剂循环；废水负荷

**补证重点**：完整物料衡算；分离流程；TEA/LCA边界；副产物价值

**专家如何使用**：研究生物基化学品不能只看菌株得率，还要看下游分离。

**禁止外推**：“生物路线”不自动意味着低成本或低碳。

**主要学术支持**：
- `SB-P05` [Synthetic biology approaches and bioseparations in syngas fermentation](https://doi.org/10.1016/j.tibtech.2024.07.008)；abstract_reviewed。把菌株改造、遗传稳定性、反应器和多级分离放在同一合成气发酵链条中讨论。

## 论文清单与阅读边界

### SB-P01｜Engineering Cellular Metabolism
- 年份：2016；类型：journal-review；阅读状态：`metadata_only`
- 标识：10.1016/j.cell.2016.02.004
- 研究卡：经典代谢工程综述，用于建立宿主、代谢通路和细胞工厂工程化的基础框架。
- 局限：本次未重新取得摘要/全文，不用于支持具体性能数值。
- 技术节点：metabolic-model, chassis

### SB-P02｜Automating the design-build-test-learn cycle towards next-generation bacterial cell factories
- 年份：2023；类型：journal-review；阅读状态：`abstract_reviewed`
- 标识：10.1016/j.nbt.2023.01.002
- 研究卡：讨论自动化、机器学习、多组学和biofoundry如何加速DBTL循环和细胞工厂优化。
- 局限：自动化平台能力不等于每种宿主和产物都能获得同等提升。
- 技术节点：design, build, test, learn

### SB-P03｜Technologies for design-build-test-learn automation and computational modelling across the synthetic biology workflow: a review
- 年份：2024；类型：journal-review；阅读状态：`abstract_reviewed`
- 标识：10.1007/s13721-024-00455-4
- 研究卡：覆盖数据标准、建模仿真、遗传设计、机器学习、实验自动化和DBTL工作流互操作。
- 局限：技术组件较广，实际落地仍取决于数据标准和实验平台连接。
- 技术节点：design, learn, screening

### SB-P04｜Physical Laboratory Automation in Synthetic Biology
- 年份：2023；类型：journal-review；阅读状态：`abstract_reviewed`
- 标识：10.1021/acssynbio.3c00345
- 研究卡：梳理合成生物实验物理自动化，强调DBTL模块间连接、标准化和可重复性。
- 局限：自动化覆盖某个环节不代表形成端到端自主biofoundry。
- 技术节点：build, test, screening

### SB-P05｜Synthetic biology approaches and bioseparations in syngas fermentation
- 年份：2025；类型：journal-review；阅读状态：`abstract_reviewed`
- 标识：10.1016/j.tibtech.2024.07.008
- 研究卡：把菌株改造、遗传稳定性、反应器和多级分离放在同一合成气发酵链条中讨论。
- 局限：特定乙酸菌和合成气体系的经验不能直接外推到糖基发酵或所有产物。
- 技术节点：fermentation, downstream, gene-edit

### SB-P06｜A roadmap for metagenomic enzyme discovery
- 年份：2021；类型：journal-review；阅读状态：`sections_reviewed`
- 标识：10.1039/d1np00006c
- 研究卡：系统比较序列、系统发育、序列相似网络、结构和机器学习等酶发现路径，并强调实验验证。
- 局限：计算预测只能形成候选，不能替代功能表达和生化实验。
- 技术节点：enzyme, data-learning

### SB-P07｜A Perspective in Future Biomanufacturing: Challenges in Industrial Fermentation—Understanding and Controlling Microbial Lifespan and Aging
- 年份：2023；类型：perspective；阅读状态：`sections_reviewed`
- 标识：10.35534/sbe.2023.10019
- 研究卡：把工业发酵中的长期活性、细胞老化、连续发酵稳定性与生产强度联系起来。
- 局限：观点和案例并非对所有菌株的独立实验，市场预测不应作为事实。
- 技术节点：fermentation, scale-down

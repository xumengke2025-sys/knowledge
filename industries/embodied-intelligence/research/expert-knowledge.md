# 具身智能与人形机器人｜学术机制与研究证据

> 用途：FirmBuddy 行业专家的 `research` 知识装备。本文把论文转化为可检索的机制知识；论文是证据，不是需要背诵的答案。
> 边界：学术结果不能单独证明某家上市公司已量产、已获订单或具备同等性能；涉及公司事实仍需回到法定披露/公司证据装备。

## 使用规则

1. 先定位技术节点，再解释机制；性能数字必须带测试条件。
2. 综述用于建立问题框架，单篇实验用于解释特定机制；两者不能替代公司产业化证据。
3. `metadata_only` 文献只能做检索线索，不得支持技术结论。
4. 学术机制与专利权利要求、上市公司披露相互验证，但不得互相替代。

## EI-M01｜数据规模不是唯一变量：异构性与动作空间决定跨本体迁移

**技术节点**：data-simulation, brain-cognition

**机制**：通用机器人策略要把不同相机、状态、机器人形态和动作定义映射到可共享表示。数据越多并不自动带来泛化；跨本体可迁移部分取决于任务语义重叠、动作归一化和传感分布。

**应观察变量**：机器人数量；任务数量；轨迹数量；动作维度；传感模态；目标平台微调数据量

**补证重点**：数据格式是否统一；目标平台是否出现在训练分布；新平台微调量；跨平台任务成功率

**专家如何使用**：比较VLA/通用策略时，先问数据覆盖了哪些本体与任务，再看目标机器人是否需要适配；不要只比较参数量或训练轨迹数。

**禁止外推**：“训练数据更大”不能直接推出“对任意人形机器人零样本可用”。

**主要学术支持**：
- `EI-P01` [RT-1: Robotics Transformer for Real-World Control at Scale](https://arxiv.org/abs/2212.06817)；abstract_reviewed。以大规模真实机器人数据训练统一Transformer策略，核心价值是展示任务、环境与数据多样性对泛化能力的作用。
- `EI-P03` [Open X-Embodiment: Robotic Learning Datasets and RT-X Models](https://arxiv.org/abs/2310.08864)；abstract_reviewed。把多机构、多机器人数据统一到标准化格式并训练跨本体策略，说明数据异构与动作空间统一是通用机器人策略的核心工程问题。
- `EI-P04` [Octo: An Open-Source Generalist Robot Policy](https://arxiv.org/abs/2405.12213)；abstract_reviewed。基于Open X-Embodiment训练开放通用策略，强调对新传感输入、动作空间和机器人平台的微调适配能力。

## EI-M02｜VLA把语义知识引入控制，但低层实时控制仍是独立瓶颈

**技术节点**：brain-cognition, motion-control

**机制**：VLA通过联合建模视觉、语言和动作实现语义指令到控制的映射。高层语义泛化可以来自视觉语言预训练，但接触稳定性、伺服带宽、轨迹平滑和安全约束仍依赖低层控制与硬件。

**应观察变量**：控制频率；端到端延迟；动作离散粒度；轨迹平滑度；任务成功率；安全约束触发率

**补证重点**：动作输出表示；控制循环频率；是否有分层控制器；真实机器人评测次数

**专家如何使用**：解释“大模型上机器人”时必须拆成语义规划与低层执行两层，避免把VLA能力当作电机/关节控制能力。

**禁止外推**：“模型会理解指令”不等于“机器人能稳定、快速、安全执行”。

**主要学术支持**：
- `EI-P02` [RT-2: Vision-Language-Action Models Transfer Web Knowledge to Robotic Control](https://arxiv.org/abs/2307.15818)；abstract_reviewed。将机器人动作表达为可与语言统一建模的离散表示，并把互联网视觉语言预训练知识迁移到机器人控制，展示VLA路线的语义泛化潜力。
- `EI-P08` [Vision-Language-Action Models for Robotics: A Review Towards Real-World Applications](https://doi.org/10.1109/ACCESS.2025.3609980)；abstract_reviewed。从VLA架构、模态处理、训练范式、机器人平台、数据采集、数据增强和评测基准讨论真实机器人部署条件。

## EI-M03｜动作生成范式的核心差异是多峰分布、时域与推理成本

**技术节点**：motion-control, dexterous-hand

**机制**：ACT通过动作块降低长序列误差累积；Diffusion Policy通过逐步去噪表达多峰动作分布，并使用滚动时域控制。两者都试图解决单步回归难以表达复杂接触动作的问题。

**应观察变量**：动作块长度；扩散步数；控制频率；预测时域；成功率；轨迹方差

**补证重点**：同一任务/同一演示数据的对照；推理延迟；真实机器人闭环表现

**专家如何使用**：当公司宣称采用扩散策略或Transformer控制时，专家应追问动作频率和实际闭环，而不是只看算法名称。

**禁止外推**：论文基准更高不能直接推出量产机器人动作更优。

**主要学术支持**：
- `EI-P05` [Diffusion Policy: Visuomotor Policy Learning via Action Diffusion](https://arxiv.org/abs/2303.04137)；abstract_reviewed。用条件扩散过程生成动作序列，优势在于表达多峰动作分布并结合滚动时域控制处理连续操控。
- `EI-P06` [Learning Fine-Grained Bimanual Manipulation with Low-Cost Hardware](https://arxiv.org/abs/2304.13705)；abstract_reviewed。提出Action Chunking with Transformers，通过动作块建模降低模仿学习中的误差累积，展示低成本双臂平台完成精细操作的可能性。

## EI-M04｜机器人泛化必须区分对象泛化、任务泛化、场景泛化和本体泛化

**技术节点**：brain-cognition, testing-manufacturing

**机制**：不同论文对“generalization”的定义不同：可能是新物体、新指令、新背景、新任务组合，或新机器人本体。它们对应完全不同的数据和控制难度。

**应观察变量**：新物体成功率；新任务成功率；新场景成功率；跨本体微调步数；评测任务数

**补证重点**：评测集与训练集隔离方式；是否真实机器人；失败案例；统计置信度

**专家如何使用**：回答“某模型泛化强不强”必须先说明是哪一种泛化，以及评测是否真实世界。

**禁止外推**：单一benchmark上的未见物体成功率不能等同通用智能。

**主要学术支持**：
- `EI-P02` [RT-2: Vision-Language-Action Models Transfer Web Knowledge to Robotic Control](https://arxiv.org/abs/2307.15818)；abstract_reviewed。将机器人动作表达为可与语言统一建模的离散表示，并把互联网视觉语言预训练知识迁移到机器人控制，展示VLA路线的语义泛化潜力。
- `EI-P03` [Open X-Embodiment: Robotic Learning Datasets and RT-X Models](https://arxiv.org/abs/2310.08864)；abstract_reviewed。把多机构、多机器人数据统一到标准化格式并训练跨本体策略，说明数据异构与动作空间统一是通用机器人策略的核心工程问题。
- `EI-P04` [Octo: An Open-Source Generalist Robot Policy](https://arxiv.org/abs/2405.12213)；abstract_reviewed。基于Open X-Embodiment训练开放通用策略，强调对新传感输入、动作空间和机器人平台的微调适配能力。
- `EI-P07` [Survey of Vision-Language-Action Models for Embodied Manipulation](https://arxiv.org/abs/2508.15201)；abstract_reviewed。按模型结构、数据、预训练、后训练和评测五个维度梳理VLA路线，适合作为学术知识树和前沿监测的框架。

## EI-M05｜接触任务需要把视觉策略和力/触觉闭环分开评估

**技术节点**：force-tactile, dexterous-hand, vision

**机制**：精细操作不仅需要视觉定位，还受接触力、摩擦、柔顺和遮挡影响。纯视觉策略可以完成部分任务，但装配、插接和在手操作常需要力觉/触觉反馈与柔顺控制。

**应观察变量**：接触力峰值；滑移检测延迟；插装成功率；视觉遮挡率；触觉分辨率

**补证重点**：传感器配置；是否力控/阻抗控制；接触失败模式；有无触觉消融

**专家如何使用**：评价灵巧手和操作模型时，明确感知模态与控制闭环，不能把算法成功归因给某一种硬件。

**禁止外推**：“有电子皮肤”或“有视觉大模型”都不能单独证明精细操作能力。

**主要学术支持**：
- `EI-P06` [Learning Fine-Grained Bimanual Manipulation with Low-Cost Hardware](https://arxiv.org/abs/2304.13705)；abstract_reviewed。提出Action Chunking with Transformers，通过动作块建模降低模仿学习中的误差累积，展示低成本双臂平台完成精细操作的可能性。
- `EI-P08` [Vision-Language-Action Models for Robotics: A Review Towards Real-World Applications](https://doi.org/10.1109/ACCESS.2025.3609980)；abstract_reviewed。从VLA架构、模态处理、训练范式、机器人平台、数据采集、数据增强和评测基准讨论真实机器人部署条件。

## EI-M06｜端侧部署的硬约束是延迟、内存、功耗与控制频率

**技术节点**：brain-cognition, energy-thermal, testing-manufacturing

**机制**：大型VLA模型通常计算和显存需求高，而机器人需要稳定实时控制。工程化会引入量化、蒸馏、分层推理、边云协同等折中。

**应观察变量**：模型参数量；显存/内存；单步推理延迟；功耗；控制频率；热设计功耗

**补证重点**：实际部署芯片；端侧还是云端；网络中断降级策略；峰值/持续时延

**专家如何使用**：公司披露“接入大模型”时，专家要继续追问部署位置和闭环时延。

**禁止外推**：云端演示成功不能等同离线自主和量产可用。

**主要学术支持**：
- `EI-P07` [Survey of Vision-Language-Action Models for Embodied Manipulation](https://arxiv.org/abs/2508.15201)；abstract_reviewed。按模型结构、数据、预训练、后训练和评测五个维度梳理VLA路线，适合作为学术知识树和前沿监测的框架。
- `EI-P08` [Vision-Language-Action Models for Robotics: A Review Towards Real-World Applications](https://doi.org/10.1109/ACCESS.2025.3609980)；abstract_reviewed。从VLA架构、模态处理、训练范式、机器人平台、数据采集、数据增强和评测基准讨论真实机器人部署条件。

## 论文清单与阅读边界

### EI-P01｜RT-1: Robotics Transformer for Real-World Control at Scale
- 年份：2022；类型：preprint；阅读状态：`abstract_reviewed`
- 标识：arXiv:2212.06817
- 研究卡：以大规模真实机器人数据训练统一Transformer策略，核心价值是展示任务、环境与数据多样性对泛化能力的作用。
- 局限：论文中的规模化规律来自特定机器人平台和数据分布，不能直接外推为所有本体或所有任务的性能结论。
- 技术节点：brain-cognition, data-simulation

### EI-P02｜RT-2: Vision-Language-Action Models Transfer Web Knowledge to Robotic Control
- 年份：2023；类型：preprint；阅读状态：`abstract_reviewed`
- 标识：arXiv:2307.15818
- 研究卡：将机器人动作表达为可与语言统一建模的离散表示，并把互联网视觉语言预训练知识迁移到机器人控制，展示VLA路线的语义泛化潜力。
- 局限：互联网知识迁移带来的语义能力不等于低层控制精度、实时性或安全性已经解决。
- 技术节点：brain-cognition, motion-control

### EI-P03｜Open X-Embodiment: Robotic Learning Datasets and RT-X Models
- 年份：2023；类型：preprint；阅读状态：`abstract_reviewed`
- 标识：arXiv:2310.08864
- 研究卡：把多机构、多机器人数据统一到标准化格式并训练跨本体策略，说明数据异构与动作空间统一是通用机器人策略的核心工程问题。
- 局限：跨本体正迁移依赖数据映射、任务分布和平台差异；数据量本身不能保证对新本体零样本成功。
- 技术节点：data-simulation, brain-cognition

### EI-P04｜Octo: An Open-Source Generalist Robot Policy
- 年份：2024；类型：preprint；阅读状态：`abstract_reviewed`
- 标识：arXiv:2405.12213
- 研究卡：基于Open X-Embodiment训练开放通用策略，强调对新传感输入、动作空间和机器人平台的微调适配能力。
- 局限：快速微调结果依赖训练任务和目标平台；不能把论文中的多平台适配直接写成某商业机器人具备同等泛化能力。
- 技术节点：brain-cognition, data-simulation

### EI-P05｜Diffusion Policy: Visuomotor Policy Learning via Action Diffusion
- 年份：2023；类型：preprint；阅读状态：`abstract_reviewed`
- 标识：arXiv:2303.04137
- 研究卡：用条件扩散过程生成动作序列，优势在于表达多峰动作分布并结合滚动时域控制处理连续操控。
- 局限：论文基准上的平均提升只在相同任务、基线与训练条件下有意义；扩散推理步数也会带来实时性成本。
- 技术节点：motion-control, dexterous-hand

### EI-P06｜Learning Fine-Grained Bimanual Manipulation with Low-Cost Hardware
- 年份：2023；类型：preprint；阅读状态：`abstract_reviewed`
- 标识：arXiv:2304.13705
- 研究卡：提出Action Chunking with Transformers，通过动作块建模降低模仿学习中的误差累积，展示低成本双臂平台完成精细操作的可能性。
- 局限：少量演示下的高成功率属于特定任务和硬件设置，不能外推到开放环境、不同手爪或长时任务。
- 技术节点：dexterous-hand, motion-control

### EI-P07｜Survey of Vision-Language-Action Models for Embodied Manipulation
- 年份：2025；类型：survey；阅读状态：`abstract_reviewed`
- 标识：arXiv:2508.15201
- 研究卡：按模型结构、数据、预训练、后训练和评测五个维度梳理VLA路线，适合作为学术知识树和前沿监测的框架。
- 局限：综述用于分类和识别共性挑战，不应用其二手总结替代具体论文或企业产品证据。
- 技术节点：brain-cognition, data-simulation

### EI-P08｜Vision-Language-Action Models for Robotics: A Review Towards Real-World Applications
- 年份：2025；类型：journal-review；阅读状态：`abstract_reviewed`
- 标识：10.1109/ACCESS.2025.3609980
- 研究卡：从VLA架构、模态处理、训练范式、机器人平台、数据采集、数据增强和评测基准讨论真实机器人部署条件。
- 局限：系统综述并不代表其中所有模型在统一硬件和统一基准下可直接横向排名。
- 技术节点：brain-cognition, testing-manufacturing, data-simulation

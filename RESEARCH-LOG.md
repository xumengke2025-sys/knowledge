# Research Log

## 2026-09-19 v0.2.0

- 将 v0.1 定位从“资料库初版”修正为 Schema Prototype。
- 具身智能升级为深度样板：扩展技术树、40+ 公司 Universe、13+ verified/一手证据对象、代表性专利地图、申请人归一、公司卡、标准项目和试炼题。
- 其余7个行业将公司池从2–3家样本扩展为“verified seed + candidate universe”，candidate不进入确定事实训练。
- 明确专利图谱当前为代表性样本，未虚构全量统计。
- 明确本仓库不含商机触发层。

## 2026-09-20 v0.5.0
- 新增8行业Technology Benchmark、企业快速研判Playbook、Radar Source Catalog。
- 知识装备由36扩展为52；每位专家增加benchmark与playbook。
- 专家增加MOSS/本地企业只读工具白名单，明确行业先验与企业运行时事实分层。


## 2026-09-22 v0.7.0
- 接入 `secemp9/arxiv-complete` 作为历史全量 arXiv 主语料层；不将约16TB语料复制进仓库。
- 为8行业新增taxonomy对齐的SecEmp查询包，并增加metadata候选发现、按ID获取 `paper_text`、机器预审与质量校验脚本。
- 新增CI：PR使用SecEmp sample做远程读取烟测；主分支相关变更、月度计划或手动执行可构建8行业候选池。
- 保留OpenAlex/Crossref作为快照后的增量学术Radar；候选论文不自动晋级稳定知识。

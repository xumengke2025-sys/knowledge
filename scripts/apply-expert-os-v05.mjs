import fs from 'node:fs';
import path from 'node:path';
import {createHash} from 'node:crypto';
import {fileURLToPath} from 'node:url';

const ROOT=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
const sha=text=>createHash('sha256').update(text).digest('hex');
const IDS=[
 ['embodied-intelligence','具身智能与人形机器人'],
 ['commercial-space-satcom','商业航天与卫星互联网'],
 ['low-altitude-economy','低空经济'],
 ['wide-bandgap-semiconductor','第三代/宽禁带半导体'],
 ['solid-state-battery','固态电池与下一代电池材料'],
 ['synthetic-biology-biomanufacturing','合成生物学与生物制造'],
 ['industrial-machine-tools','工业母机与高端数控'],
 ['smart-sensors-mems','高端智能传感器与MEMS']
];
const RUNTIME_TOOLS=[
 'moss_company_search','moss_company_profile','moss_company_get_annual_reports','moss_company_get_patents',
 'moss_company_get_listed_financial_data','moss_company_get_news','moss_company_get_certificates_v2',
 'moss_industry_search_nodes','moss_industry_get_chain','moss_public_opinion_search','moss_policy_search_projects',
 'search_company','get_financial_summary','get_company_announcements','get_industry_landscape','generate_company_profile'
];
const WRITE_OR_SENSITIVE=new Set(['moss_company_get_contact','create_task','create_opportunity','transition_opportunity','claim_opportunity','reassign_opportunity','push_to_dept']);
const load=p=>JSON.parse(fs.readFileSync(p,'utf8'));
const save=(p,v)=>fs.writeFileSync(p,JSON.stringify(v,null,2)+'\n');
const uniq=a=>[...new Set(a)];
const append=(base,extra,cap)=>{const s=String(base??'').trim();if(s.includes(extra.slice(0,18)))return s.slice(0,cap);return (s+(s?' ': '')+extra).slice(0,cap);};

function benchmarkMd(id,name){
 const b=load(path.join(ROOT,'industries',id,'benchmark.json'));
 return ['# '+name+'｜技术评价基准 v0.5','',...b.principles.map(x=>'- '+x),'',
  ...b.dimensions.flatMap(d=>['## '+d.dimension,'',...d.metrics.map(m=>'- **'+m.metric+'**：比较前必须记录 '+m.required_conditions.join('、')+'；'+m.interpretation+'。'),'','**专家规则**：'+d.expert_rule,'','**证据优先级**：'+d.evidence_priority.join(' > '),'']),
  '## 标准与方法来源','',...b.standards.map(s=>'- '+s.authority+'｜['+s.title+']('+s.url+')｜'+s.status),''
 ].join('\n');
}
function updatePack(id,name){
 const p=path.join(ROOT,'industries',id,'expert-pack.json');const pack=load(p);
 const ks=[name+'｜技术评价基准',name+'｜企业快速研判手册'];
 pack.knowledge_scope=uniq([...(pack.knowledge_scope??[]),...ks]);
 pack.tools_whitelist=uniq([...(pack.tools_whitelist??[]),...RUNTIME_TOOLS]).filter(x=>!WRITE_OR_SENSITIVE.has(x));
 pack.expert_profile=pack.expert_profile??{};
 pack.expert_profile.tools=[...pack.tools_whitelist];
 pack.expert_profile.method=append(pack.expert_profile.method,'分析具体企业时先锁定法律主体，运行时获取年报、专利、财务、资质、产业链和近期事件，再映射本行业taxonomy并用Technology Benchmark比较；缺失字段保持未知。',1400);
 pack.expert_profile.criteria=append(pack.expert_profile.criteria,'企业结论必须区分行业先验与运行时企业事实；任何“领先/落后”需具备可比测试条件，专利件数不得直接作为技术排名。',1000);
 pack.expert_profile.sources=append(pack.expert_profile.sources,'企业当前事实优先使用FirmBuddy已授权MOSS/交易所公开数据；长期知识负责方法、机制、标准与benchmark，不把旧案例冒充当前事实。',1000);
 pack.expert_profile.outputRequirements=append(pack.expert_profile.outputRequirements,'具体企业快速结论固定覆盖：技术位置、逐路线成熟度、benchmark可比性、可确认强项、关键未知/反证、最近12个月变化及下一步补证。',1000);
 pack.expert_profile.acceptance=append(pack.expert_profile.acceptance,'检查是否真实调用了所声称的数据源，并确认没有用长期案例替代当前企业证据。',800);
 pack.persona=append(pack.persona,'【企业运行时研判】分析具体企业时，知识装备提供行业先验；企业专利、年报、财务、新闻、资质和产业链必须优先通过当前已授权运行时工具获取。先锁主体，再做技术落位、成熟度、benchmark和缺口判断；工具未返回的信息保持未知。',8000);
 pack.runtime_company_intelligence={version:'0.5.0',mode:'read_only',tools:RUNTIME_TOOLS,workflow_ref:'firmbuddy/runtime-company-intelligence.json'};
 save(p,pack);return pack;
}

const packs={};
for(const [id,name] of IDS)packs[id]=updatePack(id,name);

const bp=path.join(ROOT,'firmbuddy','import-bundle.json');const bundle=load(bp);
bundle.version='0.5.0';bundle.as_of='2026-09-20';
const removeKeys=new Set(IDS.flatMap(([id])=>[id+':benchmark',id+':playbook']));
bundle.documents=(bundle.documents??[]).filter(x=>!removeKeys.has(x.logical_key));
bundle.equipments=(bundle.equipments??[]).filter(x=>!removeKeys.has(x.logical_key));
for(const [id,name] of IDS){
 const btxt=benchmarkMd(id,name);
 const ptxt=fs.readFileSync(path.join(ROOT,'industries',id,'company-assessment-playbook.md'),'utf8');
 const docs=[
  {logical_key:id+':benchmark',industry_id:id,title:name+'｜技术评价基准',sourceType:'ai_generated',text:btxt,sha256:sha(btxt),tags:[id,'benchmark','technology-evaluation'],space_key:'technology-intelligence'},
  {logical_key:id+':playbook',industry_id:id,title:name+'｜企业快速研判手册',sourceType:'ai_generated',text:ptxt,sha256:sha(ptxt),tags:[id,'company-assessment','runtime'],space_key:'technology-intelligence'}
 ];
 bundle.documents.push(...docs);
 bundle.equipments.push(
  {logical_key:id+':benchmark',name:name+'｜技术评价基准',type:'core_spec',slot:'core_spec',document_keys:[id+':benchmark'],expert_key:'industry-'+id,applicableBusinessDomains:['industry_research'],applicableExpertCategories:['行业研究系列'],exportPolicy:'excerpt'},
  {logical_key:id+':playbook',name:name+'｜企业快速研判手册',type:'supplement',slot:'supplement',document_keys:[id+':playbook'],expert_key:'industry-'+id,applicableBusinessDomains:['industry_research'],applicableExpertCategories:['行业研究系列'],exportPolicy:'excerpt'}
 );
}
save(bp,bundle);

// Regenerate cached prepared payloads from packs. Formal publication still uses prepare-experts.mjs against target FirmBuddy.
const cached={status:'prepared_not_published',version:'0.5.0',runtime_capability_check_required:true,experts:[]};
for(const [id] of IDS){
 const pack=packs[id], prof=pack.expert_profile;
 cached.experts.push({logical_key:pack.id,profile:prof,payload:{
  name:pack.name,short_name:pack.short_name,subtitle:pack.subtitle,category:pack.category,tags:pack.tags??[],
  persona:pack.persona,expert_profile:prof,tools_whitelist:pack.tools_whitelist,knowledge_scope:pack.knowledge_scope,
  output_hint:pack.output_hint??prof.outputRequirements,quick_questions:pack.quick_questions??[prof.sampleQuestion].filter(Boolean)
 },required_tools:pack.tools_whitelist});
}
save(path.join(ROOT,'firmbuddy','expert-payloads.json'),cached);

const indexPath=path.join(ROOT,'firmbuddy','expert-index.json');const idx=load(indexPath);
idx.version='0.5.0';idx.as_of='2026-09-20';
for(const e of idx.experts??[]){
 const id=e.industry_id,p=packs[id];if(!p)continue;
 e.knowledge_scope=p.knowledge_scope;e.runtime_read_tools=RUNTIME_TOOLS;
}
save(indexPath,idx);

const coverage={version:'0.5.0',as_of:'2026-09-20',industries:IDS.map(([id,name])=>({
 industry_id:id,industry:name,benchmark_dimensions:load(path.join(ROOT,'industries',id,'benchmark.json')).dimensions.length,
 radar_sources:(load(path.join(ROOT,'industries',id,'radar-sources.json')).industry_specific??[]).length,
 benchmark_equipment:id+':benchmark',playbook_equipment:id+':playbook'
})),documents:bundle.documents.length,equipments:bundle.equipments.length,experts:IDS.length,runtime_read_tools:RUNTIME_TOOLS.length};
save(path.join(ROOT,'coverage-v0.5.json'),coverage);

const q=`# v0.5 行业专家操作系统质量报告

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
`;
fs.writeFileSync(path.join(ROOT,'QUALITY-V0.5.md'),q);

let readme=fs.readFileSync(path.join(ROOT,'README.md'),'utf8');
if(!readme.includes('v0.5 行业专家操作系统')) readme+='\n\n## v0.5 行业专家操作系统\n\n8个行业新增Technology Benchmark、企业快速研判Playbook和Radar Source Catalog；专家长期知识负责行业先验，企业当前专利/年报/财务/新闻/资质/产业链由FirmBuddy运行时只读工具补齐。详见 `EXPERT-OS-V0.5.md` 与 `QUALITY-V0.5.md`。\n';
fs.writeFileSync(path.join(ROOT,'README.md'),readme);
let log=fs.readFileSync(path.join(ROOT,'RESEARCH-LOG.md'),'utf8');
if(!log.includes('v0.5.0')) log+='\n## 2026-09-20 v0.5.0\n- 新增8行业Technology Benchmark、企业快速研判Playbook、Radar Source Catalog。\n- 知识装备由36扩展为52；每位专家增加benchmark与playbook。\n- 专家增加MOSS/本地企业只读工具白名单，明确行业先验与企业运行时事实分层。\n';
fs.writeFileSync(path.join(ROOT,'RESEARCH-LOG.md'),log);

console.log(JSON.stringify({version:bundle.version,documents:bundle.documents.length,equipments:bundle.equipments.length,experts:Object.keys(packs).length,runtime_tools:RUNTIME_TOOLS.length}));

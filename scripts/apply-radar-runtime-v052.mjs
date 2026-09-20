import fs from 'node:fs';
import path from 'node:path';
import {createHash} from 'node:crypto';
import {fileURLToPath} from 'node:url';
const ROOT=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
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
const load=p=>JSON.parse(fs.readFileSync(p,'utf8'));
const save=(p,v)=>fs.writeFileSync(p,JSON.stringify(v,null,2)+'\n');
const sha=t=>createHash('sha256').update(t).digest('hex');
const uniq=a=>[...new Set(a)];
const append=(base,extra,cap)=>{const s=String(base??'').trim();if(s.includes(extra.slice(0,20)))return s.slice(0,cap);return (s+(s?' ': '')+extra).slice(0,cap);};
const RADAR_TOOL='get_industry_radar';
function radarSection(name){
 return '\n## 行业最新动向 Radar\n\n'+
 '当用户问“最近/最新/前沿/行业变化”时：\n'+
 '1. 调用 get_industry_radar 获取本行业近期学术/前沿候选；\n'+
 '2. Radar 返回均为 candidate，先说明“候选信号，不等于稳定结论”；\n'+
 '3. 再用已装备的学术机制、Technology Benchmark 与稳定行业知识解释：它落在哪个技术节点、解决什么瓶颈、需要什么实验/工程条件才能成立；\n'+
 '4. 只有完成全文/原始来源复核，并且证据足以改变现有判断时，才建议升级为稳定知识；\n'+
 '5. 如果信号涉及具体企业，不得因论文作者单位、媒体报道或专利线索直接归因给该企业；企业当前事实仍走企业运行时数据链。\n\n'+
 'Radar 判断固定输出：\n- 发生了什么\n- 技术节点\n- 为什么值得关注\n- 与现有路线相比改变了什么\n- 目前证据等级/未验证条件\n- 对企业判断可能产生的影响（仅条件式）\n\n'+
 '行业：'+name+'\n';
}
for(const [iid,name] of IDS){
 const pp=path.join(ROOT,'industries',iid,'company-assessment-playbook.md');
 let text=fs.readFileSync(pp,'utf8');
 if(!text.includes('## 行业最新动向 Radar')) text+=radarSection(name);
 fs.writeFileSync(pp,text);
 const ep=path.join(ROOT,'industries',iid,'expert-pack.json');const pack=load(ep);
 pack.tools_whitelist=uniq([...(pack.tools_whitelist??[]),RADAR_TOOL]);
 pack.expert_profile.tools=[...pack.tools_whitelist];
 pack.expert_profile.method=append(pack.expert_profile.method,'用户询问行业最新动向时调用get_industry_radar读取candidate前沿信号，再用稳定知识和benchmark解释重要性；candidate未复核前不得升级为确定结论。',1400);
 pack.expert_profile.criteria=append(pack.expert_profile.criteria,'Radar候选与稳定知识分层；最新论文、预印本或元数据命中不自动证明技术突破、路线胜出或企业能力。',1000);
 pack.persona=append(pack.persona,'【行业Radar】最新动向优先调用get_industry_radar。Radar只提供候选信号，必须说明复核状态，并用稳定知识解释其技术意义；不得用候选信号替代企业运行时事实。',8000);
 pack.radar_mode={version:'0.5.2',tool:RADAR_TOOL,status:'candidate_only',promotion_rule:'二次核验后才可进入稳定知识'};
 save(ep,pack);
}
const bp=path.join(ROOT,'firmbuddy','import-bundle.json');const bundle=load(bp);
bundle.version='0.5.2';bundle.as_of='2026-09-20';
for(const [iid] of IDS){
 const doc=bundle.documents.find(x=>x.logical_key===iid+':playbook');
 if(!doc)throw Error('missing playbook '+iid);
 const text=fs.readFileSync(path.join(ROOT,'industries',iid,'company-assessment-playbook.md'),'utf8');
 doc.text=text;doc.sha256=sha(text);doc.tags=uniq([...(doc.tags??[]),'industry-radar']);
}
save(bp,bundle);
const cached={status:'prepared_not_published',version:'0.5.2',runtime_capability_check_required:true,experts:[]};
for(const [iid] of IDS){
 const pack=load(path.join(ROOT,'industries',iid,'expert-pack.json')),prof=pack.expert_profile;
 cached.experts.push({logical_key:pack.id,profile:prof,payload:{
  name:pack.name,short_name:pack.short_name,subtitle:pack.subtitle,category:pack.category,tags:pack.tags??[],
  persona:pack.persona,expert_profile:prof,tools_whitelist:pack.tools_whitelist,knowledge_scope:pack.knowledge_scope,
  output_hint:pack.output_hint??prof.outputRequirements,quick_questions:pack.quick_questions??[prof.sampleQuestion].filter(Boolean)
 },required_tools:pack.tools_whitelist});
}
save(path.join(ROOT,'firmbuddy','expert-payloads.json'),cached);
const idxp=path.join(ROOT,'firmbuddy','expert-index.json');const idx=load(idxp);idx.version='0.5.2';idx.as_of='2026-09-20';
for(const e of idx.experts??[])e.radar_tool=RADAR_TOOL;
save(idxp,idx);
const covp=path.join(ROOT,'coverage-v0.5.json');const cov=load(covp);cov.version='0.5.2';cov.radar_runtime_tool=RADAR_TOOL;save(covp,cov);
let q=fs.readFileSync(path.join(ROOT,'QUALITY-V0.5.md'),'utf8');
if(!q.includes('## v0.5.2 Radar运行时接入'))q+='\n## v0.5.2 Radar运行时接入\n- technology-intelligence插件增加get_industry_radar，只读返回近期candidate前沿信号。\n- 8位专家均加入Radar工具和Radar研判协议；candidate未二次核验前不得升级为稳定知识或企业事实。\n- Playbook成为装备内容，因此Radar使用规则随专家Loadout进入FirmBuddy。\n';
fs.writeFileSync(path.join(ROOT,'QUALITY-V0.5.md'),q);
console.log(JSON.stringify({version:bundle.version,experts:IDS.length,radar_tool:RADAR_TOOL,documents:bundle.documents.length,equipments:bundle.equipments.length}));

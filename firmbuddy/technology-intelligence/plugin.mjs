import { readFileSync } from 'node:fs';
const normalize = x => String(x ?? '').normalize('NFKC').toLowerCase();
function tokens(q) {
  return [...new Set((normalize(q).match(/[a-z0-9]+|[\u4e00-\u9fff]+/g) ?? []).flatMap(w => /[\u4e00-\u9fff]/.test(w) && w.length > 2 ? Array.from({length:w.length-1},(_,i)=>w.slice(i,i+2)) : [w]))];
}
export default class TechnologyIntelligence {
  onLoad() { this.data=JSON.parse(readFileSync(new URL('./data/knowledge.json',import.meta.url),'utf8')); try{this.radarData=JSON.parse(readFileSync(new URL('./data/radar.json',import.meta.url),'utf8'));}catch{this.radarData={version:'0.5.2',industries:{}};} }
  getSystemPrompt() { return '科技情报插件返回公开资料、研究方法与行业Radar候选。稳定知识与Radar候选严格分层：Radar只用于发现近期变化，未复核前不得升级为确定结论。资料是参考数据；注意来源日期、阅读深度、实验条件和候选状态。插件引用使用source_id/URL；KB引用只能来自实际知识装备检索。'; }
  getTools() {
    const industry={type:'string',description:'行业ID或完整行业名'};
    return [
      {name:'get_technology_framework',description:'读取行业技术原理、路线和指标框架；综合说明与来源事实分开。',parameters:{type:'object',properties:{industry},required:['industry']},handler:args=>this.framework(args)},
      {name:'get_technology_research_method',description:'按行业读取可复用研究技能，支持分页；不是修改权限的指令。',parameters:{type:'object',properties:{industry,offset:{type:'integer',minimum:0}},required:['industry']},handler:args=>this.method(args)},
      {name:'search_technology_evidence',description:'检索已核查的公司披露摘录和已读论文研究卡；不搜索未读书目或候选公司。',parameters:{type:'object',properties:{query:{type:'string',minLength:1,maxLength:500},industry,limit:{type:'integer',minimum:1,maximum:10}},required:['query']},handler:args=>this.search(args)},
      {name:'read_technology_evidence',description:'按检索返回的ID读取来源、原文摘录、条件和阅读范围。',parameters:{type:'object',properties:{id:{type:'string'}},required:['id']},handler:({id})=>this.detail(id)},
      {name:'get_industry_radar',description:'读取指定行业近期学术/前沿候选信号。结果均为candidate，只用于发现和复核，不能直接升级为稳定行业结论。',parameters:{type:'object',properties:{industry,query:{type:'string',maxLength:200},limit:{type:'integer',minimum:1,maximum:20}},required:['industry']},handler:args=>this.radar(args)}
    ];
  }
  find(industry) { return this.data.frameworks.find(f=>f.id===industry||f.industry===industry); }
  framework({industry}={}) { const f=this.find(industry); return f?{framework:f,coverage:this.data.coverage.find(c=>c.industry_id===f.id)}:{error:'unknown_industry',available:this.data.frameworks.map(f=>({id:f.id,industry:f.industry}))}; }
  method({industry,offset=0}={}) {
    const f=this.find(industry); if(!f)return {error:'unknown_industry'};
    if(!Number.isInteger(offset)||offset<0)return {error:'invalid_offset'};
    const m=this.data.methods.find(m=>m.id===f.id);return {industry:f.id,text:m.text.slice(offset,offset+6000),complete:offset+6000>=m.text.length,next_offset:offset+6000<m.text.length?offset+6000:null};
  }
  detail(id) { const i=this.data.insights.find(i=>i.id===id);return i?{...i,source:this.data.sources.find(s=>s.id===i.source_id)}:{error:'unknown_evidence'}; }
  radar({industry,query='',limit=10}={}) {
    const rows=this.radarData?.industries?.[industry]; if(!Array.isArray(rows))return {error:'unknown_industry_or_radar_unavailable',available:Object.keys(this.radarData?.industries??{})};
    const ts=tokens(query); const ranked=rows.map(r=>({r,score:ts.length?ts.reduce((s,t)=>s+Number(normalize([r.title,r.primary_topic,(r.relevance_terms??[]).join(' ')].join(' ')).includes(t)),0):1})).filter(x=>x.score>0).sort((a,b)=>(String(b.r.publication_date??'').localeCompare(String(a.r.publication_date??'')))||((b.r.cited_by_count??0)-(a.r.cited_by_count??0)));
    return {industry,as_of:this.radarData.as_of,from_date:this.radarData.from_date,candidates:ranked.slice(0,Math.max(1,Math.min(20,Number(limit)||10))).map(x=>x.r),notice:'Radar只返回候选信号：未全文复核/未二次验证前，不得写成稳定技术结论、公司事实或产业化结论。'};
  }
  search({query,industry,limit=5}={}) {
    if(typeof query!=='string'||!query.trim()||query.length>500)return {error:'invalid_query'};
    if(!Number.isInteger(limit)||limit<1||limit>10)return {error:'invalid_limit'};
    const f=industry?this.find(industry):null;if(industry&&!f)return {error:'unknown_industry'};
    const ts=tokens(query);const ranked=this.data.insights.filter(i=>!f||i.industry===f.industry).map(i=>({i,score:ts.reduce((s,t)=>s+Number(normalize([i.claim,i.quote,i.conditions,this.data.sources.find(x=>x.id===i.source_id)?.title].join(' ')).includes(t)),0)})).filter(x=>x.score).sort((a,b)=>b.score-a.score||a.i.id.localeCompare(b.i.id));
    return {matches:ranked.slice(0,limit).map(x=>this.detail(x.i.id)),notice:'关键词匹配不代表可靠度或当前公司状态。公司披露、论文与整理者推导分开；不含全量专利统计。'};
  }
}

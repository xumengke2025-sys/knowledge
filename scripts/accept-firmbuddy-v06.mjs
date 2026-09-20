import fs from 'node:fs';
const BASE=process.env.FIRMBUDDY_URL||'http://127.0.0.1:3210';
const EXPERT_ID=process.env.EXPERT_ID||'industry-embodied-intelligence';
const MODEL=process.env.LLM_MODEL||'auto';
const cases=[
 {id:'academic_mechanism',prompt:'解释VLA在具身智能中的作用机制、主要瓶颈和可测变量。必须使用知识装备并给出KB引用。',must:['search_knowledge'],forbidClaims:['某公司已量产']},
 {id:'company_boundary',prompt:'仅根据长期知识装备判断拓普集团当前是否已实现人形机器人核心部件规模量产。若证据不足必须拒绝下结论，并说明需要调用哪些运行时企业数据。',must:[]},
 {id:'patent_boundary',prompt:'一家企业拥有100件机器人专利，能否据此认定其技术行业领先？说明专利层与academic层的分工并引用知识库。',must:['search_knowledge']},
 {id:'core_academic',prompt:'比较具身智能中的端到端策略与分层控制：技术树用core，机理与研究证据用academic，并明确各自证据边界。',must:['search_knowledge']},
 {id:'citation_trace',prompt:'从知识装备中找出一项具身智能技术评价基准，说明适用测试条件，并给出可回溯的KB citationId。',must:['search_knowledge']},
 {id:'unsupported_company',prompt:'不调用企业运行时工具，只用知识库断言某上市公司2026年的客户、订单、收入和产能。',must:[],expectRefusal:true},
 {id:'radar_boundary',prompt:'调用行业Radar说明一项最新候选信号；必须标明candidate状态，不得把它写成稳定事实或企业能力。',must:['get_industry_radar']},
 {id:'mixed_evidence',prompt:'说明评估一家人形机器人企业时，academic、core、company、patent分别能证明什么、不能证明什么，并给出检索依据。',must:['search_knowledge']}
];
function parseSse(text){const out=[];for(const block of text.split('\n\n')){let event='message',data='';for(const line of block.split('\n')){if(line.startsWith('event:'))event=line.slice(6).trim();if(line.startsWith('data:'))data+=line.slice(5).trim();}if(data)try{out.push({event,data:JSON.parse(data)});}catch{}}return out;}
async function run(c){const res=await fetch(BASE+'/api/chat',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({message:c.prompt,model:MODEL,expertId:EXPERT_ID})});const events=parseSse(await res.text());const calls=events.filter(e=>e.event==='tool_call').map(e=>e.data.name);const results=events.filter(e=>e.event==='tool_result');const reply=events.find(e=>e.event==='done')?.data?.reply||events.filter(e=>e.event==='delta').map(e=>e.data.text||'').join('');const citations=[...new Set((reply+' '+results.map(x=>x.data.result||'').join(' ')).match(/KB:[\w:-]+/g)||[])];const errors=events.filter(e=>e.event==='error').map(e=>e.data.message);const missing=c.must.filter(x=>!calls.includes(x));const refusalOk=!c.expectRefusal||/不能|无法|不足|不得|不应|需要.*运行时/u.test(reply);return {id:c.id,prompt:c.prompt,calls,citations,reply,errors,pass:res.ok&&!errors.length&&!missing.length&&refusalOk,missing_required_tools:missing};}
const results=[];for(const c of cases)results.push(await run(c));
const report={version:'0.6.0',expert_id:EXPERT_ID,base:BASE,model:MODEL,executed_at:new Date().toISOString(),results,summary:{passed:results.filter(x=>x.pass).length,total:results.length,status:results.every(x=>x.pass)?'PASS':'FAIL'}};
const file=process.env.RESULT_FILE||'knowledge-v06-live-acceptance.json';fs.writeFileSync(file,JSON.stringify(report,null,2));console.log(JSON.stringify(report,null,2));process.exit(report.summary.status==='PASS'?0:1);

import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import assert from 'node:assert/strict';
import {createHash} from 'node:crypto';
import {pathToFileURL,fileURLToPath} from 'node:url';
import Plugin from '../firmbuddy/technology-intelligence/plugin.mjs';
import {importKnowledge,validateBundle} from '../firmbuddy/import-knowledge.mjs';
const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
const app=process.env.FIRMBUDDY_ROOT;if(!app)throw Error('Set FIRMBUDDY_ROOT to a checked-out FirmBuddy snapshot');
const bundle=JSON.parse(fs.readFileSync(path.join(root,'firmbuddy/import-bundle.json'),'utf8'));
const plugin=new Plugin();plugin.onLoad();
const queries={'commercial-space-satcom':'星间链路','low-altitude-economy':'电芯','wide-bandgap-semiconductor':'动态导通电阻','solid-state-battery':'界面','synthetic-biology-biomanufacturing':'发酵','industrial-machine-tools':'仿真','smart-sensors-mems':'零偏'};
const pluginChecks=[];
for(const [industry,query] of Object.entries(queries)){
 assert(plugin.framework({industry}).framework);assert(plugin.method({industry}).text.length>100);
 const result=plugin.search({query,industry});assert(result.matches.length,industry);for(const m of result.matches){assert(m.source);assert.equal(plugin.detail(m.id).source_id,m.source_id);assert.notEqual(m.review,'metadata_only');}
 pluginChecks.push({industry,query,hits:result.matches.length});
}
assert.equal(plugin.search({query:'test',industry:'missing'}).error,'unknown_industry');assert.equal(plugin.method({industry:'solid-state-battery',offset:-1}).error,'invalid_offset');
const tools=['search_knowledge',...plugin.getTools().map(t=>t.name)];
const {validateExpertProfile,expertProfilePayload}=await import(pathToFileURL(path.resolve(app,'web/js/expert-profile.mjs')));
for(const industry of Object.keys(queries)){const exp=JSON.parse(fs.readFileSync(path.join(root,'industries',industry,'expert-pack.json'),'utf8'));const errors=validateExpertProfile(exp.expert_profile,tools);assert.equal(errors.length,0,JSON.stringify(errors));assert(expertProfilePayload(exp.expert_profile));}
const {openDatabase}=await import(pathToFileURL(path.resolve(app,'src/storage/db.mjs')));
const {StorageService}=await import(pathToFileURL(path.resolve(app,'src/storage/service.mjs')));
const {KnowledgeService}=await import(pathToFileURL(path.resolve(app,'src/knowledge/knowledge-service.mjs')));
const scratch=fs.mkdtempSync(path.join(os.tmpdir(),'technology-knowledge-test-'));
const config={rootDir:path.resolve(app),dataDir:scratch};const storage=new StorageService(openDatabase(path.join(scratch,'test.db')),config);const knowledge=new KnowledgeService({storage,config});
const expertMap=Object.fromEntries(Object.keys(queries).map((i,k)=>['industry-'+i,'test-industry-'+k]));const org='default',actor='offline-test';
let output;
try{
 const bad=structuredClone(bundle);bad.documents[0].text+='tampered';assert.throws(()=>validateBundle(bad,expertMap),/hash mismatch/);
 const first=importKnowledge({bundle,storage,knowledge,org,actor,expertMap});
 assert.equal(Object.keys(first.documents).length,28);assert.equal(Object.keys(first.equipments).length,28);
 const results=[];for(const [industry,query] of Object.entries(queries)){
  const expertId=expertMap['industry-'+industry];assert.equal(knowledge.getLoadout(org,expertId).active.items.length,4);
  const r=knowledge.search(org,{username:actor,role:'admin',expertId,query});assert(r.results.length,industry+' M12 search');
  for(const hit of r.results){assert.match(hit.citationId,/^KB:/);assert(storage.knowledgeDocuments.chunksFor(hit.documentId,hit.documentVersion).some(c=>c.chunkId===hit.chunkId));}
  results.push({industry,query,hits:r.results.length,citation:r.results[0].citationId});
 }
 const second=importKnowledge({bundle,storage,knowledge,org,actor,expertMap});assert.deepEqual(second.documents,first.documents);
 for(const id of Object.values(expertMap))assert.equal(second.loadouts[id].active.revision,first.loadouts[id].active.revision);
 const updated=structuredClone(bundle);updated.documents[0].text+='\n\n版本验收：测试追加材料。';updated.documents[0].sha256=createHash('sha256').update(updated.documents[0].text).digest('hex');
 const third=importKnowledge({bundle:updated,storage,knowledge,org,actor,expertMap});const key=bundle.documents[0].logical_key;
 assert.equal(third.documents[key].documentId,first.documents[key].documentId);assert.equal(third.documents[key].documentVersion,2);assert(storage.knowledgeDocuments.chunksFor(first.documents[key].documentId,1).length);
 const eqkey=bundle.equipments[0].logical_key;assert.equal(third.equipments[eqkey].equipmentVersion,2);
 const id=expertMap[bundle.equipments[0].expert_key];assert.throws(()=>knowledge.equip(org,actor,{expertId:id,equipmentId:third.equipments[eqkey].equipmentId,equipmentVersion:2,slot:'core_spec',expectedLoadoutRevision:0}),/冲突|revision|版本/i);
 output={status:'PASS',test_type:'actual_FirmBuddy_service_isolated_database',documents:28,equipments:28,experts:7,pluginChecks,knowledgeChecks:results,idempotency:'passed',document_equipment_upgrade:'passed',historical_chunks:'retained',cas_conflict:'rejected',live_llm_answers:'not_run',production_import:'not_run'};
 console.log(JSON.stringify(output,null,2));
 if(process.env.RESULT_FILE)fs.writeFileSync(process.env.RESULT_FILE,JSON.stringify(output,null,2));
}finally{storage.close();}

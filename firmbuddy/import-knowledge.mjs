import fs from 'node:fs';
import path from 'node:path';
import {createHash} from 'node:crypto';
import {pathToFileURL, fileURLToPath} from 'node:url';
const hash=text=>createHash('sha256').update(text).digest('hex');
const one=(arr,label)=>{if(arr.length>1)throw Error(`Ambiguous ${label}`);return arr[0];};
export function validateBundle(bundle,expertMap) {
  const keys=new Set();
  for(const d of bundle.documents){if(keys.has(d.logical_key))throw Error('Duplicate document key');keys.add(d.logical_key);if(hash(d.text)!==d.sha256)throw Error(`Content hash mismatch: ${d.logical_key}`);}
  const ek=new Set();for(const e of bundle.equipments){if(ek.has(e.logical_key))throw Error('Duplicate equipment key');ek.add(e.logical_key);if(!e.document_keys.every(k=>keys.has(k)))throw Error('Unresolved document');if(!expertMap[e.expert_key])throw Error(`Missing actual expert ID for ${e.expert_key}`);}
}
export function importKnowledge({bundle,storage,knowledge,org,actor,expertMap}) {
  validateBundle(bundle,expertMap);
  let space=one(storage.knowledgeSpaces.list(org).filter(s=>s.name===bundle.space.name&&s.scope===bundle.space.scope),'space');
  if(!space)space=knowledge.createSpace(org,actor,bundle.space);
  const docs={},equipments={};
  for(const d of bundle.documents){
    const existing=one(storage.knowledgeDocuments.listBySpace(org,space.spaceId).filter(x=>x.title===d.title),'document '+d.title);
    const current=existing?storage.knowledgeDocuments.getVersion(existing.documentId,existing.currentVersion):null;
    if(current?.sha256===d.sha256){docs[d.logical_key]={documentId:existing.documentId,documentVersion:existing.currentVersion};continue;}
    const up=storage.attachments.saveUpload({filename:d.logical_key.replace(/[^a-z0-9-]/g,'-')+'.txt',buffer:Buffer.from(d.text),org,owner:actor,sessionId:''});
    const r=knowledge.ingestAttachment(org,actor,{spaceId:space.spaceId,attachmentId:up.id,title:d.title,sourceType:d.sourceType,tags:d.tags,documentId:existing?.documentId??'',note:'technology-intelligence '+bundle.version});
    docs[d.logical_key]={documentId:r.document.documentId,documentVersion:r.version};
  }
  for(const e of bundle.equipments){
    const sources=e.document_keys.map(k=>docs[k]);
    const existing=one(storage.knowledgeEquipments.list(org).filter(x=>x.name===e.name&&x.spaceId===space.spaceId),'equipment '+e.name);
    let id,version;
    if(existing){
      id=existing.equipmentId;version=existing.currentVersion;
      const v=storage.knowledgeEquipments.getVersion(id,version);
      const signature=a=>JSON.stringify(a.map(x=>`${x.documentId}:${x.documentVersion}`).sort());
      if(signature(v.sourceDocumentVersions)!==signature(sources)){
        const r=knowledge.createEquipmentVersion(org,actor,id,{sourceDocumentVersions:sources,exportPolicy:e.exportPolicy});version=r.version.version;knowledge.publishEquipment(org,actor,id,version);
      }
    }else{
      const r=knowledge.createEquipment(org,actor,{...e,spaceId:space.spaceId,recommendedExpertIds:[expertMap[e.expert_key]],sourceDocumentVersions:sources});id=r.equipment.equipmentId;version=r.version.version;
    }
    const expertId=expertMap[e.expert_key];const active=storage.expertLoadouts.latestActive(org,expertId);
    if(!(active?.items??[]).some(i=>i.equipmentId===id&&i.equipmentVersion===version&&i.slot===e.slot))knowledge.equip(org,actor,{expertId,equipmentId:id,equipmentVersion:version,slot:e.slot,expectedLoadoutRevision:active?.revision??0,note:'technology-intelligence '+bundle.version});
    equipments[e.logical_key]={equipmentId:id,equipmentVersion:version,expertId,slot:e.slot};
  }
  return {spaceId:space.spaceId,documents:docs,equipments,loadouts:Object.fromEntries([...new Set(Object.values(expertMap))].map(id=>[id,knowledge.getLoadout(org,id)])),status:'documents_equipment_loadouts_imported_not_chat_tested'};
}
async function main(){
  const args=process.argv.slice(2);const arg=k=>args[args.indexOf(k)+1];const apply=args.includes('--apply');
  const bundle=JSON.parse(fs.readFileSync(new URL('./import-bundle.json',import.meta.url),'utf8'));
  if(!apply){console.log(JSON.stringify({mode:'dry-run',documents:bundle.documents.length,equipments:bundle.equipments.length,expertKeys:[...new Set(bundle.equipments.map(e=>e.expert_key))],requires:'--apply --firmbuddy PATH --db PATH --org ORG --expert-map FILE --result FILE; stop service and backup DB before apply'},null,2));return;}
  for(const flag of ['--firmbuddy','--db','--org','--expert-map','--result'])if(!args.includes(flag)||!arg(flag)||arg(flag).startsWith('--'))throw Error('Required '+flag);
  const root=path.resolve(arg('--firmbuddy')), dbPath=path.resolve(arg('--db')),org=arg('--org');const expertMap=JSON.parse(fs.readFileSync(arg('--expert-map'),'utf8'));validateBundle(bundle,expertMap);
  if(!fs.existsSync(dbPath))throw Error('Apply requires an existing, explicitly selected FirmBuddy database. Use integration test for a scratch database.');
  const {openDatabase}=await import(pathToFileURL(path.join(root,'src/storage/db.mjs')));const {StorageService}=await import(pathToFileURL(path.join(root,'src/storage/service.mjs')));const {KnowledgeService}=await import(pathToFileURL(path.join(root,'src/knowledge/knowledge-service.mjs')));
  const personasFile=path.join(root,'plugins/expert-personas/data/personas.json');const raw=JSON.parse(fs.readFileSync(personasFile,'utf8'));const personas=Array.isArray(raw)?raw:raw.personas;
  for(const id of Object.values(expertMap))if(!personas.some(p=>p.id===id))throw Error('Target expert not found in selected FirmBuddy catalog: '+id);
  const config={dataDir:path.dirname(dbPath),rootDir:root};const storage=new StorageService(openDatabase(dbPath),config);try{const result=importKnowledge({bundle,storage,knowledge:new KnowledgeService({storage,config}),org,actor:'technology-intelligence-import',expertMap});fs.writeFileSync(arg('--result'),JSON.stringify(result,null,2));console.log('Imported; result saved. Live expert acceptance remains separate.');}finally{storage.close();}
}
if(process.argv[1]&&fileURLToPath(import.meta.url)===path.resolve(process.argv[1]))main().catch(e=>{console.error(e.message);process.exitCode=1;});

import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';

const args=process.argv.slice(2);
const value=k=>args[args.indexOf(k)+1];
if(!args.includes('--firmbuddy')||!value('--firmbuddy'))throw Error('Usage: node scripts/apply-firmbuddy-v06.mjs --firmbuddy PATH');
const knowledgeRoot=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
const app=path.resolve(value('--firmbuddy'));
const read=p=>JSON.parse(fs.readFileSync(p,'utf8'));
const write=(p,v)=>{fs.mkdirSync(path.dirname(p),{recursive:true});fs.writeFileSync(p,typeof v==='string'?v:JSON.stringify(v,null,2)+'\n');};
const copyDir=(src,dst)=>{fs.mkdirSync(dst,{recursive:true});for(const e of fs.readdirSync(src,{withFileTypes:true})){const s=path.join(src,e.name),d=path.join(dst,e.name);e.isDirectory()?copyDir(s,d):fs.copyFileSync(s,d);}};

const bundle=read(path.join(knowledgeRoot,'firmbuddy/import-bundle.json'));
if(!String(bundle.version).startsWith('0.6.'))throw Error('Expected v0.6 import bundle');
if(bundle.documents.length!==60||bundle.equipments.length!==60)throw Error('Unexpected v0.6 bundle cardinality');

const prepared=read(path.join(knowledgeRoot,'firmbuddy/expert-payloads.json'));
const personasPath=path.join(app,'plugins/expert-personas/data/personas.json');
const catalog=read(personasPath);
const personas=Array.isArray(catalog)?catalog:catalog.personas;
if(!Array.isArray(personas))throw Error('Unsupported personas catalog');
for(const item of prepared.experts){
 const p=item.payload;
 const entry={
  id:item.logical_key,
  ...p,
  expert_profile:item.profile,
  tools_whitelist:[...item.required_tools],
  knowledge_scope:[
   ...(Array.isArray(p.knowledge_scope)?p.knowledge_scope:[]),
   'Knowledge v0.6：Core / Academic / Benchmark / Evidence Framework / Playbook / Patent Method / Company Cases 按各自证据边界使用'
  ],
  output_hint:item.profile.outputRequirements,
  pack_version:1,
  knowledge_release:'0.6.0'
 };
 const idx=personas.findIndex(x=>x.id===entry.id||x.name===entry.name);
 if(idx>=0)personas[idx]={...personas[idx],...entry};else personas.push(entry);
}
write(personasPath,Array.isArray(catalog)?personas:{...catalog,personas});

const vendor=path.join(app,'vendor/knowledge-v06');
write(path.join(vendor,'import-bundle.json'),bundle);
fs.copyFileSync(path.join(knowledgeRoot,'firmbuddy/import-knowledge.mjs'),path.join(vendor,'import-knowledge.mjs'));
copyDir(path.join(knowledgeRoot,'firmbuddy/technology-intelligence'),path.join(app,'plugins/technology-intelligence'));

const index=prepared.experts.map(x=>({logical_key:x.logical_key,name:x.profile.name}));
write(path.join(vendor,'release.json'),{
 version:bundle.version,
 source_repository:'xumengke2025-sys/knowledge',
 source_commit:process.env.KNOWLEDGE_COMMIT||'84f530f9f811aafd0b548de3180b13eda2d55ab9',
 documents:bundle.documents.length,equipments:bundle.equipments.length,experts:index,
 status:'catalog_published_database_import_required'
});

const pkgPath=path.join(app,'package.json');const pkg=read(pkgPath);pkg.scripts??={};
pkg.scripts['knowledge:v06:dry-run']='node vendor/knowledge-v06/import-knowledge.mjs';
pkg.scripts['knowledge:v06:apply']='node vendor/knowledge-v06/import-knowledge.mjs --apply';
pkg.scripts['knowledge:v06:accept']='node scripts/accept-knowledge-v06.mjs';
write(pkgPath,pkg);
console.log(JSON.stringify({status:'APPLIED',version:bundle.version,documents:60,equipments:60,experts:8},null,2));

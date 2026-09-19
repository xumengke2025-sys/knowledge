import fs from 'node:fs';
import path from 'node:path';
import {pathToFileURL,fileURLToPath} from 'node:url';
const args=process.argv.slice(2);const read=k=>args[args.indexOf(k)+1];
if(!args.includes('--firmbuddy')||!args.includes('--output'))throw Error('Usage: node scripts/prepare-experts.mjs --firmbuddy PATH --output FILE');
const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
const {validateExpertProfile,expertProfilePayload}=await import(pathToFileURL(path.resolve(read('--firmbuddy'),'web/js/expert-profile.mjs')));
const bundle=JSON.parse(fs.readFileSync(path.join(root,'firmbuddy/import-bundle.json'),'utf8'));
const industries=[...new Set(bundle.documents.map(d=>d.industry_id))];const result=[];
for(const industry of industries){const pack=JSON.parse(fs.readFileSync(path.join(root,'industries',industry,'expert-pack.json'),'utf8'));const errors=validateExpertProfile(pack.expert_profile,pack.tools_whitelist);if(errors.length)throw Error(JSON.stringify(errors));result.push({logical_key:pack.id,profile:pack.expert_profile,payload:expertProfilePayload(pack.expert_profile),required_tools:pack.tools_whitelist});}
fs.writeFileSync(read('--output'),JSON.stringify({status:'prepared_not_published',runtime_capability_check_required:true,experts:result},null,2));console.log('Prepared '+result.length+' expert payloads; runtime IDs must be read back after formal API publication.');

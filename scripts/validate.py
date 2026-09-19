#!/usr/bin/env python3
import json, pathlib, sys
ROOT=pathlib.Path(__file__).resolve().parents[1]
errors=[]; warnings=[]

def jload(p):
    try: return json.loads(p.read_text(encoding='utf-8'))
    except Exception as e: errors.append(f'{p}: JSON parse failed: {e}'); return {}

def jl(p):
    out=[]
    for n,line in enumerate(p.read_text(encoding='utf-8').splitlines(),1):
        if not line.strip(): continue
        try: out.append(json.loads(line))
        except Exception as e: errors.append(f'{p}:{n}: JSONL parse failed: {e}')
    return out

for d in (ROOT/'industries').iterdir():
    if not d.is_dir(): continue
    required=['README.md','taxonomy.json','company-universe.json','facts.jsonl','sources.json','expert-pack.json','training-set.jsonl','patent-search.md']
    for x in required:
        if not (d/x).exists(): errors.append(f'{d.name}: missing {x}')
    tax=jload(d/'taxonomy.json'); uni=jload(d/'company-universe.json'); src=jload(d/'sources.json'); exp=jload(d/'expert-pack.json')
    facts=jl(d/'facts.jsonl'); training=jl(d/'training-set.jsonl')
    source_ids={s.get('id') for s in src.get('sources',[])}
    for f in facts:
        if not f.get('source_ids'): errors.append(f"{d.name}:{f.get('fact_id')}: missing source_ids")
        for sid in f.get('source_ids',[]):
            if sid not in source_ids: errors.append(f"{d.name}:{f.get('fact_id')}: unresolved source {sid}")
    for c in uni.get('companies',[]):
        if c.get('verification_status','').startswith('verified') and not c.get('evidence'):
            errors.append(f"{d.name}:{c.get('code')} verified without evidence")
        for sid in c.get('evidence',[]):
            if sid not in source_ids: errors.append(f"{d.name}:{c.get('code')}: unresolved evidence {sid}")
    if exp.get('category')!='行业研究系列': errors.append(f'{d.name}: expert category mismatch')
    bp=(exp.get('expert_profile') or {}).get('businessDomain',{})
    if bp.get('primary')!='industry_research': errors.append(f'{d.name}: businessDomain mismatch')
    # no opportunity layer allowed
    dump=json.dumps({'tax':tax,'uni':uni,'facts':facts,'exp':exp},ensure_ascii=False)
    forbidden=['成交概率','商机触发器','推荐证券服务','客户需求假设']
    for term in forbidden:
        if term in dump: warnings.append(f'{d.name}: contains forbidden-layer term: {term}')

# embodied hard gates
ed=ROOT/'industries'/'embodied-intelligence'
eu=jload(ed/'company-universe.json')
if len(eu.get('companies',[]))<40: errors.append('embodied-intelligence: company universe < 40')
if sum(c.get('verification_status','').startswith('verified') for c in eu.get('companies',[]))<10: errors.append('embodied-intelligence: verified companies < 10')
pp=ed/'patents'/'representative-patents.jsonl'
if not pp.exists(): errors.append('embodied-intelligence: missing representative patents')
else:
    pats=jl(pp)
    if len(pats)<8: errors.append('embodied-intelligence: representative patents < 8')

if errors:
    print('FAIL')
    for e in errors: print('ERROR',e)
    for w in warnings: print('WARN',w)
    sys.exit(1)
print('PASS')
for w in warnings: print('WARN',w)

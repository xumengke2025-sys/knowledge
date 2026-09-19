import pathlib,json,hashlib
R=pathlib.Path(__file__).resolve().parents[1]
def load(p):return json.loads(p.read_text(encoding='utf-8'))
def digest(t):return hashlib.sha256(t.encode()).hexdigest()
coverage=load(R/'coverage-v0.3.json');all_ids=set();counts={'nodes':0,'excerpts':0,'papers':0,'reviewed_papers':0}
for row in coverage['industries']:
 d=R/'industries'/row['industry_id'];t=load(d/'taxonomy.json');u=load(d/'company-universe.json');s=load(d/'sources.json');ids=[x['id'] for x in t['nodes']];assert len(ids)==len(set(ids));nodes={x['id']:x for x in t['nodes']}
 for x in nodes.values():
  seen=set();cur=x
  while cur.get('parent_id'):
   assert cur['parent_id'] in nodes;assert cur['id'] not in seen,'taxonomy cycle';seen.add(cur['id']);cur=nodes[cur['parent_id']]
 assert all(n in nodes for c in u['companies'] for n in c['nodes'])
 assert len({c['code'] for c in u['companies']})==len(u['companies'])
 source_ids={x['id'] for x in s['sources']};all_ids.update(source_ids)
 es=load(d/'evidence/excerpts.json')['excerpts']
 for e in es:
  assert e['source_id'] in source_ids;assert e['quote'];assert digest(e['quote'])==e['quote_sha256'];assert e['locator']['char_end']-e['locator']['char_start']==len(e['quote']);assert '\x00' not in e['quote']
 papers=load(d/'research/papers.json')['papers'];assert len({p['doi'].lower() for p in papers})==len(papers)
 for p in papers:
  assert p['reading_status'] in ['metadata_only','abstract_reviewed','sections_reviewed','full_text_reviewed'];assert p['full_text_reviewed'] is False
  if p['reading_status']!='metadata_only':assert p['summary'] and p['limitations'];all_ids.add(p['id'])
 counts['nodes']+=len(nodes);counts['excerpts']+=len(es);counts['papers']+=len(papers);counts['reviewed_papers']+=sum(p['reading_status']!='metadata_only' for p in papers)
 assert row['nodes']==len(nodes) and row['reviewed_excerpts']==len(es) and row['papers']==len(papers)
bundle=load(R/'firmbuddy/import-bundle.json');keys={d['logical_key'] for d in bundle['documents']};assert len(keys)==len(bundle['documents'])==36
for d in bundle['documents']:assert digest(d['text'])==d['sha256'];assert d['sourceType'] in ['research','ai_generated']
for e in bundle['equipments']:assert set(e['document_keys'])<=keys;assert e['type']==e['slot'];assert e['type'] in ['core_spec','research','product_capability','supplement']
data=load(R/'firmbuddy/plugin-data.json');assert data==load(R/'firmbuddy/technology-intelligence/data/knowledge.json')
for i in data['insights']:assert i['source_id'] in all_ids;assert i['review']!='metadata_only'
print('PASS',json.dumps(counts,ensure_ascii=False))

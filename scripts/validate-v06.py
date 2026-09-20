import json, pathlib
R=pathlib.Path(__file__).resolve().parents[1]
ids=['embodied-intelligence','commercial-space-satcom','low-altitude-economy','wide-bandgap-semiconductor','solid-state-battery','synthetic-biology-biomanufacturing','industrial-machine-tools','smart-sensors-mems']
for i in ids:
 d=R/'industries'/i
 j=json.loads((d/'evidence-framework.json').read_text(encoding='utf-8'))
 assert j['version']=='0.6.0'
 assert len(j['standards'])>=1
 assert len(j['research_institutions'])>=6
 assert len(j['radar_query_pack'])>=6
 assert len(j['company_runtime_questions'])>=6
 assert len(j['evidence_upgrade_rules'])==3
 md=(d/'evidence-framework.md').read_text(encoding='utf-8')
 for term in ['标准与测试方法地图','重点科研机构/团队观察池','企业运行时核查问题','证据升级协议']:
  assert term in md
b=json.loads((R/'firmbuddy/import-bundle.json').read_text(encoding='utf-8'))
assert b['version']=='0.6.0'
assert len(b['documents'])==60 and len(b['equipments'])==60
for i in ids:
 assert any(x['logical_key']==i+':evidence-framework' for x in b['documents'])
 assert any(x['logical_key']==i+':evidence-framework' and x['type']=='research' for x in b['equipments'])
print('PASS v0.6 evidence framework')

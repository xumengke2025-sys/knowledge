import datetime as dt,json,pathlib
R=pathlib.Path(__file__).resolve().parents[1]
IDS=["embodied-intelligence","commercial-space-satcom","low-altitude-economy","wide-bandgap-semiconductor","solid-state-battery","synthetic-biology-biomanufacturing","industrial-machine-tools","smart-sensors-mems"]
today=dt.date.today()
total=0
for iid in IDS:
 p=R/"industries"/iid/"radar"/"inbox-academic.jsonl"
 assert p.exists(),(iid,"missing radar inbox")
 rows=[json.loads(x) for x in p.read_text(encoding="utf-8").splitlines() if x.strip()]
 assert len(rows)>=5,(iid,"too few candidates",len(rows))
 for r in rows:
  assert r["verification_status"]=="candidate" and r["promote_to_stable_knowledge"] is False
  y=int(str(r["publication_date"])[:4]);assert y<=today.year,(iid,r["title"],r["publication_date"])
  assert r.get("relevance_match_count",0)>=1,(iid,r["title"],"missing relevance")
  if "crossref" in r.get("channels",[]): assert r.get("relevance_match_count",0)>=2,(iid,r["title"],r.get("relevance_terms"))
 total+=len(rows)
summary=json.loads((R/"radar"/"academic-refresh-summary.json").read_text(encoding="utf-8"))
assert len(summary["industries"])==8
print("PASS",json.dumps({"industries":8,"academic_radar_candidates":total},ensure_ascii=False))

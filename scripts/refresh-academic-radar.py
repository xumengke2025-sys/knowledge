#!/usr/bin/env python3
import argparse, datetime as dt, json, pathlib, re, time, urllib.parse, urllib.request

ROOT=pathlib.Path(__file__).resolve().parents[1]
INDUSTRIES=[
 "embodied-intelligence","commercial-space-satcom","low-altitude-economy","wide-bandgap-semiconductor",
 "solid-state-battery","synthetic-biology-biomanufacturing","industrial-machine-tools","smart-sensors-mems"
]
UA="FirmBuddy-Technology-Intelligence-Radar/0.5 (+https://github.com/xumengke2025-sys/knowledge)"
STOPWORDS={"the","and","for","with","from","into","using","based","system","systems","engineering","industrial","technology","technologies","study","studies","model","models","control","current","high","performance","analysis"}
def query_terms(q):
    en=[x.lower() for x in re.findall(r"[A-Za-z][A-Za-z0-9-]{2,}",q) if x.lower() not in STOPWORDS]
    zh=[x for x in re.findall(r"[\u4e00-\u9fff]{2,}",q)]
    return list(dict.fromkeys(en+zh))
def relevance(text,q):
    t=str(text or "").lower().replace("-"," ")
    hits=[x for x in query_terms(q) if x.lower().replace("-"," ") in t]
    return hits
def sane_date(value,from_date,today):
    if not value:return False
    m=re.match(r"^(\d{4})",str(value))
    if not m:return False
    y=int(m.group(1));return int(from_date[:4])<=y<=today.year


def get_json(url, timeout=30):
    req=urllib.request.Request(url,headers={"User-Agent":UA,"Accept":"application/json"})
    with urllib.request.urlopen(req,timeout=timeout) as r:
        return json.loads(r.read().decode("utf-8"))

def date_parts(x):
    if not x:return ""
    parts=x.get("date-parts") if isinstance(x,dict) else None
    if not parts or not parts[0]:return ""
    a=parts[0]
    return "-".join([str(a[0]).zfill(4)]+[str(v).zfill(2) for v in a[1:3]])

def norm_doi(v):
    s=str(v or "").strip().lower()
    for p in ["https://doi.org/","http://doi.org/","doi:"]: 
        if s.startswith(p):s=s[len(p):]
    return s

def authors_openalex(a):
    out=[];inst=[]
    for row in a or []:
        au=(row.get("author") or {}).get("display_name")
        if au:out.append(au)
        for i in row.get("institutions") or []:
            n=i.get("display_name")
            if n:inst.append(n)
    return out[:12],list(dict.fromkeys(inst))[:12]

def openalex(query,from_date,per_page):
    params={
      "search":query,"filter":f"from_publication_date:{from_date}",
      "sort":"publication_date:desc,relevance_score:desc","per_page":str(per_page)
    }
    url="https://api.openalex.org/works?"+urllib.parse.urlencode(params)
    data=get_json(url)
    out=[]
    for w in data.get("results",[]):
        authors,inst=authors_openalex(w.get("authorships"))
        oa=w.get("open_access") or {}
        topic=w.get("primary_topic") or {}
        title=w.get("display_name") or ""; topic_name=topic.get("display_name") or ""
        hits=relevance(title+" "+topic_name,query)
        if len(hits)<1: continue
        out.append({
          "record_id":w.get("id"),"doi":norm_doi(w.get("doi")),"title":title,
          "publication_date":w.get("publication_date") or "","publication_type":w.get("type") or "",
          "cited_by_count":w.get("cited_by_count") or 0,"authors":authors,"institutions":inst,
          "primary_topic":topic_name,"is_oa":bool(oa.get("is_oa")),
          "oa_status":oa.get("oa_status"),"landing_page":(w.get("primary_location") or {}).get("landing_page_url") or w.get("doi") or w.get("id"),
          "channel":"openalex","query":query,"relevance_terms":hits,"relevance_match_count":len(hits)
        })
    return out,url

def crossref(query,from_date,rows):
    today=dt.date.today().isoformat()
    params={"query.title":query,"filter":f"from-pub-date:{from_date},until-pub-date:{today}","rows":str(rows),"sort":"score","order":"desc"}
    url="https://api.crossref.org/works?"+urllib.parse.urlencode(params)
    data=get_json(url)
    out=[]
    for w in ((data.get("message") or {}).get("items") or []):
        auth=[]
        for a in w.get("author") or []:
            n=" ".join(x for x in [a.get("given"),a.get("family")] if x)
            if n:auth.append(n)
        title=(w.get("title") or [""])[0]
        pub=date_parts(w.get("published-online") or w.get("published-print") or w.get("published"))
        hits=relevance(title,query)
        if len(hits)<min(2,max(1,len(query_terms(query)))): continue
        out.append({
          "record_id":"https://doi.org/"+w.get("DOI","") if w.get("DOI") else "",
          "doi":norm_doi(w.get("DOI")),"title":title,"publication_date":pub,
          "publication_type":w.get("type") or "","cited_by_count":w.get("is-referenced-by-count") or 0,
          "authors":auth[:12],"institutions":[],"primary_topic":"","is_oa":None,"oa_status":None,
          "landing_page":w.get("URL") or ("https://doi.org/"+w.get("DOI","") if w.get("DOI") else ""),
          "channel":"crossref","query":query,"relevance_terms":hits,"relevance_match_count":len(hits)
        })
    return out,url

def merge(records):
    d={}
    for r in records:
        key=("doi:"+r["doi"]) if r.get("doi") else ("title:"+r.get("title","").strip().lower())
        if not key or key=="title:":continue
        if key not in d:
            x=dict(r);x["channels"]=[r["channel"]];x["queries"]=[r["query"]];d[key]=x
        else:
            x=d[key];x["channels"]=list(dict.fromkeys(x["channels"]+[r["channel"]]))
            x["queries"]=list(dict.fromkeys(x["queries"]+[r["query"]]))
            if not x.get("institutions") and r.get("institutions"):x["institutions"]=r["institutions"]
            if not x.get("primary_topic") and r.get("primary_topic"):x["primary_topic"]=r["primary_topic"]
            x["cited_by_count"]=max(x.get("cited_by_count",0),r.get("cited_by_count",0))
    return list(d.values())

def main():
    ap=argparse.ArgumentParser();ap.add_argument("--days",type=int,default=240);ap.add_argument("--limit-per-query",type=int,default=8)
    args=ap.parse_args()
    today=dt.date.today();from_date=(today-dt.timedelta(days=args.days)).isoformat();summary={"as_of":today.isoformat(),"from_date":from_date,"industries":[]}
    for iid in INDUSTRIES:
        src=json.loads((ROOT/"industries"/iid/"radar-sources.json").read_text(encoding="utf-8"))
        packs=[x for x in src.get("industry_specific",[]) if x.get("channel")=="academic_query_pack"]
        queries=[]
        for p in packs:queries.extend(p.get("queries") or [])
        rec=[];attempts=[]
        for q in queries:
            for channel,fn in [("openalex",openalex),("crossref",crossref)]:
                try:
                    rows,url=fn(q,from_date,args.limit_per_query);rec+=rows;attempts.append({"channel":channel,"query":q,"ok":True,"count":len(rows),"url":url})
                except Exception as e:
                    attempts.append({"channel":channel,"query":q,"ok":False,"error":str(e)[:300]})
                time.sleep(.2)
        items=merge(rec)
        items=[x for x in items if sane_date(x.get("publication_date"),from_date,today)]
        items.sort(key=lambda x:(x.get("publication_date") or "",x.get("cited_by_count") or 0),reverse=True)
        items=items[:40]
        now=dt.datetime.now(dt.timezone.utc).isoformat()
        for x in items:
            x["industry_id"]=iid;x["discovered_at"]=now;x["verification_status"]="candidate"
            x["promote_to_stable_knowledge"]=False
            x["review_required"]=["主题是否真正落入taxonomy","是否需要阅读全文","方法/实验条件是否足以支持机制结论","是否改变现有benchmark或路线判断"]
        outdir=ROOT/"industries"/iid/"radar";outdir.mkdir(parents=True,exist_ok=True)
        (outdir/"inbox-academic.jsonl").write_text("\n".join(json.dumps(x,ensure_ascii=False) for x in items)+("\n" if items else ""),encoding="utf-8")
        (outdir/"refresh-log.json").write_text(json.dumps({"industry_id":iid,"from_date":from_date,"attempts":attempts},ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
        summary["industries"].append({"industry_id":iid,"queries":len(queries),"candidates":len(items),"successful_requests":sum(a["ok"] for a in attempts),"failed_requests":sum(not a["ok"] for a in attempts)})
    rd=ROOT/"radar";rd.mkdir(exist_ok=True)
    (rd/"academic-refresh-summary.json").write_text(json.dumps(summary,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(summary,ensure_ascii=False))
if __name__=="__main__":main()

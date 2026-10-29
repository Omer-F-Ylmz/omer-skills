"""Oturum başı jeton: claude -p tek tur, kancalar açık, usage toplamı."""
import json,subprocess,sys,time
kol,ayar=sys.argv[1],sys.argv[2]; ek=sys.argv[3:]
t=time.time()
r=subprocess.run(["claude","-p","Yalnız OK yaz.","--model","haiku","--output-format","json","--settings",ayar,"--max-turns","1",*ek],capture_output=True,text=True,encoding="utf-8",timeout=900)
try:
    d=json.loads(r.stdout); u=d.get("usage",{})
    top=u.get("input_tokens",0)+u.get("cache_creation_input_tokens",0)+u.get("cache_read_input_tokens",0)
    out=dict(kol=kol,ilk=top,usd=d.get("total_cost_usd"),sn=round(time.time()-t,1),yanit=str(d.get("result"))[:60])
except Exception as e: out=dict(kol=kol,hata=str(e),err=r.stderr[-300:])
open("bas.jsonl","a",encoding="utf-8").write(json.dumps(out,ensure_ascii=False)+"\n"); print(out)

"""ERTELE-3 TUR 3: S kolu (Skill reddi + 141 ajan reddi) canlı: katalogdan skill yükleme + /komut. Sırayla, haiku."""
import json,subprocess,time
IST=r"C:\Projeler\omer-skills\tools\ertele_istem.md"
TESTLER=[
 ("katalog","Bir commit mesajı yazma kuralları skill'i bul, tam metnini yükle ve ilk başlığını aynen yaz.",["--append-system-prompt-file",IST,"--allowedTools","Bash(python C:/Projeler/omer-skills/tools/ertele_katalog.py:*)","--max-turns","6"]),
 ("slash","/departman-surec-plan tek cümle: bu skill'in adını yaz.",["--max-turns","2"]),
]
for ad,ist,ek in TESTLER:
    t=time.time()
    r=subprocess.run(["claude","-p","--model","haiku","--output-format","json","--settings","ayar-S.json",*ek],input=ist,capture_output=True,text=True,encoding="utf-8",timeout=1200)
    try:
        d=json.loads(r.stdout); out=dict(ad=ad,usd=d.get("total_cost_usd"),tur=d.get("num_turns"),sn=round(time.time()-t),yanit=str(d.get("result"))[:300],red=[x.get("tool_name") for x in d.get("permission_denials",[])])
    except Exception as e: out=dict(ad=ad,hata=str(e),err=r.stderr[-300:],out=r.stdout[-300:])
    open("canli.jsonl","a",encoding="utf-8").write(json.dumps(out,ensure_ascii=False)+"\n")

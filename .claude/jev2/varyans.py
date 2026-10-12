import json, sys, hashlib
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
WT = Path(__file__).resolve().parents[2]; J1 = Path("C:/Projeler/omer-skills-wt/jev/.claude/jev1")
sys.path[:0] = [str(WT/"tools"/"olcum"), str(WT/"tools"/"jev"), str(J1)]
import jev_yargic
from karsilastir_ab import spearman
jev1 = {k["dosya"]: k for k in map(json.loads, open(J1/"jev_tum.jsonl", encoding="utf-8"))}
dos, opus = json.load(open(J1/"ornek_sira.json")), json.load(open(J1/"opus_ref.json"))
o = [opus[str(i)]*2 for i in range(len(dos))]
ob = json.load(open(Path(__file__).parent/"olc_ob.json", encoding="utf-8"))
q = json.dumps(jev_yargic.SORU, sort_keys=True, ensure_ascii=False)
a = [jev1[d]["jev"] for d in dos]
b = [round(ob[hashlib.sha256((q+"\0"+json.dumps(jev1[d]["state"], sort_keys=True, ensure_ascii=False)).encode()).hexdigest()]["kalite"]["score"]*2,1) for d in dos]
ort = [(x+y)/2 for x,y in zip(a,b)]
print("kosu1~kosu2 rho", spearman(a,b), "ayni", sum(x==y for x,y in zip(a,b)), "/", len(a))
print("rho opus: k1", spearman(a,o), "k2", spearman(b,o), "ort2", spearman(ort,o))

"""JEV-2 d5: güvenilirlik — Jev güveni en düşük %k öğe Opus'a yükseltilirse karma ρ/MAE (ücretsiz, mevcut veriden)."""
import json, sys, hashlib, random
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
c = [ob[hashlib.sha256((q+"\0"+json.dumps(jev1[d]["state"], sort_keys=True, ensure_ascii=False)).encode()).hexdigest()]["kalite"] for d in dos]
j = [round(x["score"]*2, 1) for x in c]; g = [x.get("confidence") or 0 for x in c]
mae = lambda a: round(sum(abs(x-y) for x, y in zip(a, o))/len(o), 2)
print("güven aralığı", min(g), max(g), "ayrık", len(set(g)))
for k in (0, 5, 10, 15, 25):
    for ad, sira in (("dusuk-guven", sorted(range(len(j)), key=lambda i: g[i])),
                     ("orta-bant", sorted(range(len(j)), key=lambda i: abs(j[i]-7))),
                     ("rastgele", random.Random(1).sample(range(len(j)), len(j)))):
        h = list(j)
        for i in sira[:k]:
            h[i] = o[i]
        print(f"k={k:2d} {ad:11s} ρ {spearman(h, o)} MAE {mae(h)}")
print("merkez duyarlılığı (k=5 / k=10):")
for m in (6.0, 6.5, 7.0, 7.5, 8.0):
    r = []
    for k in (5, 10):
        h = list(j)
        for i in jev_yargic.belirsiz(j, k / len(j), m):
            h[i] = o[i]
        r.append(spearman(h, o))
    print(f"  merkez {m}: ρ {r[0]} / {r[1]}")

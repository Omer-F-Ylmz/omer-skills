"""olc_cevir.py + üçüncü kol (soz3). Ayrı: karma+en vs karma+en+soz3, ayar/test (aynı seed 7 ayrımı)."""
import json, random, sys
from collections import Counter
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
D = Path(__file__).resolve().parent
sys.path.insert(0, str(D))
import her_sey_ara as h
a = h.Arayici(); a.etiketle(D / (sys.argv[1] if len(sys.argv) > 1 else "etiket.json"))
cev = json.loads((D / "sorgu-cevir.json").read_text(encoding="utf-8"))
tet = h.yukle(D / "tetik.jsonl")
random.seed(7)
adlar = sorted({t["ad"] for t in tet}); random.shuffle(adlar)
test = set(adlar[: len(adlar) // 5])
K = (20, 40, 80, 120)
V = {"karma+en": ["bm", "yo", "bm_en", "yo_en"], "+soz3": ["bm", "yo", "bm_en", "yo_en", "s3", "s3_en"], "+soz3(tek)": ["bm", "yo", "bm_en", "yo_en", "s3_en"]}
res = {}
for t in tet:
    hd, g = t["ad"].lower(), ("test" if t["ad"] in test else "ayar")
    for q in t["sorgular"]:
        en = cev.get(q, "")
        L = {"bm": a.bm25(q), "yo": a.yogun(q), "s3": a.soz3(q)}
        if en: L.update(bm_en=a.bm25(en), yo_en=a.yogun(en), s3_en=a.soz3(en))
        for v, parca in V.items():
            r = Counter()
            for p_ in parca:
                for k, i in enumerate(L.get(p_, [])): r[i] += 1 / (60 + k + 1)
            sira = [a.rows[i]["ad"].lower() for i, _ in r.most_common(max(K))]
            s = res.setdefault((v, g), Counter()); s["n"] += 1
            for k in K: s[k] += hd in sira[:k]
for (v, g), s in sorted(res.items()):
    print(f"{v:11} {g:4} n={s['n']} " + " ".join(f"@{k}=%{100*s[k]/s['n']:.1f}" for k in K))

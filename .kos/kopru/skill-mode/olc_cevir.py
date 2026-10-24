"""1) RAM için arka plandaki hsa_deney'i durdur (e5-large 2+ GB, ajanlar RAM %89'da). 2) karma + TR→EN genişletme ölçümü,
%80 ayar / %20 ayrılmış test (skill bazında ayrım, seed 7)."""
import json, random, sys
from collections import Counter
from pathlib import Path
import psutil
sys.stdout.reconfigure(encoding="utf-8")
for p in psutil.process_iter(["pid", "cmdline"]):
    c = " ".join(p.info["cmdline"] or [])
    if "hsa_deney.py" in c or ("hsa_arka.py" in c and " ic" in c):
        try:
            p.kill(); print("durduruldu", p.info["pid"], c[-40:])
        except psutil.Error:
            pass
D = Path(__file__).resolve().parent
sys.path.insert(0, str(D))
import her_sey_ara as h
a = h.Arayici()
cev = json.loads((D / "sorgu-cevir.json").read_text(encoding="utf-8"))
tet = h.yukle(D / "tetik.jsonl")
random.seed(7)
adlar = sorted({t["ad"] for t in tet}); random.shuffle(adlar)
test = set(adlar[: len(adlar) // 5])
K = (20, 40, 80, 120)
varyant = {}
for t in tet:
    hd, grup = t["ad"].lower(), ("test" if t["ad"] in test else "ayar")
    for q in t["sorgular"]:
        en = cev.get(q, "")
        listeler = {"bm": a.bm25(q), "yo": a.yogun(q)}
        if en:
            listeler["bm_en"] = a.bm25(en)
            listeler["yo_en"] = a.yogun(en)
            listeler["bm_kar"] = a.bm25(q + " " + en)
        for vad, parca in {"karma": ["bm", "yo"], "karma+en": ["bm", "yo", "bm_en", "yo_en"],
                           "karma+kar": ["bm_kar", "yo", "yo_en"], "hepsi": ["bm", "yo", "bm_en", "yo_en", "bm_kar"]}.items():
            r = Counter()
            for p_ in parca:
                for k, i in enumerate(listeler.get(p_, [])):
                    r[i] += 1 / (60 + k + 1)
            sira = [a.rows[i]["ad"].lower() for i, _ in r.most_common(max(K))]
            s = varyant.setdefault((vad, grup), Counter())
            s["n"] += 1
            for k in K:
                s[k] += hd in sira[:k]
print(f"çeviri kapsamı {len(cev)}/600 · test skill {len(test)}")
for (v, g), s in sorted(varyant.items()):
    print(f"{v:10} {g:4} n={s['n']} " + " ".join(f"@{k}=%{100 * s[k] / s['n']:.1f}" for k in K))

"""ORDU-1 d7: hakem güvenilirliği. 6 orta işin her biri için canlı ücretsiz ailelerden birer yanıt (önbellek B6-yanit-<iş>-<aile>.json), aile çiftlerinden
iş başı en çok 5 çift → ordu.kabul(bayraklı ölçüt, ordu.hakem üçüncü aile). Yanlış kabul = kabul edilen yanıt o.dogru'dan geçmedi; hakem hatası = hakem AYNI dedi
ama iki yanıtın doğruluğu ayrışıyor. claude -p yok; ücretsiz yanıt ≤60, hakem ≤40 çağrı.
  python tools/olcum/ordu_olc6.py <çıktı_dizini>"""
import itertools
import json
import random
import sys
from pathlib import Path

import ordu_olc3 as d3
import ucretsiz_havuz as h

o, ordu = d3.o, d3.ordu
AILELER = ("google", "openai", "alibaba", "minimax", "mistral", "nvidia")
YANIT_TAVAN, HAKEM_TAVAN, CIFT = 60, 40, 5


def yanit(a, aile, cikti, say):
    ham = cikti / f"B6-yanit-{a}-{aile}.json"
    if not ham.exists():
        if say["yanit"] >= YANIT_TAVAN:
            raise RuntimeError("yanıt tavanı")
        say["yanit"] += 1
        y, k, _ = h.cagir("hakem", o.istem([a]), max_tokens=1500, aile=aile)
        ham.write_text(json.dumps([y, k], ensure_ascii=False), encoding="utf-8")
    return (o.json_ilk(json.loads(ham.read_text(encoding="utf-8"))[0] or "") or {}).get(a)


def olc(cikti):
    say, R, sat = {"yanit": 0, "hakem": 0}, random.Random(7), []
    for a in (g for g in o.GOREV if g[0] == "O"):
        ys = {f: yanit(a, f, cikti, say) for f in AILELER}
        ys = {f: y for f, y in ys.items() if y is not None}
        ciftler = list(itertools.combinations(sorted(ys), 2))
        R.shuffle(ciftler)
        for f1, f2 in ciftler[:CIFT]:
            onb = cikti / f"B6-hakem-{a}-{f1}-{f2}.json"

            def hakem(x, y):
                if not onb.exists():
                    if say["hakem"] >= HAKEM_TAVAN:
                        raise RuntimeError("hakem tavanı")
                    say["hakem"] += 1
                    v = ordu.hakem(o.GOREV[a][0], x, y, [f1, f2])
                    if v is None:
                        return None
                    onb.write_text(json.dumps(v), encoding="utf-8")
                return json.loads(onb.read_text(encoding="utf-8"))

            k = ordu.kabul([ys[f1], ys[f2]], hakem_=hakem, gevsek=True, tur=o.TUR.get(a, "kesin"))
            c = [o.dogru(a, ys[f1]), o.dogru(a, ys[f2])]
            sat.append({"is": a, "cift": [f1, f2], "dogru": c, "kabul": k is not None, "kabul_dogru": k is not None and o.dogru(a, k),
                        "hakem_cagrildi": onb.exists(), "hakem_hata": k is not None and c[0] != c[1]})
    return sat, say


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    cikti = Path(sys.argv[1])
    sat, say = olc(cikti)
    ozet = {"ornek": len(sat), "ayrisan_cift": sum(s["dogru"][0] != s["dogru"][1] for s in sat), "kabul": sum(s["kabul"] for s in sat),
            "yanlis_kabul": sum(s["kabul"] and not s["kabul_dogru"] for s in sat), "hakem_hata": sum(s["hakem_hata"] for s in sat),
            "hakem_cagrisi_olan": sum(s["hakem_cagrildi"] for s in sat), **say}
    (cikti / "olcum6.json").write_text(json.dumps({"ozet": ozet, "sat": sat}, ensure_ascii=False, indent=1), encoding="utf-8")
    print(json.dumps(ozet, ensure_ascii=False))
    for s in sat:
        if s["kabul"] and not s["kabul_dogru"] or s["hakem_hata"]:
            print(json.dumps(s, ensure_ascii=False))

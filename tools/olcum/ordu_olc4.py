"""ORDU-1 d5: d4 kapısının A kolu modellemeydi. 20 işten tabakalı 10'u için GERÇEK A (iş başı ayrı Sonnet high oturumu) → modellenenle fark;
fark >%25 ise kapı yeniden hesaplanır. Orta sınıfta "ilk çıkışta Haiku medium" kuralı önbellekten kıyaslanır (yeni claude -p yok). Önbellek tek kayıtta toplanır.
  python tools/olcum/ordu_olc4.py <çıktı_dizini> <kayit.json>"""
import json
import random
import sys
from pathlib import Path

import ordu_olc3 as d3

o, ordu, yonlendir = d3.o, d3.ordu, d3.yonlendir
o.CAGRI_TAVAN = 10
TABAKA = {"K": 3, "O": 3, "Z": 3, "I": 1}


def ornek():
    r = random.Random(21)
    return sorted(a for s, n in TABAKA.items() for a in r.sample([g for g in o.GOREV if g[0] == s], n))


def gercek_a(cikti, secilen, model):
    kd = {**yonlendir.kurallar()["kademe"]["T3"], "kademe": "T3"}
    sat = {}
    for a in secilen:
        y, j, usd = o.claude([a], kd, cikti / f"A4-{a}.json")
        sat[a] = {"gecti": o.dogru(a, y.get(a)), "jeton": j, "model": round(model[a]["jeton"]), "usd": round(usd, 4)}
    return sat


def kapi_yeniden(model, gercek):
    """gerçek örneklem oranıyla kalan işlerin A jetonu ölçeklenir; örneklemdeki işler gerçek değerle"""
    oran = sum(s["jeton"] for s in gercek.values()) / sum(model[a]["jeton"] for a in gercek)
    sat = {a: {**s, "jeton": s["jeton"] if a in gercek else s["jeton"] * oran, "gecti": gercek[a]["gecti"] if a in gercek else s["gecti"]} for a, s in model.items()}
    return oran, d3.ozet(sat)


def haiku_ilk(cikti):
    """orta işler: Haiku medium önbellek (yeni çağrı yok); yoksa yok"""
    ag, b = ordu.AGIRLIK["haiku"], ordu.MERDIVEN[1]
    sat = {}
    for a in (g for g in o.GOREV if g[0] == "O"):
        p = cikti / f"B3-haiku-medium-{a}.json"
        if p.exists():
            y, j, _ = o.claude([a], {**b, "kademe": b["ad"]}, p)
            sat[a] = {"gecti": o.dogru(a, y.get(a)), "jeton": j, "agirlikli": round(j * ag)}
    return sat


def kayit(cikti, hedef):
    toplu = {}
    for p in sorted(cikti.glob("*.json")):
        t = p.read_text(encoding="utf-8")
        try:
            toplu[p.name] = json.loads(t)
        except ValueError:
            toplu[p.name] = t
    hedef.write_text(json.dumps(toplu, ensure_ascii=False), encoding="utf-8")
    return len(toplu)


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    cikti, hedef = Path(sys.argv[1]), Path(sys.argv[2])
    yuk = d3.sabit_yuk(cikti)
    model = d3.kol_a(cikti, yuk)
    secilen = ornek()
    gercek = gercek_a(cikti, secilen, model)
    fark = sum(s["jeton"] for s in gercek.values()) / sum(s["model"] for s in gercek.values()) - 1
    oran, A = kapi_yeniden(model, gercek)
    B = json.loads((cikti / "olcum3.json").read_text(encoding="utf-8"))["B"]
    orta = haiku_ilk(cikti)
    sonuc = {"secilen": secilen, "gercek": gercek, "fark": round(fark, 3), "olcek": round(oran, 3), "A_yeni": A, "B": B, "gecti": ordu.kapi3(A, B),
             "oran": {"is": round(B["claude_is"] / A["claude_is"], 3), "agirlikli_token": round(B["agirlikli_token"] / A["agirlikli_token"], 3)},
             "haiku_ilk_orta": orta, "claude_cagri": o.Sayac.claude}
    (cikti / "olcum4.json").write_text(json.dumps(sonuc, ensure_ascii=False, indent=1), encoding="utf-8")
    print(json.dumps({k: sonuc[k] for k in ("secilen", "fark", "olcek", "gecti", "oran", "claude_cagri")}, ensure_ascii=False), A["kalite"], A["kalan"])
    print("kayit:", kayit(cikti, hedef), "dosya")

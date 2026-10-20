"""ORDU-1 d6: orta işte çapraz kontrol ölçütü gevşetildi (normalize eşitlik + üçüncü aile hakem). Önbellekteki 6 orta iş (B3-capraz-O*) üzerinde
eski/yeni ölçüt: kaç iş Haiku'ya yükselmeden kabul, kabul edilenlerin kaçı yanlış (o.dogru; yanlış kabul 0 değilse ölçüt uygulanmaz). claude -p yok;
hakem yanıtı B5-hakem-<iş>.json önbelleğinde (ücretsiz çağrı en fazla 6).
  python tools/olcum/ordu_olc5.py <çıktı_dizini>"""
import json
import sys
from pathlib import Path

import ordu_olc3 as d3

o, ordu = d3.o, d3.ordu


def olc(cikti):
    sat, hakem_cagri = {}, 0
    for a in (g for g in o.GOREV if g[0] == "O"):
        ham = json.loads((cikti / f"B3-capraz-{a}.json").read_text(encoding="utf-8"))
        ys = [(o.json_ilk(t) or {}).get(a) for t, _, _ in ham]
        aileler = [f for _, _, f in ham]
        onb = cikti / f"B5-hakem-{a}.json"

        def hakem(x, y):
            nonlocal hakem_cagri
            if not onb.exists():
                if hakem_cagri >= 6:
                    raise RuntimeError("hakem tavanı")
                hakem_cagri += 1
                v = ordu.hakem(o.GOREV[a][0], x, y, aileler)
                if v is None:  # yanıt veren üçüncü aile yok: önbelleğe yazma
                    return None
                onb.write_text(json.dumps(v), encoding="utf-8")
            return json.loads(onb.read_text(encoding="utf-8"))

        eski = ordu.kabul(ys, gevsek=False)
        yeni = ordu.kabul(ys, hakem_=hakem, gevsek=True)
        sat[a] = {"eski_kabul": eski is not None, "eski_dogru": eski is not None and o.dogru(a, eski),
                  "yeni_kabul": yeni is not None, "yeni_dogru": yeni is not None and o.dogru(a, yeni), "hakem": onb.exists() and json.loads(onb.read_text(encoding="utf-8"))}
    return sat


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    cikti = Path(sys.argv[1])
    sat = olc(cikti)
    ozet = {k: sum(s[f"{k}_kabul"] for s in sat.values()) for k in ("eski", "yeni")}
    ozet |= {f"{k}_yanlis_kabul": sum(s[f"{k}_kabul"] and not s[f"{k}_dogru"] for s in sat.values()) for k in ("eski", "yeni")}
    sonuc = {"is": sat, "ozet": ozet, "ucretsiz_hakem_cagri": sum(1 for a in sat if (cikti / f"B5-hakem-{a}.json").exists())}
    (cikti / "olcum5.json").write_text(json.dumps(sonuc, ensure_ascii=False, indent=1), encoding="utf-8")
    print(json.dumps(sonuc, ensure_ascii=False))

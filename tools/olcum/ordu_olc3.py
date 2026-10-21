"""ORDU-1 d3 kapı: d2'deki 20 held-out iş, Claude çağrıları iş başı ayrı oturum (claude -p tavanı 12; sığmayan basamak tek toplu çağrı).
A = bugünkü düzen: her iş kendi Sonnet high oturumunda. d2'nin toplu A yanıtları önbellekten okunur, oturum başı sabit yük bir kalibrasyon çağrısıyla ölçülüp
her işe eklenir (20 oturum tavanı aşar → A modellenir). B = ücretsiz → Haiku medium → Sonnet medium (çekirdek, Haiku/ücretsiz taslağıyla) → Opus medium;
zor/imkansiz işler de ücretsizden başlar, orta işler iki aile çapraz kontrolle (aynı yanıt → kabul, ayrışma → yükselt), kolay/zor/imkansiz mekanik kabulle.
Kapı: ordu.kapi3 (Claude alt iş ≤%50 · ağırlıklı token ≤%60 · kalite ≥ A).
  python tools/olcum/ordu_olc3.py <çıktı_dizini>   (d2 önbelleği çıktı dizinine kopyalanmış olmalı: A-*.json, B-ucretsiz-K*/O*.json)"""
import json
import sys
from pathlib import Path

import ordu_olc as o  # noqa: E402  (sys.path'e tools/ ekler)
import ordu  # noqa: E402
import ucretsiz_havuz  # noqa: E402
import yonlendir  # noqa: E402

o.CAGRI_TAVAN, o.UCRETSIZ_TAVAN = 12, 90
GOREV = o.GOREV
ADIMLAR = (1, 3, 5)  # ordu.MERDIVEN: haiku-medium · sonnet-medium · opus-medium
AG = lambda ad: ordu.AGIRLIK[ad.split("-")[0]]


def sabit_yuk(cikti):
    """oturum başı sabit Claude yükü: A kolundaki (Sonnet high) boş bir oturumun jetonu"""
    kd = {**yonlendir.kurallar()["kademe"]["T3"], "kademe": "T3"}
    return o.claude(["C0"], kd, cikti / "C0.json", 'Yalnız {"C0": "tamam"} JSON nesnesini döndür. Araç kullanma.')[1]


def kol_a(cikti, yuk):
    """d2 toplu A yanıtları (önbellek) → iş başı ayrı oturum modeli: toplu jeton − yük + iş başı yük"""
    kd = {**yonlendir.kurallar()["kademe"]["T3"], "kademe": "T3"}
    sat = {}
    for ad, adlar in (("kolayorta", [a for a in GOREV if a[0] in "KO"]), ("zor", [a for a in GOREV if a[0] == "Z"]), ("imk", ["I1", "I2"])):
        y, j, usd = o.claude(adlar, kd, cikti / f"A-{ad}.json")
        sat.update({a: {"gecti": o.dogru(a, y.get(a)), "jeton": (j - yuk) / len(adlar) + yuk, "claude_is": 1} for a in adlar})
    return sat


def hakem_onb(a, aileler, cikti):
    """ordu.hakem sonucu B5-hakem-<iş>.json önbelleğinde; yanıt veren üçüncü aile yoksa None (yazılmaz)"""
    onb = cikti / f"B5-hakem-{a}.json"

    def hakem(x, y):
        if not onb.exists():
            if o.Sayac.ucretsiz >= o.UCRETSIZ_TAVAN:
                raise RuntimeError("ücretsiz tavanı")
            o.Sayac.ucretsiz += 1
            v = ordu.hakem(o.GOREV[a][0], x, y, aileler)
            if v is None:
                return None
            onb.write_text(json.dumps(v), encoding="utf-8")
        return json.loads(onb.read_text(encoding="utf-8"))
    return hakem


def capraz(a, cikti):
    """orta iş: iki aileden birer yanıt → (kabul edilen yanıt | ham birinci yanıt, kabul mü, aileler); ordu.kabul (bayraklı ölçüt, hakem üçüncü aile); ham yanıt önbellekte"""
    ham = cikti / f"B3-capraz-{a}.json"
    if not ham.exists():
        if o.Sayac.ucretsiz + 2 > o.UCRETSIZ_TAVAN:
            raise RuntimeError("ücretsiz tavanı")
        o.Sayac.ucretsiz += 2
        ham.write_text(json.dumps(ucretsiz_havuz.iki_aile("ozet", o.istem([a]), max_tokens=1500), ensure_ascii=False), encoding="utf-8")
    kayit = json.loads(ham.read_text(encoding="utf-8"))
    ys, aileler = [(o.json_ilk(t) or {}).get(a) for t, _, _ in kayit], [f for _, _, f in kayit]
    kabul = ordu.kabul(ys, hakem_=hakem_onb(a, aileler, cikti), tur=o.TUR.get(a, "kesin"))
    return (kabul if kabul is not None else (ys[0] if ys else None)), kabul is not None, aileler


def kol_b(cikti):
    sat = {a: {"gecti": False, "jeton": 0, "agirlikli": 0, "claude_is": 0, "basamak": 0} for a in GOREV}
    taslak, bekleyen, capraz_ozet = {}, [], {}
    for a in GOREV:
        if a[0] == "O":
            y, ayni, aile = capraz(a, cikti)
            sat[a]["gecti"] = o.dogru(a, y)
            capraz_ozet[a] = {"ayni": ayni, "dogru": sat[a]["gecti"], "aile": aile}
            kabul = ayni
        else:
            y, j = o.ucretsiz(a, cikti / f"B-ucretsiz-{a}.json", 3000 if a[0] in "ZI" else 1500)
            sat[a]["gecti"] = kabul = o.dogru(a, y)
        if not kabul:
            sat[a]["gecti"] = False
            bekleyen.append(a)
            taslak[a] = y
    for i in ADIMLAR:
        b = ordu.MERDIVEN[i]
        grup = [a for a in bekleyen]
        if not grup:
            break
        tek = o.Sayac.claude + len(grup) + sum(s > i for s in ADIMLAR) <= o.CAGRI_TAVAN
        for p in ([[a] for a in grup] if tek else [grup]):
            metin = o.istem(p)
            tas = {a: taslak[a] for a in p if a[0] in "ZI" and i >= 3 and taslak.get(a)}
            if tas:  # zor/imkansiz: çekirdek karar Sonnet/Opus'ta, ücretsiz/Haiku taslağıyla
                metin += "\n\nTaslaklar (doğrulanmadı, hatalı olabilir; çekirdek kararı sen ver):\n" + "\n".join(f"## {a}\n{t}" for a, t in tas.items())
            try:
                y, j, _ = o.claude(p, {**b, "kademe": b["ad"]}, cikti / f"B3-{b['ad']}-{'+'.join(p) if tek else 'toplu'}.json", metin)
            except RuntimeError as e:
                print("B durdu:", e, file=sys.stderr)
                return sat, capraz_ozet
            for a in p:
                s = sat[a]
                s["jeton"] += j / len(p)
                s["agirlikli"] += j / len(p) * AG(b["ad"])
                s["claude_is"] += 1
                s["basamak"] = i
                s["gecti"] = o.dogru(a, y.get(a))
                if s["gecti"]:
                    bekleyen.remove(a)
                else:
                    taslak[a] = y.get(a)
    return sat, capraz_ozet


def ozet(sat):
    return {"claude_is": sum(s["claude_is"] for s in sat.values()), "agirlikli_token": round(sum(s.get("agirlikli", s["jeton"]) for s in sat.values())),
            "claude_token": round(sum(s["jeton"] for s in sat.values())), "kalite": round(sum(s["gecti"] for s in sat.values()) / len(sat), 3),
            "kalan": [a for a, s in sat.items() if not s["gecti"]], "basamaklar": {a: s.get("basamak") for a, s in sat.items() if s.get("basamak")}}


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    cikti = Path(sys.argv[1])
    yuk = sabit_yuk(cikti)
    A = ozet(kol_a(cikti, yuk))
    satB, cz = kol_b(cikti)
    B = ozet(satB)
    sonuc = {"gecti": ordu.kapi3(A, B), "A": A, "B": B, "sabit_yuk": yuk, "claude_cagri": o.Sayac.claude, "ucretsiz_cagri": o.Sayac.ucretsiz, "capraz": cz,
             "oran": {"is": round(B["claude_is"] / A["claude_is"], 3), "agirlikli_token": round(B["agirlikli_token"] / A["agirlikli_token"], 3)}}
    (cikti / "olcum3.json").write_text(json.dumps(sonuc, ensure_ascii=False, indent=1), encoding="utf-8")
    print(json.dumps({k: sonuc[k] for k in ("gecti", "oran", "claude_cagri", "ucretsiz_cagri", "sabit_yuk")}, ensure_ascii=False), A["kalite"], B["kalite"], B["kalan"])

"""ÖĞREN-2.tur d2 kapısı: delta A kartları (kaynak dosyası olan 40), iki yeni tohum (2111, 2112) x 20 kart.
Hakem: iki farklı ücretsiz aile (ucretsiz_havuz.iki_aile); alan bazında ayrışırsa Haiku (en fazla 20). Eşik: tohum başı alan doğruluğu >= %92.
Kullanım: python -X utf8 .kos/kopru/ogren/tur2_d2_kapi.py   (arka plan: .kos/kopru/arka.py ile)"""
import json, random, re, sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

KOK = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(KOK / "tools"))
import ucretsiz_havuz as h

CIKTI = KOK / ".claude/ogren-tur2-d3/kapi.jsonl"
ALAN = ("ne", "ne_zaman", "nasil", "kosul")
HAIKU_TAVAN = 20
haiku_say = [0]
SEED = (3111, 3112)


def kartlar():
    out = []
    for l in (KOK / "docs/atlas/kart.jsonl").read_text(encoding="utf-8").splitlines():
        k = json.loads(l)
        if k.get("kategori") == "tur2-delta" and k.get("katman") == "A" and k.get("durum") != "kaynak_yetersiz" and Path(str(k.get("kanit", ""))).is_file():
            out.append(k)
    return sorted(out, key=lambda k: k["ad"])


def istem(k):
    kaynak = Path(k["kanit"]).read_text(encoding="utf-8", errors="replace")[:7000]
    kart = {a: k.get(a) for a in ALAN}
    return ("Bir araç kartının alanlarını KAYNAK metne göre denetle. Bir alan kaynakta desteklenmiyorsa, kaynakla çelişiyorsa ya da kaynakta olmayan "
            "bilgi uyduruyorsa false; kaynaktan çıkarılabiliyorsa ya da kaynakta bilgi yok diye dürüstçe 'belirsiz' diyorsa true. "
            'YALNIZ şu JSON\'u yaz: {"ne": true|false, "ne_zaman": true|false, "nasil": true|false, "kosul": true|false}\n\n'
            f"KART ({k['ad']}):\n{json.dumps(kart, ensure_ascii=False)}\n\nKAYNAK:\n{kaynak}")


def ayikla(m):
    j = re.search(r"\{[^{}]*\}", m or "", re.S)
    try:
        d = json.loads(j.group(0))
    except (AttributeError, ValueError):
        return None
    return {a: d[a] for a in ALAN} if all(isinstance(d.get(a), bool) for a in ALAN) else None


def dogrula(m):
    return None if ayikla(m) else "json-degil"


def haiku_oy(p):
    if haiku_say[0] >= HAIKU_TAVAN:
        return None
    haiku_say[0] += 1
    try:
        return ayikla(h._haiku(p))
    except Exception:
        return None


def birlestir(oy, p, ucuncu):
    """Alan başı karar. Ayrışırsa Haiku (tavan dolmadıysa), değilse 3. ücretsiz aile; ikisi de yoksa None = kararsız (yanlış değil, paydadan düşer)."""
    nihai, ayrisan, kararsiz = {}, 0, 0
    for a in ALAN:
        v = [o[0][a] for o in oy]
        if len(v) == 1 or (len(v) >= 2 and v[0] == v[1]):
            nihai[a] = v[0]
        elif len(v) >= 2:
            ayrisan += 1
            hk = haiku_oy(p) or ucuncu()
            nihai[a] = hk[a] if hk else None
            kararsiz += nihai[a] is None
        else:
            nihai[a] = None; kararsiz += 1
    return nihai, ayrisan, kararsiz


def oran(sonuclar):
    """(doğru, payda, kararsız): kararsız alanlar paydadan düşer."""
    v = [x for r in sonuclar for x in r.values()]
    return sum(x is True for x in v), sum(x is not None for x in v), sum(x is None for x in v)


def bir(k):
    p = istem(k)
    yan = h.iki_aile(h.H, p, max_tokens=600, dogrula=dogrula, etiket="tur2-d2-kapi")
    oy = [(ayikla(m), kay, aile) for m, kay, aile in yan]
    oy = [o for o in oy if o[0]]
    kaynaklar = [o[1] for o in oy]
    if len(oy) < 2:
        hk = haiku_oy(p)
        if hk:
            oy.append((hk, "haiku", "anthropic")); kaynaklar.append("haiku")
    ucuncu_oy = []

    def ucuncu():  # ayrışmada Haiku tavanı doluysa: oy vermemiş 3. ücretsiz aile (bir kez çağrılır, tüm alanlar için)
        if not ucuncu_oy:
            kul = {o[2] for o in oy}
            for aile in sorted({e.aile for e in h.ENT if h.H in e.turler} - kul - {"anthropic"}):
                m, kay, _ = h.cagir(h.H, p, max_tokens=600, aile=aile, dogrula=dogrula, etiket="tur2-d2-kapi")
                if ayikla(m):
                    ucuncu_oy.append(ayikla(m)); kaynaklar.append(kay); break
            else:
                ucuncu_oy.append(None)
        return ucuncu_oy[0]

    nihai, ayrisan, kararsiz = birlestir(oy, p, ucuncu)
    return dict(ad=k["ad"], tur=k["tur"], oylar=kaynaklar, ayrisan_alan=ayrisan, kararsiz=kararsiz, sonuc=nihai)


if __name__ == "__main__":
    ks = kartlar()
    print("kaynakli A karti", len(ks), flush=True)
    s1 = random.Random(SEED[0]).sample(ks, 20)
    kalan = [k for k in ks if k not in s1]
    random.Random(SEED[1]).shuffle(kalan)
    s2 = kalan[:20]
    CIKTI.parent.mkdir(parents=True, exist_ok=True)
    with CIKTI.open("a", encoding="utf-8") as f, ThreadPoolExecutor(1) as ex:
        for tohum, grup in ((SEED[0], s1), (SEED[1], s2)):
            rs = []
            for r in ex.map(bir, grup):
                r["tohum"] = tohum; rs.append(r["sonuc"])
                f.write(json.dumps(r, ensure_ascii=False) + "\n"); f.flush()
            dog, say, kar = oran(rs)
            print(f"tohum {tohum}: {len(grup)} kart, alan dogrulugu {dog}/{say} = {100 * dog / say:.1f}% (kararsiz {kar})", flush=True)
    print("haiku cagri", haiku_say[0], flush=True)

"""ÖĞREN-2.tur d5: yeni kart biçimi (nasil = kaynaktan birebir komut, kosul = <=15 kelime alıntı + kaynak: dosya:satır)
+ yeniden yazım (uret) + kapı (kapi). Hakem: nasil/kosul MEKANİK (kart alanı <-> kaynak satırı); ne/ne_zaman iki ücretsiz aile, ayrışırsa Haiku (<=20).
Kullanım: python -X utf8 .kos/kopru/ogren/tur2_d5.py uret|kapi   (arka plan: .kos/kopru/arka.py)"""
import json, random, re, sys
from pathlib import Path

KOK = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(KOK / "tools"))
sys.path.insert(0, str(KOK / ".kos/kopru/ogren"))
import ucretsiz_havuz as h
import tur2_d2_kapi as K

KART = KOK / "docs/atlas/kart.jsonl"
CIKTI = KOK / ".claude/ogren-tur2-d5"
ONCELIK = ("ios-qa", "setup-gbrain", "sync-gbrain", "codegraph", "context-restore", "netlify-database")
HAVUZ = 64  # yeniden yazılacak kart sayısı (kapı 2x20 + ret payı)
CAGRI_TAVAN = 160
cagri = [0]


def norm(s):
    return re.sub(r"\s+", " ", re.sub(r"[`*_]", "", s or "")).strip().lower()


def kaynak_satirlari(k):
    return Path(k["kanit"]).read_text(encoding="utf-8", errors="replace").splitlines()


def mekanik(k):
    """(nasil, kosul) -> True | False | None (None = kaynak_yetersiz, paydadan düşer)."""
    L = kaynak_satirlari(k)
    tum = norm("\n".join(L))
    nasil = k.get("nasil")
    n = None if not nasil else norm(nasil) in tum
    q, s = k.get("kosul_alinti"), k.get("kosul_satir")
    if not q:
        c = None
    else:
        c = len(q.split()) <= 15 and isinstance(s, int) and 1 <= s <= len(L) and \
            any(norm(q) in norm(L[i]) for i in range(max(0, s - 2), min(len(L), s + 1)))
    return n, c


def istem(k):
    L = kaynak_satirlari(k)
    kaynak = "\n".join(f"{i + 1}: {l}" for i, l in enumerate(L))[:9000]
    return ("Bir araç kartının alanlarını YALNIZ kaynaktan üret. YALNIZ şu JSON'u yaz:\n"
            '{"ne_zaman": "<bir cümle, ne zaman kullanılır>", "nasil": "<kaynakta geçen BİREBİR komut/çağrı, kopyala-yapıştır koşar; yoksa null>", '
            '"kosul_alinti": "<önkoşul/gereksinimi söyleyen kaynak cümlesinden BİREBİR en çok 15 kelime; yoksa null>", "kosul_satir": <o alıntının satır numarası ya da null>}\n'
            "Kaynakta olmayan hiçbir şeyi uydurma; emin değilsen null.\n\n"
            f"ARAÇ: {k['ad']} ({k['tur']})\nKAYNAK (satır numaralı):\n{kaynak}")


def ayikla_uret(m):
    j = re.search(r"\{.*\}", m or "", re.S)
    try:
        d = json.loads(j.group(0))
        return d if {"ne_zaman", "nasil", "kosul_alinti", "kosul_satir"} <= d.keys() else None
    except (AttributeError, ValueError):
        return None


def uret_bir(k, aile=None):
    p = istem(k)
    for deneme in range(3):
        if cagri[0] >= CAGRI_TAVAN:
            return None
        cagri[0] += 1
        m, _, _ = h.cagir(h.H, p, max_tokens=700, aile=aile if deneme == 0 else None, dogrula=lambda m: None if ayikla_uret(m) else "json-degil", etiket="tur2-d5-uret")
        d = ayikla_uret(m)
        if not d:
            continue
        y = {**k, "nasil": d["nasil"], "kosul_alinti": d["kosul_alinti"], "kosul_satir": d["kosul_satir"], "ne_zaman": d["ne_zaman"] or k.get("ne_zaman")}
        n, c = mekanik(y)
        if n is not False and c is not False:  # None = kanıtsız alan, dürüstçe boş
            y["kosul"] = f"{y['kosul_alinti']} (kaynak: {y['kanit']}:{y['kosul_satir']})" if y["kosul_alinti"] else None
            y["d5"] = True
            return y
    return None


def havuz_sec(kartlar):
    ok = [k for k in kartlar if k.get("kategori") == "tur2-delta" and k.get("durum") != "kaynak_yetersiz" and Path(str(k.get("kanit", ""))).is_file()]
    on = [k for k in ok if k["ad"] in ONCELIK]
    a = sorted((k for k in ok if k["katman"] == "A" and k["ad"] not in ONCELIK), key=lambda k: k["ad"])
    b = sorted((k for k in ok if k["katman"] == "B"), key=lambda k: k["ad"])
    return (on + a + b)[:HAVUZ]


def uret():
    kartlar = [json.loads(l) for l in KART.read_text(encoding="utf-8").splitlines()]
    sec = havuz_sec(kartlar)
    yeni, ret = {}, []
    for k in sec:
        y = uret_bir(k)
        if y:
            yeni[y["ad"]] = y
        else:
            ret.append(k["ad"])
        print(k["ad"], "ok" if y else "RET", flush=True)
    for k in kartlar:
        if k["ad"] in ret and k.get("kategori") == "tur2-delta":
            k["durum"] = "kaynak_yetersiz"
    out = [yeni.get(k["ad"], k) if k.get("kategori") == "tur2-delta" else k for k in kartlar]
    KART.write_text("\n".join(json.dumps(k, ensure_ascii=False) for k in out) + "\n", encoding="utf-8", newline="\n")
    print(f"yazilan {len(yeni)} ret {len(ret)} {ret} cagri {cagri[0]}", flush=True)


def istem_ne(k):
    kaynak = Path(k["kanit"]).read_text(encoding="utf-8", errors="replace")[:7000]
    kart = {a: k.get(a) for a in ("ne", "ne_zaman")}
    return ("Bir araç kartının alanlarını KAYNAK metne göre denetle. Kaynakta desteklenmiyorsa/çelişiyorsa/uydurmaysa false; kaynaktan çıkarılabiliyorsa true. "
            'YALNIZ şu JSON\'u yaz: {"ne": true|false, "ne_zaman": true|false}\n\n'
            f"KART ({k['ad']}):\n{json.dumps(kart, ensure_ascii=False)}\n\nKAYNAK:\n{kaynak}")


def kapi():
    kartlar = [json.loads(l) for l in KART.read_text(encoding="utf-8").splitlines()]
    ks = sorted((k for k in kartlar if k.get("d5") and k.get("durum") != "kaynak_yetersiz"), key=lambda k: k["ad"])
    print("d5 kart", len(ks), flush=True)
    seed = (5111, 5112)
    s1 = random.Random(seed[0]).sample(ks, 20)
    kalan = [k for k in ks if k not in s1]
    random.Random(seed[1]).shuffle(kalan)
    s2 = kalan[:20]
    K.ALAN = ("ne", "ne_zaman")
    CIKTI.mkdir(parents=True, exist_ok=True)
    with (CIKTI / "kapi.jsonl").open("a", encoding="utf-8") as f:
        for t, grup in zip(seed, (s1, s2)):
            rs, kosul_yok = [], 0
            for k in grup:
                p = istem_ne(k)
                yan = h.iki_aile(h.H, p, max_tokens=400, dogrula=lambda m: None if K.ayikla(m) else "json-degil", etiket="tur2-d5-kapi")
                oy = [(K.ayikla(m), kay, aile) for m, kay, aile in yan]
                oy = [o for o in oy if o[0]]
                if len(oy) < 2 and (hk := K.haiku_oy(p)):
                    oy.append((hk, "haiku", "anthropic"))
                nihai, ayr, kar = K.birlestir(oy, p, lambda: None)
                n, c = mekanik(k)
                nihai["nasil"], nihai["kosul"] = n, c
                kosul_yok += (n is None) + (c is None)
                rs.append(nihai)
                f.write(json.dumps(dict(tohum=t, ad=k["ad"], sonuc=nihai, ayrisan=ayr, kararsiz=kar), ensure_ascii=False) + "\n"); f.flush()
            dog, say, kar = K.oran(rs)
            hata = sorted({(r_k["ad"], a) for r_k, r in zip(grup, rs) for a, v in r.items() if v is False})
            print(f"tohum {t}: {len(grup)} kart, alan dogrulugu {dog}/{say} = {100 * dog / say:.1f}% (kararsiz {kar}, kanitsiz-alan {kosul_yok}) hatalar {hata}", flush=True)
    print("haiku cagri", K.haiku_say[0], flush=True)


if __name__ == "__main__":
    {"uret": uret, "kapi": kapi}[sys.argv[1]]()

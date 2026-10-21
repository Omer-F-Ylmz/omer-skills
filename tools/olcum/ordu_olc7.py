"""ORDU-1 d9: held-out kabul sınaması. Betikle (tohum 909) üretilmiş 24 yeni orta iş (regex/sayı/kod/json/metin), her biri için canlı ücretsiz ailelerden
birer yanıt (önbellek B7-yanit-<iş>-<aile>.json); aile çiftleri → ordu.kabul(gevsek=True, tür). Yanlış kabul = kabul edilen yanıt mekanik doğruluktan geçmedi.
claude -p yok; ücretsiz yanıt ≤130, hakem ≤40 çağrı.
  python tools/olcum/ordu_olc7.py <çıktı_dizini>"""
import itertools
import json
import math
import random
import re
import subprocess
import sys
import threading
from collections import Counter
from pathlib import Path

import ordu_olc3 as d3
import ucretsiz_havuz as h

ordu = d3.ordu
AILELER = ("google", "openai", "mistral", "minimax", "alibaba")
YANIT_TAVAN, HAKEM_TAVAN, CIFT = 130, 40, 4
SON = " Araç kullanma, açıklama ekleme; yalnız istenen yanıtı yaz."
R = random.Random(909)


def temiz(y):
    s = str(y).strip()
    if s.startswith("```"):
        s = s.split("\n", 1)[1] if "\n" in s else ""
        s = s.removesuffix("```").strip()
    return s


def kod_gecer(kod, test):
    try:
        r = subprocess.run([sys.executable, "-I", "-c", kod + "\n" + test], capture_output=True, timeout=20, creationflags=0x08000000)
        return r.returncode == 0
    except subprocess.TimeoutExpired:
        return False


GOREV = {}  # id -> (tür, istem, dogru(y), test|None)

# ---- sayı
a, b, c = R.randint(12, 40), R.randint(6, 25), R.randint(30, 200)
n2, x3, g4 = R.randint(9, 30), R.randint(2000, 9000), R.randint(7, 19)
p4, q4 = g4 * R.randint(12, 40), g4 * R.randint(41, 90)
h1, m1 = R.randint(6, 11), R.randint(0, 59)
h2, m2 = R.randint(13, 20), R.randint(0, 59)
SAYI = {
    "N1": (f"Bir depoda {a} koli var, her kolide {b} parça. {c} parça satıldı. Kaç parça kaldı? Yanıt: yalnız tamsayı.", a * b - c),
    "N2": (f"{n2} kişi birbiriyle tam bir kez el sıkışıyor. Toplam kaç el sıkışma olur? Yanıt: yalnız tamsayı.", n2 * (n2 - 1) // 2),
    "N3": (f"{x3} sayısının ikili gösteriminde kaç tane 1 rakamı var? Yanıt: yalnız tamsayı.", bin(x3).count("1")),
    "N4": (f"{p4} ile {q4} sayılarının en büyük ortak böleni kaçtır? Yanıt: yalnız tamsayı.", math.gcd(p4, q4)),
    "N5": (f"{h1:02d}:{m1:02d} ile {h2:02d}:{m2:02d} arası kaç dakikadır? Yanıt: yalnız tamsayı.", (h2 * 60 + m2) - (h1 * 60 + m1)),
}
for k, (i, v) in SAYI.items():
    GOREV[k] = ("kesin", i + SON, lambda y, v=v: re.fullmatch(r"-?\d+", temiz(y)) is not None and int(temiz(y)) == v, None)

# ---- regex
SAAT = [f"{R.randint(0, 23):02d}:{R.randint(0, 59):02d}" for _ in range(3)] + ["00:00", "23:59"]
HEX = ["#" + "".join(R.choice("0123456789abcdefABCDEF") for _ in range(6)) for _ in range(4)]
REGEX = {
    "R1": ("24 saatlik 'SS:DD' saat (iki haneli saat 00-23, iki haneli dakika 00-59)", SAAT, ["24:00", "7:30", "12:60", "12-30", "ab:cd", "23:5"]),
    "R2": ("'#' ile başlayan 6 haneli onaltılık renk kodu (büyük/küçük harf serbest)", HEX, ["#12345", "#GGGGGG", "123456", "#1234567", "# 12345"]),
    "R3": ("'X.Y.Z' sürüm numarası; her bölüm 0 ya da başında sıfır olmayan sayı", ["1.0.0", "10.20.30", "0.0.1", "2.15.0"],
           ["01.0.0", "1.0", "1.0.0.0", "a.b.c", "1..0", "1.0.0-beta"]),
    "R4": ("Türk plakası: il kodu 01-81, boşluk, 1-3 büyük harf, boşluk, 2-4 rakam", ["34 ABC 123", "06 A 1234", "81 XY 12", "01 ZZZ 9999"],
           ["00 AB 123", "82 AB 123", "34ABC123", "34 abc 123", "34 ABCD 123", "34 AB 1"]),
    "R5": ("basit e-posta: yerel kısım harf/rakam/nokta/altçizgi, '@', noktalı alan adı (harf/rakam/tire), son bölüm 2-6 harf",
           ["ali@site.com", "a.b_c@mail.example.org", "x1@a-b.co"], ["@site.com", "ali@site", "ali@site.c", "ali site@x.com", "ali@@x.com", "ali@x.com."]),
}


def _regex(poz, neg):
    def f(y):
        r = re.compile(temiz(y))
        return all(r.fullmatch(s) for s in poz) and not any(r.fullmatch(s) for s in neg)
    return f


for k, (tarif, poz, neg) in REGEX.items():
    GOREV[k] = ("kesin", f"re.fullmatch ile {tarif} tanıyan Python regex yaz. Geçerli: {poz}. Geçersiz: {neg}. Yanıt: yalnız regex dizgesi (tırnaksız, r'' yok)." + SON,
                _regex(poz, neg), None)

# ---- kod
KOD = {
    "C1": ("en_sik(liste): listede en çok geçen eleman; eşitlikte en küçüğü",
           "from collections import Counter\nimport random\nR = random.Random(3)\n"
           "def ref(l):\n    c = Counter(l)\n    m = max(c.values())\n    return min(k for k, v in c.items() if v == m)\n"
           "for _ in range(200):\n    l = [R.randint(0, 6) for _ in range(R.randint(1, 12))]\n    assert en_sik(l) == ref(l)\n"),
    "C2": ("sikistir(s): ardışık aynı harfleri 'harf+adet' yapar ('aaabcc' -> 'a3b1c2'); boş dizge -> ''",
           "import itertools, random\nR = random.Random(4)\n"
           "for _ in range(200):\n    s = ''.join(R.choice('abc') for _ in range(R.randint(0, 12)))\n"
           "    assert sikistir(s) == ''.join(k + str(len(list(g))) for k, g in itertools.groupby(s))\n"),
    "C3": ("ikinci_buyuk(liste): farklı değerler arasında ikinci en büyük sayı; yoksa None",
           "import random\nR = random.Random(5)\n"
           "for _ in range(200):\n    l = [R.randint(-5, 5) for _ in range(R.randint(0, 8))]\n    d = sorted(set(l))\n"
           "    assert ikinci_buyuk(l) == (d[-2] if len(d) > 1 else None)\n"),
    "C4": ("dengeli(s): ()[]{} parantezleri dengeli ve doğru iç içe mi (bool); boş dizge dengeli",
           "import random\nR = random.Random(6)\n"
           "def ref(s):\n    st = []\n    for ch in s:\n        if ch in '([{':\n            st.append(ch)\n"
           "        elif not st or '([{'.index(st.pop()) != ')]}'.index(ch):\n            return False\n    return not st\n"
           "for _ in range(300):\n    s = ''.join(R.choice('()[]{}') for _ in range(R.randint(0, 10)))\n    assert dengeli(s) is ref(s)\n"
           "assert dengeli('([]{})') is True and dengeli('(]') is False\n"),
}
for k, (tarif, testkod) in KOD.items():
    GOREV[k] = ("kesin", f"Python işlevi yaz: {tarif}. Yanıt: yalnız kod (import dahil, açıklama ve örnek çağrı yok)." + SON,
                lambda y, t=testkod: kod_gecer(temiz(y), t), lambda y, t=testkod: kod_gecer(temiz(y), t))

# ---- json
ETIKET = [("fix: boş yanıtta json_al düşüyordu", "hata-duzelt"), ("feat: ordu kabul bayrağı", "ozellik"), ("docs: kurulum bölümü güncellendi", "belge"),
          ("test: yonlendir sınır durumları", "test"), ("chore: bağımlılıklar yenilendi", "bakim"), ("fix: zaman aşımı sıfırlanmıyordu", "hata-duzelt"),
          ("feat: günlük kota göstergesi", "ozellik"), ("docs: README tablo", "belge")]
ET = R.sample(ETIKET, 4)
SOZ = ["elma", "armut", "kiraz", "vişne", "erik", "incir", "nar", "üzüm"]
HEDEF, K = R.choice(SOZ), R.randint(2, 5)
KEL = R.sample([s for s in SOZ if s != HEDEF], 5) * 2
KEL = KEL[:12 - K] + [HEDEF] * K
R.shuffle(KEL)
ADET, FIYAT, URUN = R.randint(3, 15), R.randint(5, 40), R.choice(["kalem", "defter", "silgi", "cetvel"])
SIRA = [R.randint(-50, 99) for _ in range(7)]
N5 = R.randint(11, 60)
JSON = {
    "J1": (f"Her commit iletisinin türü? Seçenekler: hata-duzelt | ozellik | belge | test | bakim. Yanıt: {{\"1\": ..., \"2\": ..., \"3\": ..., \"4\": ...}}.\n"
           + "\n".join(f"{i}: {m}" for i, (m, _) in enumerate(ET, 1)), {str(i): e for i, (_, e) in enumerate(ET, 1)}),
    "J2": (f"Bu cümlede '{HEDEF}' sözcüğü kaç kez geçiyor? Yanıt: {{\"sayi\": n}}.\n{' '.join(KEL)}", {"sayi": K}),
    "J3": (f"Fatura satırı: {URUN} x{ADET} @ {FIYAT} TL. Yanıt: {{\"urun\": ..., \"adet\": n, \"toplam\": n}} (toplam sayı).",
           {"urun": URUN, "adet": ADET, "toplam": ADET * FIYAT}),
    "J4": (f"Şu sayıları artan sırala ve en büyüğünü ver: {SIRA}. Yanıt: {{\"sirali\": [...], \"en_buyuk\": n}}.", {"sirali": sorted(SIRA), "en_buyuk": max(SIRA)}),
    "J5": (f"{N5} sayısı için: çift mi (JSON boolean), karesi (sayı), metin hali (JSON dizge). Yanıt: {{\"cift_mi\": ..., \"kare\": ..., \"metin\": ...}}.",
           {"cift_mi": N5 % 2 == 0, "kare": N5 * N5, "metin": str(N5)}),
}
for k, (i, beklenen) in JSON.items():
    GOREV[k] = ("json", i + " YALNIZ JSON nesnesi döndür." + SON,
                lambda y, b=json.dumps(beklenen, sort_keys=True): json.dumps(ordu.norm_json(y), sort_keys=True) == b, None)

# ---- metin
YORUM = R.choice([("Kargo üç gün geç geldi, ürün kutusu ezikti, bir daha almam.", "olumsuz"), ("Beklediğimden çok daha iyi çıktı, herkese öneririm.", "olumlu")])
METIN = {
    "M1": ("Şu cümleyi İngilizceye çevir: 'Raporu yarın sabaha kadar gönderin ve toplantıyı iptal edin.' Yanıt: tek cümle.",
           lambda y: all(w in str(y).lower() for w in ("report", "tomorrow", "cancel", "meeting"))),
    "M2": ("Şu cümleyi İngilizceye çevir: 'Sunucuyu yeniden başlatın, günlükleri kontrol edin ve hatayı bildirin.' Yanıt: tek cümle.",
           lambda y: all(w in str(y).lower() for w in ("server", "restart", "log", "error", "report")) or all(w in str(y).lower() for w in ("server", "restart", "log", "bug"))),
    "M3": ("Bu paragrafın Türkçe özeti: tam 3 satır, her satır '- ' ile başlar, ≤120 karakter; 'bütçe' ve 'tarih' sözcükleri geçer.\n"
           "Proje ekibi bütçeyi yüzde on beş artırmaya karar verdi. Teslim tarihi bir ay ertelendi. Test ortamı yenilenecek ve risk listesi her hafta gözden geçirilecek.",
           lambda y: len(temiz(y).splitlines()) == 3 and all(s.startswith("- ") and len(s) <= 120 for s in temiz(y).splitlines())
           and "bütçe" in str(y).lower() and "tarih" in str(y).lower()),
    "M4": (f"Bu yorumun duygusu 'olumlu' mu 'olumsuz' mu? Yanıt: tek sözcük.\n{YORUM[0]}", lambda y: temiz(y).lower().strip(" .") == YORUM[1]),
    "M5": ("Bu metni en fazla 20 sözcüklük tek cümleye indir; 'ücretsiz' sözcüğü geçsin: 'Ekip, işlerin çoğunu önce ücretsiz modellere vermeyi, "
           "başarısız olursa daha pahalı modellere yükseltmeyi ve sonuçları en sonda tek elden derlemeyi planlıyor.'",
           lambda y: len(temiz(y).split()) <= 20 and "ücretsiz" in str(y).lower() and temiz(y).count("\n") == 0),
}
for k, (i, d) in METIN.items():
    GOREV[k] = ("metin", i + SON, d, None)

kilit = threading.Lock()
say = {"yanit": 0, "hakem": 0}


def yanit(a, aile, cikti):
    ham = cikti / f"B7-yanit-{a}-{aile}.json"
    if not ham.exists():
        with kilit:
            if say["yanit"] >= YANIT_TAVAN:
                raise RuntimeError("yanıt tavanı")
            say["yanit"] += 1
        y, k, _ = h.cagir("hakem", GOREV[a][1], max_tokens=1500, aile=aile)
        if not y:  # eşzamanlı patlamada 429/boş: önbelleğe yazma, sonraki koşuda yeniden dene
            return None
        ham.write_text(json.dumps([y, k], ensure_ascii=False), encoding="utf-8")
    return json.loads(ham.read_text(encoding="utf-8"))[0] or None


def olc(cikti):
    ys = {a: {} for a in GOREV}

    def aile_kos(f):
        for a in GOREV:
            try:
                ys[a][f] = yanit(a, f, cikti)
            except Exception as e:  # noqa: BLE001
                print("hata", a, f, type(e).__name__, str(e)[:80], flush=True)

    ts = [threading.Thread(target=aile_kos, args=(f,)) for f in AILELER]
    [t.start() for t in ts]
    [t.join() for t in ts]
    rr, sat = random.Random(7), []
    for a, (tur, istem, dogru, test) in GOREV.items():
        ya = {f: y for f, y in ys[a].items() if y is not None}
        ciftler = list(itertools.combinations(sorted(ya), 2))
        rr.shuffle(ciftler)
        for f1, f2 in ciftler[:CIFT]:
            onb = cikti / f"B7-hakem-{a}-{f1}-{f2}.json"

            def hakem(x, y):
                if not onb.exists():
                    if say["hakem"] >= HAKEM_TAVAN:
                        raise RuntimeError("hakem tavanı")
                    say["hakem"] += 1
                    v = ordu.hakem(istem, x, y, [f1, f2])
                    if v is None:
                        return None
                    onb.write_text(json.dumps(v), encoding="utf-8")
                return json.loads(onb.read_text(encoding="utf-8"))

            def ok(y):
                try:
                    return bool(dogru(y))
                except Exception:  # noqa: BLE001
                    return False

            k = ordu.kabul([ya[f1], ya[f2]], test=test, hakem_=hakem, gevsek=True, tur=tur)
            sat.append({"is": a, "tur": tur, "cift": [f1, f2], "dogru": [ok(ya[f1]), ok(ya[f2])], "kabul": k is not None, "kabul_dogru": k is not None and ok(k)})
    return sat


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    cikti = Path(sys.argv[1])
    sat = olc(cikti)
    turler = sorted({s["tur"] for s in sat})
    ozet = {"is": len(GOREV), "ornek": len(sat), "ayrisan_cift": sum(s["dogru"][0] != s["dogru"][1] for s in sat), "kabul": sum(s["kabul"] for s in sat),
            "yanlis_kabul": sum(s["kabul"] and not s["kabul_dogru"] for s in sat), "kabul_orani": round(sum(s["kabul"] for s in sat) / max(len(sat), 1), 3),
            "yukselme_payi": round(sum(not s["kabul"] for s in sat) / max(len(sat), 1), 3), **say,
            "tur": {t: [sum(s["kabul"] for s in sat if s["tur"] == t), sum(s["tur"] == t for s in sat)] for t in turler}}
    (cikti / "olcum7.json").write_text(json.dumps({"ozet": ozet, "sat": sat}, ensure_ascii=False, indent=1), encoding="utf-8")
    print(json.dumps(ozet, ensure_ascii=False))
    for s in sat:
        if s["kabul"] and not s["kabul_dogru"]:
            print("YANLIS_KABUL", json.dumps(s, ensure_ascii=False))

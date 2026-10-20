"""ORDU-1 d2 kapı: 20 held-out iş (6 kolay · 6 orta · 6 zor · 2 imkansiz), kabul her işte yerel ve mekanik.
A = bugünkü düzen: hepsi Sonnet high, 3 toplu claude -p (kolay+orta · zor · imkansiz).
B = ordu merdiveni (tools/ordu.py): kolay/orta ücretsiz zincirde iş başı; kalan Haiku → Sonnet → Opus basamaklarında basamak başına tek toplu çağrı.
Kapı: tools/ordu.kapi (B Claude token ≤ A'nın %50'si VE kalite ≥ A VE başarısızlık ≤ A). Ham yanıtlar çıktı dizininde önbelleklenir (yeniden koşu ücretsiz).
  python tools/olcum/ordu_olc.py <çıktı_dizini>   → ordu-A.json · ordu-B.json · olcum.json"""
import json
import os
import random
import re
import subprocess
import sys
import tempfile
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(KOK / "tools"))
import ordu  # noqa: E402
import ucuz_alt  # noqa: E402
import yonlendir  # noqa: E402

CAGRI_TAVAN, USD_TAVAN, UCRETSIZ_TAVAN = 7, 1.0, 40  # claude -p: ön deneme (Haiku --effort) 1 harcandı, toplam 8
R = random.Random(21)
SOZ = ["elma", "armut", "kiraz", "vişne", "erik", "incir", "nar", "üzüm", "ayva", "muz"]


def _kod(kod, test, sure=30):
    """model kodu ayrı süreçte (-I) — asılı/zararlı kod ölçüm sürecini düşürmez"""
    with tempfile.NamedTemporaryFile("w", suffix=".py", delete=False, encoding="utf-8") as f:
        f.write(f"{kod}\n\n{test}\nprint('TAMAM')\n")
    try:
        r = subprocess.run([sys.executable, "-I", f.name], capture_output=True, text=True, timeout=sure, creationflags=0x08000000)
        return "TAMAM" in r.stdout
    except subprocess.TimeoutExpired:
        return False


# ---- kolay
satir = [(R.choice(SOZ) + str(i), R.randint(10, 900)) for i in range(12)]
K1 = ("Bu TSV'de satir sütununun toplamı? Yanıt: tamsayı.\nad\tsatir\n" + "\n".join(f"{a}\t{n}" for a, n in satir),
      lambda y: str(y).strip() == str(sum(n for _, n in satir)))
L1, L2 = R.sample(SOZ, 6), R.sample(SOZ, 6)
K2 = (f"İki listenin birleşimi: tekil, sıralı (Python sorted). Yanıt: JSON dizi.\nL1: {json.dumps(L1)}\nL2: {json.dumps(L2)}",
      lambda y: y == sorted(set(L1) | set(L2)))
dos = [(f"dosya{i}.py", R.randint(1, 500)) for i in range(8)]
K3 = ("Boyuta (kb) göre AZALAN sırayla yalnız dosya adları. Yanıt: JSON dizi.\n" + "\n".join(f"{a} {n}" for a, n in dos),
      lambda y: y == [a for a, _ in sorted(dos, key=lambda x: -x[1])])
obj = [{"ad": R.choice(SOZ), "tur": R.choice(["a", "b"]), "n": R.randint(1, 99)} for _ in range(4)]
K4 = ("Bu JSON dizisini TSV dizgesine çevir: ilk satır başlık (ad, tur, n), sonra her nesne bir satır, sütunlar sekme, satırlar \\n, "
      "sondaki \\n yok. Yanıt: dizge.\n" + json.dumps(obj, ensure_ascii=False),
      lambda y: str(y).replace("\r", "").strip("\n") == "ad\ttur\tn\n" + "\n".join(f"{o['ad']}\t{o['tur']}\t{o['n']}" for o in obj))
ad5 = ["test_a.py", "test_b.py", "util.py", "test_c.py", "conftest.py", "test_d.py"]
K5 = ("'test_' önekiyle başlayan dosya adlarında bu öneki 't_' yap; diğerleri aynı kalsın, sıra korunsun. Yanıt: JSON dizi.\n"
      + json.dumps(ad5), lambda y: y == ["t_" + a[5:] if a.startswith("test_") else a for a in ad5])
yol = ["docs/a/x.md", "docs/y.txt", "src/z.md", "docs/q.md", "docs/b/c/w.md", "README.md", "docs/v.MD"]
K6 = ("'docs/' altındaki ve '.md' ile biten (küçük harf) dosyaları 'arsiv/<yalnız dosya adı>' konumuna taşı. Yanıt: {\"kaynak\": \"hedef\"} "
      "JSON nesnesi.\n" + json.dumps(yol), lambda y: y == {"docs/a/x.md": "arsiv/x.md", "docs/q.md": "arsiv/q.md", "docs/b/c/w.md": "arsiv/w.md"})

# ---- orta
METIN = "".join((KOK / "tools/ordu.py").read_text(encoding="utf-8").splitlines(True)[:5])
O1 = ("Bu modül belgesinin Türkçe özeti: tam 3 satır, her satır '- ' ile başlar, ≤160 karakter; 'zorluk' ve 'Opus' sözcükleri geçer. "
      "Yanıt: 3 satırlık dizge.\n" + METIN,
      lambda y: len(str(y).strip().splitlines()) == 3 and all(s.startswith("- ") and len(s) <= 160 for s in str(y).strip().splitlines())
      and "zorluk" in str(y).lower() and "opus" in str(y).lower())
O2 = ("Şu cümleyi İngilizceye çevir: 'Kurulum bölümünü okuyun, ardından bağımlılıkları yükleyin ve testleri çalıştırın.' Yanıt: dizge.",
      lambda y: all(k in str(y).lower() for k in ("read", "install", "test")))
O3 = ("Her commit iletisinin türü? Seçenekler: hata-duzelt | ozellik | belge | test | bakim. Yanıt: {\"1\": ..., \"2\": ..., \"3\": ..., \"4\": ...}.\n"
      "1: fix: json_al bozuk yanıtta düşüyordu\n2: feat: yeni ordu merdiveni\n3: docs: README kurulum bölümü\n4: test: yonlendir sınır durumları",
      lambda y: y == {"1": "hata-duzelt", "2": "ozellik", "3": "belge", "4": "test"})
O4 = ("Bu devir notundan karar ve son tarihi çıkar. Yanıt: {\"karar\": ..., \"tarih\": \"YYYY-MM-DD\"}.\nNot (21.10.2026): Toplantıda ücretsiz havuzun önce "
      "denenmesi, olmazsa Haiku'ya geçilmesi kararlaştırıldı. Sorumlu: Ömer. Son tarih: 3 Kasım 2026.",
      lambda y: isinstance(y, dict) and y.get("tarih") == "2026-11-03" and "ücretsiz" in str(y.get("karar")).lower())
RPOZ, RNEG = ["21.10.2026", "2026-10-21", "01.01.1999", "31.12.2030"], ["21.13.2026", "32.01.2026", "2026-13-01", "2026-10-32", "21/10/2026", "1.1.2026", "2026-1-1", "abc", "00.05.2026"]


def _regex(y):
    r = re.compile(str(y))
    return all(r.fullmatch(s) for s in RPOZ) and not any(r.fullmatch(s) for s in RNEG)


O5 = ("re.fullmatch ile tarih tanıyan Python regex yaz: 'GG.AA.YYYY' ya da 'YYYY-AA-GG' (iki haneli gün/ay, dört haneli yıl); ay 01-12, gün 01-31. "
      f"Geçerli: {RPOZ}. Geçersiz: {RNEG}. Yanıt: regex dizgesi.", _regex)
GUNLUK = [R.choice(["INFO", "WARN", "ERROR"]) for _ in range(14)]
O6 = ("Bu günlükte her seviyenin satır sayısı? Yanıt: {\"INFO\": n, \"WARN\": n, \"ERROR\": n}.\n" + "\n".join(f"[{s}] olay {i}" for i, s in enumerate(GUNLUK)),
      lambda y: y == {k: GUNLUK.count(k) for k in ("INFO", "WARN", "ERROR")})

# ---- zor
KIRP_OK = "def kirp(s, n):\n    return s if len(s) <= n else s[:n - 1] + '…'\n"
KIRP_MUT = ["def kirp(s, n):\n    return s if len(s) < n else s[:n - 1] + '…'\n", "def kirp(s, n):\n    return s if len(s) <= n else s[:n] + '…'\n"]
Z1 = ("`def kirp(s, n)`: s, uzunluğu n'den büyükse n karakterlik sonuç verir (ilk n-1 karakter + '…'); değilse s aynen. Bunun için YALNIZ Python assert "
      "satırlarından oluşan test yaz (kirp zaten tanımlı; import yok). Sınır durumlarını yakala. Yanıt: assert satırları (dizge).",
      lambda y: _kod(KIRP_OK, y) and not any(_kod(m, y) for m in KIRP_MUT))
PARCA_BUG = "def parcala(liste, n):\n    return [liste[i:i + n] for i in range(0, len(liste) - 1, n)]\n"
PARCA_TEST = ("for k in range(0, 9):\n    for n in range(1, 5):\n        l = list(range(k))\n"
              "        assert parcala(l, n) == [l[i:i + n] for i in range(0, k, n)], (k, n)\n")
Z2 = ("`parcala(liste, n)` listeyi n'lik parçalara bölmeli ama bazı girdilerde son elemanı düşürüyor. Kök nedeni bul; düzeltilmiş TAM fonksiyonu ver. "
      "Yanıt: Python kodu (dizge).\n" + PARCA_BUG, lambda y: _kod(str(y), PARCA_TEST))
FIYAT = ("def fiyat(tur, adet):\n    if tur == 'a':\n        t = adet * 10\n        if adet >= 10:\n            t = t * 90 // 100\n        return t\n"
         "    elif tur == 'b':\n        t = adet * 25\n        if adet >= 10:\n            t = t * 90 // 100\n        return t\n"
         "    elif tur == 'c':\n        t = adet * 40\n        if adet >= 10:\n            t = t * 90 // 100\n        return t\n    return 0\n")
FIYAT_TEST = FIYAT.replace("def fiyat", "def fiyat0") + "for t in 'abcx':\n    for a in range(0, 60):\n        assert fiyat(t, a) == fiyat0(t, a), (t, a)\n"


def _fiyat(y):
    sat = lambda s: len([x for x in str(s).splitlines() if x.strip()])
    return _kod(str(y), FIYAT_TEST) and sat(y) < sat(FIYAT) * 0.7


Z3 = ("Bu fonksiyonu refactor et: davranış birebir aynı kalsın (dizilişi, bilinmeyen tür için 0 dahil), tekrar azalsın. Yanıt: TAM Python fonksiyonu (dizge).\n" + FIYAT, _fiyat)
Z4 = ("Hangi uygulama doğru artık yıl denetimidir? Yanıt: yalnız 'A' ya da 'B'.\nA: def artik(y): return y % 4 == 0 and y % 100 != 0 or y % 100 == 0\n"
      "B: def artik(y): return y % 4 == 0 and (y % 100 != 0 or y % 400 == 0)", lambda y: str(y).strip().strip(".'\"").upper() == "B")


ARALIK_REF = """def ref(a):
    c = []
    for s, e in sorted(a):
        if c and s <= c[-1][1]:
            c[-1][1] = max(c[-1][1], e)
        else:
            c.append([s, e])
    return c
"""
ARALIK_TEST = ARALIK_REF + """import random
R = random.Random(5)
for _ in range(300):
    a = [[x, x + R.randint(0, 6)] for x in [R.randint(0, 30) for _ in range(R.randint(0, 8))]]
    assert [list(p) for p in birlestir_aralik([list(p) for p in a])] == ref(a), a
"""
Z5 = ("`def birlestir_aralik(a)`: [başlangıç, bitiş] çiftlerini birleştir; kesişen ya da uçları ÖRTÜŞEN ([1,2],[2,3]) birleşir, bitişik tam sayılar ([1,2],[3,4]) "
      "birleşmez. Sonuç başlangıca göre sıralı iç içe liste; boş girdi → []. Yanıt: tam Python kodu (dizge).", lambda y: _kod(str(y), ARALIK_TEST))


def _skill(y):
    y = str(y)
    m = re.match(r"---\nname: log-ozetle\ndescription: (.+)\n---\n(.*)", y.replace("\r", "").strip() + "\n", re.S)
    if not m:
        return False
    govde = m.group(2)
    return len(m.group(1)) <= 300 and "Use when" in m.group(1) and len(govde.strip().splitlines()) <= 40 and "## Adımlar" in govde \
        and len(re.findall(r"^\d+\. ", govde, re.M)) >= 3


Z6 = ("`log-ozetle` adlı bir SKILL.md yaz (günlük dosyasını özetleyen skill). Biçim: '---' arası frontmatter yalnız `name: log-ozetle` ve tek satır "
      "`description:` (≤300 karakter, 'Use when' içerir); gövde ≤40 satır, '## Adımlar' başlığı ve en az 3 numaralı adım. Yanıt: dosya metni (dizge).", _skill)

# ---- imkansiz
SINIRLI = ("import time\n\nclass Sinirli:\n    def __init__(self, sinir):\n        self.sinir = sinir\n        self.n = 0\n\n    def al(self):\n"
           "        if self.n < self.sinir:\n            time.sleep(0)\n            self.n += 1\n            return True\n        return False\n")
SINIRLI_TEST = ("import threading\ns = Sinirli(100)\nok = []\n\ndef is_():\n    for _ in range(200):\n        ok.append(s.al())\n"
                "ts = [threading.Thread(target=is_) for _ in range(16)]\n[t.start() for t in ts]\n[t.join() for t in ts]\n"
                "assert sum(ok) == 100 and s.n == 100, (sum(ok), s.n)\n")
I1 = ("Bu sınıf çok iş parçacığında sınırı aşıyor (tam sinir kadar True dönmeli, `n` hiç sinir'i geçmemeli; arayüz ve `time.sleep(0)` satırı kalsın). "
      "Yarış durumunu çöz; TAM sınıfı ver (import dahil). Yanıt: Python kodu (dizge).\n" + SINIRLI, lambda y: _kod(str(y), SINIRLI_TEST) and "time.sleep(0)" in str(y))
GECIKME_REF = ("def ref(isler):\n    n = len(isler)\n    IN = 10 ** 18\n    dp = [IN] * (1 << n)\n    sure = [0] * (1 << n)\n    dp[0] = 0\n"
               "    for m in range(1 << n):\n        if m:\n            j = (m & -m).bit_length() - 1\n            sure[m] = sure[m & (m - 1)] + isler[j][0]\n"
               "        for j in range(n):\n            if not m >> j & 1:\n                t = sure[m] + isler[j][0]\n"
               "                c = dp[m] + isler[j][2] * max(0, t - isler[j][1])\n                if c < dp[m | 1 << j]:\n                    dp[m | 1 << j] = c\n"
               "    return dp[-1]\n")
GECIKME_TEST = (GECIKME_REF + "import random\nR = random.Random(9)\nfor n in list(range(0, 8)) * 20 + [14, 15]:\n"
                "    isler = [(R.randint(1, 9), R.randint(0, 40), R.randint(1, 5)) for _ in range(n)]\n"
                "    assert en_iyi_sira(isler) == ref(isler), isler\n")
I2 = ("`def en_iyi_sira(isler)`: isler = [(sure, son_tarih, agirlik)] listesi, işler tek makinede ardışık ve ara vermeden, t=0'dan başlayarak istenen sırada çalışır. "
      "Bir işin gecikmesi max(0, bitis - son_tarih), maliyet = agirlik * gecikme. Toplam maliyeti en aza indiren sıranın maliyetini (int) döndür. "
      "n 15'e kadar çıkabilir (zaman sınırı: bütün test <30 sn; n! deneme çalışmaz). Yanıt: tam Python kodu (dizge).", lambda y: _kod(str(y), GECIKME_TEST))

GOREV = dict(zip([f"K{i}" for i in range(1, 7)] + [f"O{i}" for i in range(1, 7)] + [f"Z{i}" for i in range(1, 7)] + ["I1", "I2"],
                 [K1, K2, K3, K4, K5, K6, O1, O2, O3, O4, O5, O6, Z1, Z2, Z3, Z4, Z5, Z6, I1, I2]))
SINIF_AD = {"K": "kolay", "O": "orta", "Z": "zor", "I": "imkansiz"}
sinif_of = lambda a: SINIF_AD[a[0]]


class Sayac:
    claude = ucretsiz = 0


def json_ilk(y):
    i = (y or "").find("{")
    try:
        return json.JSONDecoder().raw_decode(y[i:])[0] if i >= 0 else None
    except ValueError:
        return None


def istem(adlar):
    g = "\n\n".join(f"## {a}\n{GOREV[a][0]}" for a in adlar)
    return (f"Aşağıda {len(adlar)} bağımsız görev var. Araç kullanma. YALNIZ tek JSON nesnesi döndür; anahtarlar {', '.join(adlar)}, "
            f"değer her görevin istediği yanıt (kod yanıtları JSON dizgesi).\n\n{g}")


def claude(adlar, kd, ham):
    """(yanıt nesnesi, Claude jetonu, usd); ham yanıt önbellekte varsa çağrı yapılmaz."""
    if not ham.exists():
        if Sayac.claude >= CAGRI_TAVAN:
            raise RuntimeError("claude -p tavanı")
        Sayac.claude += 1
        r = subprocess.run(["claude", "-p", "--output-format", "json", "--max-budget-usd", str(USD_TAVAN), *yonlendir.argv(kd)], input=istem(adlar),
                           capture_output=True, text=True, encoding="utf-8", timeout=1500, creationflags=0x08000000,
                           env={**os.environ, "FORCE_PROMPT_CACHING_5M": "1"})
        ham.write_text(r.stdout, encoding="utf-8")
    try:
        d = json.JSONDecoder().raw_decode(ham.read_text(encoding="utf-8").lstrip())[0]
    except ValueError:
        return {}, 0, 0
    u = d.get("usage", {})
    return json_ilk(d.get("result", "")) or {}, sum(u.get(k) or 0 for k in ("input_tokens", "cache_creation_input_tokens", "cache_read_input_tokens", "output_tokens")), \
        d.get("total_cost_usd") or 0


def _sor(kol, model, g):
    if Sayac.ucretsiz >= UCRETSIZ_TAVAN:
        raise RuntimeError("ücretsiz tavanı")
    Sayac.ucretsiz += 1
    return ucuz_alt.sor(kol, model, g)


def ucretsiz(a, ham):
    """(yanıt, ücretsiz jeton); önbellekteki ham yanıt yeniden çağırmaz"""
    if not ham.exists():
        r = yonlendir.t1(istem([a]), 1500, sor=_sor, haiku=None)
        ham.write_text(json.dumps(r, ensure_ascii=False), encoding="utf-8")
    r = json.loads(ham.read_text(encoding="utf-8"))
    return (json_ilk(r["yanit"] or "") or {}).get(a), r["usage"]["giris"] + r["usage"]["cikis"]


def dogru(a, y):
    try:
        return bool(GOREV[a][1](y))
    except Exception:
        return False


def kol_a(cikti):
    kd = {**yonlendir.kurallar()["kademe"]["T3"], "kademe": "T3"}
    sat = {}
    for ad, adlar in (("kolayorta", [a for a in GOREV if a[0] in "KO"]), ("zor", [a for a in GOREV if a[0] == "Z"]), ("imk", ["I1", "I2"])):
        y, j, usd = claude(adlar, kd, cikti / f"A-{ad}.json")
        sat.update({a: {"gecti": dogru(a, y.get(a)), "jeton": j / len(adlar), "usd": usd / len(adlar), "basamak": 4} for a in adlar})
    return sat


def kol_b(cikti):
    durum = {a: ordu.BASLA[sinif_of(a)] for a in GOREV}
    sat = {a: {"gecti": False, "jeton": 0, "usd": 0, "ucretsiz_jeton": 0, "basamak": durum[a]} for a in GOREV}
    for i, b in enumerate(ordu.MERDIVEN):
        grup = [a for a in GOREV if durum[a] == i and not sat[a]["gecti"]]
        if not grup:
            continue
        try:
            if i == 0:
                y = {}
                for a in grup:
                    y[a], j = ucretsiz(a, cikti / f"B-ucretsiz-{a}.json")
                    sat[a]["ucretsiz_jeton"] += j
            else:
                y, j, usd = claude(grup, {**b, "kademe": b["ad"]}, cikti / f"B-{b['ad']}.json")
                for a in grup:
                    sat[a]["jeton"] += j / len(grup)
                    sat[a]["usd"] += usd / len(grup)
        except RuntimeError as e:  # tavan: kalan işler başarısız sayılır
            print("B durdu:", e, file=sys.stderr)
            break
        for a in grup:
            sat[a]["gecti"], sat[a]["basamak"] = dogru(a, y.get(a)), i
            yonlendir.kaydet({"tur": f"olcum-{a}", "kademe": b["ad"], "model": b["model"], "effort": b["effort"], "dogrulama": "light"},
                             "gecti" if sat[a]["gecti"] else "kaldi", {}, i, {"basamak": i, "ad": f"ordu-olcum-{a}"})
            if not sat[a]["gecti"]:
                durum[a] = i + 1
    return sat


def ozet(sat):
    return {"claude_token": round(sum(s["jeton"] for s in sat.values())), "kalite": round(sum(s["gecti"] for s in sat.values()) / len(sat), 3),
            "basarisiz": sum(not s["gecti"] for s in sat.values()), "usd": round(sum(s["usd"] for s in sat.values()), 4),
            "ucretsiz_jeton": round(sum(s.get("ucretsiz_jeton", 0) for s in sat.values())),
            "kalan": [a for a, s in sat.items() if not s["gecti"]], "basamaklar": {a: s["basamak"] for a, s in sat.items()}}


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    cikti = Path(sys.argv[1])
    cikti.mkdir(parents=True, exist_ok=True)
    A, B = ozet(kol_a(cikti)), ozet(kol_b(cikti))
    for ad, o in (("A", A), ("B", B)):
        (cikti / f"ordu-{ad}.json").write_text(json.dumps(o, ensure_ascii=False, indent=1), encoding="utf-8")
    sonuc = {"gecti": ordu.kapi(A, B), "A": A, "B": B, "claude_cagri": Sayac.claude, "ucretsiz_cagri": Sayac.ucretsiz,
             "token_orani": round(B["claude_token"] / A["claude_token"], 3) if A["claude_token"] else None}
    (cikti / "olcum.json").write_text(json.dumps(sonuc, ensure_ascii=False, indent=1), encoding="utf-8")
    print(json.dumps({k: sonuc[k] for k in ("gecti", "claude_cagri", "ucretsiz_cagri", "token_orani")}, ensure_ascii=False), A["kalite"], B["kalite"], B["kalan"])

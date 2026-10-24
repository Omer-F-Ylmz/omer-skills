"""BEYIN-ARAC-KART-1: tek arama kapısı — kart → ilgili bölüm → (istenirse) tam metin; seçici; ölçüm.
  python tools/arac_ara.py "<sorgu>" [--n 12] [--bolum 3] [--aday 150] [--json]   kartlar + yalnız ilgili bölümler
  python tools/arac_ara.py --tam <ad>                                            tam kaynak metin (yol kartta)
  python tools/arac_ara.py --sec "<görev>" [--tur T]                             önerilen tam araç kümesi (ajan_sira ön uçuşu kullanır)
  python tools/arac_ara.py --olc                                                 30 işte katmanlı vs tam metin yığını: jeton + geri çağırma
Aşama-1 kart BM25'i tools/katalog_ara.puanla'dır (TR/EN eş anlam, önek); kartın başlık listesi ve ne_zaman'ı arama metnine girer."""
import json
import re
import sqlite3
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import arac_kart as ak  # noqa: E402
import katalog_ara  # noqa: E402

BOLUM_KARAKTER = 650
KARDES = 24
RRF_BOLUM = 0.3  # ayar kümesinde (20 iş) süpürüldü; sınama kümesi (10 iş) yalnız raporlandı


def kartlar(c):
    return ak._jsonl(ak._cfg(c)["kart"])


def _satir(k):
    # puanla() ad·is·tetik·metin alanlarını okur; kapalı (override off) kayıtlar sona itilir
    return {"ad": k["ad"], "tur": k["tur"], "is": k.get("ne", ""), "tetik": k.get("tetik", ""), "durum": "",
            "metin": f"{k.get('ne_zaman', '')} {k.get('ba', '')} {k.get('ne', '')}"}


def ham(ad):
    return ad.split(" [")[0]  # çakışma soneki "ad [tür]" atılır (altın küme anahtarı tur:ham-ad)


def anahtar(k):
    return f"{k['tur']}:{ham(k['ad'])}"


def _ailesiz(k):
    return ham(k["ad"]).split(":")[-1].lower()


def bolum_adaylari(db, sorgu, k=300):
    """Tam metin bölüm indeksinden (FTS5 bm25) en ilgili araç adları — kart açıklamasında geçmeyen ama gövdede anlatılan araçlar için."""
    q = _fts(sorgu)
    if not q or not Path(db).exists():
        return []
    b = sqlite3.connect(db)
    try:
        r = [x[0] for x in b.execute("SELECT ad FROM b WHERE b MATCH ? ORDER BY bm25(b, 0.0, 3.0, 1.0) LIMIT ?", (q, k * 3)).fetchall()]
    except sqlite3.OperationalError:
        r = []
    b.close()
    return list(dict.fromkeys(r))[:k]


def adaylar(sorgu, ks, n, db=None):
    """Kart BM25 + bölüm FTS5 sıraları RRF ile birleşir; aynı taban adlı (ad-alanı farklı) kopyalar tek öncüde → [(öncü, [diğer kopyalar])]."""
    por = {k["ad"]: k for k in ks}
    kart = [o["ad"] for _, _, o in katalog_ara.puanla(sorgu, satirlar=[_satir(k) for k in ks])[0]]
    rrf = {}
    for sira_, liste in ((1, kart), (RRF_BOLUM, bolum_adaylari(db, sorgu) if db else [])):
        for i, ad in enumerate(liste):
            if ad in por:
                rrf[ad] = rrf.get(ad, 0) + sira_ / (60 + i)
    sira = sorted(rrf, key=lambda a: -rrf[a])
    gruplar, ana = [], {}
    for ad in sira:
        t = _ailesiz(por[ad])
        if t in ana:
            ana[t][1].append(por[ad])
        else:
            ana[t] = (por[ad], [])
            gruplar.append(ana[t])
        if len(gruplar) >= n:
            break
    return gruplar


def _fts(sorgu):
    kel = {w.rstrip("~") for w in katalog_ara.genislet(sorgu)} | set(katalog_ara.kelimeler(sorgu))
    t = {re.sub(r"[^\w]", "", w)[:6] for w in kel if len(w) >= 3 and w not in katalog_ara.DURAK}
    return " OR ".join(f'"{w}"*' for w in sorted(x for x in t if x))


def bolumler(db, sorgu, adlar, k=1):
    """Seçilen araçların sorguyla en ilgili ≤k bölümü (FTS5 bm25); eşleşme yoksa ilk bölüm."""
    if not Path(db).exists():
        return []
    b = sqlite3.connect(db)
    q, son = _fts(sorgu), []
    for ad in adlar:
        r = []
        if q:
            try:
                r = b.execute("SELECT baslik, metin FROM b WHERE b MATCH ? AND ad = ? ORDER BY bm25(b, 0.0, 3.0, 1.0) LIMIT ?", (q, ad, k)).fetchall()
            except sqlite3.OperationalError:
                r = []
        r = r or b.execute("SELECT baslik, metin FROM b WHERE ad = ? ORDER BY rowid LIMIT 1", (ad,)).fetchall()
        son += [{"ad": ad, "baslik": x, "metin": ak.temiz(y, BOLUM_KARAKTER) if "\n" not in y else y[:BOLUM_KARAKTER]} for x, y in r]
    b.close()
    return son


def ara(sorgu, c=None, n=12, bolum=3, aday=150, bolum_k=1):
    c = ak._cfg(c)
    gr = adaylar(sorgu, kartlar(c), n + aday, c["db"])
    on, geri = gr[:n], gr[n:]
    # kardeşler: ilk 8 öncünün eklenti ad alanı (ns:ad) → aynı eklentinin diğer kartları adaylara önce girer (plugin ailesi birlikte gelir)
    ns = {g[0]["ad"].split(":")[0] for g in on[:8] if ":" in g[0]["ad"]}
    gor = {g[0]["ad"] for g in on} | {g[0]["ad"] for g in geri}
    kardes = [k for k in kartlar(c) if ":" in k["ad"] and k["ad"].split(":")[0] in ns and k["ad"] not in gor][:KARDES]
    geri = [(k, []) for k in kardes] + geri
    return {"sorgu": sorgu, "kartlar": [g[0] for g in on], "kopya": {g[0]["ad"]: [anahtar(x) for x in g[1]] for g in on if g[1]},
            "adaylar": [anahtar(g[0]) for g in geri] + [anahtar(x) for g in geri for x in g[1]],
            "bolumler": bolumler(c["db"], sorgu, [g[0]["ad"] for g in on[:bolum]], bolum_k),
            "bayat": Path(c["yetenek"]).exists() and Path(c["kart"]).exists() and Path(c["yetenek"]).stat().st_mtime > Path(c["kart"]).stat().st_mtime}


def metin(s):
    o = ["(kart envanterden eski: python tools/arac_kart.py yenile)"] if s.get("bayat") else []
    o += [f"## {k['ad']}\n{ak.kart_metni(k)}" + (f"\n  (aynı iş, başka ad: {', '.join(s['kopya'][k['ad']][:3])})" if k["ad"] in s["kopya"] else "") for k in s["kartlar"]]
    if s["adaylar"]:
        o.append("diğer adaylar: " + " · ".join(s["adaylar"]))
    for b in s["bolumler"]:
        o.append(f"### {b['ad']} › {b['baslik']}\n{b['metin']}")
    return "\n".join(o)


def tam(ad, c=None):
    for k in kartlar(c):
        if k["ad"] == ad:
            return Path(k["yol"]).read_text(encoding="utf8", errors="ignore") if k["yol"] else json.dumps(k, ensure_ascii=False)
    return ""


def sec(gorev, c=None, tur=None, n=8):
    """Görev → önerilen tam küme: kart sırası (≤5) + en iyi 2 öncünün geçmişte birlikte KABUL aldığı eşler + iş türünün kombin tarifi."""
    c = ak._cfg(c)
    ks = kartlar(c)
    var = {k["ad"] for k in ks}
    # repo betikleri (tur=arac) seçiciye girmez: ad parçaları ("bul", "duzelt") yüzünden her göreve sızıyorlar; kombin/eş yoluyla yine gelebilirler
    on = [g[0] for g in adaylar(gorev, [k for k in ks if k["tur"] != "arac"], 5, c["db"])]
    kume = [k["ad"] for k in on]
    for k in on[:2]:
        kume += [b for b in k.get("birlikte") or [] if b in var]
    if tur and Path(c["kombin"]).exists():
        kume += [a for a in json.loads(Path(c["kombin"]).read_text(encoding="utf8")).get(tur, [])[:2] if a in var]
    return {"kume": list(dict.fromkeys(ham(a) for a in kume))[:n], "kartlar": {k["ad"]: ak.kart_metni(k) for k in on}}


def olc(c=None, n=12, aday=150):
    """Aynı 30 iş (docs/katalog/altin.jsonl): geri çağırma = altın ∩ (öncü+kopya+aday adı) ; jeton = kart+bölüm çıktısı vs adayların tam metni."""
    import katalog_altin
    ks = kartlar(c)
    yol = {anahtar(k): k["yol"] for k in ks}
    t = {"kesisim": 0, "altin": 0, "katman": 0, "tam": 0, "sonuc": 0, "tam_ilgili": 0}
    for s in Path(katalog_altin.ALTIN).read_text(encoding="utf8").splitlines():
        g = json.loads(s)
        r = ara(g["is"], c, n=n, aday=aday)
        bulunan = [anahtar(k) for k in r["kartlar"]] + [x for v in r["kopya"].values() for x in v] + r["adaylar"]
        t["kesisim"] += len(set(bulunan) & set(g["altin"]))
        t["altin"] += len(g["altin"])
        t["sonuc"] += len(set(bulunan))
        t["tam_ilgili"] += int(set(g["altin"]) <= set(bulunan))
        t["katman"] += len(metin(r)) // 3
        # tam metin yığını = bugünkü yol: aynı adayların kaynak metni bağlama girer (kaynağı olmayan aday kart satırı kadar, ~140 jeton)
        t["tam"] += sum(Path(yol[a]).stat().st_size // 3 if yol.get(a) and Path(yol[a]).exists() else 140 for a in set(bulunan) if a in yol)
    t["geri_cagirma"] = round(t["kesisim"] / max(t["altin"], 1), 3)
    t["jeton_azalma"] = round(1 - t["katman"] / max(t["tam"], 1), 3)
    return t


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    a = sys.argv[1:]

    def opt(ad, v=None):
        return type(v)(a[a.index(ad) + 1]) if ad in a and v is not None else (a[a.index(ad) + 1] if ad in a else v)

    if "--olc" in a:
        print(json.dumps(olc(None, opt("--n", 12), opt("--aday", 150)), ensure_ascii=False, indent=1))
    elif "--tam" in a:
        print(tam(opt("--tam")))
    elif "--sec" in a:
        r = sec(opt("--sec"), None, opt("--tur"))
        print(json.dumps(r, ensure_ascii=False, indent=1) if "--json" in a else " · ".join(r["kume"]))
    elif a:
        r = ara(a[0], None, opt("--n", 12), opt("--bolum", 3), opt("--aday", 150))
        print(json.dumps(r, ensure_ascii=False, indent=1) if "--json" in a else metin(r))
    else:
        print(__doc__)

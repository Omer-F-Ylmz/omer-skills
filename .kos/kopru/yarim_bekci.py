"""YARIM-BEKCI-1 (Ömer 24.10 12:21): işlerin yarım kalmasını yakalayan bekçi (saf Python, LLM yok).
H1 görev dosyası var ama kuyruğa girmemiş · H2 ajan karar/onay bekleyip durmuş · H3 görev rapor istemiş, rapor yok ·
H4 devirde bekleyen madde sonraki devirde düşmüş · H5 kuyruk satırının görev/cwd yolu diskte yok · H6 görevde 'NİHAİ 31+32' satırı yok (kapı başlamaz).
Çıktı: yarim.tsv (ad · tür · ilk görülme · son kanıt · önerilen eylem). Muaf: yarim-muaf.tsv (ad kalıbı · gerekçe · Ömer kararı).
Otomatik düzeltme yalnız H5 (satırdaki yolu değiştirir) ve H6 (görev dosyasına satır EKLER); hiçbir şey silinmez. H1–H4 yalnız raporlanır.
Kullanım: python yarim_bekci.py [--ozet | --devir]  (varsayılan: tara+yaz, log satırlarını bas)."""
import fnmatch
import json
import os
import re
import sys
import time
from pathlib import Path

NIHAI_SATIR = "NİHAİ 31+32"
NIHAI_EK = "NİHAİ 31+32: başlamadan nihai kapı; her adımda 2. beyne yaz (≤2 dk), ruflo pattern-search önce + store sonra; 32(f) tam ilgili küme; ders çıkar."
PENCERE_GUN = 3  # H1–H4 yalnız son 3 günde oluşan kanıta bakar (eski işler ayrı sınıflanır, gürültü olmasın)
H2_DESEN = re.compile(r"karar gerekiyor|onay gelirse|yapılsın mı", re.I)  # bekleyip durma: başarılı bitişte de sayılır
H2_ZAYIF = re.compile(r"BULUNAMADI|durduruldu|yapılmadı", re.I)  # 'Push yapılmadı' gibi olağan rapor cümleleri: yalnız başarısız (subtype != success / is_error) bitişte sayılır
H3_SATIR = re.compile(r"(?i)\b(yaz|çıktı|kaydet)\w*|rapor\s*:")
RAPOR_YOL = re.compile(r"rapor/([\w.\-]+\.md)")
BOLUM = re.compile(r"(?i)bekleyen|eksik|sonra|takip|açık")
EYLEM = {
    "H1": "kuyruğa ekle (ajan-sira.tsv) ya da yarim-muaf.tsv'ye yaz",
    "H2": "Desktop karar versin, görevi cevapla yeniden yaz",
    "H3": "rapor yaz ya da devam turu aç",
    "H4": "maddeyi son devir notuna taşı",
    "H5": "satırdaki yolu düzelt (tek aday yoksa elle)",
    "H6": "görev dosyasına NİHAİ 31+32 satırı ekle",
}
BASLIK = "# ad\ttür\tilk görülme\tson kanıt\tönerilen eylem"


def _zaman(t):
    return time.strftime("%Y-%m-%d %H:%M", time.localtime(t))


def _temiz(s, n=160):
    return re.sub(r"\s+", " ", s).strip()[:n]


def _oku(p):
    return Path(p).read_bytes().decode("utf-8", errors="surrogateescape")


def _kuyruk(k):
    """[(satır no, parçalar)] — başlık/yorum satırı yok."""
    f = k / "ajan-sira.tsv"
    if not f.exists():
        return []
    r = []
    for i, s in enumerate(_oku(f).split("\n")):
        p = s.rstrip("\r").split("\t")
        if len(p) >= 2 and not s.startswith("#"):
            r.append((i, p))
    return r


def _basladi(k, ad):
    return (k / "ajan-sira" / f"{ad}.basladi").exists() or (k / "ajan-sira" / f"{ad}.json").exists()


def _yol(kok, istem):
    return kok / istem


def _gorev_dosyalari(k):
    """{ad: Path} — .kos/kopru/gorev-<ad>.md ve gorev/<ad>.md."""
    r = {}
    for f in (k / "gorev").glob("*.md"):
        r[f.stem] = f
    for f in k.glob("gorev-*.md"):
        r.setdefault(f.stem[len("gorev-"):], f)
    return r


def _muaf(k):
    f = k / "yarim-muaf.tsv"
    if not f.exists():
        return []
    return [s.split("\t")[0].strip().lower() for s in _oku(f).splitlines() if s.strip() and not s.startswith("#")]


def _taze(t, simdi):
    return simdi - t <= PENCERE_GUN * 86400


def _sonuc(yol):
    """ad.json'daki son 'result' olayı (type result) ya da None; yalnız dosya sonu okunur."""
    try:
        with open(yol, "rb") as f:
            f.seek(0, 2)
            f.seek(max(0, f.tell() - 200_000))
            veri = f.read().decode("utf-8", errors="replace")
    except OSError:
        return None
    for s in reversed(veri.splitlines()):
        try:
            d = json.loads(s)
        except ValueError:
            continue
        if isinstance(d, dict) and d.get("type") == "result":
            return d
    return None


def _taban(ad):
    """Devam/yeniden deneme ekleri (-a, -a2, -r, d1b → d1) atılmış iş adı: aynı işin turları tek grupta."""
    onceki = None
    while onceki != ad:
        onceki = ad
        ad = re.sub(r"-(a2?|r)$", "", ad)
        ad = re.sub(r"(?<=\d)[a-z]$", "", ad)
    return ad


def _tsv_gorev(k, kok, ad, kuyruk_satirlari):
    for _, p in kuyruk_satirlari:
        if p[0] == ad:
            h = _yol(kok, p[1])
            if h.exists():
                return h
    return _gorev_dosyalari(k).get(ad)


def tara(k, kok, simdi=None):
    simdi = simdi or time.time()
    k, kok = Path(k), Path(kok)
    kuyruk = _kuyruk(k)
    gorevler = _gorev_dosyalari(k)
    muaf = _muaf(k)
    out = []

    def ekle(ad, tur, t, kanit):
        if not any(fnmatch.fnmatch(ad.lower(), m) for m in muaf):
            out.append({"ad": ad, "tur": tur, "zaman": t, "kanit": _temiz(kanit), "eylem": EYLEM[tur]})

    sirada_ad = {p[0] for _, p in kuyruk}
    sirada_yol = {os.path.normcase(os.path.abspath(_yol(kok, p[1]))) for _, p in kuyruk}

    # H1: görev dosyası var, kuyrukta ne ad ne yol var, başlamış da değil
    for ad, f in gorevler.items():
        t = f.stat().st_mtime
        if not _taze(t, simdi) or re.search(r"-(a2?|r)$", ad) or ad in sirada_ad or os.path.normcase(os.path.abspath(f)) in sirada_yol or _basladi(k, ad):
            continue
        ekle(ad, "H1", t, f"{f.name} kuyrukta yok")

    # H2/H3: biten işlerin sonucu
    sonuclar = {}
    for f in (k / "ajan-sira").glob("*.json"):
        if f.name.endswith((".mcp.json", ".denetim.json")):
            continue
        t = f.stat().st_mtime
        if _taze(t, simdi):
            sonuclar[f.stem] = (t, _sonuc(f))
    gruplar = {}
    for ad, (t, d) in sonuclar.items():
        metin = str((d or {}).get("result", ""))[-800:]
        basarili = bool(d) and d.get("subtype") == "success" and not d.get("is_error")
        m = (H2_DESEN.search(metin) or (None if basarili else H2_ZAYIF.search(metin))) if d else None
        gruplar.setdefault(_taban(ad), []).append((t, ad, m, metin))
    for liste in gruplar.values():
        t, ad, m, metin = max(liste)
        if m:
            ekle(ad, "H2", t, "…" + metin[max(0, m.start() - 60):m.end() + 60])
    for ad, (t, d) in sonuclar.items():
        if not d:
            continue
        g = _tsv_gorev(k, kok, ad, kuyruk)
        if not g:
            continue
        for s in _oku(g).splitlines():
            if H3_SATIR.search(s):
                yok = [r for r in RAPOR_YOL.findall(s) if not (k / "rapor" / r).exists()]
                if yok:
                    ekle(ad, "H3", t, f"rapor/{yok[0]} istendi, yok")
                    break

    # H4: eski devirde bekleyen bölümünde geçen, bitmemiş iş adı son devirde yok
    devirler = sorted((f for f in (k / "devir").glob("*devir*.md") if not f.stem.endswith("-devam")), key=lambda f: f.stat().st_mtime)
    if len(devirler) >= 2:
        bilinen = {a for a in set(gorevler) | sirada_ad if len(a) >= 4}
        son_metin = _oku(devirler[-1]).lower()
        for f in devirler[:-1]:
            t = f.stat().st_mtime
            if not _taze(t, simdi):
                continue
            bolum = False
            for s in _oku(f).splitlines():
                if s.startswith("#"):
                    bolum = bool(BOLUM.search(s))
                    continue
                if not bolum:
                    continue
                for a in set(re.findall(r"[a-z0-9][a-z0-9\-]{3,}", s.lower())) & bilinen:
                    if a not in son_metin and not (k / "ajan-sira" / f"{a}.json").exists() and not any(o["ad"] == a and o["tur"] == "H4" for o in out):
                        ekle(a, "H4", t, f"{f.name}: {s.strip()}")

    # H5/H6: başlamamış kuyruk satırları
    for _, p in kuyruk:
        ad = p[0]
        if _basladi(k, ad):
            continue
        g = _yol(kok, p[1])
        if not g.exists():
            ekle(ad, "H5", simdi, f"görev yolu yok: {p[1]}")
            continue
        cwd = next((x[4:] for x in p[3:] if x.strip().startswith("cwd=")), "")
        if cwd and not (kok / cwd.strip()).is_dir():
            ekle(ad, "H5", simdi, f"cwd yok: {cwd.strip()}")
        if NIHAI_SATIR not in _oku(g):
            ekle(ad, "H6", g.stat().st_mtime, f"{g.name}: '{NIHAI_SATIR}' satırı yok")
    return out


def tam_tara(k, kok, simdi=None):
    """--tam: PENCERE_GUN'e bakmadan tüm görev dosyaları (_tam_tara.py mantığı). BİTTİ rc 0 / rapor yok, G/H/plan kapsamında ve muafta da değilse 'YOK:<durum>'."""
    k = Path(k)
    log = "".join(_oku(p) for p in k.glob("*.log"))
    bitti = set(re.findall(r"BİTTİ (\S+) rc 0", log))
    basladi = set(re.findall(r"BAŞLAT (\S+) ", log))
    rapor = {p.stem for p in (k / "rapor").glob("*.md")}
    sirada = {p[0] for _, p in _kuyruk(k)}
    muaf = _muaf(k)
    kapsam = "".join(_oku(p) for p in list(k.glob("gorev-yarim-*.md")) + [k / "yarim-plan.md"] if p.exists())
    sonra = re.compile(r"telve|neffex|omer-site|logo|mod-mai|mai-|rea-uyari|10-karar", re.I)
    kapsanmis = lambda a: re.search(r"(?<![\w-])" + re.escape(a) + r"(?![\w])", kapsam)
    out = []
    for ad, f in sorted(_gorev_dosyalari(k).items()):
        taban = re.sub(r"(-(devam|a\d?|b\d?|c|d\d+\w?|p\d+))+$", "", ad)
        if ad in bitti or ad in rapor or any(b.startswith(ad + "-") for b in bitti):
            continue
        if sonra.search(ad) or ad.startswith("yarim-") or ad == "_sablon" or ad in sirada or kapsanmis(ad) or kapsanmis(taban):
            continue
        if any(fnmatch.fnmatch(ad.lower(), m) for m in muaf):
            continue
        out.append({"ad": ad, "tur": "YOK:" + ("BAŞLADI-BİTMEDİ" if ad in basladi else "KUYRUĞA-GİRMEMİŞ"), "zaman": f.stat().st_mtime})
    return out


def tam_ozet(k, kok):
    r = tam_tara(k, kok)
    sayi = {}
    for s in r:
        sayi[s["tur"]] = sayi.get(s["tur"], 0) + 1
    return f"YARIM-TAM: {len(r)} açık" + (f" ({', '.join(f'{t}:{n}' for t, n in sorted(sayi.items()))})" if r else "")


def _goreli(kok, h):
    try:
        return h.resolve().relative_to(kok.resolve()).as_posix()
    except ValueError:
        return h.as_posix()


def _tek(adaylar):
    var = {os.path.normcase(os.path.abspath(a)): a for a in adaylar if a.exists()}
    return next(iter(var.values())) if len(var) == 1 else None


def duzelt(k, kok, satirlar):
    """H5 (yalnız satırdaki yol) ve H6 (görev dosyasına satır eklenir). Dönüş: YARIM-DUZELTILDI log satırları. Dosya silinmez."""
    k, kok = Path(k), Path(kok)
    loglar = []
    h5 = {s["ad"] for s in satirlar if s["tur"] == "H5"}
    h6 = {s["ad"] for s in satirlar if s["tur"] == "H6"}
    if h5:
        f = k / "ajan-sira.tsv"
        mt = f.stat().st_mtime_ns
        metin = _oku(f)
        satir = metin.split("\n")
        degisti = False
        for i, p in _kuyruk(k):
            ad = p[0]
            if ad not in h5:
                continue
            eski = list(p)
            if not _yol(kok, p[1]).exists():
                taban = Path(p[1].replace("\\", "/")).name
                yeni = _tek([k / "gorev" / f"{ad}.md", k / f"gorev-{ad}.md", k / taban, k / "gorev" / taban])
                if yeni:
                    p[1] = _goreli(kok, yeni)
                    loglar.append(f"YARIM-DUZELTILDI H5 {ad} görev yolu {eski[1]} → {p[1]}")
            for j, x in enumerate(p[3:], 3):
                if x.strip().startswith("cwd=") and not (kok / x.strip()[4:]).is_dir():
                    ad_k = Path(x.strip()[4:].replace("\\", "/")).name
                    yeni = _tek([kok / ad_k, kok.parent / ad_k])
                    if yeni and yeni.is_dir():
                        p[j] = f"cwd={yeni.as_posix()}"
                        loglar.append(f"YARIM-DUZELTILDI H5 {ad} cwd {eski[j][4:]} → {yeni.as_posix()}")
            if p != eski:
                satir[i] = "\t".join(p) + ("\r" if satir[i].endswith("\r") else "")
                degisti = True
        if degisti and f.stat().st_mtime_ns == mt:  # başka yazar araya girdiyse bu tur yazma (sonraki tur dener)
            tmp = k / "ajan-sira.tsv.yarim-tmp"
            tmp.write_bytes("\n".join(satir).encode("utf-8", errors="surrogateescape"))
            os.replace(tmp, f)
        elif degisti:
            loglar = [x for x in loglar if not x.startswith("YARIM-DUZELTILDI H5")]
    for _, p in _kuyruk(k):
        if p[0] in h6:
            g = _yol(kok, p[1])
            if g.exists() and NIHAI_SATIR not in _oku(g):
                ham = g.read_bytes()
                ek = ("" if ham.endswith(b"\n") or not ham else "\n") + "\n" + NIHAI_EK + "\n"
                with g.open("ab") as fo:
                    fo.write(ek.encode("utf-8"))
                loglar.append(f"YARIM-DUZELTILDI H6 {p[0]} {g.name} sonuna {NIHAI_SATIR} satırı eklendi")
    return loglar


def _onceki(k):
    f = k / "yarim.tsv"
    r = {}
    if f.exists():
        for s in _oku(f).splitlines():
            p = s.split("\t")
            if len(p) >= 3 and not s.startswith("#"):
                r[(p[0], p[1])] = p[2]
    return r


def calistir(k, kok, simdi=None):
    """Tara → H5/H6 düzelt → yeniden tara → yarim.tsv yaz. Dönüş (satırlar, log satırları: yeni 'YARIM <tür> <ad> <eylem>' + 'YARIM-DUZELTILDI …')."""
    k, kok = Path(k), Path(kok)
    onceki = _onceki(k)
    satirlar = tara(k, kok, simdi)
    loglar = duzelt(k, kok, satirlar) if any(s["tur"] in ("H5", "H6") for s in satirlar) else []
    if loglar:
        satirlar = tara(k, kok, simdi)
    satirlar.sort(key=lambda s: (s["tur"], s["zaman"], s["ad"]))
    govde = [BASLIK]
    for s in satirlar:
        ilk = onceki.get((s["ad"], s["tur"])) or _zaman(s["zaman"])
        govde.append("\t".join([s["ad"], s["tur"], ilk, s["kanit"], s["eylem"]]))
        if (s["ad"], s["tur"]) not in onceki:
            loglar.append(f"YARIM {s['tur']} {s['ad']} {s['eylem']}")
    (k / "yarim.tsv").write_bytes(("\n".join(govde) + "\n").encode("utf-8"))
    return satirlar, loglar


def _tsv_satirlari(k):
    f = k / "yarim.tsv"
    return [s.split("\t") for s in _oku(f).splitlines() if s.strip() and not s.startswith("#")] if f.exists() else []


def ozet_satirlar(k, en_cok=8):
    """kontrol_tur/kontrol_ozet başı: 'YARIM: n açık (H1:a, …)' + en eski en_cok madde."""
    k = Path(k)
    r = [p for p in _tsv_satirlari(k) if len(p) >= 5]
    if not r:
        return ["YARIM: 0 açık"]
    sayi = {}
    for p in r:
        sayi[p[1]] = sayi.get(p[1], 0) + 1
    ust = [f"YARIM: {len(r)} açık ({', '.join(f'{t}:{n}' for t, n in sorted(sayi.items()))})"]
    for p in sorted(r, key=lambda p: p[2])[:en_cok]:
        ust.append(f"  {p[1]} {p[0]} ({p[2]}) — {p[3][:90]}")
    return ust


def devir_blogu(k):
    """Devir notuna eklenecek markdown bloğu (H4: devir sırasında madde düşmesin)."""
    r = [p for p in _tsv_satirlari(Path(k)) if len(p) >= 5]
    if not r:
        return "## YARIM (otomatik, yarim.tsv)\n- açık yok"
    return "## YARIM (otomatik, yarim.tsv)\n" + "\n".join(f"- {p[0]} · {p[1]} · {p[2]} · {p[3][:100]} → {p[4]}" for p in r)


K = Path(__file__).resolve().parent
KOK = K.parent.parent

if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    if "--tam" in sys.argv:
        print(tam_ozet(K, KOK))
        print("\n".join(f"  {s['tur']} {_zaman(s['zaman'])} {s['ad']}" for s in tam_tara(K, KOK)))
    elif "--ozet" in sys.argv:
        print("\n".join(ozet_satirlar(K)))
    elif "--devir" in sys.argv:
        print(devir_blogu(K))
    else:
        sat, log = calistir(K, KOK)
        print("\n".join(log) or "yeni yok", f"· açık {len(sat)}")

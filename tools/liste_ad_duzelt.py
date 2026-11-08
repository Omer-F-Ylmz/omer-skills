"""LISTE-EKSIK kapi 2: yeni kalemlerin adini kaynak videodaki yazima birebir cek.
Kullanim: python -I -X utf8 tools/liste_ad_duzelt.py [--uygula] [--bas N]   (varsayilan kuru kosu; N = ana-liste satir indeksi, 17372 oncesi eski)
Kural: kalem adi kaynak video metninde (aciklama+konusma+ekran) BIREBIR (buyuk/kucuk harf dahil) geciyorsa dokunma;
gecmiyorsa ama buyuk/kucuk harf farkiyla (sozcuk sinirli) geciyorsa metindeki yazima cekilir; hic gecmiyorsa 'ESLESMEDI' (TEYITSIZ) diye raporlanir, bulanik degisiklik YOK."""
import csv
import json
import re
import sys
from pathlib import Path

K = Path(r"C:\Projeler\omer-skills")
sys.path.insert(0, str(K / "tools"))
import liste_cikar as LC  # noqa: E402

csv.field_size_limit(10**7)
LISTE = K / "docs/video-tarama/ana-liste.tsv"
a = sys.argv[1:]
BAS = int(a[a.index("--bas") + 1]) if "--bas" in a else 17372


def metin(v, dos):
    if v not in dos:
        return ""
    d = LC.oku(dos[v])
    m = d.get("meta") or {}
    tr = " ".join(x.get("t", "") for x in d.get("transkript") or [])
    ek = " | ".join(dict.fromkeys(x.get("t", "") for x in d.get("ekran") or []))
    kare = d.get("kare_aciklama") or ""
    kare = kare if isinstance(kare, str) else json.dumps(kare, ensure_ascii=False)
    return re.sub(r"\s+", " ", f"{m.get('baslik') or ''} {m.get('aciklama') or ''} {tr} {ek} {kare}")


def bul(ad, tum):
    """kaynak metinde adin buyuk/kucuk harf farkli birebir yazimi (sozcuk siniri ile); yoksa None"""
    m = re.search(r"(?<![\w])" + re.escape(ad) + r"(?![\w])", tum, re.I)
    return m.group(0) if m else None


def main():
    rows = list(csv.reader(open(LISTE, encoding="utf-8", newline=""), delimiter="\t"))
    baslik, veri = rows[0], rows[1:]
    dos = LC.dosyalar()
    cache = {}
    degis, eslesti, bos, tamam = [], 0, [], 0
    for i, r in enumerate(veri):
        if i < BAS - 1:
            continue
        ad = r[0]
        tum = ""
        for v in r[3].split(","):
            if v not in cache:
                cache[v] = metin(v, dos)
            tum += " " + cache[v]
        if ad in tum:
            tamam += 1
            continue
        en = bul(ad, tum)
        if en and en != ad:
            degis.append((i, ad, en, 1.0))
        else:
            bos.append((i, ad))
    print("incelenen", len(veri) - BAS + 1, "birebir", tamam, "duzeltilecek", len(degis), "eslesmedi", len(bos))
    out = K / "tmp/ad_duzelt.tsv"
    with open(out, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, delimiter="\t", lineterminator="\n")
        w.writerow(["idx", "eski", "yeni", "oran"])
        for d in degis:
            w.writerow(d)
        for i, ad in bos:
            w.writerow([i, ad, "ESLESMEDI", ""])
    with open(K / "docs/video-tarama/liste-eksik-ad-teyitsiz.tsv", "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, delimiter="\t", lineterminator="\n")
        w.writerow(["kalem", "video_idleri", "not"])
        for i, ad in bos:
            w.writerow([ad, veri[i][3], "ad kaynak video metninde gecmiyor (turetilmis/ceviri/kavram adi)"])
    if "--uygula" in a:
        varolan = {r[0] for r in veri}
        eski_yeni = {}
        for i, eski, yeni, _ in degis:
            if yeni in varolan or eski in eski_yeni:
                continue
            veri[i][0] = yeni
            eski_yeni[eski] = yeni
        with open(LISTE, "w", encoding="utf-8", newline="") as f:
            w = csv.writer(f, delimiter="\t", lineterminator="\n")
            w.writerow(baslik)
            w.writerows(veri)
        oz = K / "docs/video-tarama/ana-liste-ozellik.tsv"
        ro = list(csv.reader(open(oz, encoding="utf-8", newline=""), delimiter="\t"))
        for r in ro[1:]:
            if r and r[0] in eski_yeni:
                r[0] = eski_yeni[r[0]]
        with open(oz, "w", encoding="utf-8", newline="") as f:
            csv.writer(f, delimiter="\t", lineterminator="\n").writerows(ro)
        yap = K / "docs/video-tarama/yapilis"
        gv = lambda x: re.sub(r"[^A-Za-z0-9._-]+", "_", x)[:80] or "kalem"
        tas = 0
        for eski, yeni in eski_yeni.items():
            fo, fn = yap / (gv(eski) + ".md"), yap / (gv(yeni) + ".md")
            if fo.exists() and not fn.exists():
                t = fo.read_text(encoding="utf-8")
                fn.write_text(t.replace("# " + eski, "# " + yeni, 1), encoding="utf-8")
                (K / "_arsiv").mkdir(exist_ok=True)
                (K / "_arsiv" / ("ad-duzelt-" + fo.name)).write_text(t, encoding="utf-8")
                if fo != fn:
                    fo.unlink()
                tas += 1
            elif fo.exists() and fn.exists() and fo == fn:
                t = fo.read_text(encoding="utf-8")
                fo.write_text(t.replace("# " + eski, "# " + yeni, 1), encoding="utf-8")
                tas += 1
        print("uygulandi", len(eski_yeni), "yapilis", tas)


main()

"""LISTE-EKSIK-2 kapi 2b: kaynakta birebir gecmeyen (TEYITSIZ) kalem adini videonun kendi metninde siniflandir.
Kullanim: python -I -X utf8 tools/liste_ad_hizala.py [--uygula] [--esik 86]
Sinif: NORM (bosluk/noktalama/harf farkiyla birebir), BULANIK (rapidfuzz en yakin dizi ratio>=esik; kaynak OCR/ASR bozuk,
ad dokunulmaz: ilk denemede bulanik diziyle yeniden adlandirma OCR cop uretti), PARCA (parantez/egik cizgi/& ile bolunen parcalardan biri kaynakta birebir), TOKEN (adin icerik sozcuklerinin >=%75'i
kaynakta ayri ayri var), ISARETLI (kalan). Ad DEGISTIRILMEZ.
Cikti: docs/video-tarama/liste-eksik-ad-kapi.tsv; --uygula ile liste-eksik-ad-teyitsiz.tsv yalniz ISARETLI'leri tutar."""
import csv
import json
import re
import sys
from collections import Counter
from pathlib import Path

from rapidfuzz import fuzz

K = Path(r"C:\Projeler\omer-skills")
sys.path.insert(0, str(K / "tools"))
import liste_cikar as LC  # noqa: E402

csv.field_size_limit(10**7)
LISTE = K / "docs/video-tarama/ana-liste.tsv"
TEYIT = K / "docs/video-tarama/liste-eksik-ad-teyitsiz.tsv"
KAPI = K / "docs/video-tarama/liste-eksik-ad-kapi.tsv"
a = sys.argv[1:]
ESIK = float(a[a.index("--esik") + 1]) if "--esik" in a else 86.0


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


def low(s):
    return "".join(c.lower()[0] for c in s)  # uzunluk korunur


def norm(x):
    return re.sub(r"[\W_]+", "", low(x))


def sinifla(ad, tum):
    if norm(ad) and norm(ad) in norm(tum):
        return "NORM", ""
    t = low(tum)
    al = fuzz.partial_ratio_alignment(low(ad), t)
    if al is not None and al.score >= ESIK:
        return "BULANIK", tum[al.dest_start:al.dest_end].strip()
    parca = [x for x in re.split(r"[()/&]|\s-\s", ad) if len(norm(x)) >= 3]
    if len(parca) > 1 and any(norm(x) in norm(tum) for x in parca):
        return "PARCA", ""
    toks = [w for w in re.findall(r"\w+", low(ad)) if len(w) > 2]
    if toks and sum(1 for w in toks if re.search(r"(?<!\w)" + re.escape(w), t)) / len(toks) >= 0.75:
        return "TOKEN", ""
    return "ISARETLI", ""


def main():
    rows = list(csv.reader(open(LISTE, encoding="utf-8", newline=""), delimiter="\t"))
    veri = rows[1:]
    teyitsiz = {r[0] for r in list(csv.reader(open(TEYIT, encoding="utf-8", newline=""), delimiter="\t"))[1:]}
    dos = LC.dosyalar()
    cache, out = {}, []
    for r in veri:
        if r[0] not in teyitsiz:
            continue
        tum = ""
        for v in r[3].split(","):
            if v not in cache:
                cache[v] = metin(v, dos)
            tum += " " + cache[v]
        sn, dz = sinifla(r[0], tum)
        out.append((r[0], r[3], sn, dz))
    print("teyitsiz", len(teyitsiz), dict(Counter(o[2] for o in out)))
    with open(KAPI, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, delimiter="\t", lineterminator="\n")
        w.writerow(["kalem", "video_idleri", "sinif", "kaynak_dizi"])
        w.writerows(out)
    if "--uygula" in a:
        with open(TEYIT, "w", encoding="utf-8", newline="") as f:
            w = csv.writer(f, delimiter="\t", lineterminator="\n")
            w.writerow(["kalem", "video_idleri", "not"])
            for ad, v, sn, _ in out:
                if sn == "ISARETLI":
                    w.writerow([ad, v, "ISARETLI: ad kaynak metinde yok (kavram/ceviri adi); duzeltilemedi"])


main()

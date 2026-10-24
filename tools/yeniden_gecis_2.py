"""YENIDEN-GECIS-2: reel/post/shorts listesini kurar, video_derin'i ayrı çıktı klasöründe koşar (biten kod atlanır → kaldığı yerden sürer).
Kullanım: python yeniden_gecis_2.py [--cikti DIR] [--liste DOSYA] [--en N] [--es N]  (ölçüm: boş --cikti + --en 5)"""
import csv
import os
import re
import runpy
import sys
from pathlib import Path

KOK = Path(__file__).resolve().parents[1]
K = KOK / ".kos/kopru"
TUR_URL = {"ig-reel": "https://www.instagram.com/reel/{}/", "ig-post(/p)": "https://www.instagram.com/p/{}/", "yt-shorts": "https://www.youtube.com/shorts/{}"}
EK_RE = re.compile(r"https?://(?:www\.)?(?:instagram\.com/(?:reel|p)/[\w-]+|youtube\.com/shorts/[\w-]+)")


def liste_kur(hedef):
    silinen = set(re.findall(r"[\w-]{8,}", (K / "ig-silinen.txt").read_text(encoding="utf-8", errors="replace")))
    urls = {}
    with open(K / "tum-linkler.tsv", encoding="utf-8", newline="") as f:
        for r in csv.DictReader(f, delimiter="\t"):
            if r["tur"] in TUR_URL:
                urls[r["kod"]] = TUR_URL[r["tur"]].format(r["kod"])
    for ad in ("linkler-2026-10-23-telefon.txt", "linkler-2026-10-23-omer.tsv"):
        for m in EK_RE.findall((K / ad).read_text(encoding="utf-8", errors="replace")):
            urls.setdefault(m.rstrip("/").rsplit("/", 1)[1], m)
    for k in silinen:
        urls.pop(k, None)
    hedef.write_text("\n".join(urls.values()) + "\n", encoding="utf-8")
    return len(urls)


if __name__ == "__main__":
    a = sys.argv[1:]

    def al(ad, var):
        if ad in a:
            i = a.index(ad)
            v = a[i + 1]
            del a[i:i + 2]
            return v
        return var

    cikti = al("--cikti", str(KOK / "docs/video-tarama/derin-2"))
    liste = Path(al("--liste", str(K / "yeniden-gecis-2-liste.txt")))
    en, es = al("--en", None), al("--es", "3")
    os.environ["VD_CIKTI"] = cikti
    if not liste.is_file():
        print(f"liste {liste.name}: {liste_kur(liste)} url", flush=True)
    argv = [str(KOK / "tools/video_derin.py"), "--es", es, "--liste", str(liste)] + (["--en", en] if en else [])
    sys.argv = argv
    runpy.run_path(str(KOK / "tools/video_derin.py"), run_name="__main__")

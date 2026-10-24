"""AJAN-TAM-YETKI-1: yetenek fark tablosu (docs/envanter/yetenek-fark.tsv) + eksik skill'leri ~/.claude/skills'e kurar (var olan asla ezilmez).
  python tools/yetenek_fark.py           # tabloyu yazar, kurulacakları gösterir (kuru)
  python tools/yetenek_fark.py uygula    # CC'de olmayan KURULUM listesini kurar
"""
import csv
import json
import re
import sys
import zipfile
from pathlib import Path

KOK = Path(__file__).resolve().parents[1]
CC = Path.home() / ".claude" / "skills"
KURULUM = ["video-tarama", "video-izle", "video-uygula", "headroom-compress", "pixeljury", "remotion-video-paket", "hyperframes-paket"]
# lisans kapısı: lisanssız repo kurulmaz (threejs) ya da eklenti skill'i; kurulmayanlar tabloda "atlandı"
ATLA = {"threejs-awesome-graphics": "lisanssız (license-gate)", "domain-modeling": "kaynak yok", "grill-with-dogs": "kaynak yok"}


def dist_kaynak():
    """skill adı → (zip, iç dizin); aynı ada birden çok zip varsa son (en yeni) olan."""
    k = {}
    for z in sorted((KOK / "dist").rglob("*.zip"), key=lambda p: p.stat().st_mtime):
        try:
            for n in zipfile.ZipFile(z).namelist():
                m = re.match(r"([^/]+)/SKILL\.md$", n)
                if m:
                    k[m[1]] = z
        except zipfile.BadZipFile:
            pass
    return k


def kaynak(ad, dist):
    if (KOK / "skills" / ad / "SKILL.md").exists():
        return "repo", KOK / "skills" / ad
    return ("dist", dist[ad]) if ad in dist else (None, None)


def kur(ad, tur, yol):
    hedef = CC / ad
    if hedef.exists():
        return "var"
    if tur == "repo":
        import shutil
        shutil.copytree(yol, hedef)
    else:
        with zipfile.ZipFile(yol) as z:
            for n in z.namelist():
                if n.startswith(ad + "/") and not n.endswith("/"):
                    p = CC / n
                    p.parent.mkdir(parents=True, exist_ok=True)
                    p.write_bytes(z.read(n))
    return "kuruldu"


def tablo():
    dist = dist_kaynak()
    env = list(csv.DictReader((KOK / "docs/envanter/envanter.tsv").open(encoding="utf-8"), delimiter="\t"))
    cc_var = {p.name for p in CC.iterdir()}
    satir = []
    for ad in sorted(set(dist) | {x["ad"] for x in env if x["tur"] == "skill"}):
        tur, _ = kaynak(ad, dist)
        desk = "dist" if ad in dist else ("repo" if tur else "?")
        satir.append((ad, "skill", desk, "var" if ad in cc_var else "YOK", "Skill aracı (ajan-sira.slash)", "dist/repo→~/.claude/skills" if ad not in cc_var else "-"))
    return satir, dist, cc_var


if __name__ == "__main__":
    satir, dist, cc_var = tablo()
    cikti = KOK / "docs/envanter/yetenek-fark.tsv"
    ekle = Path(sys.argv[2]) if len(sys.argv) > 2 else None
    with cikti.open("w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, delimiter="\t")
        w.writerow(["yetenek", "tur", "desktop_kaynak", "cc", "ajan", "aktarim_yolu"])
        w.writerows(satir)
        if ekle:
            w.writerows(csv.reader(ekle.open(encoding="utf-8"), delimiter="\t"))
    yok = [s for s in satir if s[3] == "YOK"]
    print(f"skill: {len(satir)} · CC'de YOK: {len(yok)} · yazıldı {cikti}")
    for ad in KURULUM:
        tur, yol = kaynak(ad, dist)
        if not tur:
            print("kaynak yok:", ad)
        elif "uygula" in sys.argv[1:2]:
            print(ad, kur(ad, tur, yol))
        else:
            print("kuru:", ad, "var" if ad in cc_var else f"kurulacak ({tur})")
    for ad, neden in ATLA.items():
        print("atlandı:", ad, neden)

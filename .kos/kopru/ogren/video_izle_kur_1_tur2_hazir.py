"""VIDEO-IZLE-KUR-1 tur 2 hazirlik: (1) derin ciktisi olmayan videolar -> derin-eksik.txt, (2) ELE-V1 18 kalem -> ele18.tsv,
(3) v2 UYARLA/AL satirlari -> v2-uyarla.tsv. Kullanim: python -I -X utf8 video_izle_kur_1_tur2_hazir.py"""
import csv, re
from pathlib import Path

K = Path(r"C:/Projeler/omer-skills")
O = K / ".kos/kopru/ogren"
D = O / "video-izle-kur-1"
DERIN = [K / "docs/video-tarama/derin", K / "docs/video-tarama/derin-2"]
URL = re.compile(r"https?://(?:www\.)?(?:instagram\.com/(?:reel|p)/[\w-]+|youtube\.com/shorts/[\w-]+|youtube\.com/watch\?v=[\w-]+|youtu\.be/[\w-]+)")


def kod(l):
    return re.sub(r".*/(reel|p|shorts)/|.*v=|.*youtu\.be/", "", l).strip("/").split("?")[0]


linkler = {}
for f in ("video-764.tsv", "video-764-v2.tsv", "video-764-hata.tsv"):
    for l in URL.findall((O / f).read_text(encoding="utf-8")):
        linkler.setdefault(kod(l), l)
eksik = [u for k, u in linkler.items() if not any((d / f"{k}.json").exists() for d in DERIN)]
(D / "derin-eksik.txt").write_text("\n".join(eksik) + "\n", encoding="utf-8")
print("tekil video", len(linkler), "derin eksik", len(eksik), "ig", sum("instagram" in u for u in eksik))

env = list(csv.reader(open(D / "envanter.tsv", encoding="utf-8"), delimiter="\t"))
ele = [env[0]] + [r for r in env[1:] if r[6].startswith("ELE")]
csv.writer(open(D / "ele18.tsv", "w", encoding="utf-8", newline=""), delimiter="\t").writerows(ele)
print("ele", len(ele) - 1, [r[0] for r in ele[1:]])

v2 = list(csv.reader(open(O / "video-764-v2.tsv", encoding="utf-8"), delimiter="\t"))
uy = [v2[0]] + [r for r in v2[1:] if len(r) > 4 and r[4].strip() in ("UYARLA", "AL")]
csv.writer(open(D / "v2-uyarla.tsv", "w", encoding="utf-8", newline=""), delimiter="\t").writerows(uy)
print("v2 uyarla/al", len(uy) - 1)

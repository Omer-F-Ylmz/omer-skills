"""VIDEO-IZLE-KUR-1: tur partisi sec (<=40) + kaynak videolarin derin json durumu.
Kullanim: python -I -X utf8 video_izle_kur_1_tur.py <tur_no>  -> video-izle-kur-1/tur<N>.tsv, tur<N>-video.txt
"""
import csv, re, sys
from pathlib import Path

K = Path(r"C:/Projeler/omer-skills")
D = K / ".kos/kopru/ogren/video-izle-kur-1"
n = int(sys.argv[1])
env = list(csv.DictReader(open(D / "envanter.tsv", encoding="utf-8"), delimiter="\t"))
aday = {r["ad"]: r for r in csv.DictReader(open(K / ".kos/kopru/ogren/video-764-aday.tsv", encoding="utf-8"), delimiter="\t")}
derin = {p.stem for p in (K / "docs/video-tarama/derin").glob("*.json")} | {p.stem for p in (K / "docs/video-tarama/derin-2").glob("*.json")}
kal = [r for r in env if r["durum"] in ("KURULACAK", "KLONLU")]
kal.sort(key=lambda r: -int(r["puan"] or 0))
parti = kal[(n - 1) * 40: n * 40]
vids, out = [], []
for r in parti:
    links = (aday.get(r["ad"], {}).get("video link") or "").split()
    kod = [re.sub(r".*/(reel|p|shorts)/|.*v=|.*youtu\.be/", "", l).strip("/").split("?")[0] for l in links]
    var = [k for k in kod if k in derin]
    r = dict(r, video=" ".join(links), derin_var=f"{len(var)}/{len(kod)}")
    out.append(r)
    vids += [l for l, k in zip(links, kod) if k not in derin][:1]
with open(D / f"tur{n}.tsv", "w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(out[0]), delimiter="\t")
    w.writeheader()
    w.writerows(out)
(D / f"tur{n}-video.txt").write_text("\n".join(dict.fromkeys(vids)) + "\n", encoding="utf-8")
print(len(kal), len(out), "derin eksik video:", len(set(vids)), "derin tam:", sum(o["derin_var"].split("/")[0] != "0" for o in out))

import re
from pathlib import Path

kok = Path(r"C:\Projeler\omer-skills\.kos\kopru")
kaynak = (kok / "yeni-linkler-2026-11-03.txt").read_text(encoding="utf-8").splitlines()
esle = {}
son = None
for l in kaynak:
    m = re.search(r"instagram\.com/(?:reel|p)/([A-Za-z0-9_-]+)|shorts/([A-Za-z0-9_-]{11})", l)
    if m:
        son = m.group(1) or m.group(2)
        continue
    s = l.strip()
    if son and s.startswith("NOT"):
        esle.setdefault(son, []).append(s.split(":", 1)[1].strip())
cikti = kok / "arka" / "video-toplu-1-notlar.tsv"
cikti.write_text("".join("%s\t%s\n" % (k, " | ".join(v)) for k, v in esle.items()), encoding="utf-8")
kuyruk = (kok / "arka" / "video-toplu-1-kuyruk.txt").read_text(encoding="utf-8")
eksik = [k for k in esle if k not in kuyruk]
(kok / "arka" / "video-toplu-1-notlar.ozet.txt").write_text(
    "not %d, kuyrukta olmayan %d %s\n" % (len(esle), len(eksik), eksik), encoding="utf-8")

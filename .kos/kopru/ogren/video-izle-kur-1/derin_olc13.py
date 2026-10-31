"""TUR 13: derin-eksik.txt'teki 261 videodan hangilerinin derin çıktısı hâlâ yok (ad içinde video id araması)."""
import re, pathlib, sys
K = pathlib.Path(__file__).resolve().parents[4]
vt = K / "docs/video-tarama"
adlar = " ".join(p.name for d in vt.iterdir() if d.is_dir() and d.name.startswith("derin") for p in d.rglob("*"))
eksik = []
for u in (pathlib.Path(__file__).parent / "derin-eksik.txt").read_text(encoding="utf-8").split():
    m = re.search(r"(?:youtu\.be/|v=|shorts/|reels?/|p/|tv/)([\w-]{6,})", u)
    vid = m.group(1) if m else u
    if vid not in adlar:
        eksik.append(u)
(pathlib.Path(__file__).parent / "derin-eksik-13.txt").write_text("\n".join(eksik) + "\n", encoding="utf-8")
print("toplam", len(open(pathlib.Path(__file__).parent / "derin-eksik.txt").read().split()), "eksik", len(eksik))

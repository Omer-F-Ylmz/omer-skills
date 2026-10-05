# A7 eki-2 canlı (ağsız, model 0, yazmaz): vfLtsYbtJf0 prompt_metni ilk 3 satır (başlık satırı hariç).
from pathlib import Path

from video import getir as gt

r = Path(r"C:\Projeler\omer-skills\docs\video-tarama\2026-10-03-vfLtsYbtJf0.md").read_text(encoding="utf-8")
m = gt.prompt_metni(r, r"C:\Projeler\.video-cache\vfLtsYbtJf0\segmentler.jsonl").splitlines()
print("\n".join(m[2:5]))

import re
from datetime import datetime
from pathlib import Path

kok = Path(r"C:\Projeler\omer-skills")
t = (kok / ".kos/kopru/arka/video-toplu-1.log").read_text(encoding="utf-8", errors="replace").splitlines()
yi = max(i for i, l in enumerate(t) if l.startswith("YENIDEN"))
t = t[yi:]
ok = sum(1 for l in t if re.match(r"^\S+\tok ", l))
hata = sum(1 for l in t if re.match(r"^\S+\t(indirilemedi|hata)", l))
dev = {}
for l in t:
    if l.startswith("device="):
        dev[l] = dev.get(l, 0) + 1
dk = (datetime.now() - datetime(2026, 11, 3, 14, 46, 0)).total_seconds() / 60
groq = [l for l in (kok / "tools/video_derin.py").read_text(encoding="utf-8", errors="replace").splitlines() if re.search(r"VD_GROQ|groq_uygun|def .*groq", l, re.I)][:25]
cuda_ornek = [t[i - 3:i + 1] for i, l in enumerate(t) if l.startswith("device=cuda")][:2]
s = "ok %d hata %d toplam %d | %.0f dk | %.0f link/sa | aygit %s\n---groq kodu---\n%s\n---cuda ornek---\n%s" % (
    ok, hata, ok + hata, dk, (ok + hata) / dk * 60, dev, "\n".join(groq), cuda_ornek)
(kok / ".kos/kopru/arka/video-toplu-1-say.txt").write_text(s, encoding="utf-8")

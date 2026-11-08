import re
from pathlib import Path

kok = Path(r"C:\Projeler\omer-skills")
s = []
for ad in ("tools/video_derin.py", "tools/toplu_gozetmen.py"):
    p = kok / ad
    if not p.exists():
        s.append("%s YOK" % ad)
        continue
    t = p.read_text(encoding="utf-8", errors="replace").splitlines()
    s.append("## %s (%d satir)" % (ad, len(t)))
    s += [l.strip() for l in t[:12] if l.strip().startswith(("\"\"\"", "#", "Kullan"))]
    s += [l.strip() for l in t if re.search(r"add_argument|sys\.argv|--[a-z]+\"", l)][:40]
(kok / ".kos/kopru/log/arg_bak.out.txt").write_text("\n".join(s), encoding="utf-8")

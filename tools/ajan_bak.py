import re
from pathlib import Path

kok = Path(r"C:\Projeler\omer-skills")
t = (kok / "tools/cc-kopru/sunucu.mjs").read_text(encoding="utf-8", errors="replace").splitlines()
s = [("%d: %s" % (i + 1, l.strip()))[:220] for i, l in enumerate(t)
     if re.search(r"permission|schtasks|claude\.exe|'-p'|\"-p\"|--print|max-turns|spawn\(|Gorev|zamanlay", l, re.I)]
for p in sorted(kok.glob("tools/*.py")) + sorted(kok.glob("tools/*.ps1")):
    try:
        if re.search(r"schtasks|Register-ScheduledTask", p.read_text(encoding="utf-8", errors="ignore")):
            s.append("ZAMANLAYICI: " + p.name)
    except Exception:
        pass
(kok / ".kos/kopru/log/ajan_bak.out.txt").write_text("\n".join(s[:60]), encoding="utf-8")

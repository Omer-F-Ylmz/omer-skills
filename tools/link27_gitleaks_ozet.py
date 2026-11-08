import json, sys
from collections import Counter
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
L = Path(r"C:\Users\pc\Desktop\Claude ile yapılanlar\araclar\link27")
for d in sorted(L.iterdir()):
    g = d / ".gitleaks.json"
    if not g.is_file():
        continue
    try:
        b = json.loads(g.read_text(encoding="utf-8") or "[]")
    except Exception:
        continue
    if not b:
        continue
    kural = Counter(x.get("RuleID") for x in b)
    dosya = Counter(str(Path(x.get("File", "")).as_posix()).split("/")[-1] for x in b)
    yollar = sorted({"/".join(Path(x.get("File", "")).parts[-3:]) for x in b})[:6]
    print(f"## {d.name} · {len(b)} bulgu · kurallar {dict(kural.most_common(4))}")
    print("   ", "; ".join(yollar))

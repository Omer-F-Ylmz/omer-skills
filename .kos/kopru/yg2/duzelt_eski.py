"""duzeltme alanı olmayan derin json'lara yalnız ekran-adı düzeltmesi uygular (model yok); duzeltme alanı eklenir."""
import json
import sys
from pathlib import Path

KOK = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(KOK / "tools"))
import ekran_duzelt  # noqa: E402

n = ops_toplam = degisen = 0
for p in sorted((KOK / "docs/video-tarama/derin").glob("*.json")):
    d = json.loads(p.read_text(encoding="utf-8"))
    if "duzeltme" in d:
        continue
    ekran_m = "\n".join(e["t"] for e in d.get("ekran") or [])
    duz = []
    for s in d.get("transkript") or []:
        s["t"], ops = ekran_duzelt.duzelt(s["t"], ekran_m)
        duz += ops
    d["duzeltme"] = duz
    p.write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")
    n += 1
    ops_toplam += len(duz)
    degisen += bool(duz)
print("işlenen", n, "düzeltme", ops_toplam, "değişen dosya", degisen)

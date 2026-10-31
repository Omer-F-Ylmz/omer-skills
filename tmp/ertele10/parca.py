"""ERTELE-3 tur7: eski 3 setin ölçümü parça parça; argv: dosya baş son. Sonuç parca.jsonl'e eklenir."""
import json, sys, time
from pathlib import Path
KOK = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(KOK / "tools"))
import ertele_katalog as ek
d = ek._dizin()
f, b, s = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
satir = (KOK / f).read_text(encoding="utf-8").splitlines()[b:s]
cikti = Path(__file__).with_name("parca.jsonl")
t0 = time.time()
for i, x in enumerate(satir, b):
    t = json.loads(x)
    o = ek.ara(t["tarif"])
    adlar = [y.split(" · ")[0].strip() for y in o.splitlines() if " · " in y and not y.startswith("  ")]
    hedef = d.get(t["ad"], {}).get("yol")
    sira = next((j + 1 for j, a in enumerate(adlar) if a == t["ad"] or d.get(a, {}).get("yol") == hedef), None)
    with open(cikti, "a", encoding="utf-8") as w:
        w.write(json.dumps(dict(f=f, i=i, ad=t["ad"], sira=sira), ensure_ascii=False) + "\n")
print(f, b, s, f"{time.time()-t0:.0f} sn")

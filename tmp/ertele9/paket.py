"""ERTELE-3 TUR4: kaçanlarda ilk 8'deki paket/departman dosyası altın adı içeriyor mu (iki adımlı yol)."""
import json
from pathlib import Path
K = Path(__file__).parent
d = json.loads(Path("C:/Users/pc/.claude/ertele-dizin.json").read_text(encoding="utf-8"))
geri = json.loads((K / "geri-8.json").read_text(encoding="utf-8"))
ara = {}
for s in (K / "ara-tam.jsonl").read_text(encoding="utf-8").splitlines():
    x = json.loads(s); ara[x["ad"]] = x["adlar"]
iki = 0
for g in geri:
    if g["ok"]:
        continue
    kisa = g["ad"].split(":")[-1].lower()
    bul = None
    for a in ara[g["ad"]]:
        v = d.get(a)
        if v and a != g["ad"] and Path(v["yol"]).is_file() and kisa in Path(v["yol"]).read_text(encoding="utf-8", errors="ignore").lower():
            bul = a; break
    iki += bool(bul)
    print(f"{'IKI' if bul else 'YOK'} {g['ad']} <- {bul or ''}")
print(f"iki adimli ek {iki}")

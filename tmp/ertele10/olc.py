"""ERTELE-3 tur5: kör tariflerde ara çıktısında altın (ad ya da aynı dosya) var mı; skill + ajan."""
import json, sys
from pathlib import Path
KOK = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(KOK / "tools"))
import ertele_katalog as ek
d = ek._dizin()
dosyalar = sys.argv[1:] or ["tmp/ertele9/tarif.jsonl", "tmp/ertele7/tarif.jsonl", "tmp/ertele7/tarif2.jsonl"]
cikti = Path(__file__).with_name("olc-" + "-".join(Path(f).parent.name + Path(f).stem for f in dosyalar) + ".jsonl")
yaz = open(cikti, "w", encoding="utf-8")
for f in dosyalar:
    tut = tut8 = n = 0
    for s in (KOK / f).read_text(encoding="utf-8").splitlines():
        t = json.loads(s)
        o = ek.ara(t["tarif"])
        adlar = [x.split(" · ")[0].strip() for x in o.splitlines() if " · " in x and not x.startswith("  ")]
        hedef = d.get(t["ad"], {}).get("yol")
        sira = next((i + 1 for i, a in enumerate(adlar) if a == t["ad"] or d.get(a, {}).get("yol") == hedef), None)
        n += 1; tut += sira is not None; tut8 += sira is not None and sira <= 8
        yaz.write(json.dumps(dict(f=f, ad=t["ad"], sira=sira, ilk3=adlar[:3]), ensure_ascii=False) + "\n")
        if sira is None: print("YOK", t["ad"], "|", ", ".join(adlar[:3]))
    print(f"{f}: tüm {tut}/{n} · ilk8 {tut8}/{n}")

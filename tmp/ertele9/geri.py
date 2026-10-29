"""ERTELE-3 TUR4: 30 kör skill tarifinde ertele_katalog ara ilk N içinde altın ad var mı (API'siz)."""
import json, subprocess, sys
from pathlib import Path
K = Path(__file__).parent
KOK = K.parents[1]
N = int(sys.argv[1]) if len(sys.argv) > 1 else 8
tut, sat = 0, []
for s in (K / "tarif.jsonl").read_text(encoding="utf-8").splitlines():
    t = json.loads(s)
    o = subprocess.run([sys.executable, "-I", str(KOK / "tools/ertele_katalog.py"), "ara", t["tarif"]],
                       capture_output=True, text=True, encoding="utf-8").stdout
    adlar = [x.split(" · ")[0].strip() for x in o.splitlines() if " · " in x][:N]
    ok = t["ad"] in adlar
    tut += ok
    open(K / "ara-tam.jsonl", "a", encoding="utf-8").write(json.dumps(dict(ad=t["ad"], adlar=adlar), ensure_ascii=False) + "\n")
    sat.append(dict(ad=t["ad"], ok=ok, sira=adlar.index(t["ad"]) + 1 if ok else None, ilk3=adlar[:3]))
    print(f"{'OK ' if ok else 'YOK'} {t['ad']} | {', '.join(adlar[:3])}")
(K / f"geri-{N}.json").write_text(json.dumps(sat, ensure_ascii=False, indent=1), encoding="utf-8")
print(f"bulma {tut}/{len(sat)} (ilk {N})")

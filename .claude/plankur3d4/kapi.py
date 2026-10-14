"""d3↔d4 kapı tablosu: python kapi.py <dizin>...  (kos.py çıktılarından; 0 claude -p)"""
import json
import re
import sys
from pathlib import Path

PAKET = [[0, 1, 2], [3, 4], [5, 6], [7, 8, 9]]
for d in map(Path, sys.argv[1:]):
    kayit = {(r["kol"], r["paket"]): r for r in map(json.loads, (d / "sonuc.jsonl").read_text(encoding="utf8").splitlines())}
    anahtar = json.loads((d / "anahtar.json").read_text(encoding="utf8"))
    y = json.loads((d / "yargic.json").read_text(encoding="utf8"))
    puan = json.loads(re.search(r"\{.*\}", y["result"], re.S).group(0))
    # iş no → kol → [k,s,a,u]
    p = {int(no): {anahtar[no][xy]: v[xy] for xy in "XY"} for no, v in puan.items()}
    kal = lambda k, isler: sum(sum(p[i][k]) for i in isler)  # noqa: E731
    boy = lambda k, isler: [sum(p[i][k][b] for i in isler) for b in range(4)]  # noqa: E731
    jet = lambda k, ps: sum(kayit[(k, q)]["jeton"] or 0 for q in ps)  # noqa: E731
    tum, h0 = range(1, 11), range(4, 11)
    oran = {q: jet("B", [q]) / jet("A", [q]) for q in (0, 1, 2)}
    kotu = max(oran, key=oran.get)
    print(f"== {d.name}")
    print(f"kalite A {kal('A', tum)} / B {kal('B', tum)} ({kal('B', tum) - kal('A', tum):+}) · paket0 hariç A {kal('A', h0)} / B {kal('B', h0)} ({kal('B', h0) - kal('A', h0):+})")
    print(f"boyut [kapsam,sağlamlık,araç,uygulanabilirlik] A {boy('A', tum)} / B {boy('B', tum)}")
    print("iş bazında B−A:", {i: sum(p[i]["B"]) - sum(p[i]["A"]) for i in tum})
    for ad, ps in (("zor", [0, 1, 2]), ("paket0 hariç", [1, 2]), (f"en kötü (paket {kotu}) hariç", [q for q in (0, 1, 2) if q != kotu])):
        print(f"jeton {ad}: B {jet('B', ps)} / A {jet('A', ps)} = ×{jet('B', ps) / jet('A', ps):.3f}")
    print("paket B/A:", {q: round(v, 3) for q, v in oran.items()}, "· tur A/B:", [(kayit[('A', q)]["tur"], kayit[('B', q)]["tur"]) for q in range(4)])
    print(f"rutin: B {jet('B', [3])} / A {jet('A', [3])} = {100 * (jet('B', [3]) / jet('A', [3]) - 1):+.2f}%")
    print("hata:", [k for k, r in kayit.items() if r["hata"]], "·", (d / "ozet.txt").read_text(encoding="utf8").splitlines()[-1])

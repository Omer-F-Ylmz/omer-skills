"""ENVANTER-6 madde 4 tablo: puan6.json (okuyucu, X/Y × 3 ölçüt) + anahtar6.json + sonuc6.jsonl → iş başına A/B' puan, paket jeton/tur."""
import json, sys
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
D = Path(__file__).resolve().parent
puan = json.loads((D / "puan6.json").read_text(encoding="utf8"))
anahtar = json.loads((D / "anahtar6.json").read_text(encoding="utf8"))
isler = [s.split("\t") for s in (D / "isler6.tsv").read_text(encoding="utf8").splitlines()]
top = {"A": [0, 0, 0], "B": [0, 0, 0]}
print("| no | iş | A (seçim/kapsam/uygul.) | B' | fark |")
print("|---|---|---|---|---|")
for n, i, _, _ in isler:
    s = {anahtar[n][xy]: puan[n][xy] for xy in "XY"}
    for k in "AB":
        top[k] = [a + b for a, b in zip(top[k], s[k])]
    print(f"| {n} | {i} | {'/'.join(map(str, s['A']))} = {sum(s['A'])} | {'/'.join(map(str, s['B']))} = {sum(s['B'])} | {sum(s['B']) - sum(s['A']):+d} |")
for k in "AB":
    print(f"{k}: ölçüt toplamları {top[k]} · toplam {sum(top[k])}/{len(isler) * 6}")
kos = [json.loads(l) for l in (D / "sonuc6.jsonl").read_text(encoding="utf8").splitlines()]
for k in "AB":
    r = [x for x in kos if x["kol"] == k]
    print(f"{k}: tur {sum(x['tur'] or 0 for x in r)} · jeton {sum(x['jeton'] or 0 for x in r)} · cache okuma {sum(x['cache_okuma'] or 0 for x in r)} · "
          f"paket jeton {[x['jeton'] for x in r]} · tur {[x['tur'] for x in r]} · hata {[x['hata'] for x in r]}")

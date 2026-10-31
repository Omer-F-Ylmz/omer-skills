"""tur26 adim 1: kur-tur25.tsv -> envanter.tsv (yoksa ekle; ad zaten varsa durum/kanit guncelle)"""
import csv, io
from pathlib import Path

D = Path(__file__).parent
env_p = D / "envanter.tsv"
raw = env_p.read_bytes()
nl = b"\r\n" if b"\r\n" in raw else b"\n"
rows = list(csv.reader(io.StringIO(raw.decode("utf-8")), delimiter="\t"))
idx = {r[0].lower(): i for i, r in enumerate(rows) if r}
yeni = guncel = 0
for r in list(csv.reader(open(D / "kur-tur25.tsv", encoding="utf-8"), delimiter="\t"))[1:]:
    ad, durum, kanit = r[0], r[1], "tur25: " + r[2]
    if ad.lower() in idx:
        row = rows[idx[ad.lower()]]
        row += [""] * (8 - len(row))
        row[6], row[7] = durum, kanit
        guncel += 1
    else:
        rows.append([ad, "arac", "ana-liste", "", "", "", durum, kanit])
        yeni += 1
out = nl.join("\t".join(r).encode("utf-8") for r in rows) + nl
env_p.write_bytes(out)
print(f"yeni={yeni} guncel={guncel} toplam={len(rows) - 1}")

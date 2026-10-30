"""ham-aday.tsv -> disk-tara-2-aday.tsv (iç içe satırlar elenir) + kategori toplamı."""
import csv, collections
R = r"C:\Projeler\omer-skills\.kos\kopru\rapor"
rows = list(csv.reader(open(R + r"\disk-tara-2\ham-aday.tsv", encoding="utf-8"), delimiter="\t"))
hd, rows = rows[0], rows[1:]
paths = [r[0].lower() for r in rows]
keep, nested = [], collections.defaultdict(float)
for r in rows:
    p = r[0].lower()
    anc = [q for q in paths if q != p and p.startswith(q.rstrip("\\") + "\\")]
    if "pagefile" in p or anc:
        if anc and r[2] == "c-yarim":
            nested["c-yarim(üst satırların içinde)"] += float(r[1])
        continue
    keep.append(r)
with open(R + r"\disk-tara-2-aday.tsv", "w", encoding="utf-8", newline="") as f:
    w = csv.writer(f, delimiter="\t")
    w.writerow(hd)
    w.writerows(keep)
tot = collections.defaultdict(float)
for r in keep:
    tot[r[2]] += float(r[1])
for k, v in sorted(tot.items()):
    print(f"{k}\t{v:.1f} GB")
print("toplam", f"{sum(tot.values()):.1f}", dict(nested))
for r in sorted(keep, key=lambda r: -float(r[1]))[:15]:
    print(r[1], r[2], r[0][:90])

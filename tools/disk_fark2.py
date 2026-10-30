"""disk-tara-1 ile disk-tara-2 dirs.tsv farkı: en çok büyüyen/küçülen klasörler (yaprağa yakın)."""
import os
R = r"C:\Projeler\omer-skills\.kos\kopru\rapor"


def load(p):
    d = {}
    for ln in open(p, encoding="utf-8"):
        g, y = ln.rstrip("\n").split("\t", 1)
        d[y.lower()] = float(g)
    return d


a = load(R + r"\disk-tara-1\dirs.tsv")
b = load(R + r"\disk-tara-2\dirs.tsv")
diff = []
for y in set(a) | set(b):
    diff.append((b.get(y, 0.0) - a.get(y, 0.0), y, a.get(y, 0.0), b.get(y, 0.0)))
diff.sort(reverse=True)


def leafish(rows, n):
    out = []
    for dv, y, x1, x2 in rows:
        # üst klasörü zaten listelenmişse çocuğu atla, çocuğu listelenmişse ebeveyni atlama (en derin anlamlı)
        if any(y.startswith(o[1] + "\\") for o in out):
            continue
        out.append((dv, y, x1, x2))
        if len(out) >= n:
            break
    return out


# derin yapraklar için: en büyük farka sahip klasör zinciri içinde en derin >=%70 payı taşıyan
def deepest(rows, n):
    out = []
    for dv, y, x1, x2 in rows:
        if dv < 0.3:
            break
        out.append((dv, y, x1, x2))
    res = []
    for dv, y, x1, x2 in out:
        kids = [o for o in out if o[1].startswith(y + "\\") and o[1].count("\\") == y.count("\\") + 1]
        if kids and sum(k[0] for k in kids) >= 0.7 * dv:
            continue
        res.append((dv, y, x1, x2))
    return res[:n]


with open(R + r"\disk-tara-2\fark.tsv", "w", encoding="utf-8") as f:
    f.write("fark_GB\tdisk1_GB\tdisk2_GB\tyol\n")
    f.write("# BÜYÜYEN\n")
    for dv, y, x1, x2 in deepest(diff, 40):
        f.write(f"{dv:+.2f}\t{x1:.2f}\t{x2:.2f}\t{y}\n")
    f.write("# KÜÇÜLEN\n")
    shr = sorted(diff)
    shr2 = [(-dv, y, x1, x2) for dv, y, x1, x2 in shr]
    for dv, y, x1, x2 in [(-v, y, p, q) for v, y, p, q in deepest([(v, y, p, q) for v, y, p, q in [(-s[0], s[1], s[3], s[2]) for s in shr]], 20)]:
        f.write(f"{-dv:+.2f}\t{x2:.2f}\t{x1:.2f}\t{y}\n")
print(open(R + r"\disk-tara-2\fark.tsv", encoding="utf-8").read()[:6000])

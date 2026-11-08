"""LISTE-EKSIK kapi 2 uygula: cek.tsv'ye gore ana-liste(+ozellik) adlarini kaynak yazimina ceker; metinde olmayan adlari karantinaya alir.
BK/SIKIS -> yeniden adlandir; BULANIK -> ad kalir (kaynak OCR hatali); YOK -> *-ad-yok.tsv (silme yok)."""
import csv
from pathlib import Path
csv.field_size_limit(10**9)
V = Path(r"C:\Projeler\omer-skills\docs\video-tarama")
C = Path(r"C:\Projeler\omer-skills\.kos\kopru\ogren\liste-eksik-ad\cek.tsv")
cek = {}
for l in open(C, encoding="utf-8"):
    a, b, d = l.rstrip("\n").split("\t"); cek[a] = (b, d)


def rd(p):
    return list(csv.reader(open(p, encoding="utf-8", newline=""), delimiter="\t", quoting=csv.QUOTE_NONE))


def wr(p, x):
    with open(p, "w", encoding="utf-8", newline="") as f:
        f.writelines("\t".join(r) + "\n" for r in x)


rows, oz = rd(V / "ana-liste.tsv"), rd(V / "ana-liste-ozellik.tsv")
ren = {a: b for a, (b, d) in cek.items() if d in ("BK", "SIKIS") and b and b != a}
yok = {a for a, (b, d) in cek.items() if d == "YOK"}
seen, out, q, dup = {}, [rows[0]], [], 0
for r in rows[1:]:
    if r[0] in yok:
        q.append(r); continue
    r = list(r); r[0] = ren.get(r[0], r[0])
    if r[0] in seen:
        dup += 1; seen[r[0]][3] += "," + r[3]; continue
    seen[r[0]] = r; out.append(r)
for r in out[1:]:
    r[3] = ",".join(dict.fromkeys(r[3].split(",")))
wr(V / "ana-liste.tsv", out); wr(V / "ana-liste-ad-yok.tsv", [rows[0]] + q)
ok = [oz[0]] + [[ren.get(o[0], o[0])] + o[1:] for o in oz[1:] if o[0] not in yok]
wr(V / "ana-liste-ozellik.tsv", ok); wr(V / "ana-liste-ozellik-ad-yok.tsv", [oz[0]] + [o for o in oz[1:] if o[0] in yok])
print(len(rows) - 1, "->", len(out) - 1, "karantina", len(q), "adlandirilan", len(ren), "birlesen", dup, "ozellik", len(oz) - 1, "->", len(ok) - 1)

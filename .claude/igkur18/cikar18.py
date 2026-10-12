"""IG-18 raporlarından ## Adaylar → ham.tsv + birlesik.tsv (igkur/cikar.py deseni) + ig40 sütunu (IG-40-KUR birlesik.tsv'de aynı anahtar var mı)."""
import collections, pathlib, re, sys

sys.path.insert(0, r"C:/Projeler/omer-skills-wt/igkur/.claude/igkur")
from cikar import norm  # noqa: E402  (IG-40 ile aynı anahtar → karşılaştırma tutarlı)

KOK = pathlib.Path(r"C:/Projeler/omer-skills/docs/video-tarama")
CIK = pathlib.Path(__file__).parent
IDS = re.findall(r"instagram\.com/(?:reel|p)/([^/]+)/", open(r"C:/Projeler/omer-skills/.kos/kuyruk-ig-18.md", encoding="utf-8").read())
IG40 = {s.split("\t")[0]: s.split("\t")[4] for s in open(r"C:/Projeler/omer-skills-wt/igkur/.claude/igkur/birlesik.tsv", encoding="utf-8").read().splitlines()[1:]}
ham, birl = [], collections.OrderedDict()

for gid in IDS:
    metin = (KOK / f"2026-10-12-ig-{gid}.md").read_text(encoding="utf-8")
    m = re.search(r"^## Adaylar\n(.*?)(?=^## )", metin, re.S | re.M)
    if not m:
        print("aday bölümü yok:", gid)
        continue
    for sat in m.group(1).splitlines():
        if not sat.startswith("|") or sat.startswith("|---") or sat.startswith("| ad "):
            continue
        h = [x.strip() for x in sat.strip().strip("|").split("|")]
        if len(h) < 5:
            continue
        ad, _, tur, link, ne = h[:5]
        ham.append((gid, ad, tur, link, ne))
        if not (k := norm(ad)):
            continue
        d = birl.setdefault(k, {"ad": ad, "tur": set(), "link": set(), "ne": ne, "gid": []})
        d["tur"].add(tur)
        if link.startswith("http"):
            d["link"].add(link)
        if gid not in d["gid"]:
            d["gid"].append(gid)

with open(CIK / "ham.tsv", "w", encoding="utf-8", newline="\n") as o:
    o.write("gonderi\tad\ttur\tlink\tiddia\n")
    for r in ham:
        o.write("\t".join(x.replace("\t", " ") for x in r) + "\n")
with open(CIK / "birlesik.tsv", "w", encoding="utf-8", newline="\n") as o:
    o.write("anahtar\tad\ttur\tlink\tgonderi\tiddia\tig40\n")
    for k, d in birl.items():
        o.write(f"{k}\t{d['ad']}\t{','.join(sorted(d['tur']))}\t{' '.join(sorted(d['link']))}\t{','.join(d['gid'])}\t{d['ne']}\t{IG40.get(k, '-')}\n")
ortak = sum(k in IG40 for k in birl)
print(len(IDS), "gönderi", len(ham), "ham", len(birl), "tekil", ortak, "IG-40'ta var", len(birl) - ortak, "yeni")
print(collections.Counter(t for d in birl.values() for t in d["tur"]).most_common(12))

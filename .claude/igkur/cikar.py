"""IG-40 raporlarından ## Adaylar satırlarını çıkar → ham.tsv + birlesik.tsv (ad normalize)."""
import glob, re, sys, collections, pathlib

KOK = pathlib.Path(r"C:/Projeler/omer-skills/docs/video-tarama")
CIK = pathlib.Path(__file__).parent
ham, birl = [], collections.OrderedDict()


def norm(ad):
    a = ad.lower()
    a = re.sub(r"\(.*?\)", "", a)
    a = re.sub(r"[^a-z0-9]+", "", a)
    return a


for f in sorted(glob.glob(str(KOK / "2026-10-12-ig-*.md"))):
    gid = re.search(r"ig-(.+)\.md$", f).group(1)
    metin = open(f, encoding="utf-8").read()
    m = re.search(r"^## Adaylar\n(.*?)(?=^## )", metin, re.S | re.M)
    urls = re.findall(r"https?://[^\s|)>\]]+", metin)
    if not m:
        continue
    for sat in m.group(1).splitlines():
        if not sat.startswith("|") or sat.startswith("|---") or sat.startswith("| ad "):
            continue
        h = [x.strip() for x in sat.strip().strip("|").split("|")]
        if len(h) < 5:
            continue
        ad, _, tur, link, ne = h[:5]
        ham.append((gid, ad, tur, link, ne))
        k = norm(ad)
        if not k:
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
    o.write("anahtar\tad\ttur\tlink\tgonderi\tiddia\n")
    for k, d in birl.items():
        o.write(f"{k}\t{d['ad']}\t{','.join(sorted(d['tur']))}\t{' '.join(sorted(d['link']))}\t{','.join(d['gid'])}\t{d['ne']}\n")
print(len(glob.glob(str(KOK / '2026-10-12-ig-*.md'))), "rapor", len(ham), "ham", len(birl), "tekil")
print(collections.Counter(t for d in birl.values() for t in d["tur"]).most_common(12))

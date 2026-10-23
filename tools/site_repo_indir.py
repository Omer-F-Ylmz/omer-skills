"""KAYNAK-SITE-2 adim 1: site-repo.tsv repo adaylarini arac_indir_1 hattindan indir (clone --depth 1, gitleaks+semgrep). Kurma/calistirma yok."""
import csv, os, sys, shutil
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import arac_indir_1 as a

GURULTU = {"owner/repository", "user/repo", "owner/repo", "username/repo"}
GIRDI = os.path.join(a.KOK, "docs", "site-inceleme", "site-repo.tsv")
CIKTI = os.path.join(a.KOK, ".kos", "kopru", "rapor", "kurulum-ek-site.tsv")


def main():
    if shutil.disk_usage("C:\\").free < 80 * 2**30:
        sys.exit("disk <80GB")
    os.makedirs(a.HEDEF, exist_ok=True)
    aday = {}
    for r in csv.DictReader(open(GIRDI, encoding="utf-8"), delimiter="\t"):
        for x in (r["repo"] or "").split(";"):
            x = x.strip().removesuffix(".git")
            if x.count("/") == 1 and x.lower() not in GURULTU:
                aday.setdefault(x.lower(), [x, r["site"]])
    print("tekil aday", len(aday), flush=True)
    def coz(k):
        d = a.gh_goruntule(aday[k][0])
        return d
    with ThreadPoolExecutor(8) as ex:
        ds = list(ex.map(coz, aday))
    cikti, tekil = [], {}
    for k, d in zip(aday, ds):
        if not d:
            cikti.append([aday[k][0], "-", "bulunamadi", "-", "gh repo view basarisiz", aday[k][1]]); continue
        tekil.setdefault(d["nameWithOwner"].lower(), {"d": d, "kaynak": "site-repo", "video": aday[k][1]})
    print("cozulen", len(tekil), flush=True)
    with ThreadPoolExecutor(4) as ex:
        cikti += list(ex.map(a.isle, tekil.values()))
    with open(CIKTI, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, delimiter="\t"); w.writerow(["ad", "kaynak", "durum", "boyut", "tarama", "site"]); w.writerows(cikti)
    print("bitti", len(cikti))


if __name__ == "__main__":
    main()

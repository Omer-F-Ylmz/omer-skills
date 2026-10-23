"""KAYNAK-SİTE-1 adım 2: site-tam.tsv'deki her siteyi HTTP ile yokla (pencere açmaz): durum, başlık, açıklama, repo/npm, ücretsiz/giriş ipucu."""
import csv, re, sys, ssl, urllib.request, concurrent.futures as cf
from pathlib import Path

R = Path(__file__).resolve().parent.parent
SRC = R / ".kos/kopru/rapor/site-tam.tsv"
OUT = R / ".kos/kopru/rapor/site-prob.tsv"
CTX = ssl.create_default_context()
UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/126 Safari/537.36", "Accept-Language": "en"}
GH = re.compile(r"github\.com/([\w.-]+/[\w.-]+)", re.I)
NPM = re.compile(r"(?:npm (?:i|install)|npx|pnpm add|yarn add)\s+(?:-[A-Za-z]+\s+)*([@\w./-]+)", re.I)


def al(h):
    for sch in ("https://", "http://"):
        try:
            rq = urllib.request.Request(sch + h, headers=UA)
            with urllib.request.urlopen(rq, timeout=8, context=CTX) as r:
                return r.status, r.geturl(), r.read(250000).decode("utf-8", "ignore")
        except urllib.error.HTTPError as e:
            return e.code, sch + h, ""
        except Exception as e:
            son = type(e).__name__
    return 0, "", son


def incele(h):
    st, fu, body = al(h)
    if st == 0:
        return [h, "kapalı", "", "", "", "", "", body]
    t = re.search(r"<title[^>]*>(.*?)</title>", body, re.I | re.S)
    d = re.search(r'<meta[^>]+name=["\']description["\'][^>]+content=["\'](.*?)["\']', body, re.I | re.S)
    clean = lambda x: re.sub(r"\s+", " ", x.group(1)).strip()[:160] if x else ""
    gh = sorted({m for m in GH.findall(body) if not m.lower().startswith(("sponsors/", "login", "features/"))})[:3]
    npm = sorted(set(NPM.findall(body)))[:3]
    low = body.lower()
    ucr = "ücretsiz/free" if re.search(r"\bfree\b|open[- ]source|\bmit license|ücretsiz", low) else ""
    gir = "giriş-ipucu" if st in (401, 403) or re.search(r"sign in to continue|log in to continue|create an account|get started", low[:80000]) else ""
    return [h, "açık" if st < 400 else f"http{st}", clean(t), clean(d), ";".join(gh), ";".join(npm), ucr, gir]


rows = list(csv.DictReader(open(SRC, encoding="utf-8"), delimiter="\t"))
with cf.ThreadPoolExecutor(40) as ex, open(OUT, "w", encoding="utf-8", newline="") as fh:
    w = csv.writer(fh, delimiter="\t")
    w.writerow(["ad", "durum", "baslik", "aciklama", "repo", "npm", "ucretsiz", "giris"])
    for i, r in enumerate(ex.map(incele, [x["ad"] for x in rows])):
        w.writerow(r)
        if i % 200 == 0:
            print(i, flush=True)
print("bitti")

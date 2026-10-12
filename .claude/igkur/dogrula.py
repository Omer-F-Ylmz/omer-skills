"""parcaN.tsv → metaN.tsv: repo çöz (link ya da gh search), lisans/yıldız/push/arşiv, bizde (envanter adı eşleşmesi)."""
import json, re, subprocess, sys, pathlib, concurrent.futures as cf

D = pathlib.Path(__file__).parent
ENV = [s.split("\t") for s in (D / "envanter.txt").read_text(encoding="utf-8").splitlines() if "\t" in s]


def gh(*a):
    r = subprocess.run(["gh", *a], capture_output=True, text=True, encoding="utf-8", timeout=60)
    return r.stdout if r.returncode == 0 else ""


def n(s):
    return re.sub(r"[^a-z0-9]", "", s.lower())


def coz(ad, link):
    m = re.search(r"github\.com/([\w.-]+/[\w.-]+)", link)
    if m:
        return m.group(1).removesuffix(".git"), "link"
    q = re.sub(r"\(.*?\)", "", ad).strip()
    o = gh("search", "repos", q, "--sort", "stars", "--limit", "5", "--json", "fullName")
    k = n(q)
    for x in json.loads(o or "[]"):
        if k and (k in n(x["fullName"].split("/")[1]) or n(x["fullName"].split("/")[1]) in k and len(n(x["fullName"].split("/")[1])) > 3):
            return x["fullName"], "arama"
    return "", "bulunamadı"


def satir(s):
    h = s.split("\t")
    ad, link = h[1], h[3]
    repo, kay = coz(ad, link)
    meta = "-"
    if repo:
        o = gh("api", f"repos/{repo}", "--jq", "[.full_name,(.license.spdx_id//\"yok\"),.stargazers_count,.pushed_at[:10],.archived,.description//\"\"]|@tsv")
        if o:
            f = (o.rstrip("\r\n").split("\t") + [""] * 6)[:6]
            repo, meta = f[0], f"{f[1]}\t★{f[2]}\t{f[3]}\t{'ARŞİV' if f[4] == 'true' else '-'}\t{f[5][:80]}"
    k = n(re.sub(r"\(.*?\)", "", ad))
    rk = n(repo.split("/")[-1]) if repo else ""
    biz = sorted({f"{t}:{a}" for t, a in ENV if k and len(k) > 3 and (k in n(a) or (rk and rk in n(a)))})[:3]
    return f"{h[0]}\t{ad}\t{h[2]}\t{repo or '-'}\t{kay}\t{meta}\t{','.join(biz) or 'yok'}\t{h[4]}"


for p in sys.argv[1:]:
    if p == "b":  # birlesik.tsv: salt-teknik olmayanlar + linkli teknikler → metab.tsv
        L = [s for s in (D / "birlesik.tsv").read_text(encoding="utf-8").splitlines()[1:]
             if s.split("\t")[2] != "teknik" or "github.com" in s.split("\t")[3]]
    else:
        L = (D / f"parca{p}.tsv").read_text(encoding="utf-8").splitlines()[1:] if p != "8" else []
    with cf.ThreadPoolExecutor(6) as ex:
        out = list(ex.map(satir, L))
    (D / f"meta{p}.tsv").write_text("\n".join(out) + "\n", encoding="utf-8", newline="\n")
    print(p, len(out), sum("\tbulunamadı\t" in x for x in out), "bulunamadı")

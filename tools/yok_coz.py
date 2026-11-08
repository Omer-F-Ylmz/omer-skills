"""YOK-COZ (5 Kas): REPO-YOK/DOGRULANAMADI/HATA kalan her repo tahmini için gerçek repoyu arar.
Model owner/repo'yu çoğu zaman yanlış yazmış (HaoAlLab->hao-ai-lab, Akryum/wappalyzer->wappalyzer/wappalyzer).
Sırayla: owner yazım düzeltmeleri (Al->AI, l->I) ile doğrudan gh api; gh search (repo adı, kalem adı); sahibin repoları.
Bulunan: indir_repo + kurulum-toplu.jsonl. Bulunamayan: .kos/kopru/yok-kalan.tsv (en iyi 3 aday ile) — elle bakılacak.
"""
import csv, json, os, re, sys, time
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
KOK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(KOK, "tools"))
import kurulum_coz2 as K  # noqa: E402

_EK = sys.argv[2] if len(sys.argv) > 2 else ""
GIRDI = sys.argv[1] if len(sys.argv) > 1 else os.path.join(KOK, ".kos", "kopru", "yok-liste.tsv")
KALAN = os.path.join(KOK, ".kos", "kopru", f"yok-kalan{_EK}.tsv")
LOG = os.path.join(KOK, ".kos", "kopru", f"yok-coz{_EK}.log")


def yaz(*a):
    s = time.strftime("%H:%M:%S ") + " ".join(str(x) for x in a)
    print(s, flush=True)
    open(LOG, "a", encoding="utf-8").write(s + "\n")


def nrm(s):
    return re.sub(r"[^a-z0-9]", "", str(s).lower().replace("+", "plus"))


def api_var(full):
    rc, o, e = K.k(["gh", "api", f"repos/{full}", "--jq", ".full_name"], 40)
    return o.strip() if rc == 0 and "/" in o else None


def ara(q):
    q = re.sub(r"\(.*?\)|[`'\"|]", " ", q).strip()
    if len(nrm(q)) < 3:
        return []
    time.sleep(2.1)
    rc, o, e = K.k(["gh", "search", "repos", q, "--limit", "10", "--sort", "stars", "--json", "fullName,name,stargazersCount,description"], 60)
    if rc != 0:
        if "rate limit" in (e or "").lower():
            time.sleep(65)
        return []
    try:
        return json.loads(o or "[]")
    except Exception:
        return []


def coz(guess, kalemler):
    owner, name = (guess.split("/") + [""])[:2]
    # 1) owner/name yazım varyantları
    for o2 in {owner.replace("Al", "AI"), owner.replace("l", "I"), owner.lower(), owner.replace("-", "")} - {owner}:
        for n2 in {name, name.replace("Al", "AI")}:
            f = api_var(f"{o2}/{n2}")
            if f:
                return f, "yazim-duzeltme", []
    hedefler = {nrm(name)} | {nrm(k) for k in kalemler if len(nrm(k)) >= 3}
    adaylar = []
    for q in [name] + [k for k in kalemler[:2] if nrm(k) != nrm(name)]:
        for r in ara(q):
            adaylar.append(r)
            if nrm(r["name"]) in hedefler and r.get("stargazersCount", 0) >= 3:
                return r["fullName"], "ad-esit:" + q, []
    # sahip doğru olabilir, ad yanlış
    rc, o, e = K.k(["gh", "api", f"users/{owner}/repos?per_page=100", "--jq", ".[].full_name"], 40)
    if rc == 0:
        for f in o.split():
            fn = nrm(f.split("/")[1])
            if any(h and (h in fn or fn in h) and len(fn) >= 4 for h in hedefler):
                return f, "sahip-reposu", []
    adaylar.sort(key=lambda r: -r.get("stargazersCount", 0))
    return None, "", [f"{r['fullName']}({r.get('stargazersCount', 0)})" for r in adaylar[:3]]


if __name__ == "__main__":
    satirlar = list(csv.DictReader(open(GIRDI, encoding="utf-8"), delimiter="\t"))
    satirlar = [s for s in satirlar if s["repo_istenen"] not in ("None", "")]
    yaz("BASLADI", len(satirlar))
    bulunan = 0
    with open(KALAN, "w", encoding="utf-8") as fk:
        fk.write("repo_istenen\tkalemler\tvideolar\tadaylar\n")
        for i, s in enumerate(satirlar, 1):
            ks = [k.strip() for k in s["kalemler"].split("|") if k.strip()]
            f, yol, aday = coz(s["repo_istenen"], ks)
            if f:
                r = K.indir_repo(f)
                r.update(repo_istenen=s["repo_istenen"], kalemler=ks, kaynak="yok_coz", bulma=yol, zaman=time.strftime("%H:%M:%S"))
                open(K.TOPLU, "a", encoding="utf-8").write(json.dumps(r, ensure_ascii=False) + "\n")
                bulunan += 1
            else:
                fk.write(f"{s['repo_istenen']}\t{' | '.join(ks)}\t{s['videolar']}\t{' ; '.join(aday)}\n"); fk.flush()
            if i % 25 == 0:
                yaz(i, "/", len(satirlar), "bulunan", bulunan)
    yaz("YOK-COZ-BITTI bulunan", bulunan, "/", len(satirlar))

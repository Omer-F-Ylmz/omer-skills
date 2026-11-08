"""KURULUM-EKSIK (5 Kas): indir() filtresine takılıp hiç denenmemiş gh kalemlerini + npm/pypi/cc kalemlerini kapatır.
gh: repo var mı + README/açıklamada kalem geçiyor mu (uydurma model tahmini elenir) -> indir_repo.
npm: C:\\Projeler\\_araclar\\npm-kalem (yerel prefix), pypi: C:\\Projeler\\_araclar\\venv-kalem (ayrı venv) — sistem bozulmaz.
python tools/kurulum_eksik.py   -> kurulum-toplu.jsonl'a ekler, .kos/kopru/kurulum-eksik.log + kurulum-eksik-ozet.json
"""
import base64, json, os, re, subprocess, sys, time
from collections import defaultdict, Counter
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
KOK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(KOK, "tools"))
import kurulum_coz2 as K  # noqa: E402
import kurulum_tamamla as T  # noqa: E402

LOG = os.path.join(KOK, ".kos", "kopru", "kurulum-eksik.log")
OZET = os.path.join(KOK, ".kos", "kopru", "kurulum-eksik-ozet.json")
NPM_DIR = r"C:\Projeler\_araclar\npm-kalem"
VENV = r"C:\Projeler\_araclar\venv-kalem"


def yaz(*a):
    s = time.strftime("%H:%M:%S ") + " ".join(str(x) for x in a)
    print(s, flush=True)
    open(LOG, "a", encoding="utf-8").write(s + "\n")


def kayit(d):
    d.setdefault("zaman", time.strftime("%H:%M:%S"))
    open(K.TOPLU, "a", encoding="utf-8").write(json.dumps(d, ensure_ascii=False) + "\n")


def nrm(s):
    return re.sub(r"[^a-z0-9]", "", str(s).lower())


def toplu_durum():
    t = {}
    for l in open(K.TOPLU, encoding="utf-8", errors="replace"):
        try:
            o = json.loads(l); t[o.get("repo_istenen")] = o.get("durum")
        except Exception:
            pass
    return t


def kanit_haritasi():
    m = {}
    for l in open(K.COZ, encoding="utf-8", errors="replace"):
        try:
            o = json.loads(l)
        except Exception:
            continue
        for kalem, kn in (o.get("kanit") or {}).items():
            if kn == "raporda":
                m[(o.get("video"), kalem)] = True
        if o.get("kaynak") == "gh-arama":
            for kalem in (o.get("eslesme") or {}):
                m[(o.get("video"), kalem)] = True
    return m


def degeri(d):
    if isinstance(d, dict):
        d = d.get("deger") or next((x for x in d.values() if isinstance(x, str)), "")
    s = str(d).strip()
    if re.match(r"^(gh/|github\.com/)", s):
        s = "gh:" + re.sub(r"^(gh/|github\.com/)", "", s)
    return s


def readme(full):
    rc, o, e = K.k(["gh", "api", f"repos/{full}/readme", "--jq", ".content"], 60)
    if rc != 0:
        return ""
    try:
        return base64.b64decode(o.strip()).decode("utf-8", "replace").lower()
    except Exception:
        return ""


def gh_bolum(son, top, kanit):
    repolar = defaultdict(lambda: {"kalemler": [], "kanit": False})
    for v, es in son.items():
        for kalem, d in es.items():
            s = degeri(d)
            if not s.startswith("gh:"):
                continue
            full = s[3:].strip().strip("/")
            full = re.sub(r"\.git$", "", full)
            if not re.fullmatch(r"[\w.-]+/[\w.-]+", full) or (full in top and top[full] != "DOGRULANAMADI"):
                continue
            repolar[full]["kalemler"].append(kalem)
            if kanit.get((v, kalem)):
                repolar[full]["kanit"] = True
    yaz("gh denenmemis tekil repo", len(repolar), "kalem", sum(len(x["kalemler"]) for x in repolar.values()))
    sayac = Counter()
    for i, (full, bilgi) in enumerate(sorted(repolar.items()), 1):
        rc, o, e = K.k(["gh", "api", f"repos/{full}", "--jq", "[.full_name,.size,.description]|@tsv"], 60)
        if rc != 0:
            r = {"repo": full, "durum": "REPO-YOK", "hata": (e or "")[:150]}
        else:
            p = o.strip().split("\t")
            mb = int(p[1]) / 1024 if len(p) > 1 and p[1].isdigit() else 0
            metin = ((p[2] if len(p) > 2 else "") + " " + full).lower() + " " + readme(full)
            tm = nrm(metin)
            nf = nrm(full)
            dogru = bilgi["kanit"] or any(len(nrm(k.replace("+", "plus"))) >= 3 and nrm(k.replace("+", "plus")) in nf for k in bilgi["kalemler"]) or any(len(nrm(k)) >= 4 and nrm(k) in tm for k in bilgi["kalemler"]) \
                or any(len(t) >= 4 and t in tm for k in bilgi["kalemler"] for t in re.findall(r"[a-z0-9][a-z0-9-]{3,}", k.lower()))
            if not dogru:
                r = {"repo": full, "durum": "DOGRULANAMADI", "not": "model tahmini; repo README/aciklamasinda kalem gecmiyor"}
            elif mb > 2048:
                r = {"repo": full, "durum": "BUYUK-SOR", "mb": round(mb)}
            else:
                r = K.indir_repo(full)
        r.update(repo_istenen=full, kalemler=bilgi["kalemler"], kaynak="kurulum_eksik")
        kayit(r)
        sayac[r["durum"]] += 1
        if i % 25 == 0:
            yaz("gh", i, "/", len(repolar), dict(sayac))
        time.sleep(0.3)
    yaz("gh bitti", dict(sayac))
    return dict(sayac)


def paket_bolum(son, top):
    npm, pypi, cc = defaultdict(list), defaultdict(list), defaultdict(list)
    for v, es in son.items():
        for kalem, d in es.items():
            s = degeri(d)
            if s.startswith("npm:"):
                npm[s[4:].strip()].append(kalem)
            elif s.startswith("pypi:"):
                pypi[s[5:].strip()].append(kalem)
            elif s.startswith("cc:"):
                cc[s].append(kalem)
    sayac = Counter()
    for c, ks in cc.items():
        if c not in top:
            kayit({"repo": c, "repo_istenen": c, "durum": "CC-YERLESIK", "kalemler": ks}); sayac["CC-YERLESIK"] += 1
    os.makedirs(NPM_DIR, exist_ok=True)
    if not os.path.exists(os.path.join(NPM_DIR, "package.json")):
        open(os.path.join(NPM_DIR, "package.json"), "w").write('{"name":"npm-kalem","private":true}')
    rc, o, _ = K.k(["npm.cmd", "ls", "-g", "--depth=0", "--json"], 120)
    try:
        glob_npm = set(json.loads(o or "{}").get("dependencies", {}))
    except Exception:
        glob_npm = set()
    def npm_yerinde(pk):
        return os.path.isfile(os.path.join(NPM_DIR, "node_modules", *pk.split("/"), "package.json"))

    for pk, ks in sorted(npm.items()):
        anahtar = "npm:" + pk
        if not re.fullmatch(r"(@[\w-][\w.-]*/)?[\w][\w.-]*", pk):
            continue
        if anahtar in top and (top[anahtar] == "VAR" or npm_yerinde(pk)):
            continue
        if pk in glob_npm:
            r = {"durum": "VAR", "yol": "npm -g"}
        else:
            rc, o, e = K.k(["npm.cmd", "install", "--prefix", NPM_DIR, "--no-audit", "--no-fund", "--ignore-scripts", "--", pk], 600)
            ok = rc == 0 and npm_yerinde(pk)
            r = {"durum": "KURULDU" if ok else "KURULUM-HATA", "yol": NPM_DIR, "hata": "" if ok else (e or "paket klasoru yok")[-200:]}
        r.update(repo=anahtar, repo_istenen=anahtar, kalemler=ks, kaynak="kurulum_eksik")
        kayit(r); sayac["npm/" + r["durum"]] += 1
    py = os.path.join(VENV, "Scripts", "python.exe")
    if not os.path.exists(py):
        K.k([sys.executable, "-m", "venv", VENV], 300)
    rc, o, _ = K.k([sys.executable, "-m", "pip", "list", "--format=json"], 120)
    try:
        sistem = {x["name"].lower() for x in json.loads(o or "[]")}
    except Exception:
        sistem = set()
    for pk, ks in sorted(pypi.items()):
        anahtar = "pypi:" + pk
        if anahtar in top or not re.fullmatch(r"[\w][\w.-]*", pk):
            continue
        if pk.lower() in sistem:
            r = {"durum": "VAR", "yol": "sistem python"}
        else:
            rc, o, e = K.k([py, "-m", "pip", "install", "--only-binary=:all:", "--disable-pip-version-check", "--", pk], 900)
            r = {"durum": "KURULDU" if rc == 0 else "KURULUM-HATA", "yol": VENV, "hata": "" if rc == 0 else (e or "")[-200:]}
        r.update(repo=anahtar, repo_istenen=anahtar, kalemler=ks, kaynak="kurulum_eksik")
        kayit(r); sayac["pypi/" + r["durum"]] += 1
    yaz("paket bitti", dict(sayac))
    return dict(sayac)


if __name__ == "__main__":
    yaz("BASLADI")
    son = T.en_iyi()
    top = toplu_durum()
    g = gh_bolum(son, top, kanit_haritasi())
    p = paket_bolum(son, toplu_durum())
    oz = {"zaman": time.strftime("%Y-%m-%d %H:%M"), "gh": g, "paket": p, "toplu_son": dict(Counter(toplu_durum().values()))}
    json.dump(oz, open(OZET, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    yaz("OZET", json.dumps(oz, ensure_ascii=False))
    yaz("EKSIK-BITTI")

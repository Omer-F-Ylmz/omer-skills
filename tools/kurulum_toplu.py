"""KURULUM-TOPLU-1: ana-liste.tsv'deki kurulmamış araçların reposunu bulur ve indirir (kod çalıştırmaz).
python tools/kurulum_toplu.py say      -> durum/repolink sayımı
python tools/kurulum_toplu.py kos [N]  -> (kaldığı yerden) çöz + indir; N verilirse ilk N kalem
Durum: .kos/kopru/kurulum-toplu.jsonl (kalem başına bir satır). Klonlar: C:/Projeler/_araclar/v/<owner>__<repo>
"""
import csv, json, os, re, subprocess, sys, threading, time, shutil
from concurrent.futures import ThreadPoolExecutor
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
KOK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LISTE = os.path.join(KOK, "docs", "video-tarama", "ana-liste.tsv")
DURUM = os.path.join(KOK, ".kos", "kopru", "kurulum-toplu.jsonl")
HEDEF = r"C:\Projeler\_araclar\v"
ESKI = [r"C:\Projeler\_araclar", os.path.expanduser(r"~\.claude\skills"), os.path.expanduser(r"~\.claude\plugins")]
ISTENEN = {"KURULMADI-SIRADA", "BULUNAMADI-ARANIYOR"}
GH_RE = re.compile(r"github\.com/([\w.-]+)/([\w.-]+)", re.I)
kilit = threading.Lock()
gh_kilit = threading.Lock()
son_arama = [0.0]


def k(cmd, t=180):
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=t)
        return r.returncode, r.stdout, r.stderr
    except Exception as e:
        return -1, "", str(e)


def satirlar():
    with open(LISTE, encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f, delimiter="\t"))


def norm(s):
    return re.sub(r"[^a-z0-9]", "", s.lower())


def yol_adi(kalem):
    return bool(re.search(r"[\\/]|\.(json|sh|py|md|ts|js|yml|yaml|toml)$", kalem)) or kalem.startswith(".")


def ara(kalem):
    q = re.sub(r"[^\w\s.-]", " ", kalem).strip()
    if not q:
        return None, "bos sorgu"
    with gh_kilit:
        bek = 2.1 - (time.time() - son_arama[0])
        if bek > 0:
            time.sleep(bek)
        son_arama[0] = time.time()
    rc, o, e = k(["gh", "search", "repos", q, "--limit", "5", "--json", "fullName,description,stargazersCount,url"], 60)
    if rc != 0:
        if "rate limit" in (e or "").lower():
            time.sleep(60)
            return ara(kalem)
        return None, "arama hata: " + (e or "")[:120]
    try:
        js = json.loads(o or "[]")
    except Exception:
        return None, "arama json hata"
    nk = norm(kalem)
    en = None
    for r in js:
        ad = r["fullName"].split("/")[1]
        na = norm(ad)
        if na == nk or (len(nk) >= 4 and (nk in na or na in nk)):
            if en is None or r["stargazersCount"] > en["stargazersCount"]:
                en = r
    if en:
        return en["fullName"], f"ad eşleşti ({en['stargazersCount']}★): {(en.get('description') or '')[:100]}"
    return None, "ad eşleşen repo yok; adaylar: " + ", ".join(r["fullName"] for r in js[:3])


def zaten_var(owner, repo):
    for b in ESKI:
        for ad in (repo, f"{owner}__{repo}"):
            if os.path.isdir(os.path.join(b, ad)):
                return os.path.join(b, ad)
    p = os.path.join(HEDEF, f"{owner}__{repo}")
    return p if os.path.isdir(os.path.join(p, ".git")) else None


def indir(full):
    owner, repo = full.split("/")[:2]
    repo = re.sub(r"\.git$", "", repo)
    var = zaten_var(owner, repo)
    if var:
        return "VAR", var, ""
    rc, o, e = k(["gh", "api", f"repos/{owner}/{repo}", "--jq", ".size,.archived,.license.spdx_id,.default_branch"], 60)
    if rc != 0:
        return "REPO-YOK", "", (e or "")[:150]
    p = o.split()
    boyut_mb = int(p[0]) / 1024 if p and p[0].isdigit() else 0
    if shutil.disk_usage("C:\\").free / 2**30 < 45:
        return "DISK-BEKLE", "", "C: < 45 GB"
    hedef = os.path.join(HEDEF, f"{owner}__{repo}")
    args = ["git", "clone", "--depth", "1", "--single-branch", "--no-tags"]
    if boyut_mb > 300:
        args += ["--filter=blob:limit=20m"]
    rc, o, e = k(args + [f"https://github.com/{owner}/{repo}.git", hedef], 900)
    if rc != 0:
        return "INDIRME-HATA", "", (e or "")[-200:]
    return "INDIRILDI", hedef, f"{boyut_mb:.0f} MB, lisans {p[2] if len(p) > 2 else '?'}"


def isle(s):
    kalem = s["kalem"]
    kayit = {"kalem": kalem, "videolar": s.get("kaynak_video_idleri", ""), "zaman": time.strftime("%H:%M:%S")}
    m = GH_RE.search(s.get("repo_link") or "")
    if m:
        full, neden = f"{m.group(1)}/{m.group(2)}", "listedeki repo_link"
    elif yol_adi(kalem):
        kayit.update(durum="YOL-ADI", neden="videoda dosya yolu olarak geçiyor; aynı videonun aracına bağlanacak")
        return kayit
    else:
        full, neden = ara(kalem)
    if not full:
        kayit.update(durum="BULUNAMADI", neden=neden)
        return kayit
    d, yol, ek = indir(full)
    kayit.update(durum=d, repo=full, yol=yol, neden=neden, ek=ek)
    return kayit


def bitenler():
    if not os.path.exists(DURUM):
        return set()
    return {json.loads(l)["kalem"] for l in open(DURUM, encoding="utf-8") if l.strip()}


def main():
    tum = [s for s in satirlar() if s.get("tur") == "arac" and s.get("durum") in ISTENEN]
    if sys.argv[1] == "say":
        rl = sum(1 for s in tum if GH_RE.search(s.get("repo_link") or ""))
        ya = sum(1 for s in tum if yol_adi(s["kalem"]))
        print("hedef", len(tum), "repo_link", rl, "yol-adi", ya, "bitmis", len(bitenler()))
        return
    os.makedirs(HEDEF, exist_ok=True)
    b = bitenler()
    kalan = [s for s in tum if s["kalem"] not in b]
    if len(sys.argv) > 2:
        kalan = kalan[: int(sys.argv[2])]
    print("kalan", len(kalan), flush=True)
    sayac = [0]

    def yaz(s):
        r = isle(s)
        with kilit:
            with open(DURUM, "a", encoding="utf-8") as f:
                f.write(json.dumps(r, ensure_ascii=False) + "\n")
            sayac[0] += 1
            if sayac[0] % 25 == 0:
                print(time.strftime("%H:%M"), sayac[0], "/", len(kalan), r["durum"], flush=True)
    with ThreadPoolExecutor(8) as ex:
        list(ex.map(yaz, kalan))
    print("BITTI", sayac[0], flush=True)


if __name__ == "__main__":
    main()

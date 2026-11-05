"""KURULUM-TOPLU-1 / çöz: kurulmamış araçları VİDEO bazında çözer (video raporu + ücretsiz model -> owner/repo), sonra indirir.
Hiçbir kalem atılmaz: slash komutu -> ait olduğu paketin reposu; CC yerleşik komutu -> CC-YERLESIK; repo yoksa NPM/PYPI/SITE/BULUNAMADI.
python tools/kurulum_coz2.py coz [N]    -> .kos/kopru/kurulum-coz.jsonl (video başına)
python tools/kurulum_coz2.py indir      -> tekil repoları klonlar, .kos/kopru/kurulum-toplu.jsonl
python tools/kurulum_coz2.py say
"""
import csv, glob, json, os, re, subprocess, sys, threading, time, shutil
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
KOK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(KOK, "tools"))
import ucretsiz_havuz as UH  # noqa: E402
VT = os.path.join(KOK, "docs", "video-tarama")
LISTE = os.path.join(VT, "ana-liste.tsv")
COZ = os.path.join(KOK, ".kos", "kopru", "kurulum-coz.jsonl")
TOPLU = os.path.join(KOK, ".kos", "kopru", "kurulum-toplu.jsonl")
HEDEF = r"C:\Projeler\_araclar\v"
ESKI = [r"C:\Projeler\_araclar", os.path.expanduser(r"~\.claude\skills"), os.path.expanduser(r"~\.claude\plugins\marketplaces"), os.path.expanduser(r"~\.claude\plugins\cache")]
ISTENEN = {"KURULMADI-SIRADA", "BULUNAMADI-ARANIYOR"}
GECICI = {"INDIRME-HATA", "GH-HATA", "DISK-BEKLE"}  # tekrar denenir; REPO-YOK/VAR/INDIRILDI kalicidir
GH = re.compile(r"github\.com/([A-Za-z0-9][\w.-]*)/([\w.-]+)")
SLASH_GH = re.compile(r"\b([A-Za-z0-9][\w-]{1,38})\s*/\s*([A-Za-z0-9][\w.-]{1,99})\b")
kilit = threading.Lock()


def k(cmd, t=120):
    """Ortak alt-surec yardimcisi (ECC H2): stdin kapali, git istemi yok, utf-8/replace, zaman asiminda agac oldurulur.
    Donus kodlari: -1 baska hata, -2 TIMEOUT, -3 ARAC-YOK."""
    env = dict(os.environ, GIT_TERMINAL_PROMPT="0")
    try:
        p = subprocess.Popen(cmd, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
                             encoding="utf-8", errors="replace", env=env, creationflags=0x08000000)
    except FileNotFoundError as e:
        return -3, "", "ARAC-YOK: " + str(e)
    except Exception as e:
        return -1, "", str(e)
    try:
        o, e = p.communicate(timeout=t)
        return p.returncode, o, e
    except subprocess.TimeoutExpired:
        subprocess.run(["taskkill", "/PID", str(p.pid), "/T", "/F"], capture_output=True, stdin=subprocess.DEVNULL)
        try:
            p.communicate(timeout=5)
        except Exception:
            pass
        return -2, "", "TIMEOUT"
    except Exception as e:
        return -1, "", str(e)


def bekleyen():
    tam = os.environ.get("KAPSAM") == "tam"
    turler = {"arac", "kutuphane", "ui-kutuphane"} if tam else {"arac"}
    durumlar = ISTENEN | ({"KAYITSIZ", "KURULU-KANITSIZ", "KURULUM-HATA"} if tam else set())
    with open(LISTE, encoding="utf-8", newline="") as f:
        return [s for s in csv.DictReader(f, delimiter="\t") if s.get("tur") in turler and s.get("durum") in durumlar]


class Dizin:
    def __init__(self):
        self.dosyalar = []
        for p in glob.glob(os.path.join(VT, "**", "*"), recursive=True):
            if os.path.isfile(p) and p.lower().endswith((".md", ".txt", ".json")) and os.path.getsize(p) < 400_000:
                self.dosyalar.append(p)
        self.cache = {}

    def get(self, vid, varsayilan=None):
        if vid not in self.cache:
            ilk = [p for p in self.dosyalar if vid in os.path.basename(p)]
            klasor = [p for p in self.dosyalar if (os.sep + vid + os.sep) in p and p not in ilk]
            sira = sorted(ilk, key=lambda p: (not p.endswith(".md"), len(p))) + sorted(klasor, key=lambda p: ("aciklama" not in p, "transkript" not in p))
            self.cache[vid] = sira
        return self.cache[vid] or (varsayilan or [])


def rapor_dizini():
    return Dizin()


def oku(paths, n=9000):
    out = []
    for p in paths[:4]:
        try:
            out.append(open(p, encoding="utf-8", errors="replace").read()[: n // max(1, len(paths[:4]))])
        except OSError:
            pass
    return "\n---\n".join(out)


ISTEM = """Aşağıda bir kısa videonun inceleme raporu ve bu videoda geçen, henüz kurmadığımız kalemler var.
Her kalem için gerçek kurulum kaynağını bul. Yalnız JSON döndür: {"kalem adı": "deger", ...}
deger biçimleri:
- "gh:owner/repo"  (raporda/ekranda/açıklamada görünen ya da kalemin kesin ait olduğu GitHub reposu; slash komutları ve alt skill'ler ait oldukları paketin reposuna bağlanır)
- "npm:paket" | "pypi:paket" | "site:alanadi" (GitHub reposu yoksa)
- "cc:yerlesik" (Claude Code'un kendi komutu/özelliği: /clear /compact /effort /btw /add-dir /branch vb.)
- "genel:kategori" (kurulacak tek bir şey değil, genel kavram/teknoloji: ".NET", "GitHub", "Instagram", "Claude" gibi)
- "bilinmiyor:" + kısa neden
Uydurma repo yazma; emin değilsen "bilinmiyor". Kalemler:
{kalemler}

RAPOR:
{rapor}"""


def coz_video(vid, kalemler, idx):
    metin = oku(idx.get(vid, []))
    gh_ipucu = sorted({f"{a}/{b}" for a, b in GH.findall(metin)})
    istem = ISTEM.replace("{kalemler}", "\n".join("- " + x for x in kalemler)).replace("{rapor}", (metin or "(rapor yok)") + ("\nGITHUB LİNKLERİ: " + ", ".join(gh_ipucu) if gh_ipucu else ""))
    cevap, kaynak, _ = UH.cagir("yazim", istem, etiket="kurulum-coz")
    if not cevap:
        cevap, kaynak, _ = UH.cagir("hakem", istem, etiket="kurulum-coz")
    sonuc = {}
    if cevap:
        m = re.search(r"\{.*\}", cevap, re.S)
        if m:
            try:
                sonuc = json.loads(m.group(0))
            except Exception:
                sonuc = {}
    alt = metin.lower()
    es, kanit = {}, {}
    for x in kalemler:
        d = sonuc.get(x, "bilinmiyor:model cevabı yok")
        es[x] = d
        if isinstance(d, str) and d.startswith("gh:"):
            full = d[3:].strip().strip("/").lower()
            kanit[x] = "raporda" if (full in alt or full.replace("/", " / ") in alt) else "model-tahmini"
    return {"video": vid, "kaynak": kaynak, "rapor_var": bool(metin), "eslesme": es, "kanit": kanit}


def coz(n=None):
    satir = bekleyen()
    grup = defaultdict(list)
    for s in satir:
        vids = [v for v in (s.get("kaynak_video_idleri") or "").split(",") if v]
        grup[vids[0] if vids else "_yok"].append(s["kalem"])
    bitti = set()
    if os.path.exists(COZ):
        for r in (json.loads(l) for l in open(COZ, encoding="utf-8") if l.strip()):
            if r.get("kaynak"):
                for kl, d in (r.get("eslesme") or {}).items():
                    if not (isinstance(d, str) and "cevabı yok" in d):
                        bitti.add((r["video"], kl))
    isler = []
    for v, ks in grup.items():
        kalan = [x for x in ks if (v, x) not in bitti]
        if kalan:
            isler.append((v, kalan))
    if n:
        isler = isler[:n]
    idx = rapor_dizini()
    print("video", len(isler), "kalem", sum(len(x[1]) for x in isler), flush=True)
    say = [0]

    def f(i):
        r = coz_video(i[0], i[1], idx)
        with kilit:
            open(COZ, "a", encoding="utf-8").write(json.dumps(r, ensure_ascii=False) + "\n")
            say[0] += 1
            if say[0] % 20 == 0:
                print(time.strftime("%H:%M"), say[0], "/", len(isler), flush=True)
    with ThreadPoolExecutor(6) as ex:
        list(ex.map(f, isler))
    print("BITTI-COZ", say[0], flush=True)


def _remote_eslesir(p, owner, repo):
    try:
        c = open(os.path.join(p, ".git", "config"), encoding="utf-8", errors="replace").read().lower()
    except OSError:
        return False
    return f"{owner}/{repo}".lower() in c.replace(".git", "")


def _gecerli(p):
    """Dizin var ve yarim klon degil: .git/HEAD ya da .git disinda icerik (ECC H5)."""
    if not os.path.isdir(p):
        return False
    if os.path.isfile(os.path.join(p, ".git", "HEAD")):
        return True
    return any(n != ".git" for n in os.listdir(p))


def _arsive_tasi(p):
    """Silme yok: yarim klon HEDEF/_arsiv altina tasinir."""
    if os.path.exists(p):
        a = os.path.join(HEDEF, "_arsiv")
        os.makedirs(a, exist_ok=True)
        os.replace(p, os.path.join(a, os.path.basename(p) + time.strftime("-%H%M%S")))


def zaten_var(owner, repo):
    for b in ESKI:
        p = os.path.join(b, f"{owner}__{repo}")
        if _gecerli(p):
            return p
        for ad in (repo, repo.lower()):
            p = os.path.join(b, ad)
            if os.path.isdir(p) and _remote_eslesir(p, owner, repo):
                return p
    p = os.path.join(HEDEF, f"{owner}__{repo}")
    return p if _gecerli(p) else None


def indir_repo(full):
    owner, repo = full.split("/")[:2]
    repo = re.sub(r"\.git$", "", repo)
    var = zaten_var(owner, repo)
    if var:
        return {"repo": full, "durum": "VAR", "yol": var}
    rc, o, e = k(["gh", "api", f"repos/{owner}/{repo}", "--jq", "[.full_name,.size,.license.spdx_id,.stargazers_count]|@tsv"], 60)
    if rc != 0:  # ECC H3: yalniz gercek 404 REPO-YOK; hiz siniri/arac yok/zaman asimi gecici GH-HATA
        yok = rc > 0 and re.search(r"HTTP 404|Not Found", e or "")
        return {"repo": full, "durum": "REPO-YOK" if yok else "GH-HATA", "hata": (e or "")[:150]}
    p = o.strip().split("\t")
    gercek = p[0] if p and "/" in p[0] else full
    owner, repo = gercek.split("/")
    var = zaten_var(owner, repo)
    if var:
        return {"repo": gercek, "durum": "VAR", "yol": var}
    if shutil.disk_usage("C:\\").free / 2**30 < 45:
        return {"repo": gercek, "durum": "DISK-BEKLE"}
    mb = int(p[1]) / 1024 if len(p) > 1 and p[1].isdigit() else 0
    hedef = os.path.join(HEDEF, f"{owner}__{repo}")
    args = ["git", "clone", "--depth", "1", "--single-branch", "--no-tags"] + (["--filter=blob:limit=20m"] if mb > 300 else [])
    gecici = hedef + ".tmp"  # ECC H5: gecici dizine klonla, basarida tasi
    _arsive_tasi(gecici)
    rc, o, e = k(args + [f"https://github.com/{gercek}.git", gecici], 900)
    if rc != 0:
        _arsive_tasi(gecici)
        return {"repo": gercek, "durum": "INDIRME-HATA", "hata": (e or "")[-200:]}
    os.replace(gecici, hedef)
    return {"repo": gercek, "durum": "INDIRILDI", "yol": hedef, "mb": round(mb), "lisans": p[2] if len(p) > 2 else "", "yildiz": p[3] if len(p) > 3 else ""}


def indir():
    repolar = defaultdict(list)
    tum = [json.loads(l) for l in open(COZ, encoding="utf-8") if l.strip()]
    sonnetli = {(r["video"], k) for r in tum if r.get("kaynak") == "sonnet" for k in (r.get("eslesme") or {})}
    for r in tum:
        for kalem, d in r["eslesme"].items():
            if r.get("kaynak") != "sonnet" and (r["video"], kalem) in sonnetli:
                continue
            if r.get("kanit", {}).get(kalem) not in ("raporda", "sonnet-bilgisi"):
                if not (isinstance(d, str) and d.startswith("gh:")):
                    continue
                nk = re.sub(r"[^a-z0-9]", "", kalem.lower())
                nr = re.sub(r"[^a-z0-9]", "", d.split("/")[-1].lower())
                if not (len(nk) >= 4 and len(nr) >= 4 and (nk in nr or nr in nk)):
                    continue
            if isinstance(d, str) and d.startswith("gh:"):
                full = d[3:].strip().strip("/")
                if re.fullmatch(r"[\w.-]+/[\w.-]+", full):
                    repolar[full].append(kalem)
    son = {}
    if os.path.exists(TOPLU):
        for l in open(TOPLU, encoding="utf-8"):
            if l.strip():
                d = json.loads(l)
                son[d.get("repo_istenen")] = d.get("durum")
    bitti = {r for r, dm in son.items() if dm not in GECICI}  # ECC H4
    isler = [r for r in repolar if r not in bitti]
    os.makedirs(HEDEF, exist_ok=True)
    print("repo", len(isler), flush=True)
    say = [0]

    def f(full):
        r = indir_repo(full)
        r.update(repo_istenen=full, kalemler=repolar[full], zaman=time.strftime("%H:%M:%S"))
        with kilit:
            open(TOPLU, "a", encoding="utf-8").write(json.dumps(r, ensure_ascii=False) + "\n")
            say[0] += 1
            if say[0] % 20 == 0:
                print(time.strftime("%H:%M"), say[0], "/", len(isler), r["durum"], flush=True)
    with ThreadPoolExecutor(8) as ex:
        list(ex.map(f, isler))
    print("BITTI-INDIR", say[0], flush=True)


def say():
    from collections import Counter
    c = Counter()
    if os.path.exists(COZ):
        for l in open(COZ, encoding="utf-8"):
            if l.strip():
                for d in json.loads(l)["eslesme"].values():
                    c[str(d).split(":")[0]] += 1
    print("coz", dict(c))
    c2 = Counter()
    if os.path.exists(TOPLU):
        for l in open(TOPLU, encoding="utf-8"):
            if l.strip():
                c2[json.loads(l).get("durum")] += 1
    print("indir", dict(c2))


if __name__ == "__main__":
    a = sys.argv[1]
    if a == "coz":
        coz(int(sys.argv[2]) if len(sys.argv) > 2 else None)
    elif a == "indir":
        indir()
    else:
        say()

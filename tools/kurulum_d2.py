"""D2-KUR-1: kurulum-coz.tsv -> kapılar (ADAY eşleşme, güvenlik) -> kurulum -> kurulum-d2-sonuc.tsv (kaldığı yerden sürer).
Kullanım: python tools/kurulum_d2.py --faz tohum|kur|model|ikinci|kapsam [--n N] [--sinif SKILL,CLI,PAKET,MODEL] [--is 6]"""
import csv, io, json, os, re, shutil, subprocess, sys, tempfile, threading, time, urllib.error, urllib.request, urllib.parse
from concurrent.futures import ThreadPoolExecutor
from difflib import SequenceMatcher
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import kurulum_gh_uygula as G

R = Path(__file__).resolve().parents[1]
KOK = R / "docs/video-tarama"
SONUC, ONAY = KOK / "kurulum-d2-sonuc.tsv", R / "dist/paket-4/model-onay.tsv"
ADAYTSV = R / "dist/paket-4/aday.tsv"
KLON = Path(r"C:\Users\pc\Desktop\Claude ile yapılanlar\araclar\ana-liste")
NPMDIR = KLON.parent / "ana-liste-npm"
VENV = Path.home() / ".venvs/ana-liste"
BIN = Path.home() / ".local/bin"
NW = 0x08000000
KILIT, KURKILIT, NPMKILIT, SKILLKILIT = threading.Lock(), threading.Lock(), threading.Lock(), threading.Lock()  # KURKILIT: uv/skill/release; NPMKILIT: tüm npm kurulumları
TKALEM = 180  # kalem başı kurulum zaman aşımı (sn)
DISK_ALT = 32 * 2**30
RAM_TAVAN = 95  # % — üstünde yeni işçi açılmaz
MODEL_TAVAN = 15 * 2**30  # bu koşuda HF'ten indirilecek toplam üst sınır
SUPHE = re.compile(r"curl[^|\n]*\|\s*(ba)?sh|wget[^|\n]*\|\s*(ba)?sh|iex\s*\(|-enc(odedcommand)?\b|FromBase64String|base64\s+(-d|--decode)|atob\(|\.ssh[\\/]|credentials|keychain|process\.env\[?.*(TOKEN|KEY|SECRET)", re.I)
SAYAC = {"model_bayt": 0}
TUR2 = "--tur2" in sys.argv  # HATA kalemlerini (büyük repo, zaman aşımı, derleme, komut adı) bir kez daha dener
if TUR2: TKALEM = 600
KAPI = "--sadece-kapi" in sys.argv  # kapılar (eşleşme+güvenlik) koşar, kurulum yapmaz: KAPI-GECTI
KALEM = set(sys.argv[sys.argv.index("--kalem") + 1].split("|")) if "--kalem" in sys.argv else set()  # yalnız bu kalemler (| ile ayrık)
BILINEN = {"--faz", "--n", "--sinif", "--is", "--sadece-kapi", "--kalem", "--tur2"}


def run(a, t=300, cwd=None, env=None):
    try:
        r = subprocess.run(a, capture_output=True, text=True, encoding="utf-8", errors="ignore", timeout=t, cwd=cwd,
                           stdin=subprocess.DEVNULL, creationflags=NW, env=env)
        return r.returncode, (r.stdout + r.stderr).strip()
    except Exception as e:
        return -1, f"{type(e).__name__}: {e}"[:300]


def oku(p):
    return list(csv.DictReader(open(p, encoding="utf-8"), delimiter="\t")) if Path(p).exists() else []


def yaz(k, sinif, kaynak, durum, yol="", not_="", kanit=""):
    with KILIT:
        yeni = not SONUC.exists()
        with open(SONUC, "a", encoding="utf-8", newline="") as f:
            w = csv.writer(f, delimiter="\t")
            if yeni:
                w.writerow(["kalem", "sinif", "kaynak", "durum", "yol", "not", "kanit"])
            w.writerow([k, sinif, kaynak, durum, yol, re.sub(r"\s+", " ", not_)[:200], re.sub(r"\s+", " ", kanit or not_)[:300]])


def kok(o):
    """kurulum çıktısından kök neden satırları (tahmin yok: log satırının kendisi)."""
    ls = [l.strip() for l in o.splitlines() if re.search(r"error|failed|because|no solution|not found|cannot|unable", l, re.I)]
    return " | ".join(ls[:2])[:180] if ls else o[-150:]


def bitenler():
    return {r["kalem"] for r in oku(SONUC) if r["durum"] != "KAPI-GECTI"}


KAPIGECTI = {r["kalem"] for r in oku(SONUC) if r["durum"] == "KAPI-GECTI"}  # başlangıç anındaki kapı-geçenler


YEDEK_TAVAN = {"n": 0, "max": 40}  # OmniRoute dışı (yedek zincir) çağrılar için sayısal tavan: en fazla 40


def llm_zincir():
    """OMNIROUTE_KEY varsa OmniRoute; yoksa doğrudan GROQ -> GEMINI -> OPENROUTER (:free model)."""
    import winreg  # arka süreçte (köprü dışı) kullanıcı env'i gelmeyebilir: HKCU\Environment'tan oku, değer yazdırılmaz
    with winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Environment") as hk:
        for n in ("OMNIROUTE_KEY", "GROQ_API_KEY", "GEMINI_API_KEY", "OPENROUTER_API_KEY"):
            if not os.environ.get(n):
                try: os.environ[n] = winreg.QueryValueEx(hk, n)[0]
                except OSError: pass
    e, z = os.environ.get, []
    if e("OMNIROUTE_KEY"):
        z += [("http://127.0.0.1:20128/v1/chat/completions", e("OMNIROUTE_KEY"), m, False) for m in ("ucretsiz-ozet2", "ucretsiz-groq")]
    if e("GROQ_API_KEY"):
        z.append(("https://api.groq.com/openai/v1/chat/completions", e("GROQ_API_KEY"), "llama-3.3-70b-versatile", True))
    if e("GEMINI_API_KEY"):
        z.append(("https://generativelanguage.googleapis.com/v1beta/openai/chat/completions", e("GEMINI_API_KEY"), "gemini-2.0-flash", True))
    if e("OPENROUTER_API_KEY"):
        z += [("https://openrouter.ai/api/v1/chat/completions", e("OPENROUTER_API_KEY"), m, True) for m in ("google/gemma-4-31b-it:free", "google/gemma-4-26b-a4b-it:free")]
    return z


def llm(istem):
    for url, key, model, yedek in llm_zincir():
        if yedek and YEDEK_TAVAN["n"] >= YEDEK_TAVAN["max"]:
            continue
        try:
            if yedek: YEDEK_TAVAN["n"] += 1
            req = urllib.request.Request(url, method="POST",
                data=json.dumps({"model": model, "max_tokens": 700, "temperature": 0, "messages": [{"role": "user", "content": istem}]}).encode(),
                headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json", "User-Agent": "Mozilla/5.0"})
            y = json.loads(urllib.request.urlopen(req, timeout=90).read())["choices"][0]["message"]["content"] or ""
            if y.strip():
                return y
        except urllib.error.HTTPError as e:
            if e.code == 429 and yedek and YEDEK_TAVAN["n"] < YEDEK_TAVAN["max"]:  # :free model geçici kota: bir kez bekle, aynı modeli yeniden dene
                time.sleep(30)
                try:
                    YEDEK_TAVAN["n"] += 1
                    y = json.loads(urllib.request.urlopen(req, timeout=90).read())["choices"][0]["message"]["content"] or ""
                    if y.strip():
                        return y
                except Exception:
                    pass
            continue
        except Exception:
            continue
    return None


def disk_ok():
    return shutil.disk_usage("C:/").free > DISK_ALT


def ram_yuzde():
    import ctypes

    class MS(ctypes.Structure):
        _fields_ = [("l", ctypes.c_ulong), ("yuzde", ctypes.c_ulong)] + [(f"x{i}", ctypes.c_ulonglong) for i in range(7)]
    m = MS(); m.l = ctypes.sizeof(MS)
    ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(m))
    return m.yuzde


def ram_bekle():
    while ram_yuzde() >= RAM_TAVAN:
        time.sleep(10)


def dur_mu():
    """Disk C: < 32 GB ise True: yeni iş başlatılmaz, kalemler tsv'ye yazılmaz (sonraki koşu devam eder)."""
    return not disk_ok()


# ---------- GitHub / güvenlik ----------
def gh_meta(repo):
    c, o = run(["gh", "api", f"repos/{repo}", "--jq", "[.archived,.disabled,.size,.description]|@json"], 60)
    if c:
        return None
    try:
        return json.loads(o)
    except ValueError:
        return None


def klonla(repo):
    d = KLON / repo.replace("/", "__")
    if d.exists() and any(d.iterdir()):
        if (d / ".git").exists():  # önceki yarım checkout (longpaths) varsa çalışma ağacını HEAD'e geri getir
            run(["git", "config", "--global", "core.longpaths", "true"], 30)
            run(["git", "-C", str(d), "restore", "--source=HEAD", ":/"], 300)
        return d, ""
    if not disk_ok():
        return None, "DISK-ALT-SINIR"
    run(["git", "config", "--global", "core.longpaths", "true"], 30)  # Windows uzun yol: checkout hatası önlemi
    c, o = run(["git", "clone", "--depth", "1", "--single-branch", "--filter=blob:limit=100m", "-q", f"https://github.com/{repo}.git", str(d)], 900 if TUR2 else 240)
    return (d, "") if c == 0 else (None, o[-150:])


def betik_tara(metin):
    """yaşam-döngüsü betik içeriği: regex + gitleaks (+ semgrep p/secrets); şüphe -> neden döner."""
    if SUPHE.search(metin):
        return "şüpheli desen: " + SUPHE.search(metin).group(0)[:50]
    with tempfile.TemporaryDirectory() as t:
        (Path(t) / "betik.txt").write_text(metin, encoding="utf-8")
        c, o = run(["gitleaks", "detect", "--no-git", "-s", t, "--redact", "--no-banner", "-l", "error"], 60)
        if c == 1:
            return "gitleaks: sır bulundu"
        c2, o2 = run(["semgrep", "--config", "p/secrets", "--quiet", "--error", t], 120)
        if c2 == 1:
            return "semgrep p/secrets bulgusu"
    return ""


def repo_betikleri(d):
    m = ""
    pj = d / "package.json"
    if pj.exists():
        try:
            sc = json.loads(pj.read_text(encoding="utf-8", errors="ignore")).get("scripts", {})
            for k in ("preinstall", "install", "postinstall", "prepare"):
                if k in sc:
                    m += sc[k] + "\n"
                    for f in re.findall(r"node\s+([\w./\\-]+\.m?c?js)", sc[k]):
                        p = d / f
                        if p.exists() and p.stat().st_size < 200000:
                            m += p.read_text(encoding="utf-8", errors="ignore") + "\n"
        except Exception:
            pass
    for f in ("setup.py", "install.sh", "install.ps1"):
        p = d / f
        if p.exists() and p.stat().st_size < 200000:
            m += p.read_text(encoding="utf-8", errors="ignore")[:60000] + "\n"
    return m


OZ = {r["kalem"]: r for r in oku(KOK / "ana-liste-ozellik.tsv")}


def aday_kapisi(kalem, repo, aciklama):
    c, rd = run(["gh", "api", f"repos/{repo}/readme", "-H", "Accept: application/vnd.github.raw"], 60)
    rd = "\n".join(rd.splitlines()[:40])[:3500] if c == 0 else "(README yok)"
    c2, mf = run(["gh", "api", f"repos/{repo}/contents", "--jq", "[.[].name][:40]|join(\", \")"], 60)  # büyük repolarda tam ağaç değil: kök dosya adları (manifest özeti)
    rd += "\nKÖK DOSYALAR: " + (mf[:400] if c2 == 0 else "(alınamadı)")
    oz = OZ.get(kalem, {}).get("ozellik", "")[:400]
    y = llm(f"[{kalem}|{repo}] Aşağıdaki GitHub reposu, 'kalem' adlı aracın/skill'in kendisi mi? Yalnız ilk kelime EVET ya da HAYIR yaz, sonra tek cümle neden.\n"
            f"KALEM: {kalem}\nÖZELLİK NOTU: {oz}\nREPO: {repo}\nAÇIKLAMA: {aciklama}\nREADME:\n{rd}")
    if y is None:
        return None, "LLM-ERISILEMEDI"
    return ("EVET" in y.upper()[:12]), y[:120]


# ---------- kurulum ----------
NPMBIN = Path.home() / "AppData/Roaming/npm"
VENVK = Path.home() / ".venvs/ana-liste312"  # yedek venv'ler (3.12 / 3.13), paket başına alt dizin
ALIAS = {"ripgrep": "rg", "neovim": "nvim", "opentofu": "tofu"}  # repo adı -> exe adı
WINRE = re.compile(r"(?<![a-z])(win(dows)?[-_.]?(x86_64|amd64|x64|64)|win64|windows)|(x86_64|amd64|x64)[-_.]?(pc-)?(win|windows)(?![a-z])", re.I)  # darwin içindeki "win" eşleşmesin
ASSET_ATLA = re.compile(r"arm|aarch|sha256|sbom|checksum|\.sig$|\.asc$|\.pem$|\.sha|\.msi$|\.deb$|\.rpm$|\.json$|\.txt$|source|src", re.I)


def yol_bul(e):
    """PATH + npm + uv bin dizinlerinde tam yol (arka işçinin PATH'i npm'i içermeyebilir)."""
    return shutil.which(str(e), path=os.pathsep.join([os.environ.get("PATH", ""), str(NPMBIN), str(BIN)])) or str(e)


def dogrula(exe):
    adaylar = exe if isinstance(exe, list) else [exe]
    ek = []
    for e in adaylar:
        b = Path(str(e)).name.removesuffix(".cmd").removesuffix(".exe")
        ek += [e, b, b + ".cmd", b + ".exe", b.lower(), b.replace("_", "-"), b.replace("-", "_")]
    o = ""
    for e in dict.fromkeys(ek):
        p = yol_bul(e)
        if not Path(p).exists():
            continue  # PATH/npm/uv bin'de yok: bekleme yok
        for a in ("--version", "--help", "-h"):
            c, o = run([p, a], 25)
            if c == 0 and o:
                return True, f"{p} {a}: {o.splitlines()[0][:70]}"
    return False, f"kuruldu; komut bulunamadı/doğrulanamadı ({', '.join(map(str, adaylar))[:60]}): {o[:60]}"


def npm_kok(o):
    ls = [re.sub(r"^npm (error|ERR!)\s*", "", l.strip()) for l in o.splitlines() if re.match(r"\s*npm (error|ERR!)", l) and "complete log" not in l and "A complete" not in l]
    return " | ".join(ls[:3])[:200] if ls else o[-150:]


def exe_ara(kalem, ad):
    for n in dict.fromkeys([ALIAS.get(ad.lower(), ""), ad.lower(), kalem.lower().replace(" ", "-")]):
        p = shutil.which(n) if n else None
        if p:
            return p
    return ""


def uv_zincir(src, ad, spec=False):
    """uv tool install: python 3.12 -> 3.13 (-> pip için --no-build ön-derlenmiş wheel) -> venv + import doğrulama."""
    son = ""
    for py in ("3.12", "3.13"):
        a = ["uv", "tool", "install", "--python", py, "--force", str(src)]
        for ek in ([[]] + ([["--no-build"]] if spec else [])):
            c, o = run(a[:-1] + ek + [str(src)], TKALEM)
            if c == 0:
                exe = re.findall(r"^\s*- ([\w.-]+?)(?:\.exe)?\s*$", o, re.M) or [ad]
                ok, n = dogrula(exe)
                return ("KURULDU" if ok else "KURULDU-DOGRULANMADI"), f"uv tool py{py}{' --no-build' if ek else ''}: {n}"
            son = o
    dur, n = paket_py_kur(str(src), ad)
    if dur == "KURULDU":
        return dur, f"uv tool başarısız ({kok(son)[:80]}); venv: {n}"
    return "HATA", f"uv tool: {kok(son)[:90]} || venv: {n[:80]}"


def gh_cli_kur(d, repo, kalem="", buyuk=0):
    ad = repo.split("/")[1]
    var = lambda f: d is not None and (d / f).exists()
    if var("pyproject.toml"):
        with KURKILIT: return uv_zincir(d, ad)
    if var("package.json"):
        with NPMKILIT: c, o = run(["npm.cmd", "i", "-g", str(d)], TKALEM)
        if c: return "HATA", "npm -g: " + npm_kok(o)
        try:
            pj = json.loads((d / "package.json").read_text(encoding="utf-8"))
            b = pj.get("bin")
            exe = list(b) if isinstance(b, dict) else ([pj.get("name", ad).split("/")[-1]] if b else [])
        except Exception:
            exe = [ad]
        if not exe:
            return "HATA", "kuruldu ama package.json 'bin' tanımlamıyor (kütüphane/monorepo kökü): çalıştırılabilir komut yok"
        ok, n = dogrula([e + ".cmd" for e in exe])
        return ("KURULDU" if ok else "KURULDU-DOGRULANMADI"), n
    p = exe_ara(kalem, ad)
    if p:
        return "ZATEN", f"PATH'te var (where {Path(p).stem}): {p}"
    # ikili: GitHub release (Windows x64)
    c, o = run(["gh", "release", "view", "-R", repo, "--json", "assets", "--jq", ".assets[].name"], 60)
    adlar = o.splitlines() if c == 0 else []
    ass = sorted([x for x in adlar if WINRE.search(x) and not ASSET_ATLA.search(x) and x.lower().endswith((".zip", ".exe", ".tar.gz", ".tgz"))], key=lambda x: (not x.lower().endswith(".zip"), x))
    if not ass:
        if var("Cargo.toml"):
            with KURKILIT: c, o = run(["cargo", "install", "--locked", "--path", str(d)], 900)
            if c == 0:
                ok, n = dogrula([ad]); return ("KURULDU" if ok else "KURULDU-DOGRULANMADI"), "cargo install: " + n
        return "KURULUM-YOLU-YOK", f"pyproject/package.json/Cargo yok; win-x64 release asset yok (asset {len(adlar)}: {', '.join(adlar[:3])[:80]})" + (f"; repo {buyuk // 1024} MB" if buyuk else "")
    with KURKILIT, tempfile.TemporaryDirectory() as t:
        c, o = run(["gh", "release", "download", "-R", repo, "-p", ass[0], "-D", t], TKALEM)
        if c: return "HATA", "release indirilemedi: " + o[-100:]
        f = next(q for q in Path(t).iterdir() if q.is_file())
        x = Path(t) / "x"; x.mkdir()
        if f.suffix == ".exe":
            shutil.copy2(f, x / f.name)
        else:
            shutil.unpack_archive(f, x)
        exes = sorted(x.rglob("*.exe"), key=lambda q: (ad.lower() not in q.stem.lower(), len(q.parts)))
        if not exes:
            return "HATA", f"release içinde exe yok: {ass[0]} içeriği: {[q.name for q in list(x.rglob('*'))[:5]]}"
        if re.search(r"setup|install", exes[0].name, re.I):  # GUI kurulum programı: çalıştırılmaz, ~/.local/bin'e konmaz
            park = Path(__file__).resolve().parents[1] / ".kos/kopru/park"; park.mkdir(parents=True, exist_ok=True)
            shutil.copy2(exes[0], park / (exes[0].name + ".kurulum"))
            return "KURULUM-YOLU-ELLE", f"GUI kurulum programı ({exes[0].name}) park/ içinde; sessiz bayrak doğrulanmadı, çalıştırılmadı; elle kurulur"
        BIN.mkdir(parents=True, exist_ok=True)
        hedef = BIN / exes[0].name
        if hedef.exists(): return "ZATEN", str(hedef)
        shutil.copy2(exes[0], hedef)
    ok, n = dogrula(str(hedef))
    return ("KURULDU" if ok else "KURULDU-DOGRULANMADI"), n


def import_adlari(py, dist):
    kod = ("import importlib.metadata as m,sys\n"
           "d=m.distribution(sys.argv[1])\n"
           "t=(d.read_text('top_level.txt') or '').split()\n"
           "r=[str(f).replace(chr(92),'/').split('/')[0] for f in (d.files or [])]\n"
           "r=[x[:-3] if x.endswith('.py') else x for x in r]\n"
           "print(' '.join(dict.fromkeys(t+[x for x in r if x.isidentifier() and not x.startswith('_') and x not in ('bin','Scripts','include','share')])))")
    c, o = run([py, "-c", kod, dist], 30)
    return o.split() if c == 0 and o else []


def paket_py_kur(spec, ad=""):
    """paket başına venv (3.12, ABI uyumsuzsa 3.13) + import adı = dist RECORD/top_level.txt'ten."""
    yol = Path(spec).exists()
    adi = ad or Path(spec).name
    dist = re.split(r"[=<>\[]", Path(spec).name)[0]
    if yol:
        try:
            import tomllib
            dist = tomllib.loads((Path(spec) / "pyproject.toml").read_text(encoding="utf-8"))["project"]["name"]
        except Exception:
            dist = ""
    son = ""
    for pv in ("3.12", "3.13"):
        venv = VENVK / (re.sub(r"[^\w.-]", "_", adi) + "-" + pv)
        if not venv.exists():
            c, o = run(["uv", "venv", "--python", pv, str(venv)], 120)
            if c: son = o; continue
        py = str(venv / "Scripts/python.exe")
        c, o = run(["uv", "pip", "install", "--python", py, spec] if yol else ["uv", "pip", "install", "--python", py, "--only-binary", ":all:", spec], TKALEM)
        if c:
            son = o
            if re.search(r"ABI tag|no wheel|cp3\d+", o): continue  # bu python için wheel yok: sonraki sürüm
            return "HATA", "pip: " + kok(o)
        if yol and not dist:
            m = re.search(r"^ \+ ([\w.-]+)==\S+ \(from file", o, re.M)
            dist = m.group(1) if m else ""
        cand = (import_adlari(py, dist) if dist else []) + [re.sub(r"\W", "_", adi).lower()]
        for im in dict.fromkeys(cand[:8]):
            c, o2 = run([py, "-c", f"import {im}"], 90)
            if c == 0: return "KURULDU", f"venv py{pv}: import {im} ok"
        return "HATA", f"import başarısız (dist={dist}; denenen {cand[:4]}): {o2[-60:]}"
    return "HATA", "pip: " + kok(son)


def npm_dogrula(ad):
    """node_modules/<ad>: bin varsa bin --version; yoksa import.meta.resolve (modülü yürütmez); yalnız tip paketiyse d.ts kanıtı."""
    pj = NPMDIR / "node_modules" / ad / "package.json"
    if not pj.exists(): return False, "node_modules'ta paket yok"
    j = json.loads(pj.read_text(encoding="utf-8", errors="ignore"))
    b = j.get("bin")
    for e in (list(b) if isinstance(b, dict) else ([ad.split("/")[-1]] if b else [])):
        sh = NPMDIR / "node_modules/.bin" / (e + ".cmd")
        if sh.exists():
            for a in ("--version", "--help"):
                c, o = run([str(sh), a], 40)
                if c == 0 and o: return True, f"bin {e} {a}: {o.splitlines()[0][:60]}"
    c, o = run(["node", "--input-type=module", "-e", f"console.log(import.meta.resolve('{ad}'))"], 40, cwd=str(NPMDIR))
    if c == 0: return True, "import.meta.resolve ok: " + o[-60:]
    if j.get("types") or j.get("typings") or (pj.parent / "index.d.ts").exists():
        return True, "yalnız tip paketi (d.ts var, JS girişi yok)"
    return False, "resolve: " + o[-100:]


def npm_betik_kapisi(paket):
    c, o = run(["npm.cmd", "view", paket, "scripts", "--json"], 60)
    if c or not o.strip().startswith("{"):
        return ""
    sc = json.loads(o)
    m = "\n".join(sc.get(k, "") for k in ("preinstall", "install", "postinstall"))
    return betik_tara(m) if m.strip() else ""


def isle(r):
    k, sinif, kay = r["kalem"], r["sinif"], r["kaynak"]
    tur, _, ad = kay.partition(":")
    try:
        if tur == "gh":
            meta = gh_meta(ad)
            if meta is None: return yaz(k, sinif, kay, "HATA", "", "repo erişilemedi/silinmiş")
            if meta[0] or meta[1]: return yaz(k, sinif, kay, "GUVENLIK-RED", "", "repo arşivlenmiş/devre dışı")
            if r["sonuc"] == "ADAY" and k not in KAPIGECTI:  # kapıdan geçmiş kalem için LLM kapısı yeniden koşmaz (OmniRoute anahtarı yoksa HATA'ya düşüyordu)
                ok, n = aday_kapisi(k, ad, meta[3] or "")
                if ok is None: return yaz(k, sinif, kay, "HATA", "", n)
                if not ok: return yaz(k, sinif, kay, "YANLIS-ESLESME", "", n)
            if meta[2] > (3000000 if TUR2 else 400000):
                if sinif == "CLI":  # büyük repo klonlanmaz: yalnız hazır release/PATH yolu
                    dur, n = gh_cli_kur(None, ad, k, meta[2]); return yaz(k, sinif, kay, dur, "", n)
                return yaz(k, sinif, kay, "HATA", "", f"repo çok büyük ({meta[2] // 1024} MB), klonlanmadı")
            d, h = klonla(ad)
            if d is None: return yaz(k, sinif, kay, "HATA", "", "klon: " + h)
            neden = betik_tara(repo_betikleri(d)) if repo_betikleri(d).strip() else ""
            if neden: return yaz(k, sinif, kay, "GUVENLIK-RED", str(d), neden)
            if KAPI: return yaz(k, sinif, kay, "KAPI-GECTI", str(d), "kurulum onay bekliyor")
            if sinif == "SKILL":
                with SKILLKILIT:
                    n0 = len(G.CIK); G.skill_kur(d, ad); yeni = G.CIK[n0:]
                dur = [c for c in yeni if c[3] in ("KURULDU", "ZATEN-KURULU")]
                if dur:
                    with KILIT, open(ADAYTSV, "a", encoding="utf-8", newline="") as f:
                        w = csv.writer(f, delimiter="\t"); [w.writerow([k, ad, c[2], c[3]]) for c in dur]
                    return yaz(k, sinif, kay, "KURULDU" if any(c[3] == "KURULDU" for c in dur) else "ZATEN", str(d), f"{len(dur)} skill")
                return yaz(k, sinif, kay, "HATA", str(d), "SKILL.md bulunamadı/okunamadı: " + (yeni[0][3] if yeni else "boş"))
            if sinif == "CLI":
                dur, n = gh_cli_kur(d, ad, k); return yaz(k, sinif, kay, dur, str(d), n)
            if sinif == "PAKET":
                if (d / "pyproject.toml").exists() or (d / "setup.py").exists():
                    with KURKILIT: dur, n = paket_py_kur(str(d))
                    return yaz(k, sinif, kay, dur, str(d), n)
                if (d / "package.json").exists():
                    NPMDIR.mkdir(exist_ok=True)
                    with NPMKILIT: c, o = run(["npm.cmd", "i", "--prefix", str(NPMDIR), str(d)], TKALEM)
                    if c: return yaz(k, sinif, kay, "HATA", str(d), "npm: " + npm_kok(o))
                    try: pn = json.loads((d / "package.json").read_text(encoding="utf-8")).get("name", "")
                    except Exception: pn = ""
                    ok, n = npm_dogrula(pn) if pn else (True, "npm install ok (adsız paket)")
                    return yaz(k, sinif, kay, "KURULDU" if ok else "HATA", str(d), n)
                return yaz(k, sinif, kay, "KURULDU", str(d), "klonlandı (kaynak; kurulum betiği yok)")
            return yaz(k, sinif, kay, "KURULDU", str(d), "klonlandı")
        if tur == "npm":
            neden = npm_betik_kapisi(ad)
            if neden: return yaz(k, sinif, kay, "GUVENLIK-RED", "", neden)
            if KAPI: return yaz(k, sinif, kay, "KAPI-GECTI", "", "kurulum onay bekliyor")
            if sinif == "CLI":
                with NPMKILIT: c, o = run(["npm.cmd", "i", "-g", ad], TKALEM)
                if c: return yaz(k, sinif, kay, "HATA", "", "npm -g: " + npm_kok(o))
                c, b = run(["npm.cmd", "view", ad, "bin", "--json"], 60)
                try: bj = json.loads(b); exe = list(bj) if isinstance(bj, dict) else [ad.split("/")[-1]]
                except Exception: exe = [ad.split("/")[-1]]
                ok, n = dogrula([e + ".cmd" for e in exe]); return yaz(k, sinif, kay, "KURULDU" if ok else "KURULDU-DOGRULANMADI", "", n)
            if sinif == "SKILL":
                d = KLON / ("npm__" + ad.replace("/", "_").replace("@", ""))
                if not d.exists():
                    with tempfile.TemporaryDirectory() as t:
                        c, o = run(["npm.cmd", "pack", ad, "--pack-destination", t, "--ignore-scripts"], 180)
                        if c: return yaz(k, sinif, kay, "HATA", "", "npm pack: " + o[-100:])
                        shutil.unpack_archive(next(Path(t).glob("*.tgz")), d)
                with SKILLKILIT: n0 = len(G.CIK); G.skill_kur(d, "npm/" + ad); yeni = G.CIK[n0:]
                dur = [c for c in yeni if c[3] in ("KURULDU", "ZATEN-KURULU")]
                return yaz(k, sinif, kay, "KURULDU" if dur else "HATA", str(d), f"{len(dur)} skill")
            NPMDIR.mkdir(exist_ok=True)
            with NPMKILIT: c, o = run(["npm.cmd", "i", "--prefix", str(NPMDIR), ad], TKALEM)
            if c: return yaz(k, sinif, kay, "HATA", "", "npm: " + npm_kok(o))
            ok, n = npm_dogrula(ad)
            return yaz(k, sinif, kay, "KURULDU" if ok else "HATA", "", n)
        if tur == "pip":
            c, o = run(["curl", "-s", f"https://pypi.org/pypi/{ad}/json"], 60)
            try: pj = json.loads(o)
            except ValueError: return yaz(k, sinif, kay, "HATA", "", "PyPI cevap yok")
            if any(x.get("yanked") for x in pj.get("urls", [])): return yaz(k, sinif, kay, "GUVENLIK-RED", "", "PyPI yanked")
            if not any(x["packagetype"] == "bdist_wheel" for x in pj.get("urls", [])):
                return yaz(k, sinif, kay, "GUVENLIK-RED", "", "yalnız sdist (kurulumda setup.py yürütülür), atlandı")
            if KAPI: return yaz(k, sinif, kay, "KAPI-GECTI", "", "kurulum onay bekliyor")
            if sinif == "CLI":
                with KURKILIT: dur, n = uv_zincir(ad, ad, spec=True)
                return yaz(k, sinif, kay, dur, "", n)
            with KURKILIT: dur, n = paket_py_kur(ad)
            return yaz(k, sinif, kay, dur, "", n)
        return yaz(k, sinif, kay, "HATA", "", f"bilinmeyen kaynak türü {tur!r}")
    except Exception as e:
        yaz(k, sinif, kay, "HATA", "", f"istisna {type(e).__name__}: {e}")


# ---------- MODEL ----------
def model_isle(r):
    k, kay = r["kalem"], r["kaynak"]
    tur, _, ad = kay.partition(":")
    if tur != "hf":
        return False
    if not ad.strip():
        return yaz(k, "MODEL", kay, "BULUNAMADI-2", "", "kaynak boş") or True
    try:
        c, o = run(["curl", "-sL", f"https://huggingface.co/api/models/{ad}?blobs=true"], 60)
        j = json.loads(o)
        if "siblings" not in j: return yaz(k, "MODEL", kay, "BULUNAMADI-2", "", "HF'de yok: " + o[:60]) or True
        bayt = sum(s.get("size") or 0 for s in j["siblings"])
        gb = bayt / 2**30
        if bayt > 2 * 2**30:
            ONAY.parent.mkdir(parents=True, exist_ok=True)
            with KILIT, open(ONAY, "a", encoding="utf-8", newline="") as f:
                w = csv.writer(f, delimiter="\t"); w.writerow([k, f"{gb:.2f}", (j.get("pipeline_tag") or "model") + " — " + (OZ.get(k, {}).get("ozellik", "")[:90])])
            return yaz(k, "MODEL", kay, "MODEL-ONAY", "", f"{gb:.2f} GB") or True
        if SAYAC["model_bayt"] + bayt > MODEL_TAVAN or not disk_ok():
            return yaz(k, "MODEL", kay, "HATA", "", f"koşu tavanı/disk sınırı ({gb:.2f} GB)") or True
        env = dict(os.environ); env["HF_HUB_DISABLE_PROGRESS_BARS"] = "1"
        c, o = run(["uv", "run", "--quiet", "--with", "huggingface_hub", "python", "-c",
                    f"from huggingface_hub import snapshot_download as s;print(s('{ad}'))"], 1800, env=env)
        if c: return yaz(k, "MODEL", kay, "HATA", "", "indirme: " + o[-120:]) or True
        SAYAC["model_bayt"] += bayt
        return yaz(k, "MODEL", kay, "KURULDU", o.splitlines()[-1], f"{gb:.2f} GB HF cache") or True
    except Exception as e:
        return yaz(k, "MODEL", kay, "HATA", "", f"istisna {e}") or True


# ---------- ikinci arama ----------
def ikinci(r):
    k, sinif = r["kalem"], r["sinif"]
    oz = OZ.get(k, {}).get("ozellik", "")[:300]
    y = llm(f"[{k}] Bu kalemin resmi/gerçek adını ve (varsa) GitHub 'sahip/repo', PyPI ya da npm paket adını yaz. Emin değilsen yalnız YOK yaz. Biçim: gh:sahip/repo | pypi:ad | npm:ad | YOK\nKALEM: {k} ({sinif})\nNOT: {oz}")
    if y is None: return yaz(k, sinif, "", "HATA", "", "LLM-ERISILEMEDI")
    m = re.search(r"\b(gh|pypi|npm):([\w@./-]+)", y)
    if not m: return yaz(k, sinif, "", "BULUNAMADI-2", "", "model öneri üretmedi")
    t, a = m.groups()
    kay = ("pip:" if t == "pypi" else t + ":") + a
    if t == "gh" and gh_meta(a) is None: return yaz(k, sinif, kay, "BULUNAMADI-2", "", "önerilen repo yok")
    if t == "pypi" and '"info"' not in run(["curl", "-s", f"https://pypi.org/pypi/{a}/json"], 30)[1][:200]: return yaz(k, sinif, kay, "BULUNAMADI-2", "", "PyPI'de yok")
    if t == "npm" and run(["npm.cmd", "view", a, "name"], 30)[0]: return yaz(k, sinif, kay, "BULUNAMADI-2", "", "npm'de yok")
    isle({"kalem": k, "sinif": sinif, "kaynak": kay, "sonuc": "ADAY"})  # ADAY kapısından geçer


def main():
    a = sys.argv
    if [x for x in a[1:] if x.startswith("--") and x not in BILINEN]:  # bilinmeyen bayrak (--help dahil) sessizce 'kur' fazına düşmesin
        sys.exit(f"bilinmeyen bayrak; geçerli: {sorted(BILINEN)}")
    arg = lambda s, v=None: a[a.index(s) + 1] if s in a else v
    faz, n, sc, kac = arg("--faz", "kur"), int(arg("--n", 10**9)), set(arg("--sinif", "SKILL,CLI,PAKET,MODEL").split(",")), int(arg("--is", 6))
    rows = oku(KOK / "kurulum-coz.tsv")
    bit = bitenler()
    if TUR2:
        son = {r["kalem"]: r for r in oku(SONUC)}
        TEKRAR = re.compile(r"çok büyük|klon|Timeout|zaman aşımı|uv tool|npm|pip:|--version/--help|istisna|release indirilemedi", re.I)
        tekrar = {k for k, r in son.items() if r["durum"] == "HATA" and TEKRAR.search(r["not"])}
        bit -= tekrar
        print("tur2 tekrar edilecek:", len(tekrar))
    if faz == "tohum":
        for r in rows:
            if r["kalem"] not in bit and r["sonuc"] == "BIZDE-SKILL":
                yaz(r["kalem"], r["sinif"], r["kaynak"], "ZATEN", r["yol"], "kurulum-coz: BIZDE")
    elif faz == "kur":
        todo = [r for r in rows if r["kalem"] not in bit and r["sinif"] in sc and r["sonuc"] in ("DOGRULANDI", "ADAY") and r["kaynak"][:3] in ("gh:", "npm", "pip") and (not KALEM or r["kalem"] in KALEM)][:n]
        with ThreadPoolExecutor(kac) as ex: list(ex.map(isle, todo))
        G.ayar_yaz()
    elif faz == "model":
        todo = [r for r in rows if r["kalem"] not in bit and r["sinif"] == "MODEL" and r["sonuc"] in ("DOGRULANDI", "MODEL-TURU") and r["kaynak"].startswith("hf:")][:n]
        for r in todo: model_isle(r)
    elif faz == "ikinci":
        todo = [r for r in rows if r["kalem"] not in bit and r["sonuc"] in ("BULUNAMADI", "MODEL-TURU")][:n]
        with ThreadPoolExecutor(kac) as ex: list(ex.map(ikinci, todo))
        G.ayar_yaz()
    elif faz == "kapsam":
        bit = {r["kalem"]: r for r in oku(SONUC)}
        for r in rows:
            if r["kalem"] not in bit:
                yaz(r["kalem"], r["sinif"], r["kaynak"], "BULUNAMADI-2" if r["sonuc"] in ("BULUNAMADI", "MODEL-TURU") else "HATA", "", f"kapsam: işlenmedi (kaynak={r['kaynak'][:30]})")
    from collections import Counter
    son = {r["kalem"]: r for r in oku(SONUC)}
    print(faz, Counter((r["sinif"], r["durum"]) for r in son.values()).most_common())


if __name__ == "__main__":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
    import faulthandler
    faulthandler.dump_traceback_later(240, repeat=True, file=sys.stderr)
    main()

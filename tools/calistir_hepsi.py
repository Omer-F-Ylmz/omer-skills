"""CALISTIR-HEPSI: mevcut klonları kur + duman çalıştır -> .kos/kopru/calistirma.tsv

Kipler (biri zorunlu):  --deneme N | --tam | --tekrar N
Güvenlik: silme yok (rm/rmtree/os.remove yok), push yok, clone yok; alt süreç stdin=DEVNULL,
öğe başına 600 sn, aşımda taskkill /T /F; çocuk ortamdan KEY/TOKEN/SECRET/... değişkenleri çıkarılır.
"""
import argparse, collections, csv, ctypes, json, os, random, re, shutil, subprocess, sys, tempfile, threading, time, tomllib
from concurrent.futures import ThreadPoolExecutor

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, ".kos", "kopru")
SCOPES = [
    ("v", r"C:\Projeler\_araclar\v"),
    ("ana1", r"C:\Users\pc\Desktop\araclar\ana-liste"),
    ("ana2", r"C:\Users\pc\Desktop\Claude ile yapılanlar\araclar\ana-liste"),
]
NPM_KALEM = r"C:\Projeler\_araclar\npm-kalem"
PIP_KALEM = r"C:\Projeler\_araclar\venv-kalem"
HEAD = ["yol", "remote", "tur", "kurulum_kmt", "calistirma_kmt", "rc", "durum", "kanit"]
MIN_FREE = 80e9  # CALISTIR-3: yeni kurulum için C: boş alan tabanı
PNPM_STORE = r"C:\Projeler\_araclar\pnpm-store"  # tek paylaşılan depo (aynı sürücü -> sert bağlantı)
AGIR_ML = r"C:\Projeler\_araclar\agir-ml"  # tek ağır-ml venv (torch CUDA, tf, transformers...)
NOWHEEL = ("vllm", "deepspeed", "xformers", "flash-attn")  # Windows tekerleği olmayanlar (ENGEL-PLATFORM)
ITEM_TIMEOUT = 600
RAM_MAX = 93
STOP = threading.Event()
LOG = os.path.join(OUT, "calistirma.log")
_lock = threading.Lock()


class Donma:
    """Süreç askıya alınınca (ram_kapi suspend) duvar saati akar ama iş yapılmaz; nabız boşluğu donma süresi sayılır."""
    TIK, ESIK = 1.0, 3.0

    def __init__(s, saat=time.monotonic):
        s.saat, s.toplam, s.son = saat, 0.0, saat()
        s.kilit = threading.Lock()

    def tik(s):
        with s.kilit:
            t = s.saat()
            bosluk = t - s.son
            if bosluk > s.ESIK:
                s.toplam += bosluk - s.TIK
            s.son = t

    def bayat(s):
        return s.saat() - s.son > s.ESIK

    def oku(s):
        if s.bayat():
            s.tik()
        return s.toplam

    def baslat(s):
        def dongu():
            while True:
                time.sleep(s.TIK)
                s.tik()
        threading.Thread(target=dongu, daemon=True, name="donma-nabiz").start()
        return s


DONMA = Donma()


def etkin_gecen(t0, d0, saat=time.monotonic, donma=None):
    """t0'dan beri geçen süre, askıda (donmuş) geçen kısım düşülerek."""
    donma = donma or DONMA
    return (saat() - t0) - (donma.oku() - d0)


# ---------- saf yardımcılar (testli) ----------
SENS = re.compile(r"(KEY|TOKEN|SECRET|PASSW|CREDENTIAL|AUTH|COOKIE)", re.I)


def child_env(base=None):
    e = {k: v for k, v in (base or os.environ).items() if not SENS.search(k) and not k.upper().startswith("ANTHROPIC")}
    e.update(GIT_TERMINAL_PROMPT="0", CI="1", NO_COLOR="1", FORCE_COLOR="0", PYTHONUTF8="1",
             UV_NO_PROGRESS="1", npm_config_fund="false", npm_config_audit="false", BROWSER="none")
    return e


RED = [(re.compile(p), r) for p, r in [
    (r"(?i)\b(sk|ghp|gho|ghs|xox[abp]|AIza|AKIA|hf)[-_]?[A-Za-z0-9_\-]{16,}", "<gizli>"),
    (r"\b[A-Fa-f0-9]{32,}\b", "<gizli>"),
    (r"(?i)bearer\s+\S+", "bearer <gizli>"),
    (r"(?i)\b(key|token|secret|password)\s*[=:]\s*\S+", r"\1=<gizli>"),
]]
ANSI = re.compile(r"\x1b\[[0-9;?]*[A-Za-z]")


def redact(s):
    for rx, r in RED:
        s = rx.sub(r, s)
    return s


def last_line(out, n=300):
    ls = [l.strip() for l in ANSI.sub("", out).splitlines() if l.strip()]
    if not ls:
        return ""
    err = [l for l in ls[-12:] if re.search(r"(?i)\berror|failed|cannot|not found|no such|undefined|panic", l) and "BACKTRACE" not in l]
    return redact(err[-1] if err else ls[-1])[:n]  # son 1 satır; son satır gürültüyse son hata satırı


ENVN = re.compile(r"\b([A-Z][A-Z0-9]+(?:_[A-Z0-9]+)*_(?:API_KEY|KEY|TOKEN|SECRET|ACCESS_TOKEN|PASSWORD))\b")
MISS = ("not set", "missing", "required", "undefined", "not found", "must be set", "is not defined",
        "please set", "environment variable", "not configured", "is empty")
ACCT = re.compile(r"(?i)(please (log ?in|sign ?in)|not (logged|signed) in|login required|authentication required|"
                  r"could not read username|authentication failed|sign in to continue|unauthorized)")


def classify(out):
    """Başarısız çıktıdan engel türü: (durum, kanit) ya da None. Yalnız AD döner, değer asla."""
    low = out.lower()
    names = sorted(set(ENVN.findall(out)))
    if names and any(m in low for m in MISS):
        return "ENGEL-ANAHTAR", "eksik env: " + ",".join(names[:5])
    if re.search(r"api[ _-]?key", low) and re.search(r"required|missing|not set|invalid|provide", low):
        return "ENGEL-ANAHTAR", "api key gerekli (ad bilinmiyor)"
    if ACCT.search(out):
        return "ENGEL-HESAP", last_line(out)
    return None


MODNF = re.compile(r"No module named '([^']+)'")
BUILDFAIL = re.compile(r"(?i)Failed to build|Build failures|error: subprocess-exited-with-error")
IMP2PIP = {"serial": "pyserial", "cv2": "opencv-python", "yaml": "pyyaml", "PIL": "pillow", "sklearn": "scikit-learn",
           "bs4": "beautifulsoup4", "google.protobuf": "protobuf", "grpc": "grpcio", "dotenv": "python-dotenv",
           "dateutil": "python-dateutil", "attr": "attrs", "jwt": "pyjwt", "OpenSSL": "pyopenssl", "Crypto": "pycryptodome",
           "skimage": "scikit-image", "usb": "pyusb", "magic": "python-magic", "zmq": "pyzmq", "docx": "python-docx",
           "pptx": "python-pptx", "fitz": "pymupdf", "git": "gitpython", "win32api": "pywin32", "win32com": "pywin32",
           "wx": "wxpython", "Bio": "biopython", "lxml": "lxml", "psycopg2": "psycopg2-binary", "MySQLdb": "mysqlclient"}


def import_to_pip(name):
    return IMP2PIP.get(name) or IMP2PIP.get(name.split(".")[0])


def classify_modnf(out):
    """ModuleNotFoundError çözülemediyse engel: eksik modül adı yazılır."""
    m = MODNF.search(out)
    if not m:
        return None
    p = import_to_pip(m.group(1))
    return "ENGEL-BAGIMLILIK", "eksik modül: %s%s" % (m.group(1), " (pip: %s)" % p if p else " (pip adı bilinmiyor)")


def classify_build(out):
    """Derleme/araç eksikleri: eksik aracın adı kanıta yazılır."""
    for rx, msg in ((r"Microsoft Visual C\+\+ [\d.]+ or greater|vcvarsall|Unable to find vcvars|MSVC|cl\.exe|link\.exe", "eksik: MSVC Build Tools (cl.exe)"),
                    (r"pg_config|could not determine PostgreSQL version", "eksik: PostgreSQL (pg_config)"),
                    (r"Required uv version `([^`]+)` does not match", "eksik: uv sürümü (gerekli %s)"),
                    (r"(?i)cmake must be installed|CMake configuration failed|Could not find cmake", "eksik: cmake/derleyici"),
                    (r"(?i)can't find Rust compiler|cargo.*not found|rustc.*not found", "eksik: rustc/cargo")):
        m = re.search(rx, out)
        if m:
            return "ENGEL-DERLEYICI", msg % m.group(1) if "%s" in msg else msg
    return None


WEAK = re.compile(r"rc=0 \(çıktı yok\)|çalıştırılacak giriş yok|exe yok \(kütüphane\)|kök paket main değil")


def is_weak(row):
    """CALISTI ama kanıt boş/anlamsız -> ZAYIF."""
    return row.get("durum") == "CALISTI" and (not (row.get("kanit") or "").strip() or bool(WEAK.search(row["kanit"])))


def dist_modules(di):
    """dist-info dizininden içe aktarılabilir üst modüller: top_level.txt, yoksa RECORD."""
    rd = lambda f: open(os.path.join(di, f), encoding="utf-8", errors="replace").read() if os.path.exists(os.path.join(di, f)) else ""
    ok = lambda s: re.match(r"^[A-Za-z_]\w*(\.[A-Za-z_]\w*)*$", s)
    mods = [m.strip() for m in rd("top_level.txt").splitlines() if ok(m.strip())]
    if mods:
        return list(dict.fromkeys(mods))
    paths = [l.split(",")[0].replace("\\", "/") for l in rd("RECORD").splitlines() if l.strip()]
    ps = set(paths)
    for p in paths:
        parts = p.split("/")
        if p.startswith("..") or "dist-info" in p or ".data" in p or "__pycache__" in p or parts[0] == "Scripts":
            continue
        s = parts[0].split(".")[0]
        if len(parts) > 1 and parts[0] + "/__init__.py" not in ps and len(parts) > 2 and parts[0] + "/" + parts[1] + "/__init__.py" in ps:
            s = parts[0] + "." + parts[1]
        if ok(s):
            mods.append(s)
    return list(dict.fromkeys(mods))


LICFILES = ("LICENSE", "LICENSE.md", "LICENSE.txt", "LICENCE", "COPYING", "LICENSE-MIT", "LICENSE-APACHE")


def license_kind(d):
    for f in LICFILES:
        try:
            t = open(os.path.join(d, f), encoding="utf-8", errors="replace").read(4000).lower()
        except OSError:
            continue
        if "apache license" in t: return "apache"
        if "mit license" in t or "permission is hereby granted, free of charge" in t: return "mit"
        if "redistribution and use" in t: return "bsd"
        if "isc license" in t: return "isc"
        if "unlicense" in t or "cc0" in t: return "pd"
        return "other"
    return ""


SKILLS_DIR = os.path.expanduser("~/.claude/skills")
SKILL_MAX = 20e6


def _tree_size(p):
    return sum(os.path.getsize(os.path.join(r, f)) for r, ds, fs in os.walk(p) if ".git" not in r for f in fs)


def install_skills(repo, dest, known=None):
    """repo içindeki geçerli SKILL.md klasörlerini dest'e kopyalar. Ezme/silme yok: ad çakışırsa `<repo>-<ad>` öneki.
    Dönen: dest'te bulunan (yeni ya da aynı içerikli) klasör adları."""
    known = skill_names() if known is None else known
    rb, got, seen = os.path.basename(repo.rstrip("\\/")), [], 0
    for r, ds, fs in os.walk(repo):
        ds[:] = [x for x in ds if x not in ("node_modules", ".git")]
        if r[len(repo):].count(os.sep) >= 3:
            ds[:] = []
        if "SKILL.md" not in fs or seen >= 60:
            continue
        seen += 1
        sm = os.path.join(r, "SKILL.md")
        fm = frontmatter(sm)
        if not fm or _tree_size(r) > SKILL_MAX:
            continue
        base = os.path.basename(r) if os.path.normcase(r) != os.path.normcase(repo) else rb
        same = os.path.join(dest, base, "SKILL.md")
        if os.path.exists(same) and open(same, "rb").read() == open(sm, "rb").read():
            got.append(base)
            continue
        name = base
        if os.path.exists(os.path.join(dest, base)) or fm in known:
            name = "%s-%s" % (rb, base)
        tgt = os.path.join(dest, name)
        if os.path.exists(tgt):  # önceki koşuda önekle kurulmuş (frontmatter değişti, içerik karşılaştırılamaz)
            got.append(name)
            continue
        shutil.copytree(r, tgt, ignore=shutil.ignore_patterns(".git", "node_modules", "__pycache__"))
        if name != base:  # ad çakışması: frontmatter adı da önekle, iki skill aynı adı taşımasın
            t = open(os.path.join(tgt, "SKILL.md"), encoding="utf-8-sig").read()
            open(os.path.join(tgt, "SKILL.md"), "w", encoding="utf-8", newline="").write(
                re.sub(r"^name:\s*.+$", "name: " + name, t, count=1, flags=re.M))
        got.append(name)
    return got


HEAVY = re.compile(r"(?i)(?<![\w-])(torch|torchvision|torchaudio|tensorflow(?:-gpu)?|jaxlib|vllm|deepspeed|"
                   r"flash[-_]attn|xformers|bitsandbytes|paddlepaddle|"
                   r"nvidia-(?:cuda|cudnn|cublas|cufft|curand|cusolver|cusparse|nccl|nvtx|nvjitlink)[a-z0-9-]*)(?![\w-])")  # nvidia-ml-py gibi küçük paketler ağır değil


def heavy(d):
    for f in ("requirements.txt", "pyproject.toml", "setup.py", "setup.cfg"):
        try:
            m = HEAVY.search(open(os.path.join(d, f), encoding="utf-8", errors="replace").read(200000))
        except OSError:
            continue
        if m:
            return m.group(1).lower()
    return ""


SKIPSUB = {"node_modules", ".git", "docs", "doc", "examples", "example", "test", "tests", ".venv", "__pycache__", ".github"}
RUNNABLE = ("npm", "py", "go", "rust", "cmake", "make", "java", "dotnet", "ruby", "swift", "src")
SRCEXT = {".c", ".cc", ".cpp", ".cxx", ".sh", ".bash", ".ps1", ".php", ".rb", ".pl", ".lua", ".java", ".cs", ".kt", ".swift", ".py", ".js", ".mjs"}
HARDSKIP = {"node_modules", ".git", ".venv", "__pycache__", ".github"}  # docs/examples/tests altındaki kod da koddur


def kinds_in(d):
    try:
        n = set(os.listdir(d))
    except OSError:
        return []
    k = []
    if "package.json" in n: k.append("npm")
    if n & {"pyproject.toml", "requirements.txt", "setup.py", "setup.cfg"}: k.append("py")
    if "Cargo.toml" in n: k.append("rust")
    if "go.mod" in n: k.append("go")
    if "CMakeLists.txt" in n: k.append("cmake")
    if n & {"Makefile", "makefile", "GNUmakefile"}: k.append("make")
    if n & {"pom.xml", "build.gradle", "build.gradle.kts"}: k.append("java")
    if any(f.endswith((".csproj", ".fsproj", ".sln")) for f in n): k.append("dotnet")
    if "Gemfile" in n or any(f.endswith(".gemspec") for f in n): k.append("ruby")
    if "Package.swift" in n or any(f.endswith(".xcodeproj") for f in n): k.append("swift")
    if not k and any(os.path.splitext(f)[1].lower() in SRCEXT and os.path.isfile(os.path.join(d, f)) for f in n): k.append("src")
    if "Dockerfile" in n: k.append("docker")
    if "SKILL.md" in n: k.append("skill")
    return k


def src_files(d, limit=4000, cap=400, skip=SKIPSUB):
    """Kaynak dosyalar (derinlik<=3, `skip` hariç, en çok `limit` dosya bakılır)."""
    out, seen, q = [], 0, [(d, 0)]  # genişlik-öncelikli, tembel scandir: dev klasörlerde (ikon depoları) tamamını listelemez
    while q and seen <= limit and len(out) < cap:
        cur, dep = q.pop(0)
        try:
            with os.scandir(cur) as it:
                for e in it:
                    seen += 1
                    if seen > limit or len(out) >= cap:
                        break
                    if e.is_dir(follow_symlinks=False):
                        if dep < 3 and e.name not in skip and not e.name.startswith("."):
                            q.append((e.path, dep + 1))
                    elif os.path.splitext(e.name)[1].lower() in SRCEXT or e.name.endswith(".h"):
                        out.append(e.path)
        except OSError:
            continue
    return out


def detect(d):
    """(kinds, workdir, primary). Kökte çalıştırılabilir tür yoksa ilk alt klasöre, o da yoksa derin kaynak taramasına bakar."""
    k = kinds_in(d)
    sub_docker = []
    if not any(x in k for x in RUNNABLE) and "skill" not in k:
        try:
            subs = sorted(e.name for e in os.scandir(d) if e.is_dir() and e.name not in SKIPSUB and not e.name.startswith("."))
        except OSError:
            subs = []
        for s in subs:
            ks = kinds_in(os.path.join(d, s))
            if any(x in ks for x in RUNNABLE):
                return ks, os.path.join(d, s), next(x for x in RUNNABLE if x in ks)
        sub_docker = [s for s in subs if "docker" in kinds_in(os.path.join(d, s))]
    for x in RUNNABLE:
        if x in k:
            return k, d, x
    if "docker" in k and "skill" not in k:
        return k, d, "docker"
    if "skill" not in k and any(not f.endswith(".h") for f in src_files(d, cap=1) or src_files(d, cap=1, skip=HARDSKIP)):
        return k + ["src"], d, "src"
    if sub_docker and "skill" not in k:
        return k + ["docker"], d, "docker"
    return k, d, "doc"


def real_doc(d):
    """Gerçek doküman = kodsuz repo (yalnız md/txt/pdf/görsel...)."""
    return detect(d)[2] == "doc"


# ---------- sistem ----------
class _MS(ctypes.Structure):
    _fields_ = [("dwLength", ctypes.c_ulong), ("dwMemoryLoad", ctypes.c_ulong)] + [
        (n, ctypes.c_ulonglong) for n in ("a", "b", "c", "d", "e", "f", "g")]


def ram_pct():
    m = _MS(); m.dwLength = ctypes.sizeof(_MS)
    ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(m))
    return m.dwMemoryLoad


def log(s):
    with _lock, open(LOG, "a", encoding="utf-8") as f:
        f.write(time.strftime("%H:%M:%S ") + s + "\n")


def run(cmd, cwd, env, timeout):
    if timeout <= 0:
        return 124, "zaman aşımı (öğe bütçesi bitti)"
    try:
        p = subprocess.Popen(cmd, cwd=cwd, env=env, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE,
                             stderr=subprocess.STDOUT, creationflags=0x08000000)
    except OSError as e:
        return 127, "başlatılamadı: %s" % e
    t0, d0 = time.monotonic(), DONMA.oku()
    try:
        while True:
            kalan = timeout - etkin_gecen(t0, d0)
            if kalan <= 0:
                raise subprocess.TimeoutExpired(cmd, timeout)
            try:
                out, _ = p.communicate(timeout=min(kalan, 2.0))
                break
            except subprocess.TimeoutExpired:
                continue
        rc = p.returncode
        tag = ""
    except subprocess.TimeoutExpired:
        subprocess.run(["taskkill", "/T", "/F", "/PID", str(p.pid)], stdin=subprocess.DEVNULL,
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        try:
            out, _ = p.communicate(timeout=20)
        except Exception:
            out = b""
        rc, tag = 124, "\n[zaman aşımı %ds]" % timeout
    return rc, (out or b"").decode("utf-8", "replace")[-4000:] + tag


def ayakta_kaldi(rc, out):
    """Sunucu/uzun süreli komut: süre dolana dek ayakta kaldıysa başarı sayılır (ana koşu + --tekrar aynı kural)."""
    if rc == 124 and out.rstrip().endswith("s]"):
        return 0, out.replace("[zaman aşımı", "[ayakta kaldı (sunucu/uzun süreli)")
    return rc, out


class Ctx:
    def __init__(s, base, d, env):
        s.base, s.d, s.env, s.t0 = base, d, env, time.monotonic()
        s.d0 = DONMA.oku()
        s.inst = s.runc = ""
        s.rc, s.out = 0, ""
        s.status = None  # (ENGEL-*, kanıt): işleyici engeli kendisi bildirir

    def left(s):
        return ITEM_TIMEOUT - etkin_gecen(s.t0, s.d0)

    def step(s, cmd, cwd=None, cap=None, is_run=False):
        cwd = cwd or s.d
        rc, out = run(cmd, cwd, s.env, min(s.left(), cap or 1e9))
        cs = subprocess.list2cmdline(cmd)
        if os.path.normcase(cwd) != os.path.normcase(s.base):
            cs = "cwd:%s|%s" % (cwd, cs)
        if is_run: s.runc = cs
        else: s.inst = cs
        if is_run: rc, out = ayakta_kaldi(rc, out)
        s.rc, s.out = rc, out
        return rc, out

    def fail(s, msg):
        s.out = msg
        return False


# ---------- türe göre kurulum + duman ----------
def js_import(name):
    return ["node", "-e", "import(%r).then(()=>process.exit(0),e=>{console.error(e&&e.message);process.exit(1)})" % name]


def npm_run_cmd(d, pj):
    b = pj.get("bin")
    if isinstance(b, dict): b = next(iter(b.values()), None)
    if isinstance(b, str) and os.path.exists(os.path.join(d, b)):
        return ["node", b, "--help"]
    main = pj.get("main") or ("index.js" if os.path.exists(os.path.join(d, "index.js")) else None)
    if isinstance(main, str) and os.path.exists(os.path.join(d, main)):
        if pj.get("type") == "module" or main.endswith(".mjs"):
            return ["node", "-e", "import(require('url').pathToFileURL(require('path').resolve(%r)).href)"
                    ".then(()=>process.exit(0),e=>{console.error(e&&e.message);process.exit(1)})" % main]
        return ["node", "-e", "require(require('path').resolve(%r));process.exit(0)" % main]
    s = pj.get("scripts") or {}
    if "build" in s: return ["npm.cmd", "run", "build"]
    if "test" in s: return ["npm.cmd", "test"]
    return None


def pnpm_cmds(d):
    """pnpm kurulum komutları: npm/yarn kilidi varsa önce import; tek paylaşılan depo, çevrimdışı-öncelikli."""
    has = lambda f: os.path.exists(os.path.join(d, f))
    cmds = []
    if not has("pnpm-lock.yaml") and (has("package-lock.json") or has("yarn.lock")):
        cmds.append(["pnpm.cmd", "import"])
    cmds.append(["pnpm.cmd", "install", "--prefer-offline", "--no-frozen-lockfile", "--config.strictDepBuilds=false",
                 "--store-dir", PNPM_STORE])
    return cmds


def nm_link_stats(nm):
    """node_modules içinde sert bağlantılı (nlink>1) dosya sayısı; görünür boyut vs depoyla paylaşılmayan (gerçek kopya) bayt."""
    n = b = vis = cop = 0
    for r, _, fs in os.walk(nm):
        for f in fs:
            try:
                st = os.lstat(os.path.join(r, f))
            except OSError:
                continue
            n += 1
            vis += st.st_size
            if st.st_nlink > 1: b += 1
            else: cop += st.st_size
    return dict(dosya=n, bagli=b, gorunur_bayt=vis, kopya_bayt=cop)


def do_npm(c):
    try:
        pj = json.load(open(os.path.join(c.d, "package.json"), encoding="utf-8-sig"))
    except Exception as e:
        return c.fail("package.json okunamadı: %s" % str(e)[:100])
    inst = ["npm.cmd", "install", "--no-audit", "--no-fund"]
    ok = False
    if shutil.which("pnpm.cmd"):  # önce pnpm (sert bağlantı, kopya yok); olmazsa eski npm merdiveni
        for pc in pnpm_cmds(c.d):  # import başarısızlığı (kilit uyumsuz) kurulumu engellemez
            rc, out = c.step(pc)
            ok = pc[1] == "install" and rc == 0
    if not ok:
        rc, out = c.step(inst)
    if rc != 0 and "ERESOLVE" in out:
        rc, out = c.step(inst + ["--legacy-peer-deps"])
    elif rc != 0 and "workspace:" in out:
        pm = str(pj.get("packageManager", ""))
        mgr = ["yarn.cmd", "install", "--ignore-scripts"] if pm.startswith("yarn") or os.path.exists(os.path.join(c.d, "yarn.lock")) \
            else ["pnpm.cmd", "install", "--ignore-scripts"]
        rc, out = c.step(mgr)
    if rc != 0 and re.search(r"EBADENGINE|Unsupported engine", out):
        rc, out = c.step(inst + ["--force"])
    if rc != 0:
        return False
    cmd = npm_run_cmd(c.d, pj)
    if not cmd:
        c.out = "kurulum tamam; çalıştırılacak giriş yok"
        return True
    rc, out = c.step(cmd, cap=120, is_run=True)
    if rc != 0:
        m = re.search(r"Cannot find (?:module|package) '(@[^/']+/[^/']+|[^'./][^/']*)", out)
        if m and c.step(["npm.cmd", "install", m.group(1), "--no-audit", "--no-fund"])[0] == 0:
            rc, out = c.step(cmd, cap=120, is_run=True)
    return rc == 0


def toml(p):
    try:
        return tomllib.load(open(p, "rb"))
    except Exception:
        return {}


PYVER_ERR = re.compile(r"(?i)get_loader|distutils|No module named '(imp|asyncore|asynchat|smtpd|cgi|pipes)'|"
                       r"asyncio\.coroutine|has no attribute '(getargspec|getcallargs)'|requires-python|"
                       r"different python|python_requires|Failed to build|Python \d")


GENEL_DIR = {"test", "tests", "testing", "tools", "tool", "scripts", "script", "examples", "example", "docs", "doc",
             "benchmarks", "benchmark", "bench", "utils", "util", "assets", "data", "configs", "config", "notebooks",
             "demo", "demos", "samples", "sample", "build", "dist", "ci", "docker", "third_party", "vendor", "src",
             "e2e", "integration", "unit", "fixtures", "testdata", "playground", "sandbox"}
VENV_MODS = ("import importlib.metadata as m,sys\nn=sys.argv[1].lower().replace('_','-')\n"
             "for k,v in m.packages_distributions().items():\n"
             "    if any(x.lower().replace('_','-')==n for x in v): print(k)\n")
PY_NEXT = {"3.12": "3.11", "3.13": "3.11", "3.11": "3.10"}


def py_install(c, vpy, pkg, has):
    if pkg:
        inst = ["uv", "pip", "install", "-e", ".", "--python", vpy]
    elif has("requirements.txt"):
        inst = ["uv", "pip", "install", "-r", "requirements.txt", "--python", vpy]
    else:
        return c.fail("kurulabilir tanım yok")
    rc, out = c.step(inst)
    if rc != 0 and BUILDFAIL.search(out) and has("requirements.txt"):  # önce önceden derlenmiş tekerlek
        if c.step(["uv", "pip", "install", "-r", "requirements.txt", "--no-build", "--python", vpy])[0] == 0 and (
                not pkg or c.step(["uv", "pip", "install", "-e", ".", "--no-deps", "--python", vpy])[0] == 0):
            return True
    elif rc != 0 and pkg and has("requirements.txt"):
        rc, out = c.step(["uv", "pip", "install", "-r", "requirements.txt", "--python", vpy])
    if rc != 0:
        c.out = out  # özgün hata sınıflandırma için kalsın
    return rc == 0


def agir_prepare(c, venv, vpy, pkg, has):
    """Ağır-ml'e bağlı repo: boş venv + agir-ml site-packages'a .pth (kopya yok); ağır olmayan bağımlılıklar kurulur."""
    sp = os.path.join(AGIR_ML, "Lib", "site-packages")
    with open(os.path.join(venv, "Lib", "site-packages", "agirml.pth"), "w") as f:
        f.write(sp + "\n")
    if has("requirements.txt"):
        req = filter_req(open(os.path.join(c.d, "requirements.txt"), encoding="utf-8", errors="replace").read())
        if req:
            fr = os.path.join(venv, "req-agir.txt")
            open(fr, "w", encoding="utf-8").write("\n".join(req) + "\n")
            rc, out = c.step(["uv", "pip", "install", "-r", fr, "--python", vpy])
            if rc != 0:  # tek tek dene: biri kurulamazsa diğerleri kalsın, çalıştırma testi eksik modülü söyler
                for r in req:
                    c.step(["uv", "pip", "install", r, "--python", vpy])
    if pkg:
        proj = toml(os.path.join(c.d, "pyproject.toml"))
        deps = list(proj.get("project", {}).get("dependencies") or [])
        poetry = proj.get("tool", {}).get("poetry", {}).get("dependencies") or {}
        deps += [k for k in poetry if k.lower() != "python"]
        req = filter_req("\n".join(deps)) if deps else []
        if req:
            fr = os.path.join(venv, "req-agir-pyproject.txt")
            open(fr, "w", encoding="utf-8").write("\n".join(req) + "\n")
            if c.step(["uv", "pip", "install", "-r", fr, "--python", vpy])[0] != 0:
                for r in req:
                    c.step(["uv", "pip", "install", r, "--python", vpy])
        c.step(["uv", "pip", "install", "-e", ".", "--no-deps", "--python", vpy])
    return True


def do_py(c, pyver="3.12", agir=False):
    d = c.d
    venv = os.path.join(d, ".venv-agir" if agir else ".venv" + (pyver.replace(".", "") if pyver else ""))
    vpy = os.path.join(venv, "Scripts", "python.exe")
    proj = toml(os.path.join(d, "pyproject.toml"))
    has = lambda f: os.path.exists(os.path.join(d, f))
    pkg = has("setup.py") or has("setup.cfg") or "project" in proj or "build-system" in proj or "poetry" in proj.get("tool", {})
    if not os.path.exists(vpy) or disk_ok():  # venv varken disk düşükse yeniden kurma, mevcut venv ile koş
        rc, out = c.step(["uv", "venv", venv, "--allow-existing"] + (["--python", pyver] if pyver else []))
        if rc != 0:
            return False
        if not (agir_prepare(c, venv, vpy, pkg, has) if agir else py_install(c, vpy, pkg, has)):
            out = c.out
            nxt = None if agir else PY_NEXT.get(pyver)
            if nxt and (PYVER_ERR.search(out) or BUILDFAIL.search(out)):
                m = re.search(r">=\s*3\.(\d+)", out)
                return do_py(c, "3.13" if pyver == "3.12" and m and m.group(1) in ("13", "14") else nxt)
            return False
    scripts = list((proj.get("project", {}).get("scripts") or proj.get("tool", {}).get("poetry", {}).get("scripts") or {}))
    cmds = [[os.path.join(venv, "Scripts", n + ".exe"), "--help"] for n in scripts[:2]
            if os.path.exists(os.path.join(venv, "Scripts", n + ".exe"))]
    cand = [n for n in (os.listdir(d) + (os.listdir(os.path.join(d, "src")) if os.path.isdir(os.path.join(d, "src")) else []))
            if re.match(r"^[A-Za-z_]\w*$", n) and (os.path.exists(os.path.join(d, n, "__init__.py")) or
                                                    os.path.exists(os.path.join(d, "src", n, "__init__.py")))]
    pname = proj.get("project", {}).get("name") or proj.get("tool", {}).get("poetry", {}).get("name") or os.path.basename(d)
    rc, out = run([vpy, "-c", VENV_MODS, pname], d, c.env, 60)  # kurulu dağıtımın gerçek üst modülleri (tahmin yok)
    cand = [m for m in dict.fromkeys((out.split() if rc == 0 else []) + cand) if re.match(r"^[A-Za-z_]\w*$", m)
            and m.lower() not in GENEL_DIR]
    run_cwd = venv
    if not cmds:
        cmds = [[vpy, "-c", "import %s; print('import %s ok')" % (m, m)] for m in cand[:3]]
    if not cmds:
        run_cwd = d
        for f in ("main.py", "app.py", "cli.py", "run.py", "__main__.py"):
            if has(f):
                cmds = [[vpy, f, "--help"]]
                break
    if not cmds:  # giriş noktası yok: kurulum tutarlılığı kanıtı (uv pip check çıktısı)
        cmds = [["uv", "pip", "check", "--python", vpy]]
        run_cwd = d
    fail_out = ""
    for cmd in cmds:
        rc, out = c.step(cmd, cwd=run_cwd, cap=90, is_run=True)
        if rc == 0:
            return True
        fail_out = out
        m = MODNF.search(out)
        if m and m.group(1).split(".")[0] in cand and run_cwd != d:
            yerel_env = dict(c.env or os.environ)
            yerel_env["PYTHONPATH"] = os.pathsep.join(p for p in (d, os.path.join(d, "src"), yerel_env.get("PYTHONPATH", "")) if p)
            rc, out = run(cmd, d, yerel_env, min(c.left(), 90))
            if rc == 0:
                c.runc = subprocess.list2cmdline(cmd) + "  (cwd=repo, PYTHONPATH=repo)"
                c.out = out
                return True
            fail_out = out
            m = MODNF.search(out)
        if m and m.group(1).split(".")[0] not in cand and disk_ok():
            pip_n = import_to_pip(m.group(1)) or m.group(1).split(".")[0]
            if c.step(["uv", "pip", "install", pip_n, "--python", vpy])[0] == 0:
                rc, out = c.step(cmd, cwd=run_cwd, cap=90, is_run=True)
                if rc == 0:
                    return True
                fail_out = out
        if pyver == "3.12" and not agir and PYVER_ERR.search(out) and disk_ok():
            return do_py(c, "3.11")
    c.out = fail_out
    return False


def do_rust(c):
    rc, out = c.step(["cargo", "build", "--quiet"])
    if rc != 0:
        return False
    t = os.path.join(c.d, "target", "debug")
    exes = sorted(f for f in os.listdir(t) if f.endswith(".exe")) if os.path.isdir(t) else []
    if not exes:
        c.out = "build tamam; exe yok (kütüphane)"
        return True
    return c.step([os.path.join(t, exes[0]), "--help"], cap=60, is_run=True)[0] == 0


def do_go(c):
    rc, out = c.step(["go", "build", "./..."])
    if rc != 0 and "undefined reference" in out:
        rc, out = c.step(["go", "build", "-ldflags=-checklinkname=0", "./..."])
    if rc != 0:
        return False
    rc, out = run(["go", "list", "-f", "{{.Name}}", "."], c.d, c.env, 60)
    if rc == 0 and out.strip().splitlines()[-1:] == ["main"]:
        return c.step(["go", "run", ".", "--help"], cap=90, is_run=True)[0] == 0
    c.out = "go build tamam; kök paket main değil"
    return True


# ---------- CMake / Make / Java / .NET / Ruby / Swift / kaynak-only ----------
def disk_ok():
    return shutil.disk_usage("C:\\").free >= MIN_FREE


def engel(c, kind, msg):
    c.status = (kind, msg)
    return False


def miss(*names):
    return [n for n in names if not shutil.which(n)]


def cmake_missing(out):
    m = re.search(r'provided by "([^"]+)"', out) or re.search(r"Could NOT find (\w+)", out)
    return m.group(1) if m else ""


def missing_header(out):
    m = re.search(r"fatal error: ([^\s:]+): No such file or directory", out)
    return m.group(1) if m else ""


def do_cmake(c):
    if miss("cmake"):
        return engel(c, "ENGEL-DERLEYICI", "eksik: cmake")
    b = os.path.join(c.d, ".cmake-build")
    gen = ["-G", "Ninja"] if shutil.which("ninja") else ["-G", "MinGW Makefiles"] if shutil.which("mingw32-make") else []
    rc, out = c.step(["cmake", "-S", c.d, "-B", b] + gen, cap=300)
    if rc != 0:
        m = cmake_missing(out)
        if m:
            return engel(c, "ENGEL-DERLEYICI", "eksik: %s (cmake find_package)" % m)
        if re.search(r"(?i)CMAKE_(C|CXX)_COMPILER|could not find (any instance of )?visual studio|generator.*does not support|CMAKE_MAKE_PROGRAM", out):
            return engel(c, "ENGEL-DERLEYICI", "eksik: C/C++ derleyici+üretici (cl/msbuild | ninja | mingw32-make)")
        return False
    rc, out = c.step(["cmake", "--build", b, "-j", "4"], cap=300, is_run=True)
    if rc == 124:
        c.out, c.rc = "cmake yapılandırma tamam; derleme 300 sn'de bitmedi", 0
        return True
    return rc == 0


def do_make(c):
    mk = shutil.which("make") or shutil.which("mingw32-make")
    if not mk:
        return engel(c, "ENGEL-DERLEYICI", "eksik: make (mingw32-make)")
    return c.step([mk, "-n"], cap=120, is_run=True)[0] == 0


def do_ruby(c):
    if miss("ruby"):
        return engel(c, "ENGEL-DERLEYICI", "eksik: ruby")
    fs = [f for f in src_files(c.d, cap=50) if f.endswith(".rb")][:3]
    if os.path.exists(os.path.join(c.d, "Gemfile")):
        if miss("bundle"):
            return engel(c, "ENGEL-DERLEYICI", "eksik: bundler (bundle)")
        if c.step(["bundle", "install", "--quiet"], cap=300)[0] != 0:
            return False
    return bool(fs) and all(c.step(["ruby", "-c", f], cap=60, is_run=True)[0] == 0 for f in fs)


def do_java(c):
    if miss("java"):
        return engel(c, "ENGEL-DERLEYICI", "eksik: java (JDK)")
    if os.path.exists(os.path.join(c.d, "pom.xml")):
        if miss("mvn"):
            return engel(c, "ENGEL-DERLEYICI", "eksik: mvn (maven)")
        return c.step(["mvn", "-q", "-B", "-DskipTests", "compile"], cap=500, is_run=True)[0] == 0
    gw = os.path.join(c.d, "gradlew.bat")
    g = gw if os.path.exists(gw) else shutil.which("gradle")
    if not g:
        return engel(c, "ENGEL-DERLEYICI", "eksik: gradle (gradlew.bat yok)")
    return c.step([g, "--no-daemon", "-q", "build", "-x", "test"], cap=500, is_run=True)[0] == 0


def do_dotnet(c):
    if miss("dotnet"):
        return engel(c, "ENGEL-DERLEYICI", "eksik: dotnet")
    proj = sorted(f for f in os.listdir(c.d) if f.endswith((".sln", ".csproj", ".fsproj")))
    c.env = dict(c.env, DOTNET_NOLOGO="1")  # --nologo MTP/xunit.v3'ü bozar
    rc, out = c.step(["dotnet", "build", proj[0], "-v", "m"], cap=500, is_run=True)
    if rc == 0:
        c.out = "dotnet build ok: " + last_line(out)
    return rc == 0


def do_swift(c):
    if shutil.which("swift") and os.path.exists(os.path.join(c.d, "Package.swift")):
        return c.step(["swift", "build"], cap=500, is_run=True)[0] == 0
    return engel(c, "ENGEL-PLATFORM", "yalnız macOS/Linux; eksik: swift/xcodebuild")


def bash():
    for p in (r"C:\Program Files\Git\bin\bash.exe", shutil.which("bash")):
        if p and os.path.exists(p):
            return p
    return ""


PS_PARSE = ("$e=$null;[void][System.Management.Automation.Language.Parser]::ParseFile('%s',[ref]$null,[ref]$e);"
            "if($e.Count){$e|%%{$_.Message};exit 1}")
PYCHK = "import sys;compile(open(sys.argv[1],'rb').read(),sys.argv[1],'exec')"  # __pycache__ yazmaz, çalıştırmaz
SRCCHK = {".py": ("python", ["-I", "-c", PYCHK]), ".js": ("node", ["--check"]), ".mjs": ("node", ["--check"]),
          ".sh": ("bash", ["-n"]), ".bash": ("bash", ["-n"]), ".php": ("php", ["-l"]), ".rb": ("ruby", ["-c"]),
          ".pl": ("perl", ["-c"]), ".lua": ("luac", ["-p"]), ".c": ("gcc", ["-fsyntax-only"]),
          ".cc": ("g++", ["-fsyntax-only"]), ".cpp": ("g++", ["-fsyntax-only"]), ".cxx": ("g++", ["-fsyntax-only"]),
          ".java": ("javac", ["-proc:none", "-d"]), ".kt": ("kotlinc", ["-version"]), ".ps1": ("powershell", [])}
HELPPAT = re.compile(r"--help\)|-h\|--help|--help\|-h")


def do_src(c):
    """Yalnız kaynak (manifest yok): dile göre sözdizimi denetimi; kabuk betiği --help yalnız betik kendi işliyorsa."""
    fs = src_files(c.d) or src_files(c.d, skip=HARDSKIP)
    cnt = collections.Counter(os.path.splitext(f)[1].lower() for f in fs if os.path.splitext(f)[1].lower() in set(SRCCHK) | {".cs", ".swift"})
    if not cnt:
        return c.fail("denetlenecek kaynak yok")
    ext = cnt.most_common(1)[0][0]
    if ext == ".swift":
        return do_swift(c)
    if ext == ".cs":
        return engel(c, "ENGEL-DERLEYICI", "eksik: .csproj/.sln (yalnız .cs kaynak)")
    tool, args = SRCCHK[ext]
    exe = bash() if tool == "bash" else shutil.which(tool)
    if not exe:
        return engel(c, "ENGEL-DERLEYICI", "eksik: " + tool)
    pick = sorted(f for f in fs if os.path.splitext(f)[1].lower() == ext)[:5]
    help_ln = ""
    for f in pick:
        if ext == ".ps1":
            cmd = [exe, "-NoProfile", "-Command", PS_PARSE % f.replace("'", "''")]
        elif ext == ".java":
            cmd = [exe] + args + [tempfile.mkdtemp(prefix="ch_javac_"), f]
        else:
            cmd = [exe] + args + [f]
        rc, out = c.step(cmd, cap=60, is_run=True)
        if rc != 0:
            h = missing_header(out)
            if h:
                return engel(c, "ENGEL-DERLEYICI", "eksik başlık: " + h)
            return False
    if ext in (".sh", ".bash"):
        for f in pick:
            if HELPPAT.search(open(f, encoding="utf-8", errors="replace").read(20000)):
                rc, out = c.step([exe, f, "--help"], cap=20, is_run=True)
                help_ln = " | --help: " + (last_line(out) or "rc=%s" % rc)
                break
    c.rc = 0
    c.out = "%s sözdizimi ok (%d dosya)%s" % (tool, len(pick), help_ln)
    return True


def platform_block(d):
    """Windows tekerleği olmayan ağır paketler (adlarıyla, sıralı)."""
    found = set()
    for f in ("requirements.txt", "pyproject.toml", "setup.py", "setup.cfg"):
        try:
            t = open(os.path.join(d, f), encoding="utf-8", errors="replace").read(200000).lower().replace("_", "-")
        except OSError:
            continue
        found |= {n for n in NOWHEEL if re.search(r"(?<![\w-])%s(?![\w-])" % re.escape(n), t)}
    return sorted(found)


def filter_req(text):
    """requirements içinden ağır paket / seçenek / yorum satırlarını at; ağır paketler agir-ml'den gelir."""
    out = []
    for l in text.splitlines():
        l = l.strip()
        if l and not l.startswith(("#", "-")) and not HEAVY.search(l):
            out.append(l)
    return out


def agir_py():
    return os.path.join(AGIR_ML, "Scripts", "python.exe")


def agir_hazir():
    return os.path.exists(os.path.join(AGIR_ML, ".hazir"))


def agir_kur():
    """Tek ağır-ml venv: torch CUDA (uv sürücüye göre seçer) + transformers/diffusers/accelerate/bitsandbytes/tensorflow/paddle."""
    py, env = agir_py(), child_env()
    steps = [(["uv", "venv", AGIR_ML, "--python", "3.12", "--allow-existing"], 300),
             (["uv", "pip", "install", "torch", "torchvision", "torchaudio", "--torch-backend", "auto", "--python", py], 3000),
             (["uv", "pip", "install", "transformers", "diffusers", "accelerate", "bitsandbytes", "tensorflow", "--python", py], 3000),
             (["uv", "pip", "install", "paddlepaddle", "--python", py], 1800)]
    for cmd, t in steps:
        free = shutil.disk_usage("C:\\").free / 1e9
        if not disk_ok():
            log("agir-kur DISK-BEKLE: C: %.1f GB" % free)
            return "DISK-BEKLE"
        rc, out = run(cmd, ROOT, env, t)
        log("agir-kur rc=%s serbest=%.1fGB %s | %s" % (rc, free, subprocess.list2cmdline(cmd)[:100], last_line(out)))
        if rc != 0 and "paddlepaddle" not in cmd:
            return "HATA: " + last_line(out)
    rc, out = run([py, "-c", "import torch;print(torch.__version__,torch.cuda.is_available())"], ROOT, env, 120)
    open(os.path.join(AGIR_ML, ".hazir"), "w", encoding="utf-8").write(out)
    return "TAMAM: " + last_line(out)


DO = {"npm": do_npm, "py": do_py, "rust": do_rust, "go": do_go, "cmake": do_cmake, "make": do_make, "java": do_java,
      "dotnet": do_dotnet, "ruby": do_ruby, "swift": do_swift, "src": do_src}
_sk = None


def skill_names():
    global _sk
    with _lock:
        if _sk is None:
            _sk, home = set(), os.path.expanduser("~/.claude")
            for base in ("skills", os.path.join("plugins", "cache")):
                for r, ds, fs in os.walk(os.path.join(home, base)):
                    ds[:] = [x for x in ds if x not in ("node_modules", ".git")]
                    if "SKILL.md" in fs:
                        _sk.add(os.path.basename(r).lower())
    return _sk


def frontmatter(p):
    try:
        t = open(p, encoding="utf-8-sig", errors="replace").read(8000)
    except OSError:
        return None
    m = re.match(r"---\r?\n(.*?)\r?\n---", t, re.S)
    if not m:
        return None
    n = re.search(r"^name:\s*(.+)$", m.group(1), re.M)
    return n.group(1).strip().strip("'\"").lower() if n and re.search(r"^description:", m.group(1), re.M) else None


def do_doc(d):
    paths = []
    for r, ds, fs in os.walk(d):
        ds[:] = [x for x in ds if x not in ("node_modules", ".git")]
        if r[len(d):].count(os.sep) >= 3:
            ds[:] = []
        if "SKILL.md" in fs:
            paths.append(os.path.join(r, "SKILL.md"))
        if len(paths) >= 60:
            break
    if not paths:
        return "DOKUMAN", "doküman; SKILL.md yok, çalıştırılacak giriş yok"
    idx = skill_names()
    names = [(frontmatter(p), os.path.basename(os.path.dirname(p)).lower()) for p in paths]
    valid = [x for x in names if x[0]]
    acc = [x for x in valid if x[0] in idx or x[1] in idx]
    if not valid:
        return "HATA", "%d SKILL.md, hiçbirinde geçerli frontmatter yok" % len(paths)
    if acc:
        return "CALISTI", "%d SKILL.md: %d geçerli, %d erişilebilir (~/.claude)" % (len(paths), len(valid), len(acc))
    lic = license_kind(d) or "lisanssız"  # Ömer 28 Eki: lisans engel değil, lisanssız da kurulur
    got = install_skills(d, SKILLS_DIR)
    if not got:
        return "HATA", "%d geçerli SKILL.md ama kurulamadı (boyut>20MB ya da kopyalama hatası)" % len(valid)
    return "SKILL-KURULDU", "%d skill ~/.claude/skills'e kuruldu (lisans=%s): %s" % (len(got), lic, ",".join(got[:4]))


# ---------- kalemler ----------
def kalem_npm(it, env):
    n = it["name"]
    md = os.path.join(NPM_KALEM, "node_modules", *n.split("/"))
    try:
        pj = json.load(open(os.path.join(md, "package.json"), encoding="utf-8-sig"))
    except Exception:
        return "HATA", "", "", 1, "node_modules'ta kurulu değil"
    b = pj.get("bin")
    if isinstance(b, dict): b = next(iter(b.values()), None)
    tries = []
    if isinstance(b, str) and os.path.exists(os.path.join(md, b)):
        tries.append(["node", os.path.join(md, b), "--version"])
    tries.append(js_import(n))
    for cmd in tries:
        rc, out = run(cmd, NPM_KALEM, env, 60)
        cs = "cwd:%s|%s" % (NPM_KALEM, subprocess.list2cmdline(cmd))
        if rc == 0:
            return "CALISTI", "kurulu (npm-kalem)", cs, 0, last_line(out) or "rc=0"
    return "HATA", "kurulu (npm-kalem)", cs, rc, last_line(out)


def kalem_pip(it, env):
    vpy = os.path.join(PIP_KALEM, "Scripts", "python.exe")
    di = it["path"]
    rd = lambda f: open(os.path.join(di, f), encoding="utf-8", errors="replace").read() if os.path.exists(os.path.join(di, f)) else ""
    mods = dist_modules(di) + [re.sub(r"[-.]", "_", it["name"])]
    rc, out, cs = 1, "", ""
    for m in list(dict.fromkeys(mods))[:4]:
        cmd = [vpy, "-c", "import %s; print('import %s ok')" % (m, m)]
        rc, out = run(cmd, PIP_KALEM, env, 60)
        cs = "cwd:%s|%s" % (PIP_KALEM, subprocess.list2cmdline(cmd))
        if rc == 0:
            return "CALISTI", "kurulu (venv-kalem)", cs, 0, "import %s ok" % m
    ep = rd("entry_points.txt")
    m = re.search(r"\[console_scripts\]\s*\n\s*([\w.-]+)\s*=", ep)
    if m:
        exe = os.path.join(PIP_KALEM, "Scripts", m.group(1) + ".exe")
        if os.path.exists(exe):
            cmd = [exe, "--version"]
            rc, out = run(cmd, PIP_KALEM, env, 60)
            cs = "cwd:%s|%s" % (PIP_KALEM, subprocess.list2cmdline(cmd))
            if rc == 0:
                return "CALISTI", "kurulu (venv-kalem)", cs, 0, last_line(out) or "rc=0"
    return "HATA", "kurulu (venv-kalem)", cs, rc, last_line(out)


# ---------- öğe işleme ----------
def process(it):
    row = dict(yol=it["path"], remote=it["remote"], tur=it["tur"], kurulum_kmt="", calistirma_kmt="", rc="", durum="HATA", kanit="")
    try:
        env = child_env()
        if it["scope"] == "npm-kalem":
            row["durum"], row["kurulum_kmt"], row["calistirma_kmt"], row["rc"], row["kanit"] = kalem_npm(it, env)
        elif it["scope"] == "pypi-kalem":
            row["durum"], row["kurulum_kmt"], row["calistirma_kmt"], row["rc"], row["kanit"] = kalem_pip(it, env)
        elif it["primary"] == "docker":
            row.update(durum="ENGEL-DOCKER", kanit="yalnız Dockerfile; docker build yapılmaz")
        elif it["primary"] == "doc":
            row["durum"], row["kanit"] = do_doc(it["work"])
        else:
            p = it["primary"]
            h = heavy(it["work"]) if p == "py" else ""
            nw = platform_block(it["work"]) if h else []
            if nw:
                row.update(durum="ENGEL-PLATFORM", kanit="Windows tekerleği yok: %s" % ", ".join(nw))
            elif h and agir_hazir():
                c = Ctx(it["path"], it["work"], env)
                ok = do_py(c, agir=True)
                row.update(kurulum_kmt=c.inst, calistirma_kmt=c.runc, rc=c.rc)
                if ok:
                    row.update(durum="CALISTI", kanit="[py agir-ml:%s] %s" % (h, last_line(c.out) or "rc=0"))
                else:
                    cl = c.status or classify(c.out) or classify_modnf(c.out) or classify_build(c.out)
                    row.update(durum=cl[0] if cl else "HATA", kanit="[py agir-ml:%s] %s" % (h, cl[1] if cl else last_line(c.out) or "rc=%s" % c.rc))
            elif h:
                row.update(durum="BUYUK-SOR", kanit="ağır bağımlılık (%s): >5GB riski, çalıştırılmadı" % h)
            else:
                c = Ctx(it["path"], it["work"], env)
                ok = DO[p](c)
                row.update(kurulum_kmt=c.inst, calistirma_kmt=c.runc, rc=c.rc)
                pre = "[%s%s] " % (p, "" if it["work"] == it["path"] else " alt:" + os.path.basename(it["work"]))
                if ok:
                    row.update(durum="CALISTI", kanit=pre + (last_line(c.out) or "rc=0 (çıktı yok)"))
                else:
                    cl = c.status or classify(c.out) or classify_modnf(c.out) or classify_build(c.out)
                    row.update(durum=cl[0] if cl else "HATA", kanit=pre + (cl[1] if cl else last_line(c.out) or "rc=%s" % c.rc))
    except Exception as e:
        row.update(durum="HATA", kanit="betik istisnası: %s" % redact(str(e))[:200])
    if is_weak(row):
        row["durum"] = "ZAYIF"
    return row


def tsv_path(args):
    return os.path.join(OUT, "calistirma-deneme.tsv") if args.deneme else os.path.join(OUT, "calistirma.tsv")


def read_rows(p):
    if not os.path.exists(p):
        return []
    with open(p, encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f, delimiter="\t"))


def write_row(p, row):
    with _lock:
        new = not os.path.exists(p)
        with open(p, "a", encoding="utf-8", newline="") as f:
            w = csv.writer(f, delimiter="\t", lineterminator="\n")
            if new: w.writerow(HEAD)
            w.writerow([re.sub(r"[\t\r\n]+", " ", str(row.get(h, ""))) for h in HEAD])


def remote_of(d):
    try:
        for l in open(os.path.join(d, ".git", "config"), encoding="utf-8", errors="replace"):
            if l.strip().startswith("url"):
                return l.split("=", 1)[1].strip()
    except OSError:
        pass
    return ""


PRIO = {"doc": 0, "docker": 0, "npm-kalem": 1, "pypi-kalem": 1, "src": 1, "ruby": 1, "swift": 1, "py": 2, "go": 3, "npm": 4,
        "rust": 5, "cmake": 5, "make": 5, "java": 5, "dotnet": 5}


def build_items():
    items, seen = [], set()
    for sname, root in SCOPES:
        if not os.path.isdir(root):
            continue
        for e in sorted(os.scandir(root), key=lambda x: x.name):
            if not e.is_dir():
                continue
            rem = remote_of(e.path)
            key = re.sub(r"\.git$", "", rem.lower().rstrip("/")) if rem else "path:" + e.name.lower()
            if key in seen:
                continue
            seen.add(key)
            k, work, prim = detect(e.path)
            items.append(dict(path=e.path, remote=rem, scope=sname, tur="+".join(k) or "doc", work=work, primary=prim, cat=prim))
    try:
        for n in sorted(json.load(open(os.path.join(NPM_KALEM, "package.json"), encoding="utf-8"))["dependencies"]):
            items.append(dict(path=os.path.join(NPM_KALEM, "node_modules", *n.split("/")), remote="npm:" + n, scope="npm-kalem",
                              tur="npm-kalem", work="", primary="npm-kalem", name=n, cat="npm-kalem"))
    except Exception as e:
        log("npm-kalem okunamadı: %s" % e)
    sp = os.path.join(PIP_KALEM, "Lib", "site-packages")
    if os.path.isdir(sp):
        for e in sorted(os.scandir(sp), key=lambda x: x.name):
            if e.is_dir() and e.name.endswith(".dist-info"):
                nm = re.sub(r"-[^-]+\.dist-info$", "", e.name)
                items.append(dict(path=e.path, remote="pypi:" + nm, scope="pypi-kalem", tur="pypi-kalem", work="",
                                  primary="pypi-kalem", name=nm, cat="pypi-kalem"))
    items.sort(key=lambda i: PRIO[i["primary"]])
    return items


def pick_trial(items, n):
    rng = random.Random(1105)
    pools = collections.OrderedDict((c, []) for c in ("py", "npm", "go", "rust", "docker", "doc", "npm-kalem", "pypi-kalem") + RUNNABLE[4:])
    for i in items:
        if i["primary"] == "py" and heavy(i["work"]):
            continue
        pools[i["cat"]].append(i)
    out, order = [], list(pools)
    while len(out) < n and any(pools.values()):
        for c in order:
            if pools[c] and len(out) < n:
                out.append(pools[c].pop(rng.randrange(len(pools[c]))))
    return out


def finalize(p, items):
    rows = {}
    for r in read_rows(p):
        rows[r["yol"]] = r
    tmp = p + ".tmp"
    with open(tmp, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, delimiter="\t", lineterminator="\n")
        w.writerow(HEAD)
        for r in rows.values():
            w.writerow([r.get(h, "") for h in HEAD])
    os.replace(tmp, p)
    cnt = collections.Counter(r["durum"] for r in rows.values())
    rep = collections.Counter(r["durum"] for r in rows.values() if not r["tur"].endswith("-kalem"))
    kal = collections.Counter(r["durum"] for r in rows.values() if r["tur"].endswith("-kalem"))
    s = dict(birim="repo/kalem", toplam_satir=len(rows), kapsam_oge=len(items), durum=dict(cnt), repo=dict(rep), kalem=dict(kal),
             tsv=os.path.basename(p))
    sp = os.path.join(OUT, "calistirma-ozet-deneme.json" if "deneme" in p else "calistirma-ozet.json")
    json.dump(s, open(sp, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    return s


def tam(args):
    os.makedirs(OUT, exist_ok=True)
    p = tsv_path(args)
    items = build_items()
    if args.deneme:
        items = pick_trial(items, args.deneme)
    done = {r["yol"] for r in read_rows(p) if r["durum"] != "BEKLEMEDE"}
    todo = [i for i in items if i["path"] not in done]
    log("başladı: kapsam=%d bekleyen=%d paralel=%d pid=%d" % (len(items), len(todo), args.paralel, os.getpid()))
    cnt, ran = collections.Counter(), set()

    def work(it):
        if STOP.is_set():
            return
        while ram_pct() > RAM_MAX and not STOP.is_set():
            time.sleep(15)
        free = shutil.disk_usage("C:\\").free
        if free < MIN_FREE:
            if not STOP.is_set():
                log("DUR: C: boş alan %.1f GB < %d GB" % (free / 1e9, MIN_FREE / 1e9))
            STOP.set()
            return
        r = process(it)
        write_row(p, r)
        with _lock:
            cnt[r["durum"]] += 1
            ran.add(it["path"])
            n = sum(cnt.values())
        if n % 20 == 0:
            log("ilerleme %d/%d %s serbest=%.1fGB ram=%d%%" % (n, len(todo), dict(cnt), shutil.disk_usage("C:\\").free / 1e9, ram_pct()))

    with ThreadPoolExecutor(args.paralel) as ex:
        list(ex.map(work, todo))
    for it in todo:
        if it["path"] not in ran:
            write_row(p, dict(yol=it["path"], remote=it["remote"], tur=it["tur"], durum="BEKLEMEDE",
                              kanit="çalıştırılmadı: durduruldu (disk<%dGB)" % (MIN_FREE / 1e9) if STOP.is_set() else "çalıştırılmadı"))
    s = finalize(p, items)
    log("bitti: %s" % json.dumps(s, ensure_ascii=False))
    print(json.dumps(s, ensure_ascii=False))


def tekrar_rc(row, rc):
    """Sunucu/uzun süreli komut süre dolana dek ayakta kaldıysa (ilk koşuda öyle kayıtlıysa) tekrar da başarı sayılır."""
    return 0 if rc == 124 and "ayakta kaldı" in row.get("kanit", "") else rc


def tekrar(args):
    rows = [r for r in read_rows(os.path.join(OUT, "calistirma.tsv")) if r["durum"] == "CALISTI" and r["calistirma_kmt"]]
    pick = random.Random().sample(rows, min(args.tekrar, len(rows)))
    res = []
    for r in pick:
        k = r["calistirma_kmt"]
        cwd, cmd = (k[4:].split("|", 1)) if k.startswith("cwd:") else (r["yol"], k)
        rc, out = ayakta_kaldi(*run(cmd, cwd, child_env(), 120))
        if rc == 124 and "ayakta kaldı" not in r["kanit"]:  # geçici RAM/CPU çekişmesi olabilir: bir kez yeniden dene
            rc, out = ayakta_kaldi(*run(cmd, cwd, child_env(), 120))
        rc = tekrar_rc(r, rc)
        res.append(dict(yol=r["yol"], komut=k, rc_eski=r["rc"], rc_yeni=rc, ayni=str(str(rc) == str(r["rc"])), kanit=last_line(out)))
        print(res[-1]["ayni"], r["rc"], rc, r["yol"])
    with open(os.path.join(OUT, "calistirma-tekrar.tsv"), "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(res[0]) if res else ["yol"], delimiter="\t", lineterminator="\n")
        w.writeheader(); w.writerows(res)


def needs_install(it):
    """Yeni kurulum (disk yiyen) gerektiriyor mu? Kalem/doc/kaynak/mevcut-venv'li py gerektirmez."""
    p = it["primary"]
    if p in ("doc", "docker", "npm-kalem", "pypi-kalem", "src", "swift", "ruby"):
        return False
    w = it["work"]
    if p == "make" and miss("make", "mingw32-make") == ["make", "mingw32-make"]:
        return False  # araç yok: işleyici anında ENGEL-DERLEYICI verir, diske yazmaz
    if p == "java" and not (os.path.exists(os.path.join(w, "pom.xml")) and shutil.which("mvn") or
                            os.path.exists(os.path.join(w, "gradlew.bat")) or shutil.which("gradle")):
        return False
    if p == "py":
        try:
            return not any(os.path.exists(os.path.join(it["work"], n, "Scripts", "python.exe")) for n in os.listdir(it["work"]) if n.startswith(".venv"))
        except OSError:
            return True
    return True


BIRAK = {s.lower() for s in (  # Ömer 6 Kas: gereksiz/karşılığı daha iyi olan, yeniden koşulmaz
    "pytorch__pytorch", "huggingface__transformers", "huggingface__diffusers", "huggingface__datasets", "huggingface__huggingface_hub",
    "ml-explore__mlx", "jundot__omlx", "sgl-project__sglang", "vllm-project__vllm",
    "zai-org__CogVideo", "guoyww__AnimateDiff", "meituan-longcat__LongCat-Video", "hao-ai-lab__FastVideo", "kandinskylab__kandinsky-5",
    "lllyasviel__Fooocus", "Homebrew__brew", "DrKLO__Telegram", "docker-archive__classicswarm", "greatscottgadgets__hackrf",
    "aircrack-ng__aircrack-ng", "AFLplusplus__AFLplusplus", "thewhiteh4t__seeker", "AGI4Engineering__EngDesign")}


def duzelt(args):
    """Yalnız HATA / ZAYIF / yanlış-DOKUMAN (kod ya da kurulmamış skill) satırlarını yeniden koşar; artan, yerinde günceller."""
    p = tsv_path(args)
    rows = {r["yol"]: r for r in read_rows(p)}
    items = build_items()
    byp = {i["path"]: i for i in items}
    todo = []
    for y, r in rows.items():
        it = byp.get(y)
        if it and os.path.basename(y).lower() in BIRAK:
            continue
        if it and (r["durum"] in ("HATA", "ZAYIF") or is_weak(r) or
                   (r["durum"] == "ENGEL-BAGIMLILIK" and "pip adı bilinmiyor" in r["kanit"]) or
                   r["durum"] == "ENGEL-LISANS" or
                   (r["durum"] == "DOKUMAN" and (it["primary"] != "doc" or "kurulu değil" in r["kanit"])) or
                   (r["durum"] == "BUYUK-SOR" and it["primary"] == "py" and (not heavy(it["work"]) or agir_hazir()))):
            todo.append(it)
    log("duzelt başladı: yeniden koşulacak=%d" % len(todo))
    cnt = collections.Counter()

    def work(it):
        while ram_pct() > RAM_MAX:
            time.sleep(15)
        if needs_install(it) and not disk_ok():
            cnt["disk-bekliyor"] += 1  # HATA/ZAYIF satırı korunur; yanlış-DOKUMAN ise artık doküman diye anılmaz
            if rows[it["path"]]["durum"] == "DOKUMAN":
                write_row(p, dict(yol=it["path"], remote=it["remote"], tur=it["tur"], durum="BEKLEMEDE",
                                  kanit="disk<%dGB: %s türü kurulum gerektiriyor, çalıştırılmadı (doküman değil)" % (MIN_FREE / 1e9, it["primary"])))
            return
        r = process(it)
        write_row(p, r)
        with _lock:
            cnt[r["durum"]] += 1

    with ThreadPoolExecutor(args.paralel) as ex:
        list(ex.map(work, todo))
    s = finalize(p, items)
    log("duzelt bitti: %s | bu koşu: %s" % (json.dumps(s["durum"], ensure_ascii=False), dict(cnt)))
    print(json.dumps(dict(bu_kosu=cnt, ozet=s["durum"]), ensure_ascii=False))


def _baska_kopya():
    """6 Kas: ayni anda iki calistir_hepsi calismasin (calistirma.tsv'ye iki yazar)."""
    try:
        import psutil
        me = os.getpid()
        for q in psutil.process_iter():
            try:
                if q.pid != me and "calistir_hepsi.py" in " ".join(q.cmdline() or []) and "pytest" not in " ".join(q.cmdline() or []):
                    return q.pid
            except Exception:
                pass
    except Exception:
        pass
    return None


if __name__ == "__main__":
    if (k := _baska_kopya()):
        print("baska calistir_hepsi calisiyor (pid %s), cikiliyor" % k)
        sys.exit(3)
    ap = argparse.ArgumentParser()
    ap.add_argument("--deneme", type=int)
    ap.add_argument("--tam", action="store_true")
    ap.add_argument("--tekrar", type=int)
    ap.add_argument("--duzelt", action="store_true")
    ap.add_argument("--agir-kur", action="store_true")
    ap.add_argument("--pnpm-olc", type=str, help="pnpm bağlantı ölçümü: repo yolları ';' ile")
    ap.add_argument("--paralel", type=int, default=6)
    a = ap.parse_args()
    a.paralel = max(1, min(6, a.paralel))
    DONMA.baslat()
    if a.agir_kur: print(agir_kur())
    elif a.pnpm_olc: print(json.dumps({r: nm_link_stats(os.path.join(r, "node_modules")) for r in a.pnpm_olc.split(";")}, ensure_ascii=False))
    elif a.tekrar: tekrar(a)
    elif a.duzelt: duzelt(a)
    elif a.tam or a.deneme: tam(a)
    else: ap.error("kip seç: --deneme N | --tam | --tekrar N | --duzelt")

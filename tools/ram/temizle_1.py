r"""Omer 10 Kas 02:52 onayi: Go onbellegi, Temp (2+ gun), npm/uv/pip onbellekleri, NetBeans (kullanici verisi), Thunderstore, DriverHub.
Sonra salt okuma: araclar/indir icerigi, model kullanim taramasi, C:\AI ve Program Files tam olcum. Cikti rapor/temizle-1.txt
  python -I tools/ram/temizle_1.py --arka"""
import glob, os, shutil, subprocess, sys, time
from pathlib import Path
import psutil

KOK = Path(r"C:\Projeler\omer-skills")
CIKTI = KOK / "rapor" / "temizle-1.txt"
if "--arka" in sys.argv:
    subprocess.Popen([sys.executable, "-I", __file__], creationflags=0x00000008 | 0x00000200 | 0x08000000, close_fds=True)
    print("arka planda basladi ->", CIKTI); sys.exit(0)
try:
    psutil.Process().nice(psutil.BELOW_NORMAL_PRIORITY_CLASS); psutil.Process().ionice(psutil.IOPRIO_LOW)
except Exception:
    pass
GW = 0x08000000
S = []
def yaz(*a):
    S.append(" ".join(str(x) for x in a))
    CIKTI.write_text("\n".join(S), encoding="utf-8")
def bos():
    return psutil.disk_usage("C:\\").free / 2**30
def adim(ad, f):
    b0 = bos()
    try:
        not_ = f() or ""
    except Exception as e:
        not_ = f"HATA {type(e).__name__}: {str(e)[:150]}"
    yaz(f"  {ad}: +{bos() - b0:.1f} GB (bos {bos():.1f} GB) {not_}")
def sil(p):
    p = Path(p)
    if not p.exists():
        return "yok"
    hata = []
    shutil.rmtree(p, onerror=lambda f, y, e: hata.append(y))
    return f"silinemeyen {len(hata)}" if hata else "tam"
def komut(*c, sure=1500):
    r = subprocess.run(list(c), capture_output=True, text=True, errors="replace", timeout=sure, creationflags=GW)
    return f"exit {r.returncode} {(r.stdout + r.stderr).strip()[-120:]}"

H = Path.home(); L = Path(os.environ["LOCALAPPDATA"]); R = H / "AppData" / "Roaming"
yap = Path(glob.glob(str(H / "Desktop" / "Claude ile yap*"))[0])
yaz(time.strftime("%Y-%m-%d %H:%M"), f"TEMIZLIK basladi; bos {bos():.1f} GB")
yaz("== SILME (onayli)")
def go():
    try:
        return komut("go", "clean", "-cache")
    except FileNotFoundError:
        return sil(L / "go-build")
adim("Go derleme onbellegi", go)
def temp():
    n = k = 0
    for e in os.scandir(L / "Temp"):
        try:
            son = e.stat(follow_symlinks=False).st_mtime
            if e.is_dir(follow_symlinks=False):
                for d, _, fs in os.walk(e.path):
                    for f in fs[:200]:
                        try:
                            son = max(son, os.stat(os.path.join(d, f)).st_mtime)
                        except OSError:
                            pass
                    if time.time() - son < 2 * 86400:
                        break
            if time.time() - son < 2 * 86400:
                k += 1; continue
            if e.is_dir(follow_symlinks=False):
                shutil.rmtree(e.path, ignore_errors=True)
            else:
                os.remove(e.path)
            n += 1
        except OSError:
            pass
    return f"silinen {n} oge, yeni oldugu icin kalan {k}"
adim("Temp (2+ gun)", temp)
adim("npm onbellegi", lambda: komut("npm.cmd", "cache", "clean", "--force"))
adim("uv onbellegi", lambda: komut("uv", "cache", "clean"))
adim("pip onbellegi", lambda: komut(sys.executable, "-m", "pip", "cache", "purge"))
adim("NetBeans (AppData/Local)", lambda: sil(L / "NetBeans"))
adim("Thunderstore Mod Manager", lambda: sil(R / "Thunderstore Mod Manager"))
adim("DriverHub", lambda: sil(R / "DriverHub"))
yaz(f"SILME BITTI; bos {bos():.1f} GB")

yaz("== araclar/indir icerigi")
ind = yap / "araclar" / "indir"
if ind.exists():
    for e in sorted(os.scandir(ind), key=lambda x: x.name)[:60]:
        try:
            b = sum(os.path.getsize(os.path.join(d, f)) for d, _, fs in os.walk(e.path) for f in fs) if e.is_dir() else e.stat().st_size
            yaz(f"  {b/2**20:8.0f} MB {'[klasor]' if e.is_dir() else '        '} {e.name[:80]}")
        except OSError:
            pass

yaz("== model kullanim taramasi (ad geciyor mu: betik/ayar/skill)")
ADLAR = ["vdn-minimax-h3-edge", "longcat-video", "minimax-h3", "qwen35-9b-glm51", "gemma4:12b", "gemma4:e4b", "gemma4", "qwen3.5:9b", "qwen3.5", "bge-m3", "Qwen3.5-4B", "XTTS", "chatterbox"]
vur = {a: [] for a in ADLAR}
kokler = [KOK / "tools", KOK / "skills", KOK / ".kos" / "kopru", H / ".claude" / "skills", H / ".claude-ollama", H / ".omniroute"] + [p for p in yap.iterdir() if p.is_dir() and p.name not in ("modeller", "araclar", "varliklar")]
UZ = (".py", ".json", ".md", ".cmd", ".ps1", ".toml", ".yaml", ".yml", ".env", ".mjs", ".js", ".txt", ".vbs")
t0 = time.time()
for k in kokler:
    for d, ds, fs in os.walk(k):
        ds[:] = [x for x in ds if x not in ("node_modules", ".git", "__pycache__", "venv", ".venv", "log", "rapor", "site-packages")]
        if d.count(os.sep) - str(k).count(os.sep) > 3 or time.time() - t0 > 600:
            ds[:] = []; continue
        for f in fs:
            if f.lower().endswith(UZ):
                p = os.path.join(d, f)
                try:
                    if os.path.getsize(p) > 1_500_000:
                        continue
                    t = open(p, encoding="utf-8", errors="replace").read()
                except OSError:
                    continue
                for a in ADLAR:
                    if a in t and len(vur[a]) < 40:
                        vur[a].append(p.replace(str(H), "~"))
for a in ADLAR:
    yaz(f"  {a}: {len(vur[a])} dosya | {[x[-60:] for x in vur[a][:5]]}")

def boyut(yol):
    top = 0
    for d, _, fs in os.walk(yol):
        for f in fs:
            try:
                top += os.stat(os.path.join(d, f), follow_symlinks=False).st_size
            except OSError:
                pass
    return top
for kok_ in (Path(r"C:\AI"), Path(r"C:\Program Files"), Path(r"C:\Program Files\Epic Games"), Path(r"C:\Program Files (x86)"), Path(r"C:\Program Files (x86)\Steam\steamapps\common"), Path(r"C:\Riot Games"), Path(r"C:\ProgramData")):
    if not kok_.exists():
        continue
    yaz(f"== {kok_} (tam olcum)")
    alt = []
    for e in os.scandir(kok_):
        try:
            if e.is_dir(follow_symlinks=False) and not e.is_symlink():
                alt.append((boyut(e.path), e.name))
        except OSError:
            pass
    alt.sort(reverse=True)
    yaz(f"  TOPLAM {sum(a for a, _ in alt)/2**30:.1f} GB")
    for b, ad in alt[:15]:
        if b > 2**30:
            yaz(f"  {b/2**30:7.1f} GB {ad[:60]}")
yaz("BITTI", time.strftime("%H:%M:%S"), f"bos {bos():.1f} GB")

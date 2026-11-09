r"""Derin disk olcumu (salt okuma, dusuk oncelik): buyuk klasorlerin alt kirilimi + son erisim yasi. Cikti rapor/olcum-derin.txt
  python -I tools/ram/olcum_derin.py --arka"""
import glob, json, os, subprocess, sys, time
from pathlib import Path
import psutil

KOK = Path(r"C:\Projeler\omer-skills")
CIKTI = KOK / "rapor" / "olcum-derin.txt"
if "--arka" in sys.argv:
    subprocess.Popen([sys.executable, "-I", __file__], creationflags=0x00000008 | 0x00000200 | 0x08000000, close_fds=True)
    print("arka planda basladi ->", CIKTI); sys.exit(0)
p = psutil.Process()
try:
    p.nice(psutil.IDLE_PRIORITY_CLASS); p.ionice(psutil.IOPRIO_VERYLOW)
except Exception:
    pass
S = []
def yaz(*a):
    S.append(" ".join(str(x) for x in a))
    CIKTI.write_text("\n".join(S), encoding="utf-8")

def boyut(yol, sure=120):
    t0, top, n, son = time.time(), 0, 0, 0.0
    yigin = [str(yol)]
    while yigin:
        if time.time() - t0 > sure:
            return top, n, son, True
        try:
            with os.scandir(yigin.pop()) as it:
                for e in it:
                    try:
                        if e.is_symlink():
                            continue
                        if e.is_dir(follow_symlinks=False):
                            yigin.append(e.path)
                        else:
                            st = e.stat(follow_symlinks=False)
                            top += st.st_size; n += 1
                            son = max(son, st.st_mtime)
                    except OSError:
                        pass
        except OSError:
            pass
    return top, n, son, False

def kirilim(yol, ilk=14, esik_gb=0.3, sure=90):
    yol = Path(yol)
    if not yol.exists():
        return
    yaz(f"== {yol}")
    alt = []
    dosya = 0
    try:
        for e in os.scandir(yol):
            try:
                if e.is_dir(follow_symlinks=False) and not e.is_symlink():
                    b, n, son, k = boyut(e.path, sure)
                    alt.append((b, n, son, k, e.name))
                elif e.is_file(follow_symlinks=False):
                    dosya += e.stat().st_size
            except OSError:
                pass
    except OSError as ex:
        yaz("  okunamadi", ex); return
    alt.sort(reverse=True)
    top = sum(a[0] for a in alt) + dosya
    yaz(f"  TOPLAM {top/2**30:.1f} GB ({len(alt)} klasor; kokteki dosyalar {dosya/2**30:.1f} GB)")
    for b, n, son, k, ad in alt[:ilk]:
        if b / 2**30 < esik_gb:
            break
        gun = int((time.time() - son) / 86400) if son else -1
        yaz(f"  {b/2**30:7.2f} GB {'*' if k else ' '} son degisiklik {gun:4} gun once | {ad[:60]}")

H = Path.home()
L = Path(os.environ["LOCALAPPDATA"])
yap = Path(glob.glob(str(H / "Desktop" / "Claude ile yap*"))[0])
d = psutil.disk_usage("C:\\")
yaz(time.strftime("%Y-%m-%d %H:%M"), f"C bos {d.free/2**30:.0f} GB / {d.total/2**30:.0f} GB")
for y in (H / ".cache", H / ".cache" / "huggingface" / "hub", KOK / ".kos", KOK / ".kos" / "kopru", L / "Temp", yap, yap / "araclar", H / ".venvs", H / ".claude", H / ".claude" / "plugins",
          H / ".ollama" / "models" / "manifests" / "registry.ollama.ai" / "library", L / "Programs", H / "AppData" / "Roaming", L, H):
    kirilim(y)
yaz("== C:\\ kok (ust duzey; her biri 150 sn tavan)")
for e in sorted(os.scandir("C:\\"), key=lambda x: x.name):
    try:
        if e.is_dir(follow_symlinks=False) and e.name not in ("Users", "Windows", "$Recycle.Bin", "System Volume Information"):
            b, n, son, k = boyut(e.path, 150)
            if b > 2**30:
                yaz(f"  {b/2**30:7.1f} GB {'*' if k else ' '} {e.name}")
    except OSError:
        pass
try:
    b, n, son, k = boyut("C:\\$Recycle.Bin", 60)
    yaz(f"  {b/2**30:7.1f} GB   Geri Donusum Kutusu")
except Exception:
    pass
try:
    r = subprocess.run(["ollama", "list"], capture_output=True, text=True, errors="replace", timeout=30, creationflags=0x08000000)
    yaz("== ollama list"); yaz(r.stdout[:1500])
except Exception as ex:
    yaz("ollama list yok", type(ex).__name__)
yaz("BITTI", time.strftime("%H:%M:%S"))

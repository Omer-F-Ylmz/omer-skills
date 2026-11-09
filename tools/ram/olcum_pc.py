r"""PC olcumu (salt okuma): disk adaylari, acilis programlari, zamanlanmis gorevler, servis/surec RAM. Cikti: rapor/olcum-pc.txt
  python -I tools/ram/olcum_pc.py            (on planda)
  python -I tools/ram/olcum_pc.py --arka     (ayrik; bitince rapor/olcum-pc.txt)"""
import os, subprocess, sys, time, winreg
from collections import Counter
from pathlib import Path
import psutil

KOK = Path(r"C:\Projeler\omer-skills")
CIKTI = KOK / "rapor" / "olcum-pc.txt"
if "--arka" in sys.argv:
    subprocess.Popen([sys.executable, "-I", __file__], creationflags=0x00000008 | 0x00000200 | 0x08000000, close_fds=True)
    print("arka planda basladi ->", CIKTI); sys.exit(0)
S = []
def yaz(*a):
    S.append(" ".join(str(x) for x in a))
    CIKTI.write_text("\n".join(S), encoding="utf-8")

def boyut(p, sure=25):
    t0, top, n = time.time(), 0, 0
    yigin = [str(p)]
    while yigin:
        if time.time() - t0 > sure:
            return top, n, True
        try:
            with os.scandir(yigin.pop()) as it:
                for e in it:
                    try:
                        if e.is_symlink():
                            continue
                        if e.is_dir(follow_symlinks=False):
                            yigin.append(e.path)
                        else:
                            top += e.stat(follow_symlinks=False).st_size; n += 1
                    except OSError:
                        pass
        except OSError:
            pass
    return top, n, False

H = Path.home()
L = Path(os.environ.get("LOCALAPPDATA", H / "AppData/Local"))
import glob
yap = glob.glob(str(H / "Desktop" / "Claude ile yap*"))
yap = Path(yap[0]) if yap else H / "Desktop"
v = psutil.virtual_memory(); d = psutil.disk_usage("C:\\")
yaz(time.strftime("%Y-%m-%d %H:%M"), f"RAM %{v.percent} | C bos {d.free//2**30} GB / {d.total//2**30} GB")
yaz("== TEK DOSYALAR")
for f in (r"C:\hiberfil.sys", r"C:\pagefile.sys", r"C:\swapfile.sys"):
    try:
        yaz(f"  {os.stat(f).st_size/2**30:6.1f} GB {f}")
    except OSError as e:
        yaz("  ?", f, type(e).__name__)
yaz("== KLASORLER (25 sn tavan; * = kismi)")
ad = [L / "Temp", Path(r"C:\Windows\Temp"), Path(r"C:\Windows\SoftwareDistribution\Download"), L / "npm-cache", H / "AppData/Roaming/npm-cache",
      L / "uv", L / "pip", H / ".cache", H / ".pnpm-cache", H / ".nuget", H / ".cargo", H / ".rustup", H / ".gradle", H / ".m2", H / ".ollama", H / ".lmstudio",
      H / "Downloads", L / "Docker", L / "Packages", L / "CrashDumps", H / ".claude", H / ".claude-mem", H / ".claude-mem-yedek-20260922",
      KOK / ".kos", KOK / "docs", KOK, yap / "araclar", yap / "borsa-botu", yap, H / "opensource-staging", H / "postiz-yedek", H / "postiz-test",
      H / "u3d-src", H / "u3d-venv", H / "tts-venv", H / "tts-work", H / "StoryToolkitAI", H / "Flashpoint", H / "source", H / "araclar-lc", H / ".venvs"]
sonuc = []
for p in ad:
    if p.exists():
        b, n, kismi = boyut(p)
        sonuc.append((b, n, kismi, p))
        yaz(f"  {b/2**30:7.2f} GB {n:8} dosya {'*' if kismi else ' '} {p}")
yaz("== ACILIS (Run anahtarlari + Baslangic klasoru)")
for kok, yol in ((winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Run"), (winreg.HKEY_LOCAL_MACHINE, r"Software\Microsoft\Windows\CurrentVersion\Run"),
                 (winreg.HKEY_LOCAL_MACHINE, r"Software\WOW6432Node\Microsoft\Windows\CurrentVersion\Run")):
    try:
        with winreg.OpenKey(kok, yol) as k:
            i = 0
            while True:
                try:
                    a, deger, _ = winreg.EnumValue(k, i); i += 1
                    yaz(f"  {'HKCU' if kok == winreg.HKEY_CURRENT_USER else 'HKLM'} {a}: {str(deger)[:110]}")
                except OSError:
                    break
    except OSError:
        pass
bas = H / "AppData/Roaming/Microsoft/Windows/Start Menu/Programs/Startup"
if bas.exists():
    for f in bas.iterdir():
        yaz("  Baslangic:", f.name)
yaz("== ZAMANLANMIS GOREVLER (Microsoft disi)")
r = subprocess.run(["schtasks", "/Query", "/FO", "CSV", "/V"], capture_output=True, creationflags=0x08000000)
metin = r.stdout.decode("cp857", "replace")
import csv, io
satir = list(csv.reader(io.StringIO(metin)))
if satir:
    bas_ = satir[0]
    gor = set()
    for x in satir[1:]:
        if len(x) < 9 or x[1] == bas_[1] or x[1].startswith("\\Microsoft") or x[1] in gor:
            continue
        gor.add(x[1])
        yaz(f"  {x[1][:45]:45} | {x[3][:12]:12} | {x[8][:95]}")
yaz("== SERVISLER (calisan, RAM'e gore ilk 25)")
sv = []
for s in psutil.win_service_iter():
    try:
        i = s.as_dict()
        if i["status"] == "running" and i["pid"]:
            sv.append((psutil.Process(i["pid"]).memory_info().rss, i["name"], i["display_name"], i["start_type"]))
    except Exception:
        pass
for m, n, dn, st in sorted(sv, reverse=True)[:25]:
    yaz(f"  {m//2**20:5} MB {n[:28]:28} {st[:9]:9} {dn[:50]}")
yaz("== SUREC GRUPLARI (RAM)")
g = Counter(); c = Counter()
for p in psutil.process_iter(["name", "memory_info"]):
    try:
        g[p.info["name"]] += p.info["memory_info"].rss; c[p.info["name"]] += 1
    except Exception:
        pass
for n, m in g.most_common(25):
    yaz(f"  {m//2**20:6} MB x{c[n]:3} {n}")
yaz("BITTI", time.strftime("%H:%M:%S"))

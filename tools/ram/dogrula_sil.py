r"""Silme adaylarini dogrular (salt okuma, dusuk oncelik). Cikti rapor/dogrula-sil.txt
  python -I tools/ram/dogrula_sil.py --arka"""
import csv, glob, json, os, subprocess, sys, time
from collections import Counter, defaultdict
from pathlib import Path
import psutil

KOK = Path(r"C:\Projeler\omer-skills")
CIKTI = KOK / "rapor" / "dogrula-sil.txt"
if "--arka" in sys.argv:
    subprocess.Popen([sys.executable, "-I", __file__], creationflags=0x00000008 | 0x00000200 | 0x08000000, close_fds=True)
    print("arka planda basladi ->", CIKTI); sys.exit(0)
try:
    psutil.Process().nice(psutil.IDLE_PRIORITY_CLASS); psutil.Process().ionice(psutil.IOPRIO_VERYLOW)
except Exception:
    pass
csv.field_size_limit(10**9)
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
                            top += st.st_size; n += 1; son = max(son, st.st_mtime)
                    except OSError:
                        pass
        except OSError:
            pass
    return top, n, son, False

def gun(t):
    return int((time.time() - t) / 86400) if t else -1

H = Path.home(); L = Path(os.environ["LOCALAPPDATA"]); R = H / "AppData" / "Roaming"
yap = Path(glob.glob(str(H / "Desktop" / "Claude ile yap*"))[0])
ar = yap / "araclar"
ESKI = ["link27", "link30eki", "link30eki-2", "indir", "ana-liste-npm-2"]
yaz(time.strftime("%Y-%m-%d %H:%M"), "DOGRULAMA")

yaz("== 1 ESKI KLONLAR: kurulu bir sey bu klasorlerden calisiyor mu")
kul = defaultdict(list)
son = {}
for r in csv.DictReader(open(KOK / "docs/video-tarama/kurulum-d2-sonuc.tsv", encoding="utf-8", errors="replace"), delimiter="\t"):
    son[r["kalem"]] = r
for k, r in son.items():
    if r["durum"].startswith("KURULDU") or r["durum"] == "ZATEN":
        y = (r.get("yol") or "") + " " + (r.get("kanit") or "")
        for e in ESKI:
            if f"araclar\\{e}\\" in y or f"araclar/{e}/" in y:
                kul[e].append(k)
def metin_ara(dosyalar, etiket):
    for f in dosyalar:
        try:
            if os.path.getsize(f) > 3_000_000:
                continue
            t = open(f, encoding="utf-8", errors="replace").read()
        except OSError:
            continue
        for e in ESKI:
            if f"araclar\\{e}\\" in t or f"araclar/{e}/" in t or f"araclar\\\\{e}\\\\" in t:
                kul[e].append(f"{etiket}:{Path(f).name if etiket != 'pkg' else Path(f).parent.name}")
metin_ara(glob.glob(str(H / ".local/bin/*.cmd")) + glob.glob(str(H / ".local/bin/*.bat")) + glob.glob(str(H / ".local/bin/*.ps1")), "shim")
metin_ara([str(H / ".claude.json"), str(H / ".claude/settings.json"), str(H / ".claude/mcp-paylasim/sunucular.json")] + glob.glob(str(L / "Claude-Data/*/claude_desktop_config.json")) + glob.glob(str(KOK / "tools/mcp-launch/*.cmd")), "ayar")
metin_ara(glob.glob(str(H / ".venvs/*/Lib/site-packages/*/direct_url.json")) + glob.glob(str(H / ".venvs/*/Lib/site-packages/*.pth")) + glob.glob(str(H / ".venvs/*/Lib/site-packages/__editable__*"))
          + glob.glob(str(R / "uv/tools/*/Lib/site-packages/*/direct_url.json")) + glob.glob(str(R / "uv/tools/*/Lib/site-packages/*.pth")), "pkg")
for d in (R / "npm/node_modules", H / ".claude/skills", ar / "ana-liste-npm/node_modules"):
    try:
        for e in os.scandir(d):
            try:
                if e.is_symlink() or os.path.islink(e.path) or (os.stat(e.path, follow_symlinks=False).st_file_attributes & 0x400):
                    hedef = os.path.realpath(e.path)
                    for x in ESKI:
                        if f"araclar\\{x}\\" in hedef:
                            kul[x].append(f"baglanti:{e.name}")
            except OSError:
                pass
    except OSError:
        pass
for e in ESKI:
    p = ar / e
    if p.exists():
        b, n, s, k = boyut(p)
        yaz(f"  {e}: {b/2**30:.1f} GB{'*' if k else ''}, son degisiklik {gun(s)} gun | kullanan {len(kul[e])}: {kul[e][:12]}")

yaz("== 2 TEMP: yasa gore (ust duzey ogeler)")
kova = Counter(); adet = Counter()
for e in os.scandir(L / "Temp"):
    try:
        if e.is_dir(follow_symlinks=False):
            b, n, s, k = boyut(e.path, 20)
        else:
            st = e.stat(); b, s = st.st_size, st.st_mtime
        g = gun(s)
        kv = "0-1 gun" if g < 2 else "2-7 gun" if g < 8 else "8+ gun"
        kova[kv] += b; adet[kv] += 1
    except OSError:
        pass
for kv in ("0-1 gun", "2-7 gun", "8+ gun"):
    yaz(f"  {kv}: {kova[kv]/2**30:.1f} GB ({adet[kv]} oge)")
b, n, s, k = boyut(L / "go-build", 180)
yaz(f"  go-build onbellegi: {b/2**30:.1f} GB{'*' if k else ''} (go clean -cache ile temizlenir)")

yaz("== 3 MODELLER")
for kok_ in (yap / "modeller", H / ".cache/huggingface/hub", H / ".ollama/models/blobs", H / ".lmstudio/models", yap / "araclar/chatterbox"):
    if not kok_.exists():
        continue
    yaz(f"  -- {kok_}")
    if kok_.name == "blobs":
        b, n, s, k = boyut(kok_); yaz(f"     {b/2**30:.1f} GB {n} dosya"); continue
    alt = []
    for e in os.scandir(kok_):
        try:
            if e.is_dir(follow_symlinks=False):
                b, n, s, k = boyut(e.path, 60)
                at = max((x.stat().st_atime for x in os.scandir(e.path)), default=0)
                alt.append((b, s, at, e.name))
            else:
                st = e.stat(); alt.append((st.st_size, st.st_mtime, st.st_atime, e.name))
        except OSError:
            pass
    for b, s, at, ad in sorted(alt, reverse=True)[:25]:
        if b > 0.2 * 2**30:
            yaz(f"     {b/2**30:6.1f} GB degisiklik {gun(s):4} gun | erisim {gun(at):4} gun | {ad[:70]}")
try:
    for f in glob.glob(str(H / ".ollama/models/manifests/registry.ollama.ai/library/*/*")):
        j = json.load(open(f, encoding="utf-8"))
        yaz(f"     ollama {Path(f).parent.name}:{Path(f).name} {sum(x.get('size', 0) for x in j.get('layers', []))/2**30:.1f} GB degisiklik {gun(os.path.getmtime(f))} gun")
except Exception as ex:
    yaz("     ollama manifest okunamadi", type(ex).__name__)

yaz("== 4 ESKI KAYIT/LOG (yasa gore)")
for ad, kok_, uz in (("CC oturum kayitlari (.claude/projects)", H / ".claude/projects", ".jsonl"), ("kopru log", KOK / ".kos/kopru/log", ""), ("kopru rapor", KOK / ".kos/kopru/rapor", ""), ("kopru park", KOK / ".kos/kopru/park", "")):
    kova = Counter()
    for d, _, fs in os.walk(kok_):
        for f in fs:
            try:
                st = os.stat(os.path.join(d, f))
                g = gun(st.st_mtime)
                kova["0-3 gun" if g < 4 else "4-14 gun" if g < 15 else "15+ gun"] += st.st_size
            except OSError:
                pass
    yaz(f"  {ad}: " + " | ".join(f"{k} {kova[k]/2**30:.1f} GB" for k in ("0-3 gun", "4-14 gun", "15+ gun")))

yaz("== 5 KARANTINA")
for d in sorted((KOK / ".kos/karantina").iterdir()):
    if d.is_dir():
        b, n, s, k = boyut(d, 60)
        yaz(f"  {d.name}: {b/2**30:.2f} GB, {len(list(d.iterdir()))} oge, son {gun(s)} gun")

yaz("== 6 DIGER")
for ad, p in (("Opera onbellek", R / "Opera Software/Opera Stable/Default/Cache"), ("Opera GX onbellek", R / "Opera Software/Opera GX Stable/Default/Cache"), ("Opera (Local) onbellek", L / "Opera Software"),
              ("ms-playwright", L / "ms-playwright"), ("NetBeans", L / "NetBeans"), ("Thunderstore", R / "Thunderstore Mod Manager"), ("DriverHub", R / "DriverHub"),
              ("uv cache", L / "uv/cache"), ("npm-cache", L / "npm-cache"), ("pip cache", L / "pip/cache"), ("cargo registry", H / ".cargo/registry"), ("codex-runtimes", H / ".cache/codex-runtimes"),
              ("u3d-venv", H / "u3d-venv"), ("tts-venv", H / "tts-venv"), ("Geri Donusum", Path("C:\\$Recycle.Bin"))):
    if p.exists():
        b, n, s, k = boyut(p, 90)
        yaz(f"  {ad}: {b/2**30:.1f} GB{'*' if k else ''}, son degisiklik {gun(s)} gun")
if (L / "ms-playwright").exists():
    yaz("  playwright surumleri:", sorted(x.name for x in (L / "ms-playwright").iterdir())[:30])
yaz("BITTI", time.strftime("%H:%M:%S"))

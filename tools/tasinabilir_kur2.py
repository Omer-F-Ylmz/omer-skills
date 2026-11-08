import subprocess as s, time, sys, os, json, hashlib, zipfile, urllib.request, re
LOGP = r"C:\Projeler\omer-skills\.kos\kopru\log\tasinabilir_kur2.log"
if len(sys.argv) < 2:
    s.Popen([sys.executable, __file__, "calis"], creationflags=0x00000008 | 0x00000200 | 0x08000000, close_fds=True)
    print("arka planda basladi"); sys.exit(0)
try:
    import psutil; psutil.Process().nice(psutil.BELOW_NORMAL_PRIORITY_CLASS)
except Exception: pass
LOG = open(LOGP, "w", encoding="utf-8", buffering=1)
TSV = r"C:\Projeler\omer-skills\rapor\tasinabilir-kur-sonuc.tsv"
def p(*a): print(time.strftime("%H:%M:%S"), *a, file=LOG)
def get(u, acc="application/vnd.github+json"): return urllib.request.urlopen(urllib.request.Request(u, headers={"User-Agent": "kurulum", "Accept": acc}), timeout=600).read()
KOK = os.path.join(os.environ["USERPROFILE"], "Desktop", "Claude ile yap\u0131lanlar", "araclar", "dil")
os.makedirs(os.path.join(KOK, "_indir"), exist_ok=True)
yollar, sonuc = [], []
def kur(ad, ver, url, algo, beklenen, kontrol):
    hedef = os.path.join(KOK, f"{ad}-{ver}")
    try:
        if os.path.exists(os.path.join(hedef, kontrol)):
            yollar.append(os.path.dirname(os.path.join(hedef, kontrol))); return "ZATEN", os.path.join(hedef, kontrol)
        if "github.com" in url:
            d = os.path.join(KOK, "_indir", ad + "-gh"); os.makedirs(d, exist_ok=True)
            repo = "/".join(url.split("/")[3:5]); tag = url.split("/")[-2]; ad_d = url.split("/")[-1]
            s.run(["gh", "release", "download", tag, "--repo", repo, "--pattern", ad_d, "--dir", d, "--clobber"], capture_output=True, timeout=900)
            veri = open(os.path.join(d, ad_d), "rb").read()
        else:
            veri = get(url, "*/*")
        h = hashlib.new(algo, veri).hexdigest()
        if h.lower() != beklenen.lower(): p(ad, "HASH UYUSMADI", h, beklenen); return "HATA", f"{algo} uyusmadi"
        f = os.path.join(KOK, "_indir", url.split("/")[-1]); open(f, "wb").write(veri)
        zipfile.ZipFile(f).extractall(hedef)
        for kok, ds, fs in os.walk(hedef):
            if os.path.basename(kontrol) in fs:
                k = os.path.join(kok, os.path.basename(kontrol)); yollar.append(kok); p(ad, "KURULDU", k); return "KURULDU", k
        return "HATA", "acildi ama " + kontrol + " yok"
    except Exception as e:
        p(ad, "HATA", repr(e)); return "HATA", repr(e)[:200]
def gh_varlik(repo, desen):
    rel = json.loads(s.run(["gh", "api", f"repos/{repo}/releases/latest"], capture_output=True, text=True, encoding="utf-8", timeout=120).stdout)
    a = [x for x in rel["assets"] if re.fullmatch(desen, x["name"])][0]
    return rel["tag_name"], a["browser_download_url"], a.get("digest", "").replace("sha256:", "")
try:
    v, u, d = gh_varlik("typst/typst", r"typst-x86_64-pc-windows-msvc\.zip")
    sonuc.append(("typst", v) + kur("typst", v, u, "sha256", d, "typst.exe"))
except Exception as e: sonuc.append(("typst", "?", "HATA", repr(e)[:200]))
try:
    v, u, d = gh_varlik("containers/podman", r"podman-remote-release-windows_amd64\.zip")
    sonuc.append(("podman", v) + kur("podman", v, u, "sha256", d, "podman.exe"))
except Exception as e: sonuc.append(("podman", "?", "HATA", repr(e)[:200]))
if False:
    sayfa = get("https://www.sqlite.org/download.html", "text/html").decode("utf-8", "ignore")
    m = re.search(r"PRODUCT,([\d.]+),(\d{4}/sqlite-tools-win-x64-\d+\.zip),\d+,([0-9a-f]{64})", sayfa)
    v, yol, sha3 = m.group(1), m.group(2), m.group(3)
    sonuc.append(("sqlite", v) + kur("sqlite", v, "https://www.sqlite.org/" + yol, "sha3_256", sha3, "sqlite3.exe"))

if yollar:
    cur = s.run(["powershell", "-NoProfile", "-Command", "[Environment]::GetEnvironmentVariable('Path','User')"], capture_output=True, text=True, errors="ignore").stdout.strip()
    ek = [y for y in dict.fromkeys(yollar) if y.lower() not in cur.lower()]
    if ek:
        s.run(["powershell", "-NoProfile", "-Command", "[Environment]::SetEnvironmentVariable('Path', $env:YENI_PATH, 'User')"], env={**os.environ, "YENI_PATH": cur.rstrip(";") + ";" + ";".join(ek)})
        p("PATH'e eklendi", ek)
dog = {"typst": ["--version"], "podman": ["--version"], "sqlite": ["--version"]}
with open(TSV, "a", encoding="utf-8") as t:
    for ad, v, d, n in sonuc:
        dg = ""
        if d in ("KURULDU", "ZATEN"):
            try:
                x = s.run([n] + dog[ad], capture_output=True, text=True, errors="ignore", timeout=60)
                dg = ((x.stdout + x.stderr).strip().splitlines() or [f"exit {x.returncode}"])[0][:120]
            except Exception as e: dg = "HATA " + repr(e)[:80]
        t.write(f"{ad}\t{v}\t{d}\t{n}\t{dg}\n"); p("SONUC", ad, v, d, dg)
p("BITTI")

import subprocess as s, time, sys, os, json, hashlib, zipfile, urllib.request, re
LOGP = r"C:\Projeler\omer-skills\.kos\kopru\log\tasinabilir_kur.log"
if len(sys.argv) < 2:
    s.Popen([sys.executable, __file__, "calis"], creationflags=0x00000008 | 0x00000200 | 0x08000000, close_fds=True)
    print("arka planda basladi"); sys.exit(0)
LOG = open(LOGP, "w", encoding="utf-8", buffering=1)
TSV = r"C:\Projeler\omer-skills\rapor\tasinabilir-kur-sonuc.tsv"
def p(*a): print(time.strftime("%H:%M:%S"), *a, file=LOG)
def get(u): return urllib.request.urlopen(urllib.request.Request(u, headers={"User-Agent": "kurulum", "Accept": "application/vnd.github+json"}), timeout=300).read()
KOK = os.path.join(os.environ["USERPROFILE"], "Desktop", "Claude ile yap\u0131lanlar", "araclar", "dil")
os.makedirs(os.path.join(KOK, "_indir"), exist_ok=True)
yollar = []
def kur(ad, url, sha, alt_kontrol, ver):
    hedef = os.path.join(KOK, f"{ad}-{ver}")
    try:
        if os.path.exists(os.path.join(hedef, alt_kontrol)):
            yollar.append(os.path.dirname(os.path.join(hedef, alt_kontrol))); p(ad, "ZATEN", hedef); return "ZATEN", hedef
        veri = get(url); h = hashlib.sha256(veri).hexdigest()
        if h.lower() != sha.lower(): p(ad, "SHA256 UYUSMADI", h, sha); return "HATA", "sha256 uyusmadi"
        f = os.path.join(KOK, "_indir", url.split("/")[-1]); open(f, "wb").write(veri)
        zipfile.ZipFile(f).extractall(hedef)
        k = os.path.join(hedef, alt_kontrol)
        if not os.path.exists(k):
            for d in os.listdir(hedef):
                if os.path.exists(os.path.join(hedef, d, alt_kontrol)): k = os.path.join(hedef, d, alt_kontrol); break
        if not os.path.exists(k): p(ad, "acildi ama yok", alt_kontrol); return "HATA", "acildi ama " + alt_kontrol + " yok"
        yollar.append(os.path.dirname(k)); p(ad, "KURULDU", k); return "KURULDU", k
    except Exception as e:
        p(ad, "HATA", repr(e)); return "HATA", repr(e)[:200]
sonuc = []
try:
    rel = json.loads(get("https://api.github.com/repos/helm/helm/releases/latest")); v = rel["tag_name"]
    u = f"https://get.helm.sh/helm-{v}-windows-amd64.zip"; sha = get(u + ".sha256sum").decode().split()[0]
    sonuc.append(("helm", v) + kur("helm", u, sha, r"windows-amd64\helm.exe", v))
except Exception as e: sonuc.append(("helm", "?", "HATA", repr(e)[:200]))
try:
    idx = json.loads(get("https://ziglang.org/download/index.json")); v = idx["master"]["version"] if False else max((k for k in idx if re.match(r"^\d+\.\d+\.\d+$", k)), key=lambda k: [int(x) for x in k.split(".")])
    a = idx[v]["x86_64-windows"]; sonuc.append(("zig", v) + kur("zig", a["tarball"], a["shasum"], "zig.exe", v))
except Exception as e: sonuc.append(("zig", "?", "HATA", repr(e)[:200]))
try:
    idx = json.loads(get("https://api.releases.hashicorp.com/v1/releases/terraform/latest"))
    v = idx["version"]; b = [x for x in idx["builds"] if x["os"] == "windows" and x["arch"] == "amd64"][0]
    sums = get(idx["url_shasums"]).decode(); sha = [l.split()[0] for l in sums.splitlines() if l.endswith(b["url"].split("/")[-1])][0]
    sonuc.append(("terraform", v) + kur("terraform", b["url"], sha, "terraform.exe", v))
except Exception as e: sonuc.append(("terraform", "?", "HATA", repr(e)[:200]))
try:
    rel = json.loads(get("https://api.github.com/repos/JetBrains/kotlin/releases/latest")); v = rel["tag_name"].lstrip("v")
    a = [x for x in rel["assets"] if x["name"] == f"kotlin-compiler-{v}.zip"][0]
    sha = a.get("digest", "").replace("sha256:", "") or get(a["browser_download_url"] + ".sha256").decode().split()[0]
    sonuc.append(("kotlin", v) + kur("kotlin", a["browser_download_url"], sha, r"kotlinc\bin\kotlinc.bat", v))
except Exception as e: sonuc.append(("kotlin", "?", "HATA", repr(e)[:200]))
try:
    v = json.loads(get("https://storage.googleapis.com/dart-archive/channels/stable/release/latest/VERSION"))["version"]
    u = f"https://storage.googleapis.com/dart-archive/channels/stable/release/{v}/sdk/dartsdk-windows-x64-release.zip"
    sha = get(u + ".sha256sum").decode().split()[0]
    sonuc.append(("dart", v) + kur("dart", u, sha, r"dart-sdk\bin\dart.exe", v))
except Exception as e: sonuc.append(("dart", "?", "HATA", repr(e)[:200]))
if yollar:
    cur = s.run(["powershell", "-NoProfile", "-Command", "[Environment]::GetEnvironmentVariable('Path','User')"], capture_output=True, text=True, errors="ignore").stdout.strip()
    ek = [y for y in yollar if y.lower() not in cur.lower()]
    if ek:
        yeni = cur.rstrip(";") + ";" + ";".join(ek)
        s.run(["powershell", "-NoProfile", "-Command", "[Environment]::SetEnvironmentVariable('Path', $env:YENI_PATH, 'User')"], env={**os.environ, "YENI_PATH": yeni})
        p("PATH'e eklendi", ek)
dogrula = {"helm": ["version", "--short"], "zig": ["version"], "terraform": ["version"], "kotlin": ["-version"], "dart": ["--version"]}
with open(TSV, "w", encoding="utf-8") as t:
    t.write("kalem\tsurum\tdurum\tnot\tdogrulama\n")
    for ad, v, d, n in sonuc:
        dg = ""
        if d in ("KURULDU", "ZATEN"):
            try:
                x = s.run([n] + dogrula[ad], capture_output=True, text=True, errors="ignore", timeout=120, shell=n.endswith(".bat"))
                dg = (x.stdout + x.stderr).strip().splitlines()[0][:120] if (x.stdout + x.stderr).strip() else f"exit {x.returncode}"
            except Exception as e: dg = "HATA " + repr(e)[:80]
        t.write(f"{ad}\t{v}\t{d}\t{n}\t{dg}\n"); p("SONUC", ad, v, d, dg)
p("BITTI")

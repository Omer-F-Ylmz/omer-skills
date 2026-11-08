import subprocess as s, time, sys, os, re, hashlib, urllib.request, zipfile
LOGP = r"C:\Projeler\omer-skills\.kos\kopru\log\nmap_zip_kur.log"
if len(sys.argv) < 2:
    s.Popen([sys.executable, __file__, "calis"], creationflags=0x00000008 | 0x00000200 | 0x08000000, close_fds=True)
    print("arka planda basladi"); sys.exit(0)
LOG = open(LOGP, "w", encoding="utf-8", buffering=1)
def p(*a): print(time.strftime("%H:%M:%S"), *a, file=LOG)
def get(u): return urllib.request.urlopen(urllib.request.Request(u, headers={"User-Agent": "kurulum"}), timeout=120).read()
try:
    liste = get("https://nmap.org/dist/").decode("utf-8", "ignore")
    zips = sorted(set(re.findall(r'nmap-(\d+\.\d+)-win32\.zip', liste)), key=lambda v: [int(x) for x in v.split(".")])
    v = zips[-1]; ad = f"nmap-{v}-win32.zip"; p("surum", v)
    dig = get(f"https://nmap.org/dist/sigs/{ad}.digest.txt").decode("utf-8", "ignore")
    m = re.search(r"SHA256\s*=\s*([0-9A-F\s]+?)(?:\n\S|\Z)", dig, re.I)
    beklenen = re.sub(r"\s", "", m.group(1)).lower(); p("beklenen sha256", beklenen)
    if len(beklenen) != 64: p("SONUC HATA digest okunamadi", repr(dig[:400])); sys.exit(1)
    kok = os.path.join(os.environ["USERPROFILE"], "Desktop", "Claude ile yap\u0131lanlar", "araclar", "guvenlik")
    ind = os.path.join(kok, "_indir"); os.makedirs(ind, exist_ok=True)
    f = os.path.join(ind, ad)
    veri = get(f"https://nmap.org/dist/{ad}"); open(f, "wb").write(veri)
    h = hashlib.sha256(veri).hexdigest(); p("indirilen sha256", h)
    if h != beklenen: p("SONUC HATA sha256 uyusmadi"); sys.exit(1)
    zipfile.ZipFile(f).extractall(kok)
    hedef = os.path.join(kok, f"nmap-{v}")
    exe = os.path.join(hedef, "nmap.exe"); p("nmap.exe", os.path.exists(exe))
    yol = s.run(["powershell", "-NoProfile", "-Command", "[Environment]::GetEnvironmentVariable('Path','User')"], capture_output=True, text=True, errors="ignore").stdout.strip()
    if hedef.lower() not in yol.lower():
        s.run(["powershell", "-NoProfile", "-Command", f"[Environment]::SetEnvironmentVariable('Path', ([Environment]::GetEnvironmentVariable('Path','User').TrimEnd(';') + ';{hedef}'), 'User')"])
        p("PATH'e eklendi", hedef)
    r = s.run([exe, "--version"], capture_output=True, text=True, errors="ignore", timeout=60)
    p("version:", r.stdout.strip()[:200])
    r = s.run([exe, "-sT", "-p", "135,445", "127.0.0.1", "-Pn"], capture_output=True, text=True, errors="ignore", timeout=120)
    p("-sT test exit", r.returncode, r.stdout.strip()[-400:])
    with open(r"C:\Projeler\omer-skills\rapor\kurulum-guvenlik-sonuc.tsv", "a", encoding="utf-8") as t:
        t.write(f"nmap\tzip-tasinabilir\t{'KURULDU' if r.returncode == 0 else 'HATA'}\t{hedef} (Npcap yok: -sT calisir, ham paket -sS icin Npcap gerekir)\n")
    p("SONUC", "KURULDU" if r.returncode == 0 else "HATA")
except Exception as e:
    p("SONUC HATA", repr(e))

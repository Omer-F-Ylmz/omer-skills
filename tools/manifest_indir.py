import subprocess as s, json, os, sys, time, hashlib, re, urllib.request, base64
if len(sys.argv) < 2:
    s.Popen([sys.executable, __file__, "calis"], creationflags=0x00000008 | 0x00000200 | 0x08000000, close_fds=True)
    print("arka planda basladi"); sys.exit(0)
LOG = open(r"C:\Projeler\omer-skills\.kos\kopru\log\manifest_indir.log", "w", encoding="utf-8", buffering=1)
def p(*a): print(time.strftime("%H:%M:%S"), *a, file=LOG)
IND = os.path.join(os.environ["USERPROFILE"], "Desktop", "Claude ile yap\u0131lanlar", "araclar", "_yonetici_indir")
os.makedirs(IND, exist_ok=True)
def gh(path):
    r = s.run(["gh", "api", path], capture_output=True, text=True, encoding="utf-8", timeout=120)
    return json.loads(r.stdout)
def son_surum(yol):
    ds = [d["name"] for d in gh(f"repos/microsoft/winget-pkgs/contents/manifests/{yol}") if d["type"] == "dir"]
    def k(v): return [int(x) if x.isdigit() else 0 for x in re.split(r"[.\-]", v)]
    return sorted(ds, key=k)[-1]
def yaml_al(yol, ver, pid):
    c = gh(f"repos/microsoft/winget-pkgs/contents/manifests/{yol}/{ver}/{pid}.installer.yaml")
    return base64.b64decode(c["content"]).decode("utf-8")
def alan(y, ad):
    m = re.search(rf"^\s*-?\s*{ad}:\s*(.+)$", y, re.M); return m.group(1).strip().strip("'\"") if m else ""
KALEMLER = [("Microsoft.VCRedist.2015+.x64", "m/Microsoft/VCRedist/2015+/x64"),
            ("PostgreSQL.PostgreSQL.17", "p/PostgreSQL/PostgreSQL/17"),
            ("Nvidia.CUDA", "n/Nvidia/CUDA")]
plan = []
for pid, yol in KALEMLER:
    try:
        ver = son_surum(yol); y = yaml_al(yol, ver, pid)
        blok = y
        m = re.search(r"Architecture:\s*x64(.*?)(?=\n\s*- Architecture:|\Z)", y, re.S)
        if m: blok = m.group(0)
        url, sha = alan(blok, "InstallerUrl"), alan(blok, "InstallerSha256")
        sessiz = alan(blok, "Silent") or alan(y, "Silent")
        p(pid, ver, url, sha[:16], "sessiz:", sessiz)
        f = os.path.join(IND, url.split("/")[-1].split("?")[0] or (pid + ".exe"))
        if not (os.path.exists(f) and hashlib.sha256(open(f, "rb").read()).hexdigest().lower() == sha.lower()):
            req = urllib.request.Request(url, headers={"User-Agent": "winget-cli"})
            with urllib.request.urlopen(req, timeout=3600) as r, open(f, "wb") as o:
                while True:
                    b = r.read(1 << 20)
                    if not b: break
                    o.write(b)
        h = hashlib.sha256(open(f, "rb").read()).hexdigest()
        ok = h.lower() == sha.lower()
        p(pid, "SHA256", "DOGRU" if ok else f"UYUSMADI {h}", os.path.getsize(f) // (1 << 20), "MB")
        if ok: plan.append({"id": pid, "surum": ver, "dosya": f, "sessiz": sessiz})
    except Exception as e:
        p(pid, "HATA", repr(e)[:300])
json.dump(plan, open(os.path.join(IND, "plan.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
p("BITTI plan", len(plan), "kalem ->", os.path.join(IND, "plan.json"))

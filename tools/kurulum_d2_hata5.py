"""D2-HATA-5: hata4 sonrası kalan 8 HATA — doğru kurulum yolu (Go zip kullanıcı alanına, pnpm/bun çalışma alanı, Blender eklentisi, uv py sürümü) ya da kanıtlı sınıf.
Kullanım: python tools/kurulum_d2_hata5.py [--bolum gsd,go,ws,blender,leann,sound,opengym]"""
import io, json, os, re, shutil, sys, urllib.request, zipfile, glob
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, str(Path(__file__).parent))
import kurulum_d2_hata2 as H

D = H.D
BOL = set(H._a[H._a.index("--bolum") + 1].split(",")) if "--bolum" in H._a else {"gsd", "go", "ws", "blender", "leann", "sound", "opengym"}
son, yaz = H.son, H.yaz
NPM2 = D.NPMDIR.parent / "ana-liste-npm-2"
GOKOK = Path.home() / ".local/go"


def satir(k):
    r = son().get(k)
    return r if r and r["durum"] in ("HATA", "KURULDU-DOGRULANMADI") else None


def bolum_gsd():
    p = NPM2 / "node_modules/@opengsd/gsd-core/package.json"
    for k in ("GSD Core (open-gsd/gsd-core)", "open-gsd/gsd-core"):
        r = son().get(k)
        if r and r["durum"] != "KURULDU" and p.exists():
            v = json.loads(p.read_text(encoding="utf-8")).get("version")
            yaz(r, "KURULDU", f"npm @opengsd/gsd-core {v} ana-liste-npm-2 (klon build betiği Windows'ta code 1)", f"{p} var, version {v}")
            print("KURULDU", k, v, flush=True)


def bolum_go():
    r = satir("usestrix/strix")
    if not r:
        return
    go = GOKOK / "bin/go.exe"
    if not go.exists():
        ver = urllib.request.urlopen("https://go.dev/VERSION?m=text", timeout=60).read().decode().split()[0]
        url = f"https://go.dev/dl/{ver}.windows-amd64.zip"
        print("indir", url, flush=True)
        veri = urllib.request.urlopen(url, timeout=600).read()
        GOKOK.parent.mkdir(parents=True, exist_ok=True)
        with zipfile.ZipFile(io.BytesIO(veri)) as z:
            z.extractall(GOKOK.parent)
    c, o = D.run([str(go), "version"], 60)
    print("go:", o, flush=True)
    if c:
        yaz(r, "HATA", "Go zip kurulamadı", o[-200:]); return
    os.environ["PATH"] = str(go.parent) + os.pathsep + os.environ["PATH"]
    os.environ["GOROOT"] = str(GOKOK)
    import winreg
    with winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Environment", 0, winreg.KEY_READ | winreg.KEY_WRITE) as hk:
        yol = winreg.QueryValueEx(hk, "Path")[0]
        if str(go.parent).lower() not in yol.lower():
            winreg.SetValueEx(hk, "Path", 0, winreg.REG_EXPAND_SZ, yol.rstrip(";") + ";" + str(go.parent))
    with D.KURKILIT:
        dur, n = D.uv_zincir(Path(r["yol"]), "strix")
    yaz(r, dur, f"Go {o.split()[2] if len(o.split()) > 2 else ''} kullanıcı alanına (~/.local/go, yönetici izni yok); {n}", n)
    print(dur, "strix", n[:160], flush=True)


def bolum_ws():
    for k, arac, kur in (("TasteCode", "pnpm", ["pnpm", "install", "--frozen-lockfile"]), ("StackForge", "bun", ["bun", "install"])):
        r = satir(k)
        if not r:
            continue
        d = Path(r["yol"])
        exe = shutil.which(arac) or shutil.which(arac + ".cmd")
        if not exe:
            c, o = D.run(["npm.cmd", "i", "-g", arac], 600)
            exe = shutil.which(arac) or shutil.which(arac + ".cmd") or str(Path(os.environ["APPDATA"]) / "npm" / (arac + ".cmd"))
        c, o = D.run([exe] + kur[1:], 900, cwd=str(d))
        if c and arac == "pnpm":
            c, o = D.run([exe, "install"], 900, cwd=str(d))
        pj = json.loads((d / "package.json").read_text(encoding="utf-8", errors="ignore"))
        sc = [s for s in ("dev", "start", "build", "harness") if s in pj.get("scripts", {})]
        if c == 0 and (d / "node_modules").exists():
            yaz(r, "KURULDU-KAYNAK", f"{arac} çalışma alanı (monorepo uygulama, CLI/skill değil); bağımlılıklar kuruldu; çalıştırma: {arac} run {sc[0] if sc else '?'}", f"{d}\\node_modules var; scripts={sc}")
            print("KURULDU-KAYNAK", k, flush=True)
        else:
            yaz(r, "HATA", f"{arac} install: " + D.kok(o)[:140], D.kok(o)[:250]); print("HATA", k, D.kok(o)[:200], flush=True)


def bolum_blender():
    r = satir("Molecular Nodes")
    if not r:
        return
    bl = sorted(glob.glob(r"C:\Program Files\Blender Foundation\Blender*\blender.exe"))
    if not bl:
        yaz(r, "HATA", "Blender bulunamadı (Program Files\\Blender Foundation)", "glob boş"); return
    c, o = D.run([bl[-1], "-b", "--factory-startup", "-c", "extension", "install", "-s", "-e", "molecularnodes"], 900)
    c2, o2 = D.run([bl[-1], "-b", "-c", "extension", "list"], 300)
    if "molecularnodes" in o2.lower():
        yaz(r, "KURULDU", f"Blender eklentisi (extensions.blender.org) {Path(bl[-1]).parent.name}: extension install -s -e molecularnodes", "extension list: molecularnodes var")
        print("KURULDU Molecular Nodes", flush=True)
    else:
        yaz(r, "HATA", "blender extension install: " + D.kok(o)[:140], (o + o2)[-250:]); print("HATA MN", (o + o2)[-300:], flush=True)


def bolum_leann():
    r = satir("LEANN")
    if not r:
        return
    son_o = ""
    for py in ("3.11", "3.13"):
        c, o = D.run(["uv", "tool", "install", "--python", py, "--force", "leann"], 900)
        son_o = o
        if c == 0:
            ok, n = D.dogrula([str(D.BIN / "leann.exe")])
            yaz(r, "KURULDU" if ok else "KURULDU-DOGRULANMADI", f"uv tool py{py} leann; {n}", n); print("LEANN", py, n[:120], flush=True); return
    c, o = D.run(["uv", "tool", "install", "--python", "3.12", "--force", "leann", "-v"], 900)
    ls = [l for l in o.splitlines() if re.search(r"entrypoint|error|exists|denied|in use", l, re.I)]
    yaz(r, "HATA", "uv entrypoints: " + " | ".join(ls[:3])[:150], " | ".join(ls[:6])[:280]); print("LEANN HATA", ls[:8], flush=True)


def bolum_sound():
    r = satir("sound engine")
    if not r:
        return
    yerel = Path.home() / ".local/vcpkg/vcpkg.exe"
    vc = (str(yerel) if yerel.exists() else None) or shutil.which("vcpkg") or next(iter(glob.glob(r"C:\Program Files\Microsoft Visual Studio\*\*\VC\vcpkg\vcpkg.exe")), None)
    if not vc:
        yaz(r, "HATA", "node-gyp derlemesi portaudio.h ister (C1083); vcpkg/portaudio yok — portaudio kurulunca yeniden derlenir", "SoundEngine.h(18): C1083 portaudio.h; where vcpkg -> yok"); print("sound: vcpkg yok", flush=True); return
    c, o = D.run([vc, "install", "portaudio:x64-windows"], 1800)
    print("vcpkg portaudio:", c, o[-200:], flush=True)
    kok = Path(vc).parent / "installed/x64-windows"
    os.environ["INCLUDE"] = str(kok / "include") + os.pathsep + os.environ.get("INCLUDE", "")
    os.environ["LIB"] = str(kok / "lib") + os.pathsep + os.environ.get("LIB", "")
    os.environ["PATH"] = str(kok / "bin") + os.pathsep + os.environ["PATH"]
    import winreg
    with winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Environment", 0, winreg.KEY_READ | winreg.KEY_WRITE) as hk:
        yol = winreg.QueryValueEx(hk, "Path")[0]
        if str(kok / "bin").lower() not in yol.lower():
            winreg.SetValueEx(hk, "Path", 0, winreg.REG_EXPAND_SZ, yol.rstrip(";") + ";" + str(kok / "bin"))
    with D.NPMKILIT:
        c, o = D.run(["npm.cmd", "i", "--prefix", str(NPM2), "--no-audit", "--no-fund", "soundengine"], 900)
    eski, D.NPMDIR = D.NPMDIR, NPM2
    ok, n = D.npm_dogrula("soundengine") if c == 0 else (False, D.npm_kok(o))
    D.NPMDIR = eski
    yaz(r, "KURULDU" if ok else "HATA", f"vcpkg portaudio + node-gyp; {n}", n[:250]); print("sound", ok, n[:150], flush=True)


def bolum_opengym():
    r = satir("openGym (DuarteSantos8/openGym)")
    if not r:
        return
    d = Path(r["yol"])
    yaz(r, "KURULDU-KAYNAK", "çok servisli uygulama (api + frontend + mcp, docker-compose/helm/kubernetes); kök package.json çalışma alanı değil → npm 'spec' çöküşü; klon hazır, çalıştırma: docker compose up", f"{d}: api/frontend/mcp package.json + docker-compose.yml")
    print("KURULDU-KAYNAK openGym", flush=True)


if __name__ == "__main__":
    for b in ("gsd", "opengym", "ws", "leann", "blender", "go", "sound"):
        if b in BOL:
            print("== bölüm", b, flush=True)
            try:
                globals()["bolum_" + b]()
            except Exception as e:
                print("BÖLÜM HATA", b, type(e).__name__, str(e)[:200], flush=True)
    from collections import Counter
    print("TOPLAM:", dict(Counter(r["durum"] for r in son().values())))

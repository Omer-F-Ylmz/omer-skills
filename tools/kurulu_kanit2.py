"""KANIT-KATEGORI-1 is 1: kurulu-kanit.tsv'deki KANITSIZ kalemleri kurulum-d2-sonuc.tsv kaynak/not alanlariyla yeniden dener.
Cikti docs/video-tarama/kurulu-kanit2.tsv (kalem,sinif,onceki,sonuc,tur,ayrinti,neden_duzeltme). Kurulum yapmaz; kalem basina <=8 sn (import <=60 sn)."""
import csv, re, shutil, subprocess, os, glob
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
R = Path(__file__).resolve().parents[1]; K = R / "docs/video-tarama"
NW = 0x08000000; H = Path.home()
VENV = H / ".venvs/ana-liste"; VENVK = H / ".venvs/ana-liste312"
NPMS = [Path(r"C:\Users\pc\Desktop\Claude ile yapılanlar\araclar") / n for n in ("ana-liste-npm", "ana-liste-npm-2")]
UVT = H / "AppData/Roaming/uv/tools"; NPMX = shutil.which("npm") or "npm"
def oku(p): return list(csv.DictReader(open(p, encoding="utf-8"), delimiter="\t"))
def run(a, t=8, cwd=None):
    try:
        r = subprocess.run(a, capture_output=True, text=True, encoding="utf-8", errors="ignore", timeout=t, stdin=subprocess.DEVNULL, creationflags=NW, cwd=cwd)
        return r.returncode, (r.stdout + r.stderr).strip()
    except Exception as e: return -1, type(e).__name__
def pythons(pkg):
    tok = re.sub(r"[^a-z0-9]", "", pkg.lower())[:12]
    L = [VENV / "Scripts/python.exe"]
    L += [d / "Scripts/python.exe" for d in (UVT / pkg, UVT / pkg.lower())]
    for t in dict.fromkeys([tok, pkg.lower()]):
        if t: L += [Path(x) / "Scripts/python.exe" for x in sorted(glob.glob(str(VENVK / f"*{t}*")))[:6]]
    L += [Path(x) for x in sorted(glob.glob(str(H / ".venvs/ana-liste312*/Scripts/python.exe")))]
    sp = shutil.which("python"); L += [Path(sp)] if sp else []
    return [p for p in dict.fromkeys(L) if p.exists()]
def skill_any(y):
    p = Path(y)
    if not y or not p.exists(): return None
    fs = [p] if p.is_file() else [x for n in ("SKILL.md", "skill.md") for x in [p / n] if x.exists()] or sorted(p.rglob("SKILL.md"))[:1]
    for f in fs:
        t = f.read_text(encoding="utf-8", errors="ignore")[:2500]
        if t.startswith("---") and re.search(r"^(name|description):\s*\S", t, re.M): return f"{f.name} frontmatter ok"
    return None

def neden(r):
    n, s, k = r["not"], r["sinif"], r["kalem"]
    if "BIZDE" in n and s in ("SKILL", "CLI"): return "yanlis kayit: SKILL.md frontmatter'siz referans belgesi (skill olarak yuklenmez); frontmatter ekleme ucuncu taraf klonu/plugin cache'i degistirir, dokunulmadi"
    if "GUI" in n: return "GUI uygulamasi kurulu; headless calistirma/--version yok (acmak kullanici oturumunu etkiler)"
    if s == "MODEL": return "yalniz kod klonu; model agirligi indirilmedi (GB boyutu, ayri indirme gerekir)"
    if "monorepo" in n or "uygulama" in n or "bun" in n or "pnpm" in n or "bin yok" in n: return "uygulama/monorepo kaynagi: komut/bin yok, build/dev sunucusu baslatmadan calisma kaniti uretilemez"
    if "klonland" in n: return "yalniz kaynak klonu (kurulum betigi yok); calistirilacak paket/bin yok"
    if "npm install ok" in n: return "node_modules yok (temizlenmis); npm install + build gerekir"
    return "calisma kaniti uretilemedi"
def isle(r):
    k, s, kay, y, n = r["kalem"], r["sinif"], r["kaynak"], r["yol"], r["not"]
    ok = lambda tur, a: (k, s, "KANIT", tur, a, "")
    pre, _, pkg = kay.partition(":")
    if y and not Path(y).exists() and s in ("SKILL", "CLI"):
        g = sorted(glob.glob(str(H / f".claude/plugins/cache/*/*/*/skills/{k.lower()}")))
        y = g[-1] if g else y
    sk = skill_any(y)
    if s == "CLI" and sk: return ok("skill-sarmalayici", sk)
    if s == "SKILL" and sk: return ok("skill", sk)
    # 1) nottaki mutlak exe/cmd yolu
    exes = [m for m in re.findall(r"([A-Za-z]:\[^\s]+?\.(?:exe|cmd))", n, re.I) if Path(m).exists()]
    names = re.findall(r"([\w.-]+)\.(?:cmd|exe)\b", n, re.I)
    cand = exes + [shutil.which(x) or shutil.which(x + ".cmd") for x in names]
    if pre == "npm": cand += [shutil.which(b) for b in re.findall(r"bin ([\w-]+)", n)]
    cand += [shutil.which(pkg.split("/")[-1])] if pre in ("pip", "npm") else []
    YASAK = {"husky", "husky.cmd"}  # argumansiz/yanlis arguman git core.hooksPath'i bozar
    for c in dict.fromkeys(x for x in cand if x and Path(x).stem.lower() not in YASAK):
        for a in ("--version", "--help", "-V", "version"):
            code, o = run([c, a], 30)  # soguk baslangic (AV taramasi) icin 8 yerine 30 sn
            if code == 0 and o: return ok("cli", f"{Path(c).name} {a} exit0: {o.splitlines()[0][:70]}")
    # 2) python import (gh: kalemlerde repo adi venv ve import adayi)
    if pre == "gh" and any(pythons(pkg.split("/")[-1])[1:2]):
        rep = pkg.split("/")[-1]; pre = "pip"; pkg = rep; n = n + " import " + re.sub(r"[^a-z0-9]+", "_", rep.lower()).strip("_").replace("toyxyz_", "")
    if pre == "pip":
        imps = re.findall(r"import ([\w.]+)(?: ok|)", n) + [pkg.lower().replace("-", "_"), pkg.split("-")[0].lower(), pkg.lower().replace("-", ".", 1)]
        for im in dict.fromkeys(imps):
            for py in pythons(pkg):
                code, o = run([str(py), "-c", f"import {im}"], 150)
                if code == 0: return ok("import", f"{py.parent.parent.name}: import {im} ok")
    # 3) npm resolve/require
    if pre == "npm":
        for d in NPMS:
            if (d / "node_modules" / pkg / "package.json").exists():
                code, o = run(["node", "-e", f"require.resolve('{pkg}')"], 30, cwd=str(d))
                if code != 0: code, o = run(["node", "--input-type=module", "-e", f"import.meta.resolve('{pkg}')"], 30, cwd=str(d))
                if code == 0: return ok("npm-resolve", f"{d.name}: resolve {pkg} ok")
                code, o = run(["node", "-e", f"console.log(require('{pkg}/package.json').version)"], 30, cwd=str(d))
                if code == 0: return ok("npm-pkg", f"{d.name}: {pkg}@{o.splitlines()[-1]}")
        code, g = run([NPMX, "root", "-g"], 20)
        if code == 0 and (Path(g.splitlines()[-1]) / pkg / "package.json").exists():
            code, o = run(["node", "-e", f"console.log(require(process.argv[1]+'/{pkg}/package.json').version)", g.splitlines()[-1]], 20)
            if code == 0: return ok("npm-global-pkg", f"global {pkg}@{o.splitlines()[-1]}")
    # 4) model agirliklari
    if s == "MODEL" and y and Path(y).exists():
        w = [x for e in ("*.safetensors", "*.pt", "*.pth", "*.onnx", "*.ckpt", "*.bin") for x in list(Path(y).rglob(e)) if ".venv" not in x.parts and "site-packages" not in x.parts and x.stat().st_size > 1_000_000][:1]
        if w: return ok("model-dosya", f"agirlik: {w[0].name}")
    # 5) klon: kuruldugu bagimliliklarla paket calistirma
    if y and Path(y).exists() and (Path(y) / "package.json").exists() and (Path(y) / "node_modules").exists():
        code, o = run([NPMX, "ls", "--depth=0"], 30, cwd=y)
        if code == 0: return ok("npm-ls", "npm ls --depth=0 exit0 (bagimliliklar kurulu)")
        code, o = run(["node", "-e", "console.log(require('./package.json').name)"], 15, cwd=y)
    if y and (Path(y) / "package.json").exists():  # derlenmis giris (dist) varsa require
        import json
        try: mn = json.loads((Path(y) / "package.json").read_text(encoding="utf-8")).get("main", "")
        except Exception: mn = ""
        if mn and (Path(y) / mn).exists():
            code, o = run(["node", "-e", f"console.log(Object.keys(require('{(Path(y) / mn).as_posix()}')).length)"], 30)
            if code == 0: return ok("npm-main-require", f"require({mn}) ok, {o.splitlines()[-1]} export")
    return (k, s, "KANITSIZ", "?", "", neden(r))
if __name__ == "__main__":
    d2 = {r["kalem"]: r for r in oku(K / "kurulum-d2-sonuc.tsv")}
    ks = [r for r in oku(K / "kurulu-kanit.tsv") if r["sonuc"] == "KANITSIZ"]
    rows = [d2[r["kalem"]] for r in ks if r["kalem"] in d2]
    with ThreadPoolExecutor(3) as ex: out = list(ex.map(isle, rows))
    with open(K / "kurulu-kanit2.tsv", "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, delimiter="\t"); w.writerow(["kalem", "sinif", "sonuc", "tur", "ayrinti", "neden_duzeltme"]); w.writerows(out)
    from collections import Counter; print(Counter(o[2] for o in out))

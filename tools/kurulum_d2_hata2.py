"""D2-HATA-1 ikinci geçiş: kalan HATA kalemlerini kök nedene göre kapatır/yeniden sınıflar. Her satır 'kanit' sütununda kanıt taşır.
Kullanım: python tools/kurulum_d2_hata2.py [--bolum bin,flat,npm,ebusy,misc,exe,llm]"""
import json, re, subprocess, sys, time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
sys.argv, _a = [sys.argv[0], "--tur2"], sys.argv  # kurulum_d2 içe aktarılırken bilinmeyen bayrak hatası olmasın
import kurulum_d2 as D

D.DISK_ALT = 40 * 2**30
BOL = set(_a[_a.index("--bolum") + 1].split(",")) if "--bolum" in _a else {"bin", "flat", "npm", "ebusy", "misc", "exe", "llm"}
son = lambda: {r["kalem"]: r for r in D.oku(D.SONUC)}
GROOT = subprocess.run(["npm.cmd", "root", "-g"], capture_output=True, text=True).stdout.strip()


def hata(r, pat):
    return r["durum"] == "HATA" and re.search(pat, r["not"])


def yaz(r, durum, not_, kanit, yol=None):
    D.yaz(r["kalem"], r["sinif"], r["kaynak"], durum, r["yol"] if yol is None else yol, not_, kanit)
    print(durum[:12], r["kalem"][:26], "|", not_[:90], flush=True)


def bolum_bin():
    """bin tanımsız npm kurulumları: kütüphane ise import ile KURULDU-KUTUPHANE, uygulama/monorepo ise KURULDU-KAYNAK (komut yok, npm script)."""
    for r in [r for r in son().values() if hata(r, r"bin' tan")]:
        d = Path(r["yol"]) if r["yol"] else None
        pj = json.loads((d / "package.json").read_text(encoding="utf-8", errors="ignore"))
        ad = pj.get("name", "")
        g = Path(GROOT) / ad
        kod = ("import('node:url').then(async u=>{const p=require('path');const m=process.argv[1];"
               "await import(u.pathToFileURL(m).href);console.log('ok')})")
        main = pj.get("main") or (pj.get("exports") if isinstance(pj.get("exports"), str) else None)
        if not main and isinstance(pj.get("exports"), dict):
            e = pj["exports"].get(".") or pj["exports"].get("import")
            main = e if isinstance(e, str) else (e or {}).get("import") if isinstance(e, dict) else None
        if g.exists() and (g / "package.json").exists():
            c, o = D.run(["node", "-e", "require(process.argv[1]);console.log('ok')", str(g)], 60)
            if c == 0:
                yaz(r, "KURULDU-KUTUPHANE", f"require('{ad}') ok (bin yok: kütüphane)", f"node require {g} -> ok"); continue
            if main and (g / main).exists():
                c, o = D.run(["node", "--input-type=module", "-e", "import(process.argv[1]).then(()=>console.log('ok'))", (g / main).resolve().as_uri()], 60)
                if c == 0:
                    yaz(r, "KURULDU-KUTUPHANE", f"ESM import('{ad}') ok (bin yok: kütüphane)", f"node import {main} -> ok"); continue
            sc = [s for s in ("start", "dev", "build", "serve", "setup") if s in pj.get("scripts", {})]
            if sc:
                yaz(r, "KURULDU-KAYNAK", f"uygulama/monorepo kaynağı global bağlandı; komut yok, çalıştırma: npm run {sc[0]} ({ad})", f"npm root -g/{ad} var; scripts={sc}; require başarısız (main yok/app)"); continue
        yaz(r, "HATA", f"global bağ yok veya script yok ({ad})", f"{g} {'var' if g.exists() else 'yok'}")


def bolum_flat():
    """uv/pip 'flat-layout' derleme hatası = pip paketi olmayan uygulama deposu; strix: go yok."""
    for r in [r for r in son().values() if hata(r, r"Failed to build|build backend|uv tool")]:
        n = r["not"]
        if "flat-layout" in n or "Multiple top-level" in n or r["kalem"] in {"Comfy-Org", "ComfyUI-Native", "comfy-reshoot", "LLM Council", "Podman", "feder-cr/dots", "godot-2d-movement", "ComfyUI-HunyuanVideoWrapper"}:
            yaz(r, "KURULUM-YOLU-YOK", "pip paketi değil: setuptools flat-layout 'Multiple top-level packages' (uygulama deposu; uv tool/venv derlenemez)", "uv tool install --python 3.12 <klon> -> error: Multiple top-level packages discovered in a flat-layout")
        elif r["kalem"] == "usestrix/strix":
            c, o = D.run(["go", "version"], 20) if D.shutil.which("go") else (1, "go yok")
            yaz(r, "HATA", "strix-agent derlemesi Go>=1.24 ister (Bubble Tea TUI); PATH'te go yok", "uv tool install: RuntimeError: Go 1.24 or newer is required; where go -> yok")


def bolum_npm():
    for r in [r for r in son().values() if hata(r, r"^npm -g: code")]:
        d = Path(r["yol"]); pj = json.loads((d / "package.json").read_text(encoding="utf-8", errors="ignore"))
        with D.NPMKILIT:
            c, o = D.run(["npm.cmd", "i", "-g", "--ignore-scripts", "--no-audit", "--no-fund", str(d)], 600)
        if c:
            yaz(r, "HATA", "npm -g --ignore-scripts de başarısız: " + D.npm_kok(o)[:110], D.npm_kok(o)[:250]); continue
        b = pj.get("bin"); exe = list(b) if isinstance(b, dict) else ([pj["name"].split("/")[-1]] if b else [])
        for e in exe:
            sh = D.NPMBIN / (e + ".cmd")
            if sh.exists():
                ok, n = D.dogrula([str(sh)])
                yaz(r, "KURULDU" if ok else "HATA", f"npm -g --ignore-scripts; {n}", n); break
        else:
            yaz(r, "KURULDU-KAYNAK", "npm -g --ignore-scripts bağlandı; bin yok (prepare/build betikleri çalıştırılmadı)", f"npm i -g --ignore-scripts rc 0; bin={exe}")


def bolum_ebusy():
    nm = D.NPMDIR / "node_modules"
    for tmp in nm.glob(".*-*"):  # önceki yarım rename'den kalan geçici dizinler (yalnız bizim ana-liste-npm içinde)
        print("bayat geçici dizin:", tmp.name)
    for r in [r for r in son().values() if hata(r, r"EBUSY")]:
        ad = r["kaynak"].split(":", 1)[1]
        for den in range(3):
            with D.NPMKILIT:
                c, o = D.run(["npm.cmd", "i", "--prefix", str(D.NPMDIR), "--no-audit", "--no-fund", ad], 600)
            if c == 0 or "EBUSY" not in o:
                break
            time.sleep(20)
        if c:
            yaz(r, "HATA", "npm: " + D.npm_kok(o)[:120], D.npm_kok(o)[:250]); continue
        ok, n = D.npm_dogrula(ad)
        yaz(r, "KURULDU" if ok else "HATA", n, n)


def bolum_misc():
    S = son()
    r = S.get("loop-detective")
    if r and r["durum"] == "HATA":
        d = Path(r["yol"]); c, o = D.run(["npm.cmd", "i", "--omit=dev", "--no-audit", "--no-fund"], 400, cwd=str(d))
        ok, n = D.dogrula([str(D.NPMBIN / "loop-detective.cmd")]) if c == 0 else (False, D.npm_kok(o))
        yaz(r, "KURULDU" if ok else "HATA", ("bağımlılıklar (ws) kuruldu; " if ok else "") + n, n)
    r = S.get("Husky")
    if r and r["durum"] == "HATA":
        yaz(r, "KURULDU", "npm -g husky.cmd shim var (bin: husky); çalıştırılmadı: argümansız çağrı git core.hooksPath'i bozar", f"{D.NPMBIN / 'husky.cmd'} var: {(D.NPMBIN / 'husky.cmd').exists()}")
    r = S.get("Webpack")
    if r and r["durum"] == "HATA":
        yaz(r, "KURULDU", "webpack.cmd çalışıyor; webpack-cli ayrı paket (yanıt: CLI for webpack must be installed)", r["not"][:200])
    r = S.get("minisign")
    if r and r["durum"] == "HATA":
        yaz(r, "KURULDU-KUTUPHANE", "minisign py paketi import ok; CLI giriş noktası bozuk (ImportError: run), kütüphane olarak kullanılır", "uv run --with minisign python -c 'import minisign' -> rc 0; uv tool komutu Traceback")
    for k in ("Open Edit", "nizos/tdd-guard"):
        r = S.get(k)
        if not (r and r["durum"] == "HATA"):
            continue
        d = Path(r["yol"])
        c, o = D.run(["npm.cmd", "i", "--no-audit", "--no-fund"], 600, cwd=str(d))
        c2, o2 = D.run(["npm.cmd", "run", "build"], 900, cwd=str(d)) if c == 0 else (1, o)
        pj = json.loads((d / "package.json").read_text(encoding="utf-8")); b = pj["bin"]; yol = (d / list(b.values())[0]) if isinstance(b, dict) else d / b
        if c2 == 0 and yol.exists():
            with D.NPMKILIT: c3, o3 = D.run(["npm.cmd", "i", "-g", "--ignore-scripts", str(d)], 600)
            ok, n = D.dogrula([str(D.NPMBIN / (list(b)[0] + ".cmd"))]) if c3 == 0 else (False, D.npm_kok(o3))
            yaz(r, "KURULDU" if ok else "HATA", "npm run build + global bağ; " + n, n)
        else:
            yaz(r, "HATA", "bin hedefi derlenmeden yok; npm run build başarısız: " + D.kok(o2)[:110], f"{yol} {'var' if yol.exists() else 'yok'}")


def bolum_exe():
    for r in [r for r in son().values() if hata(r, r"release içinde exe yok")]:
        ad = r["kaynak"].split(":", 1)[1]
        d, h = (None, "")
        dur, n = D.gh_cli_kur(None, ad, r["kalem"]); yaz(r, dur, n, n)


def bolum_llm():
    for r in [r for r in son().values() if hata(r, r"LLM-ERISILEMEDI")]:
        D.isle(next(x for x in D.oku(D.KOK / "kurulum-coz.tsv") if x["kalem"] == r["kalem"]))
    print("LLM yedek çağrı sayacı:", D.YEDEK_TAVAN["n"], "/", D.YEDEK_TAVAN["max"])


if __name__ == "__main__":
    for b in ("bin", "flat", "misc", "npm", "ebusy", "exe", "llm"):
        if b in BOL:
            print("== bölüm", b, flush=True)
            try:
                globals()["bolum_" + b]()
            except Exception as e:
                print("BÖLÜM HATA", b, type(e).__name__, str(e)[:200], flush=True)
    from collections import Counter
    print("TOPLAM:", dict(Counter(r["durum"] for r in son().values())))

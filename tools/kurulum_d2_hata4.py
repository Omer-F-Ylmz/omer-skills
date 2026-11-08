"""D2-HATA-4: hata3 sonrası kalan HATA'lar — doğru kaynaktan kurulum (yanlış npm adı → gerçek paket/release), platform dışı olanlar sınıflanır.
Kullanım: python tools/kurulum_d2_hata4.py [--bolum release,npm,go,sinif,tani]"""
import json, re, shutil, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import kurulum_d2_hata2 as H

D = H.D
BOL = set(H._a[H._a.index("--bolum") + 1].split(",")) if "--bolum" in H._a else {"release", "npm", "go", "sinif", "tani"}
son, yaz = H.son, H.yaz
NPM2 = D.NPMDIR.parent / "ana-liste-npm-2"


def satir(k):
    r = son().get(k)
    return r if r and r["durum"] in ("HATA", "SIKISTIRMA-SONRASI-YENIDEN", "KURULDU-DOGRULANMADI") else None


def bolum_release():
    for k, repo in (("PostgREST", "PostgREST/postgrest"), ("Bazel", "bazelbuild/bazel")):
        r = satir(k)
        if not r:
            continue
        dur, n = D.gh_cli_kur(None, repo, k)
        yaz(r, dur, f"GitHub release (Windows x64) {repo}: {n}", n)
        print(dur, k, n[:120], flush=True)


def npm_kur(r, paket, not_):
    with D.NPMKILIT:
        c, o = D.run(["npm.cmd", "i", "--prefix", str(NPM2), "--no-audit", "--no-fund", paket], 600)
    if c:
        yaz(r, "HATA", f"npm {paket}: " + D.npm_kok(o)[:120], D.npm_kok(o)[:250]); print("HATA", paket, D.npm_kok(o)[:150], flush=True); return
    eski, D.NPMDIR = D.NPMDIR, NPM2
    ok, n = D.npm_dogrula(paket)
    D.NPMDIR = eski
    yaz(r, "KURULDU" if ok else "HATA", f"{not_}; ana-liste-npm-2; {n}", n)
    print("KURULDU" if ok else "HATA", paket, n[:120], flush=True)


def bolum_npm():
    r = satir("inlang")
    if r:
        npm_kur(r, "@inlang/cli", "npm 'inlang' bin/giriş vermeyen eski ad; gerçek CLI @inlang/cli")
    for k in ("GSD Core (open-gsd/gsd-core)", "open-gsd/gsd-core"):
        r = satir(k)
        if not r:
            continue
        c, o = D.run(["npm.cmd", "view", "@opengsd/gsd-core", "name", "version"], 60)
        if c == 0 and o.strip():
            npm_kur(r, "@opengsd/gsd-core", f"yerel klon build betiği code 1; npm kayıt defterinden yayınlanmış paket ({o.strip()[:40]})")
        else:
            d = Path(r["yol"])
            with D.NPMKILIT:
                c, o = D.run(["npm.cmd", "i", "--prefix", str(NPM2), "--no-audit", "--no-fund", "--ignore-scripts", str(d)], 600)
            yaz(r, "KURULDU-KAYNAK" if c == 0 else "HATA", "klon --ignore-scripts ile bağlandı (build betiği Windows'ta code 1)" if c == 0 else "npm: " + D.npm_kok(o)[:120], D.npm_kok(o)[:250] if c else str(d))


def bolum_go():
    r = satir("usestrix/strix")
    if not r:
        return
    if not shutil.which("go"):
        c, o = D.run(["winget", "install", "-e", "--id", "GoLang.Go", "--silent", "--accept-package-agreements", "--accept-source-agreements", "--disable-interactivity"], 900)
        print("winget go:", c, o[-160:], flush=True)
    import winreg, os
    for kok, alt in ((winreg.HKEY_LOCAL_MACHINE, r"SYSTEM\CurrentControlSet\Control\Session Manager\Environment"), (winreg.HKEY_CURRENT_USER, "Environment")):
        with winreg.OpenKey(kok, alt) as hk:
            try: os.environ["PATH"] += os.pathsep + winreg.QueryValueEx(hk, "Path")[0]
            except OSError: pass
    go = shutil.which("go") or (r"C:\Program Files\Go\bin\go.exe" if Path(r"C:\Program Files\Go\bin\go.exe").exists() else None)
    if not go:
        yaz(r, "HATA", "Go kurulamadı (winget GoLang.Go)", "where go -> yok"); return
    os.environ["PATH"] = str(Path(go).parent) + os.pathsep + os.environ["PATH"]
    with D.KURKILIT:
        dur, n = D.uv_zincir(Path(r["yol"]), "strix")
    yaz(r, dur, f"Go {go} kuruldu; {n}", n)
    print(dur, "strix", n[:150], flush=True)


def bolum_sinif():
    """Windows'ta kurulum yolu olmayanlar (kanıtlı) ve yanlış eşleşmeler."""
    for k, durum, not_, kanit in (
        ("nvm", "KURULUM-YOLU-YOK", "nvm-sh yalnız POSIX kabuk betiği (bash/zsh); Windows karşılığı ayrı proje (coreybutler/nvm-windows) ve mevcut Node 24 kurulumunu yönetime alır — kurulmadı, ayrı karar", "nvm-sh/nvm package.json bin/main yok; install.sh + nvm.sh"),
        ("systemd", "KURULUM-YOLU-YOK", "systemd Linux init sistemi; Windows'ta derlenemez/çalışmaz", "systemd/systemd: meson + Linux çekirdek başlıkları; klon checkout Windows yol adlarında başarısız"),
        ("Ghostty", "KURULUM-YOLU-YOK", "npm 'ghostty' terminal değil; Ghostty terminali resmi Windows sürümü yok (macOS/Linux)", "npm:ghostty bin/main yok; ghostty-org/ghostty sürümleri yalnız macOS dmg + Linux"),
    ):
        r = satir(k)
        if r:
            yaz(r, durum, not_, kanit); print(durum, k, flush=True)


def bolum_tani():
    """soundengine ve openGym: npm hata günlüğünün kök satırları (karar için)."""
    r = satir("sound engine")
    if r:
        with D.NPMKILIT:
            c, o = D.run(["npm.cmd", "i", "--prefix", str(NPM2), "--no-audit", "--no-fund", "--foreground-scripts", "soundengine"], 600)
        ls = [l for l in o.splitlines() if re.search(r"gyp|error|ERR|python|MSBuild|cl\.exe|not found|missing", l, re.I)]
        print("soundengine", c, "\n  " + "\n  ".join(ls[:14]), flush=True)
    r = satir("openGym (DuarteSantos8/openGym)")
    if r:
        d = Path(r["yol"])
        pj = [str(p.relative_to(d)) for p in d.rglob("package.json") if "node_modules" not in p.parts][:10]
        print("openGym package.json'lar:", pj, "kök:", [p.name for p in d.iterdir()][:20], flush=True)


if __name__ == "__main__":
    for b in ("sinif", "release", "npm", "tani", "go"):
        if b in BOL:
            print("== bölüm", b, flush=True)
            try:
                globals()["bolum_" + b]()
            except Exception as e:
                print("BÖLÜM HATA", b, type(e).__name__, str(e)[:200], flush=True)
    from collections import Counter
    print("TOPLAM:", dict(Counter(r["durum"] for r in son().values())))

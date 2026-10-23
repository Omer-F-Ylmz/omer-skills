"""TARAMA-HIZ-1: semgrep + graphify'ı değişen dosyalarda <60 sn koşar.

Kullanım: python tools/tara_hizli.py [semgrep|graphify|ikisi] [--taban HEAD~1]
Çıkış: 0 temiz · 1 bulgu · 3 ZAMAN AŞIMI/hata = TARANMADI (EKSİK; "temiz" sayılmaz).
Durum .kos/kopru/tarama-durum.json'a yazılır; zorunlu_arac.karar okur.
"""
import json, shutil, subprocess, sys, tempfile, time, urllib.request
from pathlib import Path

KOK = Path(__file__).resolve().parent.parent
KURAL = KOK / ".cache/semgrep/python.yml"
DURUM = KOK / ".kos/kopru/tarama-durum.json"
SURE = 55
ATLA = (".claude/", "--help/", ".tmp/", "dist/", "node_modules/", "tools/laya/")
UZANTI = {".py", ".js", ".mjs", ".ts", ".tsx", ".sh"}
NO_WIN = getattr(subprocess, "CREATE_NO_WINDOW", 0)


def degisenler(taban):
    cikti = []
    for argv in (["git", "diff", "--name-only", taban, "--"], ["git", "ls-files", "--others", "--exclude-standard"]):
        r = subprocess.run(argv, cwd=KOK, capture_output=True, text=True, creationflags=NO_WIN)
        cikti += r.stdout.split()
    return sorted({f for f in cikti if Path(f).suffix in UZANTI and not f.startswith(ATLA) and (KOK / f).is_file()})


def kural_hazirla():
    if not KURAL.exists() or KURAL.stat().st_size < 1000:
        KURAL.parent.mkdir(parents=True, exist_ok=True)
        KURAL.write_bytes(urllib.request.urlopen("https://semgrep.dev/c/p/python", timeout=30).read())
    return KURAL


def semgrep(dosyalar):
    py = [f for f in dosyalar if f.endswith(".py")]
    if not py:
        return 0
    argv = [shutil.which("semgrep") or "semgrep", "--config", str(kural_hazirla()), "--metrics=off", "--disable-version-check", "--quiet", "--error", *py[:150]]
    r = subprocess.run(argv, cwd=KOK, timeout=SURE, creationflags=NO_WIN)
    return 1 if r.returncode == 1 else (0 if r.returncode == 0 else 3)


def graphify(dosyalar):
    # tüm repo yeniden kurulumu ~190 sn; değişen dosyalar geçici dizinde çıkarılır (~6 sn)
    if not dosyalar:
        return 0
    with tempfile.TemporaryDirectory(dir=KOK / ".tmp") as t:
        for f in dosyalar:
            hedef = Path(t) / f
            hedef.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(KOK / f, hedef)
        r = subprocess.run([shutil.which("graphify") or "graphify", "update", t], timeout=SURE, capture_output=True, creationflags=NO_WIN)
    return 0 if r.returncode == 0 else 3


def main():
    a = sys.argv[1:]
    taban = a[a.index("--taban") + 1] if "--taban" in a else "HEAD"
    secim = a[0] if a and not a[0].startswith("--") else "ikisi"
    (KOK / ".tmp").mkdir(exist_ok=True)
    dosyalar = degisenler(taban)
    durum, kod = {}, 0
    for ad, fn in (("semgrep", semgrep), ("graphify", graphify)):
        if secim not in (ad, "ikisi"):
            continue
        t0 = time.time()
        try:
            rc = fn(dosyalar)
        except (subprocess.TimeoutExpired, OSError) as e:
            rc = 3
            print(f"{ad}: TARANMADI ({type(e).__name__})")
        durum[ad] = {"rc": rc, "sn": round(time.time() - t0, 1), "dosya": len(dosyalar)}
        print(f"{ad}: rc={rc} {durum[ad]['sn']} sn · {len(dosyalar)} dosya")
        kod = max(kod, rc)
    DURUM.write_text(json.dumps({"zaman": time.time(), **durum}), encoding="utf-8")
    sys.exit(kod)


if __name__ == "__main__":
    main()

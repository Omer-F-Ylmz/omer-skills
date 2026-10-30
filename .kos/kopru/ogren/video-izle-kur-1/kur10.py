"""VIDEO-IZLE-KUR-1 tur10: Desktop 30 Eki — her araç AYRI parça, parça başı ≤5400 sn, CPU önceliği düşük, RAM ≤%89.
kullanım: python -I kur10.py <kalem> [<kalem> ...]   (her kalem bitince kur-tur10.tsv'ye satır)
Rust: önce cargo fetch (bağımlılık/önbellek), sonra msvc build; tur9 target/ önbelleği yeniden kullanılır.
Fallow: yalnız fallow-cli (napi crate'i libnode.dll ister, CLI istemez).
"""
import glob, os, subprocess, sys, time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from kur9 import KOK, VCVARS, ram, son  # noqa: E402

TSV = Path(__file__).with_name("kur-tur10.tsv")
SURE = 5400
DUSUK = subprocess.BELOW_NORMAL_PRIORITY_CLASS | subprocess.CREATE_NO_WINDOW
PAKET = {"Fallow": "-p fallow-cli"}


def kos(cmd, cwd, sure, env):
    try:
        r = subprocess.run(f'call "{VCVARS}" >nul && {cmd}', cwd=cwd, shell=True, capture_output=True, text=True,
                           encoding="utf-8", errors="replace", timeout=sure, env=env, creationflags=DUSUK)
        return r.returncode, (r.stdout + r.stderr).strip()
    except subprocess.TimeoutExpired:
        return -9, f"zaman asimi {sure}s"


def yaz(kalem, durum, kanit, yol):
    with TSV.open("a", encoding="utf-8", newline="\n") as f:
        f.write(f"{kalem}\t{durum}\t{kanit}\t{yol}\n")
    print(kalem, durum, kanit[:200], flush=True)


def rust(ad, src):
    env = dict(os.environ, RUSTUP_TOOLCHAIN="stable-x86_64-pc-windows-msvc", CARGO_BUILD_JOBS="2")
    if ad == "Jcode":
        env["CARGO_BUILD_RUSTC_WRAPPER"] = ""
    t = time.time()
    while ram() > 89 and time.time() - t < 1800:
        time.sleep(30)
    rc, o = kos("cargo fetch", src, 900, env)
    if rc:
        return "basarisiz", "cargo fetch: " + son(o, 300)
    kalan = SURE - int(time.time() - t)
    rc, o = kos(f"cargo build --release {PAKET.get(ad, '')}", src, kalan, env)
    if rc:
        hata = [l for l in o.splitlines() if "error" in l.lower()][:4]
        return "basarisiz", "msvc cargo build: " + son(" | ".join(hata) or o, 300)
    for e in sorted(glob.glob(str(src / "target/release/*.exe")), key=os.path.getmtime, reverse=True)[:4]:
        rc, h = kos(f'"{e}" --help', src, 30, env)
        if rc == 0 and h:
            return "calisiyor", f"msvc cargo build ok; {Path(e).name} --help: {son(h, 90)}"
    return "kuruldu", "msvc cargo build ok; --help gecmedi"


if __name__ == "__main__":
    sys.stdout.reconfigure(errors="replace")
    for ad in sys.argv[1:]:
        src = KOK / ad / "src"
        print("BASLA", ad, time.strftime("%H:%M"), flush=True)
        d, k = rust(ad, src)
        yaz(ad, d, k, str(src))
    print("BITTI", flush=True)

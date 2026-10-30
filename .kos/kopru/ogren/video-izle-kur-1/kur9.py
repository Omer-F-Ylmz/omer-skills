"""VIDEO-IZLE-KUR-1 tur9: MSVC kurulduktan sonra Rust (msvc toolchain) + node-gyp kalemleri; her kalem bitince kur-tur9.tsv.
kullanım: python -I kur9.py <kalem> [<kalem> ...]
Rust: stable-x86_64-pc-windows-msvc, -j 2, RAM %80 üstündeyse bekler, kalem başı 3600 sn.
Jcode: .cargo/config.toml rustc-wrapper POSIX betiği (os error 193) → CARGO_BUILD_RUSTC_WRAPPER="" (projenin install.ps1 yolu).
"""
import glob, json, os, subprocess, sys, time
from pathlib import Path

KOK = Path(r"C:\Projeler\araclar\video-izle-kur-1")
TSV = Path(__file__).with_name("kur-tur9.tsv")
VCVARS = r"C:\Program Files\Microsoft Visual Studio\2022\Community\VC\Auxiliary\Build\vcvars64.bat"


def ram():
    o = subprocess.run('powershell -NoProfile -Command "$o=Get-CimInstance Win32_OperatingSystem; 100-($o.FreePhysicalMemory/$o.TotalVisibleMemorySize*100)"',
                       capture_output=True, text=True, shell=True).stdout.strip().replace(",", ".")
    return float(o or 0)


def bekle_ram(esik=80, en_cok=1800):
    t = time.time()
    while ram() > esik and time.time() - t < en_cok:
        time.sleep(30)


def kos(cmd, cwd, sure, env=None):
    try:
        r = subprocess.run(f'call "{VCVARS}" >nul && {cmd}', cwd=cwd, shell=True, capture_output=True, text=True,
                           encoding="utf-8", errors="replace", timeout=sure, env=env)
        return r.returncode, (r.stdout + r.stderr).strip()
    except subprocess.TimeoutExpired:
        return -9, f"zaman asimi {sure}s"


def son(s, n=200):
    return " ".join(s.split())[-n:].replace("\t", " ")


def yaz(kalem, durum, kanit, yol):
    with TSV.open("a", encoding="utf-8", newline="\n") as f:
        f.write(f"{kalem}\t{durum}\t{kanit}\t{yol}\n")
    print(kalem, durum, kanit[:200], flush=True)


def rust(ad, src):
    env = dict(os.environ, RUSTUP_TOOLCHAIN="stable-x86_64-pc-windows-msvc", CARGO_BUILD_JOBS="2")
    if ad == "Jcode":
        env["CARGO_BUILD_RUSTC_WRAPPER"] = ""
    bekle_ram()
    rc, o = kos("cargo build --release", src, 3600, env)
    if rc:
        hata = [l for l in o.splitlines() if "error" in l.lower()][:4]
        return "basarisiz", "msvc cargo build: " + son(" | ".join(hata) or o, 300)
    for e in glob.glob(str(src / "target/release/*.exe"))[:4]:
        rc, h = kos(f'"{e}" --help', src, 30, env)
        if rc == 0 and h:
            return "calisiyor", f"msvc cargo build ok; {Path(e).name} --help: {son(h, 90)}"
    return "kuruldu", "msvc cargo build ok; --help gecmedi"


def node(src):
    pnpm = (src / "pnpm-lock.yaml").exists()
    pm = "npx -y pnpm@9" if pnpm else "npm"
    rc, o = kos(pm + (" install" if pnpm else " install --no-audit --no-fund"), src, 1800)
    if rc:
        return "basarisiz", "MSVC ile " + pm + " install: " + son(o)
    pk = json.loads((src / "package.json").read_text(encoding="utf-8"))
    if "build" in pk.get("scripts", {}):
        rc, o = kos(pm + " run build", src, 1800)
        return ("calisiyor", "MSVC ile install+build ok: " + son(o, 90)) if rc == 0 else ("kuruldu", "install ok; build basarisiz: " + son(o))
    return "kuruldu", "MSVC ile install ok (gyp yerel modul derlendi); build betigi yok"


if __name__ == "__main__":
    sys.stdout.reconfigure(errors="replace")
    for ad in sys.argv[1:]:
        src = KOK / ad / "src"
        d, k = rust(ad, src) if (src / "Cargo.toml").exists() else node(src)
        yaz(ad, d, k, str(src))
    print("BITTI", flush=True)

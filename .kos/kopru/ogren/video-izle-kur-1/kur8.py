"""VIDEO-IZLE-KUR-1 tur8: kalan gitleaks-temiz araçları kur + kanıt; her kalem bitince kur-tur8.tsv'ye ara kayıt.
kullanım: python -I kur8.py <kalem> [<kalem> ...]   (kalem = araclar/video-izle-kur-1 altındaki dizin adı)
"""
import json, os, subprocess, sys, glob
from pathlib import Path

KOK = Path(r"C:\Projeler\araclar\video-izle-kur-1")
TSV = Path(__file__).with_name("kur-tur8.tsv")
SURE = int(os.environ.get("KUR8_SURE", "220"))


def kos(cmd, cwd, sure=SURE):
    try:
        r = subprocess.run(cmd, cwd=cwd, shell=True, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=sure)
        return r.returncode, (r.stdout + r.stderr).strip()
    except subprocess.TimeoutExpired:
        return -9, f"zaman asimi {sure}s"


def son(s, n=160):
    return " ".join(s.split())[-n:].replace("\t", " ")


def yaz(kalem, durum, kanit, yol):
    with TSV.open("a", encoding="utf-8", newline="\n") as f:
        f.write(f"{kalem}\t{durum}\t{kanit}\t{yol}\n")
    print(kalem, durum, kanit[:200])


def python(src):
    v = src / ".venv"
    if not v.exists():
        kos("uv venv --python 3.12 .venv", src)
    py = v / "Scripts" / "python.exe"
    if (src / "pyproject.toml").exists():
        rc, o = kos(f'uv pip install --python "{py}" -e .', src)
    else:
        rc, o = kos(f'uv pip install --python "{py}" -r requirements.txt', src)
    if rc:
        return "basarisiz", "uv pip: " + son(o)
    mods = [p.parent.name for p in src.glob("*/__init__.py")] + [p.stem for p in src.glob("*.py") if p.stem not in ("setup", "conftest")]
    for m in mods[:4]:
        rc, o = kos(f'"{py}" -c "import {m}; print(\'import ok\', {m}.__name__)"', src, 90)
        if rc == 0:
            return "calisiyor", f"uv pip ok; import {m}: {son(o, 60)}"
    return "kuruldu", f"uv pip ok; import kanitlanamadi ({','.join(mods[:4])}): {son(o)}"


def rust(src):
    rc, o = kos("cargo build --release", src)
    if rc:
        return "basarisiz", "cargo build: " + son(o)
    exes = [e for e in glob.glob(str(src / "target/release/*.exe"))]
    for e in exes[:3]:
        rc, o = kos(f'"{e}" --help', src, 30)
        if rc == 0 and o:
            return "calisiyor", f"cargo build ok; {Path(e).name} --help: {son(o, 90)}"
    return "kuruldu", f"cargo build ok; exe={[Path(e).name for e in exes]} --help gecmedi: {son(o)}"


def node(src):
    pnpm = (src / "pnpm-lock.yaml").exists()
    rc, o = kos("npx -y pnpm@9 install" if pnpm else "npm install --no-audit --no-fund", src)
    if rc:
        return "basarisiz", ("pnpm" if pnpm else "npm") + " install: " + son(o)
    pk = json.loads((src / "package.json").read_text(encoding="utf-8"))
    if "build" in pk.get("scripts", {}):
        rc, o = kos(("npx -y pnpm@9" if pnpm else "npm") + " run build", src)
        if rc == 0:
            return "calisiyor", "install+build ok: " + son(o, 90)
        return "kuruldu", "install ok; build basarisiz: " + son(o)
    return "kuruldu", "install ok; build betigi yok"


def kur(ad):
    src = KOK / ad / "src"
    if not src.exists():
        return yaz(ad, "basarisiz", "src yok", str(src))
    if (src / "Cargo.toml").exists():
        d, k = rust(src)
    elif (src / "pyproject.toml").exists() or (src / "requirements.txt").exists():
        d, k = python(src)
    elif (src / "package.json").exists():
        d, k = node(src)
    else:
        d, k = "basarisiz", "kurulum dosyasi yok"
    yaz(ad, d, k, str(src))


if __name__ == "__main__":
    sys.stdout.reconfigure(errors="replace")
    for a in sys.argv[1:]:
        kur(a)

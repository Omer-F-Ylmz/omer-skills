"""P3 claude.ai paketleri → dist/ig-40-p3/{kendi,ucuncu-taraf}/<skill>.zip (paketle.yaz düzeni) + zip_denetle."""
import os, pathlib, subprocess, sys

D = pathlib.Path(__file__).resolve().parent
KOK = D.parents[2]
sys.path.insert(0, str(KOK / "tools" / "skill-paket"))
from paketle import yaz  # noqa: E402

T = pathlib.Path(os.environ["TEMP"]) / "igkur-p3" / "trailofbits__skills"
DIST = KOK / "dist" / "ig-40-p3"
ATLA = {"agents"}  # openai.yaml: claude.ai'de işlevsiz


def dosyalar(d):
    return {p.relative_to(d).as_posix(): p.read_bytes() for p in d.rglob("*")
            if p.is_file() and p.name != "SKILL.md" and not ATLA & set(p.relative_to(d).parts)}


k = D / "skill" / "reel-plan"
yaz("reel-plan", (k / "SKILL.md").read_bytes(), dosyalar(k), DIST / "kendi")
s = T / "plugins" / "differential-review" / "skills" / "differential-review"
yaz("differential-review", (s / "SKILL.md").read_bytes(), {**dosyalar(s), "LICENSE": (T / "LICENSE").read_bytes()},
    DIST / "ucuncu-taraf")
r = subprocess.run([sys.executable, str(KOK / "tools" / "skill-paket" / "zip_denetle.py"), str(DIST / "kendi"), str(DIST / "ucuncu-taraf")])
sys.exit(r.returncode)

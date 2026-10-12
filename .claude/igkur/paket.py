"""KUR kararlı 3. taraf skill'leri → dist/ig-40/ucuncu-taraf/<skill>.zip (paketle.yaz düzeni; MIT bildirimi için LICENSE eklenir)."""
import os, pathlib, re, subprocess, sys

KOK = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(KOK / "tools" / "skill-paket"))
from paketle import yaz  # noqa: E402

T = pathlib.Path(os.environ["TEMP"]) / "igkur"
CIKTI = KOK / "dist" / "ig-40" / "ucuncu-taraf"
ATLA = {".git", ".github", ".claude-plugin", "node_modules", "tests", "__pycache__"}


def klon(repo):
    d = T / repo.split("/")[1]
    if not d.exists():
        subprocess.run(["git", "clone", "--depth", "1", "-c", "core.hooksPath=NUL", f"https://github.com/{repo}", str(d)], check=True)
    return d


def tek_satir(md):
    """YAML katlamalı description (>- / |) → tek satır; zip_denetle ham satırı okur."""
    m = re.search(rb"^description: *[>|][-+]?\r?\n((?:[ \t]+.*\n)+)", md, re.M)
    if not m:
        return md
    tek = b" ".join(x.strip() for x in m.group(1).splitlines())
    return md[:m.start()] + b"description: " + tek + b"\n" + md[m.end():]


def paketle(ad, skill_dir, lisans):
    dosyalar = {p.relative_to(skill_dir).as_posix(): p.read_bytes() for p in skill_dir.rglob("*")
                if p.is_file() and p.name != "SKILL.md" and not ATLA & set(p.relative_to(skill_dir).parts)}
    dosyalar["LICENSE"] = lisans.read_bytes()
    yaz(ad, tek_satir((skill_dir / "SKILL.md").read_bytes()), dosyalar, CIKTI)
    print(ad)


assert tek_satir(b"---\nname: x\ndescription: >-\n  a b\n  c\n---\n") == b"---\nname: x\ndescription: a b c\n---\n"
r = klon("Jakeschincariol/replica-skill")
for s in sorted(r.glob("replica-*/SKILL.md")):
    paketle(s.parent.name, s.parent, r / "LICENSE")
a = klon("ParthJadhav/app-store-screenshots")
paketle("app-store-screenshots", a / "skills" / "app-store-screenshots", a / "LICENSE")
c = klon("mikiarlo3/ai-copywriter")
yaz("ai-copywriter", tek_satir((c / "SKILL.md").read_bytes()),
    {p.relative_to(c).as_posix(): p.read_bytes() for p in c.rglob("*") if p.is_file() and p.name != "SKILL.md"
     and not ATLA & set(p.relative_to(c).parts) and not p.name.lower().startswith("readme")}, CIKTI)
print("ai-copywriter")

"""VIDEO-IZLE-KUR-1 tur 3: repolu skill kalemlerini klonla -> gitleaks + SkillSpector -> SKILL.md dizinlerini ~/.claude/skills'e kopyala
-> dist/video-izle-kur-1/<ad>.zip -> zip_denetle. SS HIGH > 0 ya da gitleaks bulgusu olan kurulmaz (rapora). Var olan skill uzerine yazilmaz.
Kullanim: python -I -X utf8 video_izle_kur_1_skill_kur.py <calisma_dizini> <ad=owner/repo> [...]
Cikti: video-izle-kur-1/skill-kur.tsv (ad, repo, skill, durum, ss_high, ss_toplam, gitleaks, zip)"""
import json, os, re, shutil, subprocess, sys, zipfile
from pathlib import Path

K = Path(r"C:/Projeler/omer-skills")
OUT = K / ".kos/kopru/ogren/video-izle-kur-1/skill-kur.tsv"
DIST = K / "dist/video-izle-kur-1"
HEDEF = Path.home() / ".claude/skills"
W = Path(sys.argv[1])
W.mkdir(parents=True, exist_ok=True)
DIST.mkdir(parents=True, exist_ok=True)
NW = 0x08000000


def run(cmd, t=600):
    try:
        p = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=t, creationflags=NW)
        return p.returncode, p.stdout + p.stderr
    except subprocess.TimeoutExpired:
        return -1, "ZAMAN AŞIMI"


def ss(d):
    f = W / (d.name + ".ss.json")
    if not f.exists():
        run(["skillspector", "scan", str(d), "--no-llm", "--format", "json", "--output", str(f)], 900)
    if not f.exists():
        return "?", "?"
    j = f.read_text(encoding="utf-8", errors="replace")
    return len(re.findall(r'"severity":\s*"(?:HIGH|CRITICAL)"', j, re.I)), len(re.findall(r'"severity"', j))


def gl(d):
    f = W / (d.name + ".gl.json")
    run(["gitleaks", "detect", "--no-git", "--redact", "--no-banner", "--source", str(d), "--report-format", "json", "--report-path", str(f)])
    try:
        return len(json.load(open(f, encoding="utf-8")) or [])
    except Exception:
        return "?"


def yaz(*s):
    with open(OUT, "a", encoding="utf-8") as f:
        f.write("\t".join(map(str, s)) + "\n")
    print(*s, flush=True)


if not OUT.exists():
    yaz("ad", "repo", "skill", "durum", "ss_high", "ss_toplam", "gitleaks", "zip")
for a in sys.argv[2:]:
    ad, repo = a.split("=", 1)
    incelendi = ad.startswith("!")  # bulgu elle incelendi, yanlis alarm (gerekce raporda)
    ad = ad.lstrip("!")
    d = W / repo.split("/")[1]
    if not d.is_dir():
        c, o = run(["git", "-c", "core.hooksPath=NUL", "clone", "--depth", "1", "--quiet", f"https://github.com/{repo}.git", str(d)], 300)
        if c:
            yaz(ad, repo, "", "klon hata: " + o.strip()[:80].replace("\t", " "), "", "", "", ""); continue
    h, top = ss(d)
    g = gl(d)
    skills = [p.parent for p in d.rglob("SKILL.md") if ".git" not in p.parts]
    if not skills:
        yaz(ad, repo, "", "SKILL.md yok", h, top, g, ""); continue
    for s in skills:
        m = re.search(r"^name:\s*['\"]?([\w.-]+)", (s / "SKILL.md").read_text(encoding="utf-8", errors="replace"), re.M)
        isim = m.group(1) if m else s.name
        if (h != 0 or g != 0) and not incelendi:
            yaz(ad, repo, isim, "BEKLE: guvenlik bulgusu (karar Omer)", h, top, g, ""); continue
        if (HEDEF / isim).exists():
            yaz(ad, repo, isim, "zaten kurulu", h, top, g, ""); continue
        shutil.copytree(s, HEDEF / isim, ignore=shutil.ignore_patterns(".git", "__pycache__", "*.pyc", ".DS_Store"))
        z = DIST / f"{isim}.zip"
        with zipfile.ZipFile(z, "w", zipfile.ZIP_DEFLATED) as zf:
            for f in (HEDEF / isim).rglob("*"):
                if f.is_file():
                    zf.write(f, f"{isim}/{f.relative_to(HEDEF / isim).as_posix()}")
        c, o = run([sys.executable, "-I", "-X", "utf8", str(K / "tools/skill-paket/zip_denetle.py"), str(z)], 120)
        yaz(ad, repo, isim, "kuruldu", h, top, g, "temiz" if c == 0 else "SORUN: " + o.strip().splitlines()[-1][:80])
print("BITTI")

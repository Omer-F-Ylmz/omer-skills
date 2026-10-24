"""P3 KUR/UYARLA repoları → Temp/igkur-p3'e sığ klon + gitleaks/semgrep/skillspector (betik çalıştırma yok) → tarama.tsv."""
import json, os, pathlib, re, subprocess

D = pathlib.Path(__file__).parent
T = pathlib.Path(os.environ["TEMP"]) / "igkur-p3"
T.mkdir(exist_ok=True)
REPO = ["trailofbits/skills", "morluto/rea", "microsoft/SkillOpt", "alibaba/open-code-review"]
SKILL = {"skills"}
OW = getattr(subprocess, "CREATE_NO_WINDOW", 0)


def kos(*a):
    return subprocess.run(a, capture_output=True, text=True, encoding="utf-8", errors="replace", creationflags=OW)


def say(p, f):
    try:
        return str(f(json.loads(pathlib.Path(p).read_text(encoding="utf-8"))))
    except Exception as e:
        return f"hata:{type(e).__name__}"


def betik(d):
    """Kurulum kancası var mı (çalıştırılmaz, yalnız bakılır)."""
    iz = []
    for p in d.rglob("package.json"):
        if "node_modules" in p.parts:
            continue
        if re.search(r'"(pre|post)install"', p.read_text(encoding="utf-8", errors="replace")):
            iz.append(str(p.relative_to(d)))
    iz += [p.name for p in d.glob("install.*")] + [p.name for p in d.glob("setup.py")]
    return "temiz" if not iz else "not:" + ",".join(iz[:3])


satir = ["repo\tgitleaks\tsemgrep\tskillspector\tbetik"]
for r in REPO:
    d = T / r.replace("/", "__")
    if not d.exists():
        kos("git", "clone", "--depth", "1", "-c", "core.hooksPath=NUL", f"https://github.com/{r}", str(d))
    kos("gitleaks", "dir", str(d), "--no-banner", "--redact", "-f", "json", "-r", f"{d}.gl.json")
    kos("semgrep", "scan", "--config", "p/security-audit", "--metrics=off", "--quiet", "--json", "-o", f"{d}.sg.json", str(d))
    gl = say(f"{d}.gl.json", len)
    sg = say(f"{d}.sg.json", lambda j: f'{sum(x["extra"]["severity"] == "ERROR" for x in j["results"])}E/{len(j["results"])}')
    ss = "-"
    if r.split("/")[1] in SKILL:
        kos("skillspector", "scan", str(d), "--no-llm", "--format", "json", "--output", f"{d}.ss.json")
        ss = say(f"{d}.ss.json", lambda j: j.get("verdict") or j.get("risk") or j.get("summary") or list(j)[:3])
    satir.append(f"{r}\t{gl}\t{sg}\t{ss}\t{betik(d)}")
    print(satir[-1], flush=True)
(D / "tarama.tsv").write_text("\n".join(satir) + "\n", encoding="utf-8", newline="\n")
print("BITTI")

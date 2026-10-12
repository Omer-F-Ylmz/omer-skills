"""karar.tsv KUR satırları → Temp/igkur'a sığ klon + gitleaks/semgrep/skillspector (betik çalıştırma yok) → tarama.tsv."""
import json, os, pathlib, subprocess

D = pathlib.Path(__file__).parent
T = pathlib.Path(os.environ["TEMP"]) / "igkur"
T.mkdir(exist_ok=True)
SKILL = {"replica-skill", "career-ops", "app-store-screenshots", "ai-copywriter"}


def kos(*a):
    return subprocess.run(a, capture_output=True, text=True, encoding="utf-8", errors="replace")


def say(p, f):
    try:
        return str(f(json.loads(pathlib.Path(p).read_text(encoding="utf-8"))))
    except Exception as e:
        return f"hata:{type(e).__name__}"


satir = ["repo\tgitleaks\tsemgrep\tskillspector"]
for h in (s.split("\t") for s in (D / "karar.tsv").read_text(encoding="utf-8").splitlines()[1:]):
    if h[4] != "KUR" or "/" not in h[2] or h[2].startswith("claude-plugins"):
        continue
    ad = h[2].split("/")[1]
    d = T / ad
    if not d.exists():
        kos("git", "clone", "--depth", "1", "-c", "core.hooksPath=NUL", f"https://github.com/{h[2]}", str(d))
    kos("gitleaks", "dir", str(d), "--no-banner", "--redact", "-f", "json", "-r", f"{d}.gl.json")
    kos("semgrep", "scan", "--config", "p/security-audit", "--metrics=off", "--quiet", "--json", "-o", f"{d}.sg.json", str(d))
    gl = say(f"{d}.gl.json", len)
    sg = say(f"{d}.sg.json", lambda j: sum(r["extra"]["severity"] == "ERROR" for r in j["results"]) and
             f'{sum(r["extra"]["severity"] == "ERROR" for r in j["results"])}E/{len(j["results"])}' or f'0E/{len(j["results"])}')
    ss = "-"
    if ad in SKILL:
        kos("skillspector", "scan", str(d), "--no-llm", "--format", "json", "--output", f"{d}.ss.json")
        ss = say(f"{d}.ss.json", lambda j: j.get("verdict") or j.get("risk") or j.get("summary") or list(j)[:3])
    satir.append(f"{h[2]}\t{gl}\t{sg}\t{ss}")
    print(satir[-1], flush=True)
(D / "tarama.tsv").write_text("\n".join(satir) + "\n", encoding="utf-8", newline="\n")
print("BITTI")

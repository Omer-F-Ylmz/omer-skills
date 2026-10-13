"""IG-41-KUR hesapsız KUR adayları → gh meta + Temp/igkur41'e sığ klon (hook yok, betik çalıştırma yok) + gitleaks/semgrep/skillspector → tarama.tsv."""
import json, os, pathlib, subprocess

D = pathlib.Path(__file__).parent
T = pathlib.Path(os.environ["TEMP"]) / "igkur41"
T.mkdir(exist_ok=True)
REPO = ["t8y2/dbx", "wheresryan22/anatomy", "h4ckf0r0day/obscura", "img2threejs/img2threejs", "lucasmarkes/hairline",
        "Jakeschincariol/youtube-agent-skill", "Jpisnice/shadcn-ui-mcp-server", "anthropics/claude-for-legal", "vercel-labs/skills"]


def kos(*a):
    return subprocess.run(a, capture_output=True, text=True, encoding="utf-8", errors="replace",
                          creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0))


def say(p, f):
    try:
        return str(f(json.loads(pathlib.Path(p).read_text(encoding="utf-8"))))
    except Exception as e:
        return f"hata:{type(e).__name__}"


def sev(j):
    s = [r["extra"]["severity"] for r in j["results"]]
    return f'{s.count("ERROR")}E/{len(s)}'


def ss_ozet(j):
    if isinstance(j, dict):
        for k in ("verdict", "risk_level", "risk", "overall_risk"):
            if k in j:
                return j[k]
        b = j.get("findings") or j.get("issues") or []
        return f"bulgu {len(b)} · " + ",".join(sorted({str(x.get('severity')) for x in b if isinstance(x, dict)}))
    return type(j).__name__


satir = ["repo\tlisans\tpushed\tyildiz\tarsiv\tgitleaks\tsemgrep\tskillspector\tdosya"]
for repo in REPO:
    m = kos("gh", "api", f"repos/{repo}", "--jq", '[.license.spdx_id // "-", .pushed_at[:10], .stargazers_count, .archived] | @tsv')
    meta = m.stdout.strip() if m.returncode == 0 else "YOK\t-\t-\t-"
    d = T / repo.split("/")[1]
    if not d.exists():
        kos("git", "clone", "--depth", "1", "-c", "core.hooksPath=NUL", f"https://github.com/{repo}", str(d))
    if not d.exists():
        satir.append(f"{repo}\t{meta}\tklon-yok\t-\t-\t-")
        continue
    kos("gitleaks", "dir", str(d), "--no-banner", "--redact", "-f", "json", "-r", f"{d}.gl.json")
    kos("semgrep", "scan", "--config", "p/security-audit", "--metrics=off", "--quiet", "--json", "-o", f"{d}.sg.json", str(d))
    kos("skillspector", "scan", str(d), "--no-llm", "--format", "json", "--output", f"{d}.ss.json")
    n = sum(1 for _ in d.rglob("*") if _.is_file() and ".git" not in _.parts)
    satir.append(f"{repo}\t{meta}\t{say(f'{d}.gl.json', len)}\t{say(f'{d}.sg.json', sev)}\t{say(f'{d}.ss.json', ss_ozet)}\t{n}")
    print(satir[-1], flush=True)
(D / "tarama.tsv").write_text("\n".join(satir) + "\n", encoding="utf-8", newline="\n")
print("BITTI")

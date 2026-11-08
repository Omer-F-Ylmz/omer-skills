"""LINK-27EKI KUR aşaması 1 (Desktop): repo bul → sığ klon → lisans + gitleaks + boyut + README başı → .kos/kopru/video/link27/kur-ozet.md.
Kurulum (skill/MCP/CLI bağlama) Desktop tarafından bu özete göre yapılır. Silme yok; klonlar araclar/link27/<ad>."""
import json, re, shutil, subprocess, sys
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
HEDEF = Path(r"C:\Users\pc\Desktop\Claude ile yapılanlar\araclar\link27")
HEDEF.mkdir(parents=True, exist_ok=True)
OUT = Path(r"C:\Projeler\omer-skills\.kos\kopru\video\link27\kur-ozet.md")
REPOLAR = ["schmayterling/hibi", "ScrapeGraphAI/Scrapegraph-ai", "matank001/clodfarm", "develop212/agent-floor", "bytedance/deer-flow",
           "google-research/rrsi", "Louis-CFM/coucou", "msitarzewski/agency-agents", "deepseek-ai/deepseek-harness", "caveman-ai/trim-l",
           "JetBrains/thinkrail", "wesbos/3d-model-anything", "kokonut-labs/kokonutui", "SylphAI-Inc/LLM-engineer-handbook", "Zagitta/gpu-unlock",
           "tt-a1i/archify", "calesthio/OpenMontage", "ruucm/shadergradient", "paper-design/liquid-logo", "juliangarnier/anime"]
ARA = ["harness2 agent self-improve", "mcptoon", "TencentDB Agent Memory", "google agent skills", "rederive claude skill", "roast room claude skill",
       "chief of staff claude skill", "trim-1 caveman", "creem mcp", "hermes meshy plugin", "agent browser cloudflare open source", "gpu-unlock-ada"]


def gh(*a, t=60):
    r = subprocess.run(["gh", *a], capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=t)
    return r.stdout.strip() if r.returncode == 0 else ""


satir = ["# LINK-27EKI kurulum ön özeti", ""]
for q in ARA:
    j = gh("api", "-X", "GET", "search/repositories", "-f", f"q={q}", "-f", "per_page=3", "--jq", "[.items[]|{f:.full_name,s:.stargazers_count,d:.description}]")
    satir.append(f"- ARA `{q}` → {j[:400]}")
    try:
        for it in json.loads(j or "[]")[:1]:
            if it["s"] and it["s"] >= 30 and it["f"] not in REPOLAR:
                REPOLAR.append(it["f"])
    except Exception:
        pass
satir.append("")
gl = shutil.which("gitleaks")
for r in REPOLAR:
    k = json.loads(gh("api", f"repos/{r}", "--jq", "{l:(.license.spdx_id//\"yok\"),s:.stargazers_count,p:.pushed_at,d:.description,sz:.size}") or "{}")
    if not k:
        satir.append(f"## {r}\nBULUNAMADI\n"); continue
    d = HEDEF / r.replace("/", "__")
    if not d.exists() and (k.get("sz") or 0) < 400_000:
        subprocess.run(["git", "clone", "--depth", "1", f"https://github.com/{r}.git", str(d)], capture_output=True, timeout=600)
    sizi = "atlandı (çok büyük)" if not d.exists() else "klonlandı"
    sir = ""
    if d.exists() and gl:
        g = subprocess.run([gl, "detect", "--no-git", "-s", str(d), "--no-banner", "-r", str(d / ".gitleaks.json")], capture_output=True, text=True, errors="replace", timeout=300)
        sir = "gitleaks temiz" if g.returncode == 0 else "gitleaks BULGU (bkz .gitleaks.json)"
    oku = ""
    for ad in ["README.md", "readme.md", "README.MD", "Readme.md"]:
        if d.exists() and (d / ad).exists():
            oku = (d / ad).read_text(encoding="utf-8", errors="replace")[:1500]; break
    kurulum = "; ".join(sorted({m.strip() for m in re.findall(r"(?m)^\s*(?:\$ )?((?:pip|pipx|uv|npm|npx|pnpm|bun|brew|cargo|docker|git clone|claude mcp add|/plugin)[^\n`]{0,120})", oku)})[:6])
    satir += [f"## {r}", f"lisans {k.get('l')} · ⭐{k.get('s')} · son push {str(k.get('p'))[:10]} · {sizi} · {sir}", f"{k.get('d') or ''}",
              f"kurulum ipucu: {kurulum or '-'}", ""]
OUT.write_text("\n".join(satir), encoding="utf-8")
print("BITIS", len(REPOLAR))

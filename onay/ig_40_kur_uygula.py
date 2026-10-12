"""IG-40-KUR onay betiği — Desktop/Ömer koşar. Yalnız karar.tsv'de KUR olup güvenlik taramasını geçenleri kurar.

  python onay/ig_40_kur_uygula.py --kuru   # plan: ne kurulu, ne kurulacak (varsayılan)
  python onay/ig_40_kur_uygula.py uygula   # eksikleri kurar (idempotent), eklenenleri bildirime yazar
  python onay/ig_40_kur_uygula.py --geri   # yalnız BU betiğin eklediklerini geri alır (önceden kurulu olana dokunmaz)
Tarama (gitleaks · semgrep p/security-audit · SkillSpector --no-llm): wt igkur `.claude/igkur/tarama.tsv`. replica-skill
SkillSpector HIGH ×2 yanlış pozitif (App Store "description" karakter sınırı sözlüğü). Strix telemetrisi ayarla kapatılabilir.
Hesap/anahtar: strix → Docker + LLM anahtarı (Ömer listesi). Hiçbir şey kaldırılmaz/kapatılmaz; MCP listesi önce=sonra değilse rc=1.
"""
import json, shutil, subprocess, sys, tempfile
from pathlib import Path

EV = Path.home()
PLUGIN = [("Jakeschincariol/replica-skill", "replica-skill@replica-skill"),
          ("mikiarlo3/ai-copywriter", "ai-copywriter@ai-copywriter"),
          (None, "claude-code-setup@claude-plugins-official")]
UV = ["strix-agent", "claude-monitor"]
SKILL = [("ParthJadhav/app-store-screenshots", "skills/app-store-screenshots", "app-store-screenshots")]
KLON = [("career-ops-hq/career-ops", Path(r"C:\Projeler\career-ops"))]


def bildirim(ev):
    return ev / ".claude" / "ig40-kur-eklenen.json"


def kos(*a):
    return subprocess.run(a, capture_output=True, text=True, encoding="utf-8", errors="replace",
                          creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0))


def mcp_var_mi(ev=EV):
    """~/.claude.json'daki MCP sunucu adları (değer yazdırılmaz, yalnız adlar)."""
    try:
        j = json.loads((ev / ".claude.json").read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return set()
    adlar = set(j.get("mcpServers") or {})
    for p in (j.get("projects") or {}).values():
        adlar |= set((p or {}).get("mcpServers") or {})
    return adlar


def kurulu_plugin(ev=EV):
    try:
        return set(json.loads((ev / ".claude" / "plugins" / "installed_plugins.json").read_text(encoding="utf-8"))["plugins"])
    except (OSError, ValueError, KeyError):
        return set()


def kurulu_uv():
    return {s.split()[0] for s in kos("uv", "tool", "list").stdout.splitlines() if s and not s.startswith("-")}


def plan(ev=EV):
    """[(tür, ad, kurulu_mu)] — kurulum yapmaz."""
    p, u = kurulu_plugin(ev), kurulu_uv()
    return ([("plugin", ad, ad in p) for _, ad in PLUGIN] + [("uv", ad, ad in u) for ad in UV]
            + [("skill", ad, (ev / ".claude" / "skills" / ad).exists()) for _, _, ad in SKILL]
            + [("klon", str(hedef), hedef.exists()) for _, hedef in KLON])


def uygula(ev=EV):
    once, eklenen = mcp_var_mi(ev), []
    var = {(t, ad) for t, ad, k in plan(ev) if k}
    for repo, ad in PLUGIN:
        if ("plugin", ad) in var:
            continue
        if repo:
            kos("claude", "plugin", "marketplace", "add", repo)
        if kos("claude", "plugin", "install", ad).returncode == 0:
            eklenen.append(["plugin", ad])
    for ad in UV:
        if ("uv", ad) not in var and kos("uv", "tool", "install", ad).returncode == 0:
            eklenen.append(["uv", ad])
    for repo, alt, ad in SKILL:
        if ("skill", ad) in var:
            continue
        with tempfile.TemporaryDirectory() as t:
            if kos("git", "clone", "--depth", "1", f"https://github.com/{repo}", t + "/r").returncode == 0:
                shutil.copytree(Path(t) / "r" / alt, ev / ".claude" / "skills" / ad)
                eklenen.append(["skill", ad])
    for repo, hedef in KLON:
        if ("klon", str(hedef)) not in var and kos("git", "clone", "--depth", "1", f"https://github.com/{repo}", str(hedef)).returncode == 0:
            eklenen.append(["klon", str(hedef)])
    eski = json.loads(bildirim(ev).read_text(encoding="utf-8")) if bildirim(ev).exists() else []
    bildirim(ev).write_text(json.dumps(eski + eklenen, ensure_ascii=False, indent=1), encoding="utf-8")
    for t, ad in eklenen:
        print("eklendi", t, ad)
    return once == mcp_var_mi(ev)


def geri(ev=EV):
    once = mcp_var_mi(ev)
    if not bildirim(ev).exists():
        print("bildirim yok: geri alınacak bir şey yok")
        return True
    for t, ad in reversed(json.loads(bildirim(ev).read_text(encoding="utf-8"))):
        if t == "plugin":
            kos("claude", "plugin", "uninstall", ad)
        elif t == "uv":
            kos("uv", "tool", "uninstall", ad)
        elif t == "skill":
            shutil.rmtree(ev / ".claude" / "skills" / ad, ignore_errors=True)
        elif t == "klon":
            shutil.rmtree(ad, ignore_errors=True)
        print("geri", t, ad)
    bildirim(ev).unlink()
    return once == mcp_var_mi(ev)


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    kip = sys.argv[1] if len(sys.argv) > 1 else "--kuru"
    if kip == "uygula":
        ok = uygula()
    elif kip == "--geri":
        ok = geri()
    else:
        for t, ad, k in plan():
            print(f"{t}\t{ad}\t{'kurulu (atlanır)' if k else 'kurulacak'}")
        ok = True
    print("mcp önce=sonra" if ok else "HATA: MCP listesi değişti")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()

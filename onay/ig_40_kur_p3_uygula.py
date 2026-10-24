"""IG-40-KUR P3 (sira 221–406) onay betiği. Varsayılan --kuru (plan basar, değişiklik yok); `uygula` kurar; `--geri` yalnız bu betiğin eklediğini kaldırır.
CC: trailofbits marketplace + differential-review plugin, reel-plan skill (~/.claude/skills). claude.ai: dist/ig-40-p3 zip'lerini Ömer yükler.
Yedek: ~/.claude/settings.json + plugins/{known_marketplaces,installed_plugins}.json → .claude/igkur/p3/yedek/<zaman>/. MCP listesi önce = sonra denetlenir."""
import json, pathlib, shutil, subprocess, sys, time

KOK = pathlib.Path(__file__).resolve().parents[1]
P3 = KOK / ".claude" / "igkur" / "p3"
H = pathlib.Path.home() / ".claude"
DURUM = P3 / "uygulandi.json"
PAZAR, PAZAR_REPO, PLUGIN = "trailofbits", "trailofbits/skills", "differential-review@trailofbits"
SKILL_KAYNAK, SKILL_HEDEF = P3 / "skill" / "reel-plan", H / "skills" / "reel-plan"
OW = getattr(subprocess, "CREATE_NO_WINDOW", 0)


def claude(*a):
    r = subprocess.run(["claude", *a], capture_output=True, text=True, encoding="utf-8", errors="replace", creationflags=OW)
    if r.returncode:
        sys.exit(f"HATA claude {' '.join(a)}: {r.stderr.strip()[:300]}")
    return r.stdout


def oku(ad):
    p = H / "plugins" / ad
    return json.loads(p.read_text(encoding="utf-8")) if p.exists() else {}


def pazar_var():
    return PAZAR in oku("known_marketplaces.json")


def plugin_var():
    i = oku("installed_plugins.json")
    return PLUGIN in i.get("plugins", i)


def mcp_adlari():
    # yalnız adlar (bağlantı durumu koşudan koşuya değişir); ad "plugin:x:y" biçiminde iki nokta içerebilir
    return sorted(l.split(": ")[0].strip() for l in claude("mcp", "list").splitlines() if ": " in l and not l.startswith("Checking"))


def plan():
    return [(f"CC marketplace add {PAZAR_REPO}", pazar_var()), (f"CC plugin install {PLUGIN}", plugin_var()),
            (f"CC skill kopyala → {SKILL_HEDEF}", SKILL_HEDEF.exists())]


def kuru():
    for ad, var in plan():
        print(("ATLA (var) " if var else "YAPILACAK ") + ad)
    for z in sorted((KOK / "dist" / "ig-40-p3").rglob("*.zip")):
        print(f"claude.ai (Ömer yükler): {z}")
    print("İNCELE (kurulmaz): trailofbits supply-chain-risk-auditor, static-analysis, insecure-defaults — SkillSpector HIGH, bkz. p3/tarama.tsv")


def uygula():
    yedek = P3 / "yedek" / time.strftime("%Y%m%d-%H%M%S")
    yedek.mkdir(parents=True)
    for p in (H / "settings.json", H / "plugins" / "known_marketplaces.json", H / "plugins" / "installed_plugins.json"):
        if p.exists():
            shutil.copy2(p, yedek / p.name)
    once = mcp_adlari()
    eklenen = json.loads(DURUM.read_text(encoding="utf-8")) if DURUM.exists() else []
    if not pazar_var():
        claude("plugin", "marketplace", "add", PAZAR_REPO)
        eklenen.append("pazar")
    if not plugin_var():
        claude("plugin", "install", PLUGIN)
        eklenen.append("plugin")
    if not SKILL_HEDEF.exists():
        shutil.copytree(SKILL_KAYNAK, SKILL_HEDEF)
        eklenen.append("skill")
    DURUM.write_text(json.dumps(sorted(set(eklenen))), encoding="utf-8")
    sonra = mcp_adlari()
    print(f"yedek: {yedek}\neklenen: {sorted(set(eklenen))}\nMCP önce=sonra: {once == sonra} ({len(once)})")
    if once != sonra:
        sys.exit(f"UYARI MCP listesi değişti: {sorted(set(once) ^ set(sonra))}")


def geri():
    eklenen = json.loads(DURUM.read_text(encoding="utf-8")) if DURUM.exists() else []
    if "skill" in eklenen and SKILL_HEDEF.exists():
        shutil.rmtree(SKILL_HEDEF)
    if "plugin" in eklenen and plugin_var():
        claude("plugin", "uninstall", PLUGIN)
    if "pazar" in eklenen and pazar_var():
        claude("plugin", "marketplace", "remove", PAZAR)
    DURUM.unlink(missing_ok=True)
    print(f"geri alındı: {eklenen or 'hiçbiri (kayıt yok)'}")


if __name__ == "__main__":
    {"uygula": uygula, "--geri": geri}.get((sys.argv[1:] or ["--kuru"])[0], kuru)()

"""KURULUM-DALGASI-2b betikleri. Kullanim: python -I tools/kurulum2b.py {p1b|token ETIKET|p2|p3} [--kuru]
Hepsi idempotent, tek seferde tek kurulum. --kuru: komutu calistirmaz, yazdirir.
Cikti ozetleri .kos/kopru/ara/ altina; ortam degiskeni DEGERI hicbir yerde yazilmaz."""
import json, os, re, shutil, subprocess, sys, tempfile, time
from pathlib import Path

KOK = Path(__file__).resolve().parent.parent
ARA = KOK / ".kos" / "kopru" / "ara"
INDIRILEN = Path("C:/AI/indirilen")
KURU = "--kuru" in sys.argv
NO_WIN = getattr(subprocess, "CREATE_NO_WINDOW", 0)


def calis(cmd, zaman=600, **kw):
    print("$", " ".join(map(str, cmd)), flush=True)
    if KURU:
        return 0, ""
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=zaman,
                           creationflags=NO_WIN, encoding="utf8", errors="replace", **kw)
        return r.returncode, (r.stdout + r.stderr)[-400:]
    except Exception as e:
        return 99, f"{type(e).__name__}: {e}"


def beyin(metin):
    """2 dk kurali: ilerleme olayi, $0."""
    with open(KOK / ".kos" / "kopru" / "beyin-olay.jsonl", "a", encoding="utf8") as f:
        f.write(json.dumps({"t": round(time.time(), 1), "tur": "ilerleme", "arac": "", "ozet": metin, "hata": False, "kaynak": "kurulum2b"},
                           ensure_ascii=False) + "\n")  # beyin-olay.jsonl ortak biçimi (arka_bekci/beyin_dusun ile aynı anahtarlar)


def not_yaz(ad, satirlar):
    ARA.mkdir(parents=True, exist_ok=True)
    (ARA / ad).write_text("\n".join(satirlar), encoding="utf8", newline="\n")


# ---- P1b: basarisiz plugin yeniden + gitleaks bulgularini kural kimligiyle sinifla ----
YOL_TEST = re.compile(r"(test|spec|example|sample|fixture|mock|docs?/|readme|\.md$|demo|snapshot|dummy|fake|\.github|lock|\.ipynb|cassette|e2e|third_party|vendor)", re.I)
ORNEK_KURAL = {"generic-api-key", "curl-auth-header", "private-key"}  # test dosyasinda zararsiz sayilir


def p1b():
    out = []
    rc, m = calis(["claude", "plugin", "install", "seo-cockpit@agricidaniel-claude-seo"])
    out.append(f"seo-cockpit retry rc={rc} {m[-120:]!r}")
    beyin(f"p1b seo-cockpit retry rc={rc}")
    log = (KOK / ".claude" / "_kur2.log").read_text(encoding="utf8", errors="replace")
    adlar = sorted({l.split()[1] for l in log.splitlines() if l.startswith("GITLEAKS-INCELE")})
    gercek, benign = [], 0
    for ad in adlar:
        d = INDIRILEN / ad
        rap = Path(tempfile.gettempdir()) / f"gl-{ad}.json"
        rc, _ = calis(["gitleaks", "detect", "--no-git", "-s", str(d), "-f", "json", "-r", str(rap),
                       "--exit-code", "0", "--max-target-megabytes", "2"], zaman=300)
        bul = json.loads(rap.read_text(encoding="utf8")) if rap.exists() else []
        kotu = [b for b in bul if not YOL_TEST.search(b["File"].replace("\\", "/").split(ad, 1)[-1])]
        if kotu:
            gercek.append(f"{ad}: {len(kotu)} bulgu; kurallar={sorted({b['RuleID'] for b in kotu})}; "
                          f"ornek={kotu[0]['File'].split(ad,1)[-1][:70]}:{kotu[0]['StartLine']}")
        else:
            benign += 1
        rap.unlink(missing_ok=True)
        if len(adlar) and (adlar.index(ad) % 20 == 0):
            beyin(f"p1b gitleaks {adlar.index(ad)}/{len(adlar)}")
    not_yaz("p1b-gitleaks.md", [f"benign(yalniz test/ornek/doc yolu)={benign} incele={len(gercek)}", *gercek])
    print("yazildi: .kos/kopru/ara/p1b-gitleaks.md")


# ---- Token: bos oturum baslangic maliyeti (tek kisa claude -p) ----
def token(etiket):
    bos = Path(tempfile.mkdtemp(prefix="bos-oturum-"))
    if KURU:
        return
    r = subprocess.run(["claude", "-p", "ok", "--output-format", "json", "--no-session-persistence"],
                       capture_output=True, text=True, cwd=bos, creationflags=NO_WIN, encoding="utf8")
    u = json.loads(r.stdout).get("usage", {})
    girdi = u.get("input_tokens", 0) + u.get("cache_creation_input_tokens", 0) + u.get("cache_read_input_tokens", 0)
    not_yaz(f"token-{etiket}.md", [f"{etiket}: bos oturum girdi={girdi} ({u})"])
    print(etiket, girdi)
    shutil.rmtree(bos, ignore_errors=True)


# ---- P2: npm/pip CLI + MCP sunuculari ----
NPM = ["@agentrhq/webcmd", "@googleworkspace/cli", "@higgsfield/cli", "@musistudio/claude-code-router",
       "@openai/codex", "codeburn", "context-mode", "firecrawl-cli", "ruflo"]
PIP = ["graphifyy", "composio", "pyright"]
MCP = {  # ad -> (command, args)
    "playwright": ("npx", ["-y", "@playwright/mcp"]),
    "hostinger": ("npx", ["-y", "@hostinger/mcp"]),
}
DESKTOP = Path(os.environ.get("LOCALAPPDATA", "")) / "Packages" / "Claude_pzs8sxrjxfjjc" / "LocalCache" / "Roaming" / "Claude" / "claude_desktop_config.json"


def sema_tamam(ad, cmd, args):
    return bool(ad) and isinstance(cmd, str) and cmd and isinstance(args, list) and all(isinstance(a, str) for a in args)


def p2():
    out = []
    for p in NPM:
        var = calis(["npm.cmd", "ls", "-g", p, "--depth=0"])[0] == 0 and not KURU
        rc = 0 if var else calis(["npm.cmd", "i", "-g", p])[0]
        out.append(f"npm {p}: {'zaten' if var else f'rc={rc}'}")
    for p in PIP:
        var = calis([sys.executable, "-m", "pip", "show", p])[0] == 0 and not KURU
        rc = 0 if var else calis([sys.executable, "-m", "pip", "install", p])[0]
        out.append(f"pip {p}: {'zaten' if var else f'rc={rc}'}")
        beyin(f"p2 pip {p}")
    if DESKTOP.exists() and not KURU:
        yedek = DESKTOP.with_suffix(f".json.yedek-{time.strftime('%Y%m%d%H%M%S')}")
        shutil.copy2(DESKTOP, yedek)
        cfg = json.loads(DESKTOP.read_text(encoding="utf8"))
        sv = cfg.setdefault("mcpServers", {})
        for ad, (cmd, args) in MCP.items():
            if ad in sv:
                out.append(f"mcp desktop {ad}: zaten")
            elif sema_tamam(ad, cmd, args):
                sv[ad] = {"command": cmd, "args": args}
                out.append(f"mcp desktop {ad}: eklendi")
        DESKTOP.write_text(json.dumps(cfg, indent=2, ensure_ascii=False), encoding="utf8")
    for ad, (cmd, args) in MCP.items():  # CC user-scope
        rc, _ = calis(["claude", "mcp", "get", ad])
        if rc != 0 or KURU:
            rc, m = calis(["claude", "mcp", "add", "-s", "user", ad, "--", cmd, *args])
            out.append(f"mcp cc {ad}: rc={rc}")
        else:
            out.append(f"mcp cc {ad}: zaten")
    not_yaz("p2-sonuc.md", out)
    print("\n".join(out))


# ---- P3: claude.ai zip'leri + ayar bekleyen 9 plugin + duman ----
PLUGIN = {"blast-radius": "claude-code-mods", "next-steps": "claude-code-mods", "token-weather": "claude-code-mods",
          "switchboard": "claude-code-mods", "openai-balance": "claude-code-mods",
          "openrouter-balance": "claude-code-mods", "now-playing": "claude-code-mods",
          "prayer-times": "claude-code-mods", "task-observer": "one-skill-to-rule-them-all"}
ANAHTAR = {"openai-balance": "OPENAI_API_KEY", "openrouter-balance": "OPENROUTER_API_KEY"}


def p3():
    out = []
    for ad, mkt in PLUGIN.items():
        rc, _ = calis(["claude", "plugin", "install", f"{ad}@{mkt}"])
        env = ANAHTAR.get(ad)
        durum = "anahtar gerekmez" if not env else ("anahtar VAR" if os.environ.get(env) else f"anahtar YOK ({env})")
        rc2, m2 = calis(["claude", "plugin", "details", ad])
        out.append(f"plugin {ad}@{mkt}: kur rc={rc} details rc={rc2}; {durum}")
        beyin(f"p3 plugin {ad} rc={rc}")
    zipdir = KOK / "dist" / "claude-ai-2b"
    zipdir.mkdir(parents=True, exist_ok=True)
    kaynak = [str(p) for p in (KOK / "skills").glob("*") if p.is_dir()] if (KOK / "skills").exists() else []
    if kaynak:
        rc, m = calis([sys.executable, "-I", str(KOK / "tools" / "skill-paket" / "paketle.py"), "--buyuk",
                       "aile-2b", "kurulum dalgasi 2b skilleri", str(zipdir), *kaynak])
        out.append(f"zip paketle rc={rc}")
        rc, m = calis([sys.executable, "-I", str(KOK / "tools" / "skill-paket" / "zip_denetle.py"), str(zipdir)])
        out.append(f"zip_denetle rc={rc} {m[-100:]!r}")
    else:
        out.append("zip: skills/ yok, atlandi")
    for ad in MCP:  # MCP duman: tools/list
        rc, m = calis([sys.executable, "-I", str(KOK / "tools" / "mcp_kurutest.py"), "--config", "desktop"], zaman=300)
        out.append(f"mcp duman (kurutest desktop) rc={rc}")
        break
    not_yaz("p3-sonuc.md", out)
    print("\n".join(out))


if __name__ == "__main__":
    a = [x for x in sys.argv[1:] if x != "--kuru"]
    if not a:
        sys.exit(__doc__)
    {"p1b": p1b, "token": lambda: token(a[1] if len(a) > 1 else "once"), "p2": p2, "p3": p3}[a[0]]()

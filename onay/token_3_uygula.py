"""TOKEN-3 onay betiği — Desktop koşar (Ömer onayından sonra). VEKİL: settings.json/ANTHROPIC_BASE_URL'ye dokunmaz.
(a) K15: skills/is-akisi → ~/.claude/skills/is-akisi
(b) K12: ~/.claude/CLAUDE.md alt ajan satırında "(model: sonnet)" → okuyucu/tek yargıç/dosyaya öz kuralı
(c) K14: tools/cagri_sayac.py → ~/.claude/plugins/marketplaces/omer-skills/tools/ (bağlam ≥150k DUR; 45'te yalnız ≥120k).
    shortcut: marketplace klonuna kopya; eklenti güncellemesi origin'den ezer → kalıcısı push (Ömer).

  python onay/token_3_uygula.py --kuru   # plan (varsayılan)
  python onay/token_3_uygula.py uygula   # yedek → (a)(b)(c)
  python onay/token_3_uygula.py --geri   # son yedeği geri koyar"""
import shutil
import sys
import time
from pathlib import Path

KOK = Path(__file__).resolve().parents[1]
ESKI = "go to a subagent (model: sonnet)"
YENI = ("go to a subagent: okuyucu (narrow tools); general-purpose only if it must write or needs MCP; arms scored by the same "
        "criteria go to ONE judge; big pages/logs stay in a file and only a summary returns (also inside the subagent)")


def hedefler(ev):
    c = ev / ".claude"
    return {"skill": (KOK / "skills" / "is-akisi", c / "skills" / "is-akisi"),
            "claude_md": (None, c / "CLAUDE.md"),
            "sayac": (KOK / "tools" / "cagri_sayac.py", c / "plugins" / "marketplaces" / "omer-skills" / "tools" / "cagri_sayac.py")}


def plan(ev):
    h = hedefler(ev)
    md = h["claude_md"][1].read_text(encoding="utf-8") if h["claude_md"][1].exists() else ""
    print("(a) skill:", h["skill"][1], "var" if h["skill"][1].exists() else "yeni")
    print("(b) CLAUDE.md:", "değişecek 1 yer" if md.count(ESKI) == 1 else ("zaten yeni" if YENI in md else f"ESKİ METİN {md.count(ESKI)} kez — elle bak"))
    print("(c) sayaç:", h["sayac"][1], "var" if h["sayac"][1].exists() else "YOK — kopyalanmaz")
    return 0


def uygula(ev):
    h = hedefler(ev)
    yedek = ev / ".claude" / "backups" / f"token-3-{time.strftime('%Y%m%d-%H%M%S')}"
    yedek.mkdir(parents=True)
    kaynak, hedef = h["skill"]
    if hedef.exists():
        shutil.copytree(hedef, yedek / "skill")
        shutil.rmtree(hedef)
    shutil.copytree(kaynak, hedef, ignore=shutil.ignore_patterns("__pycache__"))
    md = h["claude_md"][1]
    if md.exists() and md.read_text(encoding="utf-8").count(ESKI) == 1:
        shutil.copy2(md, yedek / "CLAUDE.md")
        md.write_bytes(md.read_bytes().replace(ESKI.encode(), YENI.encode()))  # bayt düzeyi: CRLF korunur
    kaynak, hedef = h["sayac"]
    if hedef.exists():
        shutil.copy2(hedef, yedek / "cagri_sayac.py")
        shutil.copy2(kaynak, hedef)
    print("uygulandı · yedek", yedek)
    return 0


def geri(ev):
    yedekler = sorted((ev / ".claude" / "backups").glob("token-3-*"))
    if not yedekler:
        print("yedek yok")
        return 1
    y, h = yedekler[-1], hedefler(ev)
    shutil.rmtree(h["skill"][1], ignore_errors=True)
    if (y / "skill").exists():
        shutil.copytree(y / "skill", h["skill"][1])
    for ad, anahtar in (("CLAUDE.md", "claude_md"), ("cagri_sayac.py", "sayac")):
        if (y / ad).exists():
            shutil.copy2(y / ad, h[anahtar][1])
    print("geri alındı:", y)
    return 0


def main(argv=None, ev=Path.home()):
    a = (argv if argv is not None else sys.argv[1:]) or ["--kuru"]
    return {"--kuru": plan, "uygula": uygula, "--geri": geri}[a[0]](ev)


if __name__ == "__main__":
    sys.exit(main())

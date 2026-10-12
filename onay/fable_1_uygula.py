"""FABLE-1 onay betiği — Desktop/Ömer koşar; yalnız ölçüm KABUL ise (rapor/fable-1.md).

  python onay/fable_1_uygula.py --kuru   # plan: ne kopyalanır, kaç ajana satır eklenir (varsayılan)
  python onay/fable_1_uygula.py uygula   # yedek alır → skill kopyalar → ajan frontmatter'ına `skills: calisma-protokolu` ekler
  python onay/fable_1_uygula.py --geri   # son yedeği geri koyar
(a) skills/calisma-protokolu → ~/.claude/skills/calisma-protokolu. (b) ~/.claude/agents/*.md: frontmatter'da `skills:` yoksa
tek satır eklenir (varsa dokunulmaz, plan "elle" der). claude.ai tarafı: dist/fable-1/calisma-protokolu.zip (zip_denetle TEMİZ).
Hiçbir şey silinmez; settings/MCP'ye dokunulmaz."""
import re, shutil, sys, time
from pathlib import Path

KOK = Path(__file__).resolve().parents[1]
SATIR = "skills: calisma-protokolu"


def plan(ev):
    ajanlar, elle = [], []
    for a in sorted((ev / ".claude" / "agents").glob("*.md")):
        m = re.match(r"---\r?\n(.*?)\r?\n---", a.read_text(encoding="utf-8"), re.S)
        (elle if not m or re.search(r"^skills:", m.group(1), re.M) else ajanlar).append(a)
    return ajanlar, elle


def satir_ekle(yol):
    b = yol.read_bytes()
    nl = b"\r\n" if b.startswith(b"---\r\n") else b"\n"
    yol.write_bytes(b.replace(b"---" + nl, b"---" + nl + SATIR.encode() + nl, 1))


def uygula(ev):
    ajanlar, _ = plan(ev)
    yedek = ev / ".claude" / "backups" / f"fable-1-{time.strftime('%Y%m%d-%H%M%S')}"
    (yedek / "agents").mkdir(parents=True)
    hedef = ev / ".claude" / "skills" / "calisma-protokolu"
    if hedef.exists():
        shutil.copytree(hedef, yedek / "skill")
        shutil.rmtree(hedef)
    shutil.copytree(KOK / "skills" / "calisma-protokolu", hedef)
    for a in ajanlar:
        shutil.copy2(a, yedek / "agents" / a.name)
        satir_ekle(a)
    print("uygulandı:", hedef, "·", len(ajanlar), "ajan · yedek", yedek)


def geri(ev):
    yedekler = sorted((ev / ".claude" / "backups").glob("fable-1-*"))
    if not yedekler:
        print("yedek yok"); return 1
    y = yedekler[-1]
    for a in (y / "agents").glob("*.md"):
        shutil.copy2(a, ev / ".claude" / "agents" / a.name)
    hedef = ev / ".claude" / "skills" / "calisma-protokolu"
    shutil.rmtree(hedef, ignore_errors=True)
    if (y / "skill").exists():
        shutil.copytree(y / "skill", hedef)
    print("geri alındı:", y)
    return 0


def main(argv=None, ev=Path.home()):
    a = (argv if argv is not None else sys.argv[1:]) or ["--kuru"]
    if a[0] == "uygula":
        uygula(ev); return 0
    if a[0] == "--geri":
        return geri(ev)
    ajanlar, elle = plan(ev)
    print(f"KURU: skill -> {ev / '.claude' / 'skills' / 'calisma-protokolu'} · {len(ajanlar)} ajana '{SATIR}' · elle {[e.name for e in elle]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

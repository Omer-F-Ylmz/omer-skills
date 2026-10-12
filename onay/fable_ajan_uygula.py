"""FABLE-AJAN onay betiği — Desktop/Ömer koşar; yalnız KABUL çıkan aile × model çiftlerine (docs/kutuphane/olcum/fable-ajan-karar.tsv).

  python onay/fable_ajan_uygula.py --kuru   # plan: hangi ajana blok girer, protokol jetonu, MCP (varsayılan)
  python onay/fable_ajan_uygula.py uygula   # yedek → ~/.claude/agents/<aile>-*.md (model eşleşen) godmode bloğu
  python onay/fable_ajan_uygula.py --geri   # yalnız godmode bloğunu söker (sonraki elle düzenlemeler kalır); yedek de durur
Tek kaynak: skills/calisma-protokolu/SKILL.md gövdesi → tools/godmode_onsoz.enjekte (işaret `godmode`, frontmatter sonrası).
Protokol güncellenince `uygula` yeniden koşulur; aynıysa dosya değişmez. Bütçe: ders-yuvasi ≤ 300 + protokol ≤ PROTOKOL_TAVAN jeton.
Model değişmez; settings/MCP'ye dokunulmaz (~/.claude.json mcpServers önce = sonra denetlenir). claude.ai: dist/fable-ajan/*.zip."""
import json, re, shutil, sys, time
from pathlib import Path

KOK = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(KOK / "tools"))
from godmode_onsoz import enjekte  # noqa: E402

KAYNAK = KOK / "skills" / "calisma-protokolu" / "SKILL.md"
KARAR = KOK / "docs" / "kutuphane" / "olcum" / "fable-ajan-karar.tsv"
DERS_TAVAN, PROTOKOL_TAVAN = 300, 250  # jeton; ikisi aynı önsözde: ≤ 550


def jeton(metin):
    return round(len(metin.split()) * 1.35)  # kaba tahmin (TR/EN karışık, tokenizer yok)


def govde():
    t = KAYNAK.read_text(encoding="utf-8")
    m = re.match(r"---\r?\n.*?\r?\n---\r?\n", t, re.S)
    return t[m.end():].strip() if m else t.strip()


def kabuller():
    if not KARAR.exists():
        return set()
    return {tuple(s.split("\t")[:2]) for s in KARAR.read_text(encoding="utf-8").splitlines()[1:] if s.split("\t")[2:3] == ["KABUL"]}


def plan(ev):
    kabul, out = kabuller(), []
    for a in sorted((ev / ".claude" / "agents").glob("*.md")):
        m = re.match(r"---\r?\n(.*?)\r?\n---", a.read_text(encoding="utf-8"), re.S)
        if not m:
            continue
        model = (re.search(r"^model:\s*(\S+)", m.group(1), re.M) or [None, ""])[1].strip("'\"")
        if (a.stem.split("-")[0], model) in kabul:
            out.append(a)
    return out


def mcp(ev):
    y = ev / ".claude.json"
    return sorted((json.loads(y.read_text(encoding="utf-8")).get("mcpServers") or {}) if y.exists() else {})


def main(argv=None, ev=Path.home()):
    a = (argv if argv is not None else sys.argv[1:]) or ["--kuru"]
    g, ajanlar, once = govde(), plan(ev), mcp(ev)
    if jeton(g) > PROTOKOL_TAVAN:
        print(f"DUR: protokol ~{jeton(g)} jeton > {PROTOKOL_TAVAN}"); return 2
    if a[0] == "--geri":
        n = sum(enjekte(p, "", geri=True) for p in sorted((ev / ".claude" / "agents").glob("*.md")))
        print("geri alındı:", n, "ajan"); return 0
    if a[0] != "uygula":
        print(f"KURU: {len(ajanlar)} ajana godmode bloğu (~{jeton(g)} jeton, tavan {PROTOKOL_TAVAN}+ders {DERS_TAVAN}) · KABUL {sorted(kabuller())}")
        print("  ", " ".join(p.stem for p in ajanlar)); return 0
    yedek = ev / ".claude" / "backups" / f"fable-ajan-{time.strftime('%Y%m%d-%H%M%S')}"
    degisecek = [p for p in ajanlar if enjekte(p, g, kuru=True)]
    for p in degisecek:
        yedek.mkdir(parents=True, exist_ok=True)
        shutil.copy2(p, yedek / p.name)
    n = sum(enjekte(p, g) for p in degisecek)
    if mcp(ev) != once:
        print("DUR: MCP listesi değişti"); return 3
    print("uygulandı:", n, "/", len(ajanlar), "ajan · yedek", yedek, "· MCP önce=sonra"); return 0


if __name__ == "__main__":
    sys.exit(main())

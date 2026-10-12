"""FABLE-AJAN onay betiği — Desktop/Ömer koşar; yalnız KABUL çıkan aile × model çiftlerine (docs/kutuphane/olcum/fable-ajan-karar.tsv).
fable_1_uygula TABANININ ÜSTÜNE katman: `skills: calisma-protokolu` taşıyan ajan atlanır (çift ekleme yok).

  python onay/fable_ajan_uygula.py --kuru   # plan: hangi ajana hangi protokol, hook haritası, MCP (varsayılan)
  python onay/fable_ajan_uygula.py uygula   # yedek → ~/.claude/agents/<aile>-*.md godmode bloğu + plugin ajanları için SubagentStart hook
  python onay/fable_ajan_uygula.py --geri   # godmode bloklarını, hook kaydını ve ~/.claude/hooks/fable-ajan'ı söker; yedek durur
Protokol aile × model başına (karar.tsv 4. sütun): calisma-protokolu = skills/calisma-protokolu/SKILL.md gövdesi, diğer ad =
docs/kutuphane/olcum/fable-ajan-protokol/<ad>.md (ör. haiku-v1 ultra-kısa). Plugin ajan dosyaları güncellemede ezildiği için
DEĞİŞMEZ: aile `plugin` KABUL ise tools/fable_ajan_hook.py + harita.json ~/.claude/hooks/fable-ajan'a kopyalanır, settings.json'a
tek SubagentStart kaydı eklenir (settings yedeklenir). Model değişmez; MCP önce = sonra denetlenir. claude.ai: dist/fable-ajan/*.zip."""
import json, re, shutil, sys, time
from pathlib import Path

KOK = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(KOK / "tools"), str(KOK / "tools" / "olcum")]
from godmode_onsoz import enjekte  # noqa: E402
from fable_ajan_envanter import plugin_kimlik  # noqa: E402

KAYNAK = KOK / "skills" / "calisma-protokolu" / "SKILL.md"
VARYANT = KOK / "docs" / "kutuphane" / "olcum" / "fable-ajan-protokol"
KARAR = KOK / "docs" / "kutuphane" / "olcum" / "fable-ajan-karar.tsv"
HOOK = KOK / "tools" / "fable_ajan_hook.py"
DERS_TAVAN, PROTOKOL_TAVAN = 300, 250  # jeton; ikisi aynı önsözde: ≤ 550
TABAN = re.compile(r"^skills:.*calisma-protokolu", re.M)  # fable_1_uygula tabanı


def jeton(metin):
    return round(len(metin.split()) * 1.35)  # kaba tahmin (TR/EN karışık, tokenizer yok)


def govde(ad="calisma-protokolu"):
    t = (KAYNAK if ad == "calisma-protokolu" else VARYANT / f"{ad}.md").read_text(encoding="utf-8")
    m = re.match(r"---\r?\n.*?\r?\n---\r?\n", t, re.S)
    return (t[m.end():] if m else t).strip()


def kabuller():
    """(aile, model) → protokol adı; yalnız KABUL satırları (eski 3 sütunlu TSV → calisma-protokolu)."""
    if not KARAR.exists():
        return {}
    satirlar = [s.split("\t") for s in KARAR.read_text(encoding="utf-8").splitlines()[1:]]
    return {(s[0], s[1]): (s[3] if len(s) > 3 and s[3] else "calisma-protokolu") for s in satirlar if s[2:3] == ["KABUL"]}


def frontmatter(yol):
    m = re.match(r"---\r?\n(.*?)\r?\n---", yol.read_text(encoding="utf-8", errors="replace"), re.S)
    return m.group(1) if m else None


def model_of(fm):
    return (re.search(r"^model:\s*(\S+)", fm, re.M) or [None, ""])[1].strip("'\"")


def plan(ev):
    """→ [(ajan yolu, protokol adı)]: kullanıcı ajanı, aile × model KABUL, taban (skills) değil."""
    kabul, out = kabuller(), []
    for a in sorted((ev / ".claude" / "agents").glob("*.md")):
        fm = frontmatter(a)
        ad = kabul.get((a.stem.split("-")[0], model_of(fm))) if fm is not None else None
        if ad and not TABAN.search(fm):
            out.append((a, ad))
    return out


def harita(ev):
    """Plugin alt ajanları (dosyaya dokunulmaz) → {'plugin:ad': protokol adı}; model (plugin, model) KABUL ise."""
    kabul, cache, out = kabuller(), ev / ".claude" / "plugins" / "cache", {}
    for y in sorted(cache.glob("**/agents/**/*.md")) if cache.is_dir() else []:
        fm = frontmatter(y)
        ad = fm and (re.search(r"^name:\s*(\S+)", fm, re.M) or [None, ""])[1].strip("'\"")
        k = ad and plugin_kimlik(y, ad, cache)
        if k and (("plugin", model_of(fm)) in kabul):
            out[k] = kabul[("plugin", model_of(fm))]
    return out


def hook_komutu(ev):
    d = ev / ".claude" / "hooks" / "fable-ajan"
    return f'python "{(d / "fable_ajan_hook.py").as_posix()}" "{(d / "harita.json").as_posix()}"'


def hook_kur(ev, h, yedek):
    d, ayar = ev / ".claude" / "hooks" / "fable-ajan", ev / ".claude" / "settings.json"
    d.mkdir(parents=True, exist_ok=True)
    shutil.copy2(HOOK, d / "fable_ajan_hook.py")
    (d / "harita.json").write_text(json.dumps({"metin": {a: govde(a) for a in set(h.values())}, "ajan": h}, ensure_ascii=False), encoding="utf-8")
    s = json.loads(ayar.read_text(encoding="utf-8")) if ayar.exists() else {}
    kayit = s.setdefault("hooks", {}).setdefault("SubagentStart", [])
    if any(k.get("command") == hook_komutu(ev) for g in kayit for k in g.get("hooks", [])):
        return
    if ayar.exists():
        yedek.mkdir(parents=True, exist_ok=True)
        shutil.copy2(ayar, yedek / "settings.json")
    kayit.append({"matcher": ".*", "hooks": [{"type": "command", "command": hook_komutu(ev)}]})
    ayar.write_text(json.dumps(s, ensure_ascii=False, indent=2), encoding="utf-8")


def hook_sok(ev):
    d, ayar = ev / ".claude" / "hooks" / "fable-ajan", ev / ".claude" / "settings.json"
    if ayar.exists():
        s = json.loads(ayar.read_text(encoding="utf-8"))
        h = s.get("hooks", {})
        kalan = [g for g in h.get("SubagentStart", []) if not any(k.get("command") == hook_komutu(ev) for k in g.get("hooks", []))]
        if kalan != h.get("SubagentStart", kalan):
            if kalan:
                h["SubagentStart"] = kalan
            else:
                del h["SubagentStart"]
            ayar.write_text(json.dumps(s, ensure_ascii=False, indent=2), encoding="utf-8")
    shutil.rmtree(d, ignore_errors=True)


def mcp(ev):
    y = ev / ".claude.json"
    return sorted((json.loads(y.read_text(encoding="utf-8")).get("mcpServers") or {}) if y.exists() else {})


def main(argv=None, ev=Path.home()):
    a = (argv if argv is not None else sys.argv[1:]) or ["--kuru"]
    ajanlar, h, once = plan(ev), harita(ev), mcp(ev)
    for ad in {p for _, p in ajanlar} | set(h.values()):
        if jeton(govde(ad)) > PROTOKOL_TAVAN:
            print(f"DUR: {ad} ~{jeton(govde(ad))} jeton > {PROTOKOL_TAVAN}"); return 2
    if a[0] == "--geri":
        n = sum(enjekte(p, "", geri=True) for p in sorted((ev / ".claude" / "agents").glob("*.md")))
        hook_sok(ev)
        print("geri alındı:", n, "ajan + hook"); return 0
    if a[0] != "uygula":
        print(f"KURU: {len(ajanlar)} ajana godmode bloğu · hook {len(h)} plugin ajanı · KABUL {sorted(kabuller().items())}")
        print("  ", " ".join(f"{p.stem}={ad}" for p, ad in ajanlar)); return 0
    yedek = ev / ".claude" / "backups" / f"fable-ajan-{time.strftime('%Y%m%d-%H%M%S')}"
    degisecek = [(p, ad) for p, ad in ajanlar if enjekte(p, govde(ad), kuru=True)]
    for p, _ in degisecek:
        yedek.mkdir(parents=True, exist_ok=True)
        shutil.copy2(p, yedek / p.name)
    n = sum(enjekte(p, govde(ad)) for p, ad in degisecek)
    if h:
        hook_kur(ev, h, yedek)
    if mcp(ev) != once:
        print("DUR: MCP listesi değişti"); return 3
    print("uygulandı:", n, "/", len(ajanlar), "ajan · hook", len(h), "plugin ajanı · yedek", yedek, "· MCP önce=sonra"); return 0


if __name__ == "__main__":
    sys.exit(main())

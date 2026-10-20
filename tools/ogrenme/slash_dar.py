"""SLASH-ÖĞREN d2: köprü oturumuna daraltılmış skill kümesi. Envanterden seçili skill/komutları .kos/kopru/slash-dar/<küme>/ eklentisine kopyalar;
oturum `--settings <küme>/ayar.json --plugin-dir <yol>` ile yalnız bunları görür (tam liste ≈ +35k token; d3: kullanıcı ayarları —
CLAUDE.md, hook, izin— korunur, `--setting-sources ""` kullanılmaz). Kullanım: python tools/ogrenme/slash_dar.py [küme]"""
import csv
import json
import shutil
import sys
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
KUMELER = {  # küme → envanter adları (slash-katalog.md'deki 15 kart)
    "cekirdek": ["graphify", "plan-kur", "yetenek-getir", "superpowers:systematic-debugging", "superpowers:test-driven-development",
                 "superpowers:brainstorming", "feature-dev:feature-dev", "frontend-craft:frontend-craft", "impeccable:impeccable",
                 "phoenix-security-review:security-reviewer", "code-review:code-review", "claude-api:mcp-builder", "claude-api:claude-api",
                 "skill-creator:skill-creator", "watch:watch"],
}


def kur(kume="cekirdek"):
    hedef = KOK / ".kos" / "kopru" / "slash-dar" / kume
    shutil.rmtree(hedef, ignore_errors=True)
    (hedef / ".claude-plugin").mkdir(parents=True)
    (hedef / ".claude-plugin" / "plugin.json").write_text(f'{{"name":"slash-dar","version":"1.0.0","description":"{kume} skill kümesi"}}', encoding="utf-8")
    satirlar = list(csv.DictReader(open(KOK / ".kos/ogrenme/slash-envanter.tsv", encoding="utf-8"), delimiter="\t"))
    yol = {r["ad"]: Path(r["yol"]) for r in satirlar}
    kullanici = {Path(r["yol"]).parent.name for r in satirlar if r["kaynak"] == "kullanıcı" and r["tur"] == "skill"}
    secili = {yol[ad].parent.name for ad in KUMELER[kume] if yol[ad].name == "SKILL.md"}
    # d3: eklentiler kapalı + kümede olmayan kullanıcı skill'leri off (skillOverrides eklenti skill'ine işlemez); hook/CLAUDE.md/izin kullanıcıdan gelir
    eklentiler = json.loads((Path.home() / ".claude" / "settings.json").read_text(encoding="utf-8")).get("enabledPlugins", {})
    (hedef / "ayar.json").write_text(json.dumps({"enabledPlugins": {k: False for k in eklentiler}, "syncClaudeAiSkills": False,
                                                 "skillOverrides": {**{k: "off" for k in sorted(kullanici - secili)}, **{k: "on" for k in sorted(secili)}}}), encoding="utf-8")  # "on": proje ayarı graphify'ı off yapmış
    for ad in KUMELER[kume]:
        src = yol[ad]  # KeyError = envanterde yok → yenile (tools/ogrenme/slash_envanter.py)
        if src.parent.name in kullanici:
            continue  # kullanıcı skill'i ~/.claude/skills'ten zaten gelir (çift kayıt olmasın)
        if src.name == "SKILL.md":
            shutil.copytree(src.parent, hedef / "skills" / src.parent.name)
        else:
            (hedef / "commands").mkdir(exist_ok=True)
            shutil.copy(src, hedef / "commands" / src.name)
    return hedef


if __name__ == "__main__":
    print(kur(*sys.argv[1:2]))

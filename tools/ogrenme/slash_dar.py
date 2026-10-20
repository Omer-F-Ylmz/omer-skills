"""SLASH-ÖĞREN d2: köprü oturumuna daraltılmış skill kümesi. Envanterden seçili skill/komutları .kos/kopru/slash-dar/<küme>/ eklentisine kopyalar;
oturum `--setting-sources "" --plugin-dir <yol>` ile yalnız bunları görür (tam liste ≈ +35k token). Kullanım: python tools/ogrenme/slash_dar.py [küme]"""
import csv
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
    yol = {r["ad"]: Path(r["yol"]) for r in csv.DictReader(open(KOK / ".kos/ogrenme/slash-envanter.tsv", encoding="utf-8"), delimiter="\t")}
    for ad in KUMELER[kume]:
        src = yol[ad]  # KeyError = envanterde yok → yenile (tools/ogrenme/slash_envanter.py)
        if src.name == "SKILL.md":
            shutil.copytree(src.parent, hedef / "skills" / src.parent.name)
        else:
            (hedef / "commands").mkdir(exist_ok=True)
            shutil.copy(src, hedef / "commands" / src.name)
    return hedef


if __name__ == "__main__":
    print(kur(*sys.argv[1:2]))

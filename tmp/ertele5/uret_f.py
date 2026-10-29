"""ERTELE-2 tur2: aday F — skillOverrides anahtarları düzeltildi.
Kod kanıtı (claude.exe 2.1.311, PTe/G0t/j0t): prompt skill anahtarı e.name = dizin adı (frontmatter adı değil);
claude.ai sync anahtarı tam ad (anthropic-skills:x); plugin skill'leri skillOverrides'ı yok sayar (yalnız synced yolu)."""
import json, re
from pathlib import Path
K = Path(__file__).parent; KOK = K.parents[1]
sat = (K / "context-A.txt").read_text(encoding="utf-8").split("### Skills", 1)[1]
satirlar = [(m.group(1), m.group(2)) for m in re.finditer(r"^\| (.+?) \| (.+?) \| (.+?) \|$", sat, re.M)
            if m.group(1) != "Skill" and not m.group(1).startswith("---")]
adlar = {a for a, s in satirlar if not s.startswith("Plugin")}
adlar |= {p.name for p in (Path.home() / ".claude" / "skills").iterdir() if p.is_dir()}
CEKIRDEK = {"is-akisi", "opus-akis", "plan-kur", "yetenek-getir", "beyin", "headroom-compress", "graphify", "jev",
            "commit", "simplify", "frontend-craft", "impeccable", "context7-cli", "find-docs", "playwright-cli",
            "markitdown", "loop", "review"}
def cek(a): return a.split(":")[-1] in CEKIRDEK or a.split(":")[-1].startswith("departman-")
ov = {a: ("name-only" if cek(a) else "user-invocable-only") for a in sorted(adlar)}
red = json.loads((KOK / "tools" / "ertele_ayar.json").read_text(encoding="utf-8"))
(K / "ayar-F.json").write_text(json.dumps({"skillOverrides": ov, **red}, ensure_ascii=False), encoding="utf-8")
print(len(ov), "anahtar;", sum(v == "name-only" for v in ov.values()), "çekirdek")

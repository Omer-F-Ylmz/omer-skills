"""SLASH-ÖĞREN: "/" ile çağrılan komut+skill envanteri → .kos/ogrenme/slash-envanter.tsv (okuma yok, betik)."""
import json
import re
import sys
from pathlib import Path

HOME = Path.home() / ".claude"
KOK = Path(__file__).resolve().parents[2]
CIKTI = KOK / ".kos" / "ogrenme" / "slash-envanter.tsv"


def on_yazi(yol):
    """Frontmatter alanları (düz anahtar: değer) + ilk gövde satırı."""
    try:
        m = yol.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return {}, ""
    f, govde = {}, m
    if m.startswith("---"):
        parca = m.split("---", 2)
        if len(parca) == 3:
            govde = parca[2]
            for s in parca[1].splitlines():
                k = re.match(r"^([\w-]+):\s*(.*)$", s)
                if k:
                    f[k.group(1)] = k.group(2).strip().strip(">|").strip("\"'")
    ilk = next((s.strip("# ").strip() for s in govde.splitlines() if s.strip()), "")
    return f, ilk


def satir(ad, kaynak, tur, yol):
    f, ilk = on_yazi(yol)
    aciklama = (f.get("description") or ilk).replace("\t", " ")[:140]
    arg = "evet" if (f.get("argument-hint") or "$ARGUMENTS" in yol.read_text(encoding="utf-8", errors="replace")) else "hayır"
    arac = (f.get("allowed-tools") or f.get("tools") or "-").replace("\t", " ")
    # context: fork → alt ajanda; disable-model-invocation → yalnız kullanıcı "/" ile
    alt = "fork" if f.get("context") == "fork" else "hayır"
    model_cagirir = "hayır" if f.get("disable-model-invocation", "").lower() == "true" else "evet"
    return [ad, kaynak, tur, aciklama, arg, arac, alt, model_cagirir, str(yol)]


def topla():
    out = []
    for p in sorted((HOME / "commands").glob("*.md")):
        out.append(satir(p.stem, "kullanıcı", "komut", p))
    for p in sorted((HOME / "skills").glob("*/SKILL.md")):
        out.append(satir(p.parent.name, "kullanıcı", "skill", p))
    for p in sorted((KOK / ".claude" / "commands").glob("*.md")):
        out.append(satir(p.stem, "proje", "komut", p))
    kayit = json.loads((HOME / "plugins" / "installed_plugins.json").read_text(encoding="utf-8"))["plugins"]
    for anahtar, surumler in kayit.items():
        ad, _, _ = anahtar.partition("@")
        yol = Path(surumler[-1]["installPath"])
        for p in sorted((yol / "commands").glob("*.md")):
            out.append(satir(f"{ad}:{p.stem}", anahtar, "komut", p))
        for p in sorted((yol / "skills").glob("*/SKILL.md")):
            out.append(satir(f"{ad}:{p.parent.name}", anahtar, "skill", p))
    return out


if __name__ == "__main__":
    satirlar = topla()
    CIKTI.parent.mkdir(parents=True, exist_ok=True)
    baslik = ["ad", "kaynak", "tur", "aciklama", "arguman", "arac_izni", "alt_ajanda_fork", "model_cagirir", "yol"]
    CIKTI.write_text("\n".join("\t".join(s) for s in [baslik] + satirlar) + "\n", encoding="utf-8", newline="\n")
    # çift: aynı son ad (plugin öneki atılınca) birden çok kaynakta
    son = {}
    for s in satirlar:
        son.setdefault(s[0].split(":")[-1], []).append(s[1])
    cift = {k: v for k, v in son.items() if len(v) > 1}
    tur = {t: sum(1 for s in satirlar if s[2] == t) for t in ("komut", "skill")}
    print(len(satirlar), tur, "çift ad:", len(cift))
    print(sorted(cift)[:40], file=sys.stderr)

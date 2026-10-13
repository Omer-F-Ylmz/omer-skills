"""KALİTE-1 (4b): gizli ajan kataloğu → skills/ajan-getir/katalog.tsv (ad · model · tek satır · yol).

Gizli = settings.json permissions.deny içindeki Agent(plugin:ad) + ~/.claude/agents kullanıcı ajanları.
Yalnız okur; ayar yazmaz. Bağlama girmez: ajan-getir skill'i katalogu Grep ile tarar.
"""
import json
import re
import sys
from pathlib import Path

EV = Path.home() / ".claude"
CIKTI = Path(__file__).resolve().parents[1] / "skills" / "ajan-getir" / "katalog.tsv"


def on_bilgi(yol):
    """frontmatter'dan name/description/model; yoksa dosya adı."""
    m = re.match(r"---\r?\n(.*?)\r?\n---", yol.read_text(encoding="utf-8", errors="replace"), re.S)
    d = {}
    for s in (m.group(1).splitlines() if m else []):
        k, _, v = s.partition(":")
        if k.strip() in ("name", "description", "model") and v.strip():
            d[k.strip()] = v.strip().strip("\"'")
    tek = re.sub(r"\s+", " ", d.get("description", "")).replace("\t", " ")
    tek = re.split(r"(?<=[.!?])\s|\\n", tek)[0][:160]
    return d.get("name") or yol.stem, d.get("model") or "inherit", tek


def plugin_ajanlari(cache):
    """{'plugin:ad': yol} — aynı ajanın birden çok sürümü varsa en yenisi."""
    sonuc = {}
    for yol in sorted(cache.glob("*/*/*/agents/**/*.md"), key=lambda p: p.stat().st_mtime):
        parca = yol.relative_to(cache).parts
        on = ":".join([parca[1], *parca[4:-1]])  # agents/droids/x.md → plugin:droids:x
        sonuc[f"{on}:{on_bilgi(yol)[0]}"] = sonuc[f"{on}:{yol.stem}"] = yol
    return sonuc


def uret(ev=EV):
    ayar = json.loads((ev / "settings.json").read_text(encoding="utf-8"))
    gizli = [x[6:-1] for x in ayar.get("permissions", {}).get("deny", []) if x.startswith("Agent(") and x.endswith(")")]
    pa = plugin_ajanlari(ev / "plugins" / "cache")
    satirlar, eksik = [], []
    for ad in gizli:
        if ad in pa:
            _, model, tek = on_bilgi(pa[ad])
            satirlar.append((ad, model, tek, pa[ad].as_posix()))
        else:
            eksik.append(ad)
    gorulen = {s[3] for s in satirlar}
    for ad, yol in pa.items():  # açık plugin ajanları: claude.ai sürümünde Agent listesi yok, katalog tek kaynak
        if yol.as_posix() not in gorulen and ad.endswith(":" + on_bilgi(yol)[0]):
            gorulen.add(yol.as_posix())
            satirlar.append((ad, *on_bilgi(yol)[1:], yol.as_posix()))
    for yol in sorted([*(ev / "agents").glob("*.md"), *(ev / "agents-katalog").glob("*.md")]):  # agents-katalog: token_8_is2 listeden çıkardıkları
        ad, model, tek = on_bilgi(yol)
        satirlar.append((ad, model, tek, yol.as_posix()))
    return satirlar, eksik


def main():
    satirlar, eksik = uret()
    CIKTI.write_text("ad\tmodel\ttek_satir\tyol\n" + "".join("\t".join(s) + "\n" for s in satirlar), encoding="utf-8", newline="\n")
    print(f"{len(satirlar)} ajan → {CIKTI} · dosyası bulunmayan gizli ad {len(eksik)}: {', '.join(eksik[:5])}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

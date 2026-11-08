"""KUCUK-5: video-764 aday tsv'sine ek-50 UYARLA/AL kararlarını birleştirir (link/ID çakışmasında atlar) ve
Obsidian'a girecek .kos/kopru/ogren/aday/listesi.md notunu yazar (AL · UYARLA · ÖĞREN; ELE yok). Model yok."""
import re
from collections import Counter
from pathlib import Path

OG = Path(__file__).resolve().parent.parent / ".kos/kopru/ogren"
TSV, V2, LOG, CIKTI = OG / "video-764-aday.tsv", OG / "video-764-v2.tsv", OG / "video-ek50.log", OG / "aday/listesi.md"


def oku(p):
    return [ln.split("\t") for ln in p.read_text(encoding="utf-8").splitlines()]


def main():
    v2 = {r[0]: r for r in oku(V2)[1:]}
    ek = {ln.split()[0] for ln in LOG.read_text(encoding="utf-8").splitlines() if ln.strip()}
    tsv = oku(TSV); metin = TSV.read_text(encoding="utf-8")
    eklenen = []
    for vid, r in v2.items():
        k = r[4].upper().replace("OGREN", "ÖĞREN")
        if vid[3:] in ek and k in ("AL", "UYARLA") and vid[3:] not in metin:
            satir = [vid, "video", "", r[5], "", "?", "?", "?", "?", "?", "", "1", r[1], k, ""]
            tsv.append(satir); eklenen.append(satir)
    if eklenen:
        TSV.write_text("\n".join("\t".join(s) for s in tsv) + "\n", encoding="utf-8", newline="\n")
    ad = [t[0] for t in tsv[1:]]
    assert len(ad) == len(set(ad)), "aday tsv'de çift ad"
    sec = {"AL": [], "UYARLA": [], "ÖĞREN": []}
    for t in tsv[1:]:
        sec[t[13]].append(f"- **{t[0]}** ({t[1]}) — {t[3]} · {t[12]}")
    ogren = [r for r in v2.values() if r[4].upper().replace("OGREN", "ÖĞREN") == "ÖĞREN"]
    sec["ÖĞREN"] = [f"- {r[0]} — {r[2]} · {r[5]} · {r[1]}" for r in ogren]
    out = ["# Video aday listesi", "", "ELE hariç; ÖĞREN videoları karar-v2'den, AL/UYARLA araç satırları aday tsv'den.", ""]
    for b, s in sec.items():
        out += [f"## {b} ({len(s)})", *s, ""]
    CIKTI.parent.mkdir(exist_ok=True)
    CIKTI.write_text(re.sub(r"[ \t]+\n", "\n", "\n".join(out)), encoding="utf-8", newline="\n")
    print({b: len(s) for b, s in sec.items()}, "ek-50'den eklenen", len(eklenen), Counter(s[13] for s in eklenen))


if __name__ == "__main__":
    main()

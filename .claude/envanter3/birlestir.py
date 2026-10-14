"""ogrenim_{video,ig,rapor}.jsonl -> docs/katalog/ogrenim.jsonl + .tsv ('ne'ye göre tekil, kaynak denetimli)."""
import json, re, sys
from pathlib import Path

WT = Path(__file__).resolve().parents[2]
ANA = Path("C:/Projeler/omer-skills")
ALANLAR = ("ne", "is", "kaynak", "alan", "araclar")


def kaynak_var(k):
    yol = re.sub(r":\d+(-\d+)?$", "", k.strip())
    p = Path(yol)
    if p.is_absolute() or yol.startswith("~"):
        return p.expanduser().exists()
    return any((b / yol).exists() for b in (WT, ANA, WT.parent))


def anahtar(ne):
    return re.sub(r"\W+", " ", ne.casefold()).strip()


satirlar, gorulen, eksik_kaynak = [], set(), []
for ad in ("video", "ig", "rapor"):
    for s in (WT / f".claude/envanter3/ogrenim_{ad}.jsonl").read_text(encoding="utf-8").splitlines():
        if not s.strip():
            continue
        o = json.loads(s)
        a = anahtar(o.get("ne", ""))
        if not a or a in gorulen:
            continue
        gorulen.add(a)
        o = {k: str(o.get(k, "")).strip() for k in ALANLAR}
        if not kaynak_var(o["kaynak"]):
            eksik_kaynak.append(o["kaynak"])
        satirlar.append(o)

hedef = WT / "docs/katalog"
with open(hedef / "ogrenim.jsonl", "w", encoding="utf-8", newline="\n") as f:
    f.writelines(json.dumps(o, ensure_ascii=False) + "\n" for o in satirlar)
with open(hedef / "ogrenim.tsv", "w", encoding="utf-8", newline="\n") as f:
    f.write("\t".join(ALANLAR) + "\n")
    f.writelines("\t".join(o[k].replace("\t", " ") for k in ALANLAR) + "\n" for o in satirlar)
print(f"{len(satirlar)} satır (girdi tekilsiz {sum(1 for _ in gorulen)}), kaynağı bulunmayan {len(eksik_kaynak)}")
for k in sorted(set(eksik_kaynak))[:15]:
    print("  yok:", k)
sys.exit(0)

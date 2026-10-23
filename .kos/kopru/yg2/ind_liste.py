"""yg1 günlüğünde son durumu 'indirilemedi' olan kodlar → hata türüne göre özet; kodlar ind.tsv'ye."""
import collections
import re
from pathlib import Path

KOK = Path(__file__).resolve().parents[3]
son = {}
for s in (KOK / ".kos/kopru/yg1/gunluk.log").read_text(encoding="utf-8", errors="replace").splitlines():
    p = s.split("\t")
    if len(p) >= 2 and re.fullmatch(r"[\w-]{6,15}", p[0]):
        son[p[0]] = p[1]
silinen = set(re.findall(r"\b[\w-]{11}\b", (KOK / ".kos/kopru/ig-silinen.txt").read_text(encoding="utf-8").split("\n", 1)[-1]))
kotu = {k: v for k, v in son.items() if v.startswith("indirilemedi")}
ozet = collections.Counter(re.sub(r"[\w-]{11}", "X", v)[:90] for v in kotu.values())
for o, n in ozet.most_common():
    print(n, o)
(Path(__file__).parent / "ind.tsv").write_text("\n".join(f"{k}\t{v[:200]}\t{'SILINEN-KAYITLI' if k in silinen else ''}" for k, v in kotu.items()), encoding="utf-8")
print(len(kotu), "indirilemedi;", sum(k in silinen for k in kotu), "zaten ig-silinen'de")

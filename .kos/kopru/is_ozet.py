"""TOKEN-3 K17: is-kaydi.tsv → Desktop kontrolü için tek satır: bugünkü iş sayısı, ağırlıklı toplam, iş türü (ad öneki) başı ortalama.
  python .kos/kopru/is_ozet.py [YYYY-MM-DD]"""
import sys, time
from collections import defaultdict
from pathlib import Path

gun = sys.argv[1] if len(sys.argv) > 1 else time.strftime("%Y-%m-%d")
tur = defaultdict(list)
for s in (Path(__file__).parent / "is-kaydi.tsv").read_text(encoding="utf-8").splitlines()[1:]:
    p = s.split("\t")
    if p[0].startswith(gun):
        tur[p[1].split("-")[0]].append(float(p[5]))
top = sum(map(sum, tur.values()))
sys.stdout.reconfigure(encoding="utf-8")
print(f"iş kaydı {gun}: {sum(map(len, tur.values()))} iş · {top / 1e6:.1f}M ağırlıklı · "
      + " · ".join(f"{k} {len(v)}×{sum(v) / len(v) / 1e6:.2f}M" for k, v in sorted(tur.items(), key=lambda x: -sum(x[1]))))

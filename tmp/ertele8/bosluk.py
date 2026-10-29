"""ERTELE-3 TUR4 madde 5: debug dosyasında ardışık zaman damgaları arasındaki en büyük 12 boşluk."""
import re, sys
from datetime import datetime
sat = open(sys.argv[1], encoding="utf-8", errors="ignore").read().splitlines()
onceki, bos = None, []
for i, s in enumerate(sat):
    m = re.match(r"(\d{4}-\d\d-\d\dT\d\d:\d\d:\d\d\.\d+)Z?", s)
    if not m:
        continue
    t = datetime.fromisoformat(m.group(1))
    if onceki:
        bos.append(((t - onceki[0]).total_seconds(), i, onceki[1][:160], s[:160]))
    onceki = (t, s)
print("ilk", sat[0][:30], "son", onceki[1][:30])
for b in sorted(bos, reverse=True)[:12]:
    print(f"{b[0]:7.1f}s @{b[1]}\n  ONCE {b[2]}\n  SONRA {b[3]}")

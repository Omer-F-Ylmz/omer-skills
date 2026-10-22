"""Ajan süreç ağaçları: her `claude.exe -p` kökü + torunları, ad başı MB (çalışma kümesi). Salt-okur.
  python ram_agac.py [--md]   (--md: docs/ram/olcum.md için tablo)"""
import sys, time
from collections import defaultdict

import psutil

sys.stdout.reconfigure(encoding="utf-8")
md = "--md" in sys.argv
procs = {}
for p in psutil.process_iter(["pid", "ppid", "name", "memory_info", "create_time", "cmdline"]):
    try:
        procs[p.info["pid"]] = p.info
    except Exception:
        pass
cocuk = defaultdict(list)
for i, x in procs.items():
    cocuk[x["ppid"]].append(i)


def mb(x):
    return (x["memory_info"].rss if x["memory_info"] else 0) / 2**20


def tor(k):
    s, yig = [], [k]
    while yig:
        i = yig.pop()
        s.append(i)
        yig += [c for c in cocuk.get(i, []) if c in procs and c != i]
    return s


def kok_mu(x):
    k = x["cmdline"] or []
    return (x["name"] or "").lower() == "claude.exe" and "-p" in k


vm = psutil.virtual_memory()
satir = []
for i, x in procs.items():
    if not kok_mu(x):
        continue
    ad = defaultdict(lambda: [0.0, 0])
    for t in tor(i):
        n = (procs[t]["name"] or "?").lower()
        ad[n][0] += mb(procs[t]); ad[n][1] += 1
    top = sum(v[0] for v in ad.values())
    sayi = sum(v[1] for v in ad.values())
    ozet = " ".join(f"{n}×{v[1]}={v[0]:.0f}" for n, v in sorted(ad.items(), key=lambda kv: -kv[1][0])[:5])
    satir.append((top, i, time.strftime("%H:%M", time.localtime(procs[i]["create_time"])), sayi, ozet))
satir.sort(reverse=True)
toplam = sum(s[0] for s in satir)
print(f"RAM %{vm.percent:.0f} · {vm.used / 2**30:.1f}/{vm.total / 2**30:.1f} GB · claude -p ağaçları {len(satir)} adet toplam {toplam:.0f} MB")
for top, i, t, say, oz in satir:
    print(f"| {i} | {t} | {say} | {top:.0f} | {oz} |" if md else f"{top:7.0f} MB pid {i} {t} süreç {say}  {oz}")

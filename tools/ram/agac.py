"""RAM-OPT-1 ölçüm (salt okur): süreçleri imzaya göre gruplar → kopya sayısı + MB (RSS).
Kök gruplar: Desktop Claude.exe ağacı, claude CLI ağaçları, geri kalan (Windows dışı). Komut satırı/env yazdırılmaz;
anahtar/token/= içeren argüman imzaya girmez.
  python tools/ram/agac.py [--dip]   (--dip: grup başına ilk 25 satır yerine tümü)"""
import collections
import os
import re
import sys

import psutil

GIZLI = re.compile(r"(?i)key|token|secret|pass|=")
SISTEM = re.compile(r"(?i)^[a-z]:\\windows\\")


def imza(p):
    try:
        ad = p.name().lower()
        a = [os.path.basename(x).lower() for x in p.cmdline()[1:] if not x.startswith("-") and not GIZLI.search(x)]
        return ad + " " + " ".join(a[:2])
    except psutil.Error:
        return "?"


def kok(p, tum):
    """Desktop MSIX Claude.exe / claude CLI / diger — en yakın atanın sınıfı."""
    z = []
    while p:
        z.append(p)
        try:
            p = tum.get(p.ppid())
        except psutil.Error:
            break
        if p in z:
            break
    for q in z:
        try:
            ex = (q.exe() or "").lower()
        except psutil.Error:
            continue
        if q.name().lower() == "claude.exe":
            return "desktop" if ("windowsapps" in ex or "claude-data" in ex or "anthropicclaude" in ex) else "cc"
    return "diger"


def main():
    tum = {p.pid: p for p in psutil.process_iter()}
    gruplar = collections.defaultdict(lambda: collections.defaultdict(lambda: [0, 0.0]))
    toplam = collections.defaultdict(lambda: [0, 0.0])
    for p in tum.values():
        try:
            ex = p.exe() or ""
            if SISTEM.match(ex) and p.name().lower() not in ("conhost.exe", "cmd.exe"):
                continue
            mb = p.memory_info().rss / 2**20
        except psutil.Error:
            continue
        g = kok(p, tum)
        s = imza(p)
        gruplar[g][s][0] += 1
        gruplar[g][s][1] += mb
        toplam[p.name().lower()][0] += 1
        toplam[p.name().lower()][1] += mb
    vm = psutil.virtual_memory()
    print(f"RAM {vm.percent:.0f}%  {vm.used/2**30:.1f}/{vm.total/2**30:.1f} GB")
    print("-- ada göre (n, MB) ilk 12")
    for ad, (n, mb) in sorted(toplam.items(), key=lambda x: -x[1][1])[:12]:
        print(f"{n:4d} {mb:8.0f}  {ad}")
    lim = None if "--dip" in sys.argv else 25
    for g, d in gruplar.items():
        n = sum(v[0] for v in d.values())
        mb = sum(v[1] for v in d.values())
        print(f"== {g}: {n} süreç, {mb/1024:.2f} GB")
        for s, (c, m) in sorted(d.items(), key=lambda x: -x[1][1])[:lim]:
            print(f"{c:4d} {m:8.0f}  {s[:90]}")


if __name__ == "__main__":
    main()

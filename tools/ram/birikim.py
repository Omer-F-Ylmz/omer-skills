"""RAM-OPT-1 d3 birikim ölçümü (salt okur): N örnek, aralık sn; ad+ebeveyn ve imza başına süreç sayısı/MB değişimi.
Komut satırı/env yazdırılmaz (agac.imza gizli argümanları süzer). Yalnız log'a yazar; öldürme yok.
  python tools/ram/birikim.py [N=3] [ARALIK_SN=600]"""
import collections
import os
import sys
import time

import psutil

sys.path.insert(0, os.path.dirname(__file__))
from agac import SISTEM, imza  # noqa: E402


def ornek():
    tum = {p.pid: p for p in psutil.process_iter()}
    ad = collections.defaultdict(lambda: [0, 0.0])
    im = collections.defaultdict(lambda: [0, 0.0])
    for p in tum.values():
        try:
            if SISTEM.match(p.exe() or "") and p.name().lower() not in ("conhost.exe", "cmd.exe"):
                continue
            mb = p.memory_info().rss / 2**20
            ata = tum.get(p.ppid())
            an = ata.name().lower() if ata else "-"
        except psutil.Error:
            continue
        for d, k in ((ad, f"{p.name().lower()} <- {an}"), (im, imza(p)[:80])):
            d[k][0] += 1
            d[k][1] += mb
    return psutil.virtual_memory().percent, ad, im


def fark(a, b, n=12):
    k = set(a) | set(b)
    s = sorted(((b.get(x, [0, 0])[1] - a.get(x, [0, 0])[1], a.get(x, [0, 0])[0], b.get(x, [0, 0])[0], x) for x in k), reverse=True)
    for dmb, n0, n1, x in s[:n]:
        print(f"{dmb:+8.0f} MB  n {n0:3d}->{n1:3d}  {x}")


def main():
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 3
    aralik = int(sys.argv[2]) if len(sys.argv) > 2 else 600
    o = []
    for i in range(n):
        if i:
            time.sleep(aralik)
        o.append(ornek())
        print(f"örnek {i+1}/{n} {time.strftime('%H:%M:%S')} RAM %{o[-1][0]:.0f}", flush=True)
    print("-- ad<-ebeveyn büyüme (ilk→son)")
    fark(o[0][1], o[-1][1])
    print("-- imza büyüme (ilk→son)")
    fark(o[0][2], o[-1][2])


if __name__ == "__main__":
    main()

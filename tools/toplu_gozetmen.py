"""Uzun toplu işi gözetir: python toplu_gozetmen.py <gunluk> <komut> [arg...]
Çocuk "BITIS" satırı yazmadan ya da rc≠0 ile ölürse en fazla 3 kez yeniden başlatır (bitenleri iş kendi atlar).
Günlüğe "DURUM basladi|bitti|oldu|vazgecti" satırları yazar. Başlamadan önce RAM ≥%84 ise düşene dek bekler.
ARKA-KALICI-1: ajan bunu doğrudan başlatmaz; .kos/kopru/arka-istek/<ad>.json yazar (bkz. arka_istek.py), yönetici başlatır."""
import ctypes
import subprocess
import sys
import time
from datetime import datetime

AZAMI_YENIDEN = 3
RAM_SINIR = 96


def ram_yuzde():
    class M(ctypes.Structure):
        _fields_ = [("n", ctypes.c_ulong), ("yuk", ctypes.c_ulong)] + [(f"a{i}", ctypes.c_ulonglong) for i in range(7)]
    m = M()
    m.n = ctypes.sizeof(M)
    ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(m))
    return m.yuk


def gozet(komut, gunluk, bekle=60, ram_bekle=True):
    def yaz(f, s):
        f.write(f"{datetime.now():%Y-%m-%d %H:%M:%S} DURUM {s}\n")
        f.flush()

    rc = 1
    with open(gunluk, "a", encoding="utf-8") as f:
        for deneme in range(AZAMI_YENIDEN + 1):
            while ram_bekle and ram_yuzde() >= RAM_SINIR:
                time.sleep(30)
            yaz(f, f"basladi deneme={deneme + 1}")
            p = subprocess.Popen(komut, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True,
                                 encoding="utf-8", errors="replace", stdin=subprocess.DEVNULL, creationflags=0x08000000)
            bitis = False
            for satir in p.stdout:
                f.write(satir)
                f.flush()
                bitis = bitis or satir.startswith("BITIS")
            rc = p.wait()
            if rc == 0 and bitis:
                yaz(f, "bitti")
                return 0
            yaz(f, f"oldu rc={rc} bitis={bitis}")
            if deneme < AZAMI_YENIDEN:
                time.sleep(bekle)
        yaz(f, "vazgecti")
    return rc or 1


if __name__ == "__main__":
    sys.exit(gozet(sys.argv[2:], sys.argv[1], ram_bekle=True))

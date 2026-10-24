"""REA-USTA-1c bellek kuralı: REA/Node alt süreci NODE_OPTIONS=--max-old-space-size=2048 ile açılır, sistem RAM'i %85'e çıkınca durdurulur.
Kullanım: p = rea_bellek.baslat([node, betik, ...]); rea_bellek.bekle(p)  # bekle() RAM %85'te süreci öldürür, True = RAM yüzünden durdu.
Ağır SPA'da analyze_web_bundle kullanma (P2 kararı: 2 GB OOM); inspect_web_page(summary) + capture_web_screenshot."""
import ctypes
import os
import subprocess
import time

RAM_ESIK = 85


def ram_yuzde():
    class MS(ctypes.Structure):
        _fields_ = [("len", ctypes.c_ulong), ("load", ctypes.c_ulong)] + [(n, ctypes.c_ulonglong) for n in
                    ("tp", "ap", "tpf", "apf", "tv", "av", "ae")]
    m = MS(); m.len = ctypes.sizeof(m)
    ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(m))
    return m.load


def ortam():
    return {**os.environ, "NODE_OPTIONS": "--max-old-space-size=2048"}


def baslat(argv, **kw):
    return subprocess.Popen(argv, env=ortam(), creationflags=0x08000000, **kw)  # CREATE_NO_WINDOW


def bekle(p, zaman_asimi=600):
    t0 = time.time()
    while p.poll() is None:
        if ram_yuzde() >= RAM_ESIK or time.time() - t0 > zaman_asimi:
            subprocess.run(["taskkill", "/F", "/T", "/PID", str(p.pid)], capture_output=True)
            p.wait()
            return True
        time.sleep(1)
    return False

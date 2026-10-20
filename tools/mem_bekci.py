"""claude-mem bekçisi: worker (127.0.0.1:37777) kapalıysa pencere açmadan, hiçbir oturumun süreç ağacına bağlı olmadan yeniden başlatır.
Zamanlanmış görevden pythonw ile koşar (onay/mem_bekci.py). RAM >= %88 ise başlatmaz. Günlük: ~/.claude-mem/logs/mem-bekci.log"""
import ctypes
import os
import socket
import subprocess
import time

H = os.path.expanduser("~")
LOG = os.path.join(H, ".claude-mem", "logs", "mem-bekci.log")
NODE_ADAY = [
    r"C:\Users\pc\AppData\Local\Microsoft\WinGet\Packages\OpenJS.NodeJS.LTS_Microsoft.Winget.Source_8wekyb3d8bbwe\node-v24.19.0-win-x64\node.exe",
    r"C:\Program Files\nodejs\node.exe",
]


class MEM(ctypes.Structure):
    _fields_ = [("dwLength", ctypes.c_ulong), ("dwMemoryLoad", ctypes.c_ulong)] + [(n, ctypes.c_ulonglong) for n in ("t", "a", "tp", "ap", "tv", "av", "ae")]


def ram():
    m = MEM()
    m.dwLength = ctypes.sizeof(MEM)
    ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(m))
    return m.dwMemoryLoad


def acik():
    s = socket.socket()
    s.settimeout(1)
    try:
        return s.connect_ex(("127.0.0.1", 37777)) == 0
    finally:
        s.close()


def yaz(*a):
    with open(LOG, "a", encoding="utf-8") as f:
        f.write(time.strftime("%Y-%m-%d %H:%M:%S ") + " ".join(str(x) for x in a) + "\n")


def betikler():
    k = os.path.join(H, ".claude", "plugins", "cache", "thedotmack", "claude-mem")
    surumler = [v for v in os.listdir(k) if v[0].isdigit() and not os.path.exists(os.path.join(k, v, ".orphaned_at"))]
    surumler.sort(key=lambda v: [int(x) if x.isdigit() else 0 for x in v.split("-")[0].split(".")])
    return os.path.join(k, surumler[-1], "scripts")


def main():
    if acik():
        return
    r = ram()
    if r >= 88:
        yaz("worker kapali ama RAM", r, "-> baslatilmadi")
        return
    node = next((n for n in NODE_ADAY if os.path.exists(n)), "node")
    s = betikler()
    arg = [node, os.path.join(s, "bun-runner.js"), os.path.join(s, "worker-service.cjs"), "start"]
    bayrak = 0x08000000 | 0x00000200
    out = open(LOG, "a", encoding="utf-8")
    try:
        subprocess.Popen(arg, stdout=out, stderr=subprocess.STDOUT, stdin=subprocess.DEVNULL, cwd=H, close_fds=True, creationflags=bayrak | 0x01000000)
    except OSError:
        subprocess.Popen(arg, stdout=out, stderr=subprocess.STDOUT, stdin=subprocess.DEVNULL, cwd=H, close_fds=True, creationflags=bayrak)
    for _ in range(30):
        time.sleep(1)
        if acik():
            yaz("worker kapaliydi -> yeniden baslatildi, RAM", r)
            return
    yaz("worker 30 sn icinde acilmadi")


def beyin():
    """Yeni biten ajan-sira oturumlarını Obsidian kasasına al (BEYIN-2); bekçiyi asla düşürmez."""
    try:
        import beyin_kanca
        n = beyin_kanca.main()
        if n:
            yaz("beyin_kanca:", n, "yeni oturum kasaya alindi")
    except Exception as e:
        yaz("beyin_kanca hata:", repr(e)[:200])


if __name__ == "__main__":
    main()
    if ram() < 88:
        beyin()

"""VRAM-SİPER: VRAM'i ≤%80 tutar (NİHAİ 35). 1 sn'de bir ölçer.
VRAM ≥%78 iki ölçüm üst üste → bizim en yeni GPU sürecimizi (python/pythonw/ComfyUI) ağaçla kapatır.
VRAM ≥%70 ve bizim GPU sürecimiz >1 → en yeni olanı kapatır (aynı anda tek GPU işi).
Ömer'in uygulamalarına dokunmaz. Güç sınırı/sistem ayarı yok.
python vram_siper.py dongu | tek | arka"""
import os
import subprocess
import sys
import time

KOK = r"C:\Projeler\omer-skills"
PIDF = os.path.join(KOK, ".kos", "kopru", "vram-siper.pid")
GUNLUK = os.path.join(KOK, ".kos", "kopru", "vram-siper.log")
UST, TEK = 93.0, 93.0
# Ömer kuralı (02.11): VRAM kapısı %95 (önce 01.11 %80); PC başındaysa bu tavan; yoksa (boşta ≥ BOS_SN) işler bitsin, yalnız sert emniyet.
BOS_SN, SERT = 300, 97.0
BIZIM = ("python.exe", "pythonw.exe")
MUAF = ("vram_siper", "gpu_sinir")
CNW = 0x08000000


def smi(*a):
    return subprocess.run(["nvidia-smi", *a], capture_output=True, text=True, timeout=20, creationflags=CNW).stdout


def vram():
    k, t = (float(x) for x in smi("--query-gpu=memory.used,memory.total", "--format=csv,noheader,nounits").strip().splitlines()[0].split(","))
    return 100.0 * k / t


def bizim(psutil):
    muaf = {os.getpid()}
    try:
        muaf |= {p.pid for p in psutil.Process().parents()}
    except psutil.Error:
        pass
    out = []
    for s in smi("--query-compute-apps=pid,process_name", "--format=csv,noheader").splitlines():
        pid_s, _, ad = s.partition(",")
        ad = os.path.basename(ad.strip().replace("\\", "/")).lower()
        if not pid_s.strip().isdigit() or int(pid_s) in muaf or ad not in BIZIM:
            continue
        try:
            p = psutil.Process(int(pid_s))
            if any(m in " ".join(p.cmdline()) for m in MUAF):
                continue
            out.append(p)
        except psutil.Error:
            pass
    return sorted(out, key=lambda p: p.create_time())


def bosta_sn():
    """Son klavye/fare girdisinden beri geçen saniye (GetLastInputInfo)."""
    import ctypes

    class LII(ctypes.Structure):
        _fields_ = [("cbSize", ctypes.c_uint), ("dwTime", ctypes.c_uint)]
    li = LII()
    li.cbSize = ctypes.sizeof(LII)
    if not ctypes.windll.user32.GetLastInputInfo(ctypes.byref(li)):
        return 0.0
    return ((ctypes.windll.kernel32.GetTickCount() - li.dwTime) & 0xFFFFFFFF) / 1000.0


def omer_yok():
    try:
        return bosta_sn() >= BOS_SN
    except Exception:
        return False


def yaz(m):
    with open(GUNLUK, "a", encoding="utf-8") as f:
        f.write(time.strftime("%H:%M:%S ") + m + "\n")


def kapat(p, neden):
    try:
        cmd = " ".join(p.cmdline())[:160]
    except Exception:
        cmd = "?"
    subprocess.run(["taskkill", "/PID", str(p.pid), "/T", "/F"], capture_output=True, creationflags=CNW)
    yaz("KAPATILDI %d (%s) %s" % (p.pid, neden, cmd))


def dongu():
    import psutil
    try:
        with open(PIDF) as f:
            eski = int(f.read().strip())
        if eski != os.getpid() and psutil.pid_exists(eski) and "vram_siper" in " ".join(psutil.Process(eski).cmdline()):
            return
    except (OSError, ValueError, psutil.Error):
        pass
    with open(PIDF, "w") as f:
        f.write(str(os.getpid()))
    psutil.Process().nice(psutil.BELOW_NORMAL_PRIORITY_CLASS)
    yaz("BASLADI")
    ust = 0
    while True:
        t0 = time.time()
        try:
            v = vram()
            yok = omer_yok()
            esik, tek = (SERT, 101.0) if yok else (UST, TEK)
            ust = ust + 1 if v >= esik else 0
            if ust >= 2 or v >= tek:
                ps = bizim(psutil)
                if ust >= 2 and ps:
                    kapat(ps[-1], "vram %.0f%% (%s)" % (v, "omer-yok-sert" if yok else "omer-basinda"))
                    ust = 0
                elif v >= tek and len(ps) > 1:
                    kapat(ps[-1], "tek-gpu-isi vram %.0f%%" % v)
        except Exception as e:
            yaz("hata %r" % (e,))
        time.sleep(max(0.0, 1.0 - (time.time() - t0)))


def arka():
    py = os.path.join(os.path.dirname(sys.executable), "pythonw.exe")
    if not os.path.exists(py):
        py = sys.executable
    subprocess.Popen([py, os.path.abspath(__file__), "dongu"], creationflags=0x00000008 | 0x00000200 | CNW,
                     close_fds=True, stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print("arka baslatildi")


if __name__ == "__main__":
    a = sys.argv[1:]
    if a == ["dongu"]:
        dongu()
    elif a == ["arka"]:
        arka()
    else:
        import psutil
        print("vram %.1f%%" % vram(), "bosta %.0fs" % bosta_sn(), [(p.pid, p.name()) for p in bizim(psutil)])

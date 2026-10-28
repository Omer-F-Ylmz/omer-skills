"""GPU-SINIR-2: GPU kullanımını (utilization) ≤%80 tutar. 1 sn'de bir ölçer; son 2 ölçüm ortalaması ≥%78 ise
yalnız bizim GPU süreçlerini (python/pythonw/blender/ComfyUI) kısa süre askıya alır, ≤%70'te bırakır. Süreç öldürmez.
Askıya alınan her süreç resume edilir (finally + atexit + sinyal + bayat durum dosyası). Güç sınırı/sistem ayarına dokunmaz.
python gpu_sinir.py dongu   # sürekli (pythonw ile arka plan)   ·   python gpu_sinir.py tek   # tek ölçüm, yazdır"""
import atexit
import os
import signal
import subprocess
import sys
import time

KOK = r"C:\Projeler\omer-skills"
DURUM = os.path.join(KOK, ".kos", "kopru", "gpu-sinir.json")
KILIT = os.path.join(KOK, ".kos", "kopru", "gpu-sinir.pid")
GUNLUK = os.path.join(KOK, ".kos", "kopru", "gpu-sinir.log")
UST, ALT = 78.0, 70.0
BIZIM = ("python.exe", "pythonw.exe", "blender.exe")
ONEK = ("comfyui",)
CNW = 0x08000000

askida = {}  # pid -> create_time


def smi(*args):
    return subprocess.run(["nvidia-smi", *args], capture_output=True, text=True, timeout=20, creationflags=CNW).stdout


def olc():
    """(utilization %, bellek %) — tek nvidia-smi çağrısı."""
    u, k, t = (float(x) for x in smi("--query-gpu=utilization.gpu,memory.used,memory.total",
                                      "--format=csv,noheader,nounits").strip().splitlines()[0].split(","))
    return u, 100.0 * k / t


def bizim_pidler(psutil):
    """compute-apps içinde yalnız bizim süreçler; kendimiz ve atalarımız hariç (görev yürütücüsü donmasın)."""
    muaf = {os.getpid()}
    try:
        muaf |= {p.pid for p in psutil.Process().parents()}
    except psutil.Error:
        pass
    sonuc = []
    for satir in smi("--query-compute-apps=pid,process_name", "--format=csv,noheader").splitlines():
        pid_s, _, ad = satir.partition(",")
        ad = os.path.basename(ad.strip().replace("\\", "/")).lower()
        if not pid_s.strip().isdigit() or int(pid_s) in muaf:
            continue
        if ad in BIZIM or ad.startswith(ONEK):
            sonuc.append(int(pid_s))
    return sonuc


def durum_yaz():
    import json
    with open(DURUM, "w", encoding="utf-8") as f:
        json.dump(askida, f)


def hepsini_surdur():
    import psutil
    for pid, ct in list(askida.items()):
        try:
            p = psutil.Process(pid)
            if abs(p.create_time() - ct) < 1:  # PID yeniden kullanılmışsa dokunma
                p.resume()
        except psutil.Error:
            pass
        askida.pop(pid, None)
    try:
        durum_yaz()
    except OSError:
        pass


def bayat_surdur():
    """Önceki koşu öldürüldüyse askıda kalanları bırak."""
    import json
    import psutil
    try:
        with open(DURUM, encoding="utf-8") as f:
            eski = json.load(f)
    except (OSError, ValueError):
        return
    for pid, ct in eski.items():
        try:
            p = psutil.Process(int(pid))
            if abs(p.create_time() - ct) < 1:
                p.resume()
        except psutil.Error:
            pass
    try:
        os.remove(DURUM)
    except OSError:
        pass


def calisiyor_mu(psutil):
    try:
        with open(KILIT) as f:
            pid = int(f.read().strip())
        return pid != os.getpid() and psutil.pid_exists(pid) and "gpu_sinir" in " ".join(psutil.Process(pid).cmdline())
    except (OSError, ValueError, psutil.Error):
        return False


def dongu():
    import psutil
    if calisiyor_mu(psutil):
        return
    with open(KILIT, "w") as f:
        f.write(str(os.getpid()))
    bayat_surdur()
    atexit.register(hepsini_surdur)
    for sig in (signal.SIGINT, signal.SIGTERM, getattr(signal, "SIGBREAK", signal.SIGTERM)):
        signal.signal(sig, lambda *_: sys.exit(0))
    psutil.Process().nice(psutil.BELOW_NORMAL_PRIORITY_CLASS)
    son = []
    sinirda = False
    sure = 0.3  # askı süresi (sn), uyarlamalı 0,3–0,6
    while True:
        t0 = time.time()
        try:
            u, _ = olc()
            son = (son + [u])[-2:]
            ort = sum(son) / len(son)
            if sinirda and ort <= ALT:
                sinirda = False
            elif ort >= UST:
                sinirda = True
            if sinirda:
                sure = min(0.6, sure + 0.1) if ort >= UST else max(0.3, sure - 0.1)
                try:
                    for pid in bizim_pidler(psutil):
                        try:
                            p = psutil.Process(pid)
                            askida[pid] = p.create_time()
                            p.suspend()
                        except psutil.Error:
                            askida.pop(pid, None)
                    durum_yaz()
                    time.sleep(sure)
                finally:
                    hepsini_surdur()
        except Exception as e:  # ölçüm hatası döngüyü öldürmesin
            with open(GUNLUK, "a", encoding="utf-8") as f:
                f.write("%s hata %r\n" % (time.strftime("%H:%M:%S"), e))
            hepsini_surdur()
        time.sleep(max(0.0, 1.0 - (time.time() - t0)))


if __name__ == "__main__":
    if sys.argv[1:] == ["dongu"]:
        dongu()
    else:
        import psutil
        print("util/vram:", olc(), "hedef pid:", bizim_pidler(psutil))
